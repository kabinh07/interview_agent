from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from state import MessageState
from agents import Interviewer
from PIL import Image
import io
from dotenv import load_dotenv
load_dotenv()

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
        },
        current_index = 0,
        chat_history= []
    )

prompts = {}
with open("prompts/clarification_node.txt", "r") as f:
    prompts["clarification_node"] = f.read()
with open("prompts/decider_node.txt", "r") as f:
    prompts["decider_node"] = f.read()
with open("prompts/fetch_keyword.txt", "r") as f:
    prompts["fetch_keyword"] = f.read()
with open("prompts/generate_question.txt", "r") as f:
    prompts["generate_question"] = f.read()

if __name__ == "__main__":
    builder = StateGraph(MessageState)
    interviewer = Interviewer("llama3.2:1b", 0.0, prompts) 

    builder.add_node("keyword_fetcher", interviewer.fetch_keyword)
    builder.add_node("question_generator", interviewer.generate_question)
    builder.add_node("question_asker", interviewer.ask_questions)
    builder.add_node("explainer", interviewer.clarification_node)

    builder.add_edge(START, "keyword_fetcher")
    builder.add_edge("keyword_fetcher", "question_generator")
    builder.add_edge("question_generator", "question_asker")
    builder.add_conditional_edges(
        "question_asker",
        interviewer.decider_node,
        {
            "next": "question_asker",
            "confusion": "explainer",
            "end": END
        }
    )
    builder.add_conditional_edges(
        "explainer",
        interviewer.decider_node,
        {
            "next": "question_asker",
            "confusion": "explainer",
            "end": END
        }
    )

    graph = builder.compile()
    png_bytes = graph.get_graph().draw_mermaid_png()
    image = Image.open(io.BytesIO(png_bytes))
    image.save("graph.png")
    reponse = graph.invoke(message)
    print(reponse)