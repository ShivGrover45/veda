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
Query → Embedding → Similarity Search → Gemini 3.5 Flash → Answer

## Known Limitations

- **Weak-topic tracking uses exact-match topic labels.** Each query's topic is extracted 
  via a separate LLM call and tracked per-session using string matching. Semantically 
  related questions phrased differently (e.g. "PI controller terms" vs "PID control terms") 
  may be tracked as distinct topics rather than clustering under one label, which can 
  under-count how often a student is actually struggling with a given concept. A more 
  robust approach would embed topic labels and cluster by similarity rather than exact 
  string match — noted as a potential future improvement.

  - **Chat history is not persisted across page reloads.** Messages are held in frontend 
  React state only; reloading the browser tab clears the visible conversation, even 
  though the backend's chat history for that session (in-memory, per `session_id`) 
  may still exist until the server restarts. A production version would fetch 
  existing history on page load via a dedicated endpoint, and likely persist sessions 
  in Redis or a database rather than in-memory dicts. Noted as a planned improvement.

## Setup

1. Clone the repo
```bash
   git clone https://github.com/ShivGrover45/veda.git
   cd veda
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
- `POST /upload` — Upload a PDF for ingestion (PDF only, text-based)
- `POST /query` — Ask a question about uploaded PDFs (supports conversation history via session_id)
- `POST /clear/{session_id}` — Clear conversation history for a session
- `DELETE /reset` — Reset the vector store (clear all ingested PDFs)
