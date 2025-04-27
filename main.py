from langgraph.graph import StateGraph, START, END
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
from state import State
from PIL import Image
import io
import os 

os.environ

llm = ChatOllama(model="llama3.2:1b", temperature=0.5)

class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State, *args, **kwds):
        print(f"State: {state} | Secret: {self._value}")
        return {"state": [self._value]}
    
builder = StateGraph(State)

builder.add_node("node_1", ReturnNodeValue("kabin"))
builder.add_node("node_2", ReturnNodeValue("jahid"))
builder.add_node("node_3", ReturnNodeValue("sajid"))
builder.add_node("node_4", ReturnNodeValue("roni"))

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", "node_4")
builder.add_edge("node_3", "node_4")
builder.add_edge("node_4", END)

graph = builder.compile()

bytes = graph.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(bytes))

image.save("graph.png")

graph.invoke({"state": [1]})