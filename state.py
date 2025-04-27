from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list[str], operator.add]