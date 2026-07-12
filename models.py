from pydantic import BaseModel
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class MCQ(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str | None = None

class MCQResponse(BaseModel):
    topic:str
    questions: list[MCQ]
