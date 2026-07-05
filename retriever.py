import chromadb
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
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


def generate_query_variants(query:str):
    model=ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    prompt=ChatPromptTemplate.from_messages([
        ("system",f"Generate {n} different rephrasings of the user's question "
                   "to help retrieve relevant study material. Return one per line, "
                   "no numbering, no extra text."),("human", "{query}")
    ])
def retrieve(query:str,embedder,k:int=4,session_id:str="default"):
    vector_store = get_vector_store(embedder, session_id)
    results= vector_store.similarity_search_with_relevance_scores(query, k=k)
    return results