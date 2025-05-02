from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from state import MessageState
from agents import Interviewer
from PIL import Image
import io
from dotenv import load_dotenv
load_dotenv()

builder = StateGraph(MessageState)
interviewer = Interviewer("llama3.2:1b", 0.0) 

builder.add_node("keyword_fetcher", interviewer.fetch_keyword)
builder.add_node("question_generator", interviewer.generate_question)

builder.add_edge(START, "keyword_fetcher")
builder.add_edge("keyword_fetcher", "question_generator")
builder.add_edge("question_generator", END)

graph = builder.compile()

bytes = graph.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(bytes))

image.save("graph.png")

message = MessageState(
    cv_data= {
        "text": "I am working as an AI/ML engineer. I prefer working with python, java, SQL and fluent in Bangla, and English languages",
        "keywords": []
    },
    questions= {
        "candidate_questions": [],
        "generated_questions": []
    },
    answers= {
        "candidate_answers": []
    }
)

graph = builder.compile()
reponse = graph.invoke(message)
print(reponse)