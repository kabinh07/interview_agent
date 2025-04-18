from utils.state import State
import random

python_questions = [
    "What is the difference between == and is in Python?",
    "List 5 common Python data types with examples.",
    "What is the difference between a list and a tuple?",
    "What are *args and **kwargs used for in Python functions?",
    "How does list comprehension work in Python?",
    "How is exception handling done in Python?",
    "What is a dictionary and how is it different from a list?",
    "Explain how the range() function works.",
    "What happens when you assign one list to another variable and modify it?",
    "How do you import and use modules in Python?"
]
def query_bot(state: State):
    return {"state": random.random(python_questions)}