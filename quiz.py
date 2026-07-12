from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import MCQResponse
from quiz_config import get_config

def generate_mcqs(topic:str,context_snippet:list)->MCQResponse:
    #generate multiple choice questions based on the topic and context snippet
    config=get_config()
    context="\n\n".join(doc.page_content for doc in context_snippet)
    model=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
    structured_model=model.with_structured_output(MCQResponse)
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a study assistant creating a quiz to test understanding of a topic
the student has struggled with. Based ONLY on the provided context, generate {config.n_questions}
multiple-choice questions about the topic: {topic}.
Difficulty level: {config.difficulty}.
{config.style_notes}
Each question must have exactly 4 options, one correct answer matching an option exactly,
and a brief explanation.

Context:
{context}"""),
        ("human", f"Generate {config.n_questions} MCQs about {topic}")
    ])
    chain=prompt | structured_model
    return chain.invoke({})


