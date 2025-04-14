from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

model = ChatOllama(model="llama3.2:1b", temperature=0.7)

def call_model(state: AgentState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    return "end"  # Always finishes after one response for simplicity

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {
    "end": END
})

app = graph.compile()

inputs = {"messages": [HumanMessage(content="What is LangGraph?")]}
output = app.invoke(inputs)

for msg in output["messages"]:
    print(msg.content)