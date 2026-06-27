import chromadb
from langchain_chroma import Chroma
from embedder import get_embedder

collection_name = "veda"

CHROMA_PATH="./chroma_db"
def get_vector_store():
    embedder = get_embedder()
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embedder,
        persist_directory=CHROMA_PATH
    )
    return vector_store

def ingest_documents(chunks):
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    return vector_store
def retrieve(query:str,k:int=4):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query,k=k)
    return results