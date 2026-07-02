import chromadb
from langchain_chroma import Chroma

collection_name = "veda"

CHROMA_PATH="./chroma_db"
def get_vector_store(embedder,session_id:str="default"):
    
    vector_store = Chroma(
        collection_name=f"{collection_name}_{session_id}",
        embedding_function=embedder,
        persist_directory=CHROMA_PATH
    )
    return vector_store

def ingest_documents(chunks,embedder,session_id:str="default"):
    vector_store = get_vector_store(embedder, session_id)
    vector_store.add_documents(chunks)
    return vector_store
def retrieve(query:str,embedder,k:int=4,session_id:str="default"):
    vector_store = get_vector_store(embedder, session_id)
    results = vector_store.similarity_search(query,k=k)
    return results