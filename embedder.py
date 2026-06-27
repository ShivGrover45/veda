from langchain_huggingface import HuggingFaceEmbeddings

def get_embedder():
    embedder = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
    return embedder