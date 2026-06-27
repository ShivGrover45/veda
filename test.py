from ingestor import load_and_split
from retriever import ingest_documents, retrieve
from generator import generate_answer

chunks = load_and_split("sample.pdf")
ingest_documents(chunks)

query = "what is vehicle to grid technology?"
results = retrieve(query)
for i, doc in enumerate(results):
    print(f"\n--- Chunk {i+1} ---")
    print(doc.page_content)

generated_answer = generate_answer(query, results)
print(f"\n--- Generated Answer ---")
print(generated_answer)