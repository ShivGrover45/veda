import os
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ingestor import load_and_split
from retriever import ingest_documents, retrieve
from generator import generate_answer
from embedder import get_embedder
from langchain.messages import HumanMessage,AIMessage
from models import QueryRequest
app=FastAPI(title="Veda AI",version="1.0.0")

embedder=get_embedder()
chat_history={}
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
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    contents=await file.read()
    temp_path=f"tem_{file.filename}"
    try:
        with open(temp_path,"wb") as f:
            f.write(contents)
        chunks=load_and_split(temp_path)
        if len(chunks) == 0:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF. Make sure it is not a scanned document.")
        ingest_documents(chunks,embedder)
        return {"message": f"File '{file.filename}' uploaded and processed successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while saving the file: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    
    

@app.post("/query")
async def student_query(payload: QueryRequest):
    try:
        if payload.session_id not in chat_histories:
            chat_histories[payload.session_id] = []
        
        history = chat_histories[payload.session_id]
        results = retrieve(payload.query, embedder)
        
        if not results:
            raise HTTPException(status_code=404, detail="No relevant content found for your query.")
        
        answer = generate_answer(payload.query, results, history)
        
        history.append(HumanMessage(content=payload.query))
        history.append(AIMessage(content=answer))
        
        return {"answer": answer, "session_id": payload.session_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")