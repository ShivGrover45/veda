# RAG Study Assistant

An AI-powered study assistant that lets you upload PDF documents and ask questions about them. Built with LangChain, Gemini 3.5 Flash, and ChromaDB.

## Tech Stack

- **Framework:** FastAPI
- **LLM:** Gemini 3.5 Flash (via LangChain)
- **Embeddings:** BAAI/bge-small-en-v1.5 (local)
- **Vector Store:** ChromaDB
- **PDF Processing:** PyPDF + LangChain Text Splitters

## Architecture

PDF Upload → Text Extraction → Chunking → Embedding → ChromaDB
Query → Embedding → Similarity Search → Gemini 2.5 Flash → Answer

## Setup

1. Clone the repo
```bash
   git clone https://github.com/ShivGrover45/rag-study-assistant.git
   cd rag-study-assistant
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create `.env` file
```bash
   GEMINI_API_KEY=your-api
```
4. Run the server
```bash
   uvicorn main:app --reload
```

5. Open `http://localhost:8000/docs` to test the API

## Endpoints

- `GET /health` — Health check
- `POST /upload` — Upload a PDF for ingestion
- `POST /ask` — Ask a question about uploaded PDFs
