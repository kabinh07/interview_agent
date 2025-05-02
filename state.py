from typing import TypedDict, Annotated, List
import operator

class CVData(TypedDict):
    text: str
    keywords: List[str]

class QuestionData(TypedDict):
    generated_questions : List[str]
    candidate_questions : List[str]

class AnswerData(TypedDict):
    candidate_answers: List[str]

class MessageState(TypedDict): 
    cv_data: CVData
    questions: QuestionData
    answers: AnswerData
    current_index : int = 0
    chat_history : Annotated[List, operator.add] = []