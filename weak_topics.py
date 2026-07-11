from collections import defaultdict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

WEAK_THRESHOLD=2
topic_tracker:dict[str,dict[str,int]]=defaultdict(lambda: defaultdict(int))
def extract_topic(query:str,context_snippet:str)->str:
    model=ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    prompt=ChatPromptTemplate.from_messages([
        ("system", "Identify the single core academic topic/concept being asked about, "
                   "in 2-4 words. Return only the topic, nothing else."),
        ("human", "Question: {query}\n\nRelevant context: {context}")
    ])
    chain = prompt | model
    response = chain.invoke({"query": query, "context": context_snippet[:500]})
    content= response.content
    if isinstance(content, list):
        content = " ".join(
            block["text"] if isinstance(block, dict) and "text" in block else str(block)
            for block in content
        )
    return content.strip().lower()
def record_query(session_id:str,context_snippet:str,query:str)->str:
    topic=extract_topic(query, context_snippet)
    topic_tracker[session_id][topic] += 1
    return topic
def get_weak_topics(session_id:str)->list[dict]:
    return [{"topic": topic, "count": count} for topic, count in topic_tracker[session_id].items() if count >= WEAK_THRESHOLD]

def clear_topics(session_id:str):
    if session_id in topic_tracker:
        del topic_tracker[session_id]
