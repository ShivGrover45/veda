import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

load_dotenv()

def generate_answer(query: str, chunks: list, chat_history: list = []) -> str:
    context = "\n\n".join([doc.page_content for doc in chunks])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful study assistant. Answer the question based only on the provided context.
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}")
    ])
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash") 
    chain = prompt | model
    response = chain.invoke({
        "context": context,
        "chat_history": chat_history,
        "query": query
    })
    return response.content
 