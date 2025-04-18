from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b", temperature=0.5)

def kabin_rule(a: KeyboardInterrupt)