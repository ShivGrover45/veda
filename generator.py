import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def generate_answer(query:str,chunks:list):
   context="\n\n ".join([chunk.page_content for chunk in chunks])
   prompt = ChatPromptTemplate.from_template("""You are a helpful study assistant. Answer the question based only on the provided context.
   If the answer is not in the context, say "I don't have enough information to answer this."

   Context:
   {context}

   Question: {query}

   Answer:""")

   model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
   chain=prompt|model
   response=chain.invoke({"context":context,"query":query})
   return response.content