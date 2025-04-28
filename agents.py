from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from state import MessageState
import re

class Interviewer:
    def __init__(self, model_name: str, temperature: float):
        system_message = (
            "You are a strict information extractor. "
            "Only return a raw list of programming language names separated by commas. "
            "No extra text, no thinking, no explanation, no markdown formatting. "
            "Respond minimally and precisely."
        )
        self.model = ChatOllama(model=model_name, temperature=temperature, system_message=system_message)

    def fetch_keyword(self, state: MessageState) -> MessageState:
        input_text = state.get("cv_data").get("text")
        prompt = PromptTemplate.from_template(
            """
        You are an information extractor specialized in programming languages.

        Given a text describing a person's skills, extract ONLY the programming language names mentioned.
        Confirm if the names are really a programming langauage or not.

        Rules:
        - Only output programming languages (e.g., Python, Java, C++).
        - Separate names by commas without any extra explanation.
        - If no programming languages are found, output an empty string.

        Input:
        {text}

        Output:
        """
        )
        final_prompt = prompt.format(text=input_text)
        response = self.model.invoke(final_prompt).content.strip()
        state["cv_data"]["keywords"] = response
        return state