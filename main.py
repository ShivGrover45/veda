import os
from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from ingestor import load_and_split
from retriever import ingest_documents, retrieve
from generator import generate_answer
from embedder import get_embedder

app=FastAPI(title="Veda AI",version="1.0.0")

embedder=get_embedder()

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
    contents=await file.read()
    temp_path=f"tem_{file.filename}"
    with open(temp_path,"wb") as f:
        f.write(contents)
    chunks=load_and_split(temp_path)
    ingest_documents(chunks,embedder)
    os.remove(temp_path)
    return {"message": f"File '{file.filename}' uploaded and processed successfully."}

@app.post("/query")
async def student_query(payload: dict):
    query = payload.get("query")
    if not query:
        return {"error": "Query not provided."}
    results = retrieve(query, embedder)
    answer=generate_answer(query, results)
    return {"answer":answer}
