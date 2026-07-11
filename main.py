import os
import uuid
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ingestor import load_and_split
from retriever import ingest_documents, retrieve
from generator import generate_answer
from embedder import get_embedder
from langchain_core.messages import HumanMessage, AIMessage
from models import QueryRequest
from weak_topics import *
app=FastAPI(title="Veda AI",version="1.0.0")

embedder=get_embedder()
chat_histories={}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...),session_id: str = "default"):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    contents=await file.read()
    req_id=uuid.uuid4()
    temp_path=f"tem_{file.filename}_{session_id}_{req_id}"
    try:
        with open(temp_path,"wb") as f:
            f.write(contents)
        chunks=load_and_split(temp_path)
        if len(chunks) == 0:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF. Make sure it is not a scanned document.")
        ingest_documents(chunks,embedder,session_id=session_id)
        return {"message": f"File '{file.filename}' uploaded and processed successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while saving the file: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    
    

@app.post("/query")
async def query(payload: QueryRequest):
    try:
        if payload.session_id not in chat_histories:
            chat_histories[payload.session_id] = []
        
        history = chat_histories[payload.session_id]
        results = retrieve(payload.query, embedder, session_id=payload.session_id)
        
        if not results:
            raise HTTPException(status_code=404, detail="No relevant content found for your query.")
        
        answer = generate_answer(payload.query, results, history)
        context_snippet="\n".join([doc.page_content for doc in results[:1]])
        topic=record_query(payload.session_id,context_snippet,payload.query)
        
        history.append(HumanMessage(content=payload.query))
        history.append(AIMessage(content=answer))
        
        return {"answer": answer, "session_id": payload.session_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    
@app.get('/weak-topics/{session_id}')
async def weak_topics(session_id:str):
    return {"weak_topics": get_weak_topics(session_id)}
    
@app.post('/clear/{session_id}')
async def clear_session(session_id: str):
    if session_id in chat_histories:
        chat_histories.pop(session_id)
        clear_topics(session_id)
        return {"message": f"Session '{session_id}' cleared successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
@app.post('/restore')
async def restore_vector_db():
    try :
        from langchain_chroma import Chroma
        vector_store=Chroma(persist_directory="chroma_db", embedding_function=embedder)
        vector_store.delete_collection()
        return {"message":"Vector database restored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restoring vector database: {str(e)}")