from typing import TypedDict, Literal
import random
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    state : str

def node_1(state):
    print("---Node 1---")
    return {"state": state['state'] + " I am"}

def node_2(state):
    print("---Node 2---")
    return {"state": state['state'] + " happy!"}

def node_3(state):
    print("---Node 3---")
    return {"state": state['state'] + " sad!"}

def decide_mode(state) -> Literal["node_2", "node_3"]:
    return "node_2" if random.random() < 0.5 else "node_3"

if __name__ == "__main__": 
    builder = StateGraph(State)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", decide_mode)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    graph = builder.compile()

    result = graph.invoke({"state": "Hi, this is Kabin."})
    print("Final result:", result)
