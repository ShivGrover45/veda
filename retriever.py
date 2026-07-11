import chromadb
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
collection_name = "veda"

CHROMA_PATH="./chroma_db"
RESPONSE_THRESHOLD=0.6
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


def generate_query_variants(query:str,n:int=3)->list[str]:
    model=ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    prompt=ChatPromptTemplate.from_messages([
        ("system",f"Generate {n} different rephrasings of the user's question "
                   "to help retrieve relevant study material. Return one per line, "
                   "no numbering, no extra text."),("human", "{query}")
    ])
    chain = prompt | model
    response = chain.invoke({"query": query})
    content = response.content  # grab the box (or letter) as-is
    if isinstance(content, list):  # check: is it a box?
        content = " ".join(
            block["text"] if isinstance(block, dict) and "text" in block else str(block)
            for block in content
        )
    variants=[line.strip() for line in content.split("\n") if line.strip()]
    return variants[:n]

def retrieve(query:str,embedder,k:int=4,session_id:str="default"):
    vector_store = get_vector_store(embedder, session_id)
    results= vector_store.similarity_search_with_relevance_scores(query, k=k)
    if not results:
        return []
    top_score=results[0][1]
    if top_score>RESPONSE_THRESHOLD:
        return [doc for doc,score in results ]
    variants=generate_query_variants(query)
    seen=set()
    merged=[]
    for doc,score in results:
        if score>=RESPONSE_THRESHOLD:
            seen.add(doc.page_content)
            merged.append(doc)
    for variant in variants:
        for doc in vector_store.similarity_search(variant, k=k):
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                merged.append(doc)
    return merged