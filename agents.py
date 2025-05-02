from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from state import MessageState
import random

class Interviewer:
    def __init__(self, model_name: str, temperature: float):
        self.model = ChatOllama(model=model_name, temperature=temperature)

    def fetch_keyword(self, state: MessageState) -> MessageState:
        input_text = state.get("cv_data").get("text")
        prompt = PromptTemplate.from_template(
            """
            You are an information extractor that strictly identifies **only programming language names** from a text describing a person’s skills.

            ⚠️ Your task is to exclude any **spoken languages** (like English, Bangla, French, etc.) even if they appear alongside programming terms.

            ### Objective:
            Extract and return a comma-separated list of **only** programming language names found in the text. **Do not include any other text**. If none are found, return an empty string.

            ### ✅ Examples (Valid Extraction):
            Text: I love doing codes in python and c++.
            Output: Python, C++

            Text: I have experience in Java, Kotlin, and some scripting in Bash.
            Output: Java, Kotlin, Bash

            Text: Skilled in Rust and JavaScript.
            Output: Rust, JavaScript

            ### ❌ Examples (Ignore spoken languages):
            Text: I always speak in English.
            Output: 

            Text: Fluent in Bangla and Hindi.
            Output: 

            Text: I know Python, but I also speak Bengali.
            Output: Python

            ### Rules:
            - Only include valid programming languages.
            - Do **not** include any human or spoken languages.
            - The output must be a single line.
            - Capitalize each programming language's name correctly.
            - If no programming languages are found, return an empty string (just a blank line).
            - Do not add any language that is not mentioned in the input.

            ### Input:
            {text}

            ### Output:
            """
        )
        final_prompt = prompt.format(text= input_text)
        response = self.model.invoke(final_prompt).content.split('Output:')[-1].strip().split(',')
        keywords = [text.strip() for text in response]
        state["cv_data"]["keywords"] = keywords
        return state

    def generate_question(self, state: MessageState) -> MessageState:
        keywords = state.get("cv_data").get("keywords")
        prompt = PromptTemplate.from_template(
        """
        You are a technical interviewer assistant.

        Your job is to generate **exactly 3 technical questions** per programming language listed below.

        ### Instructions:
        - Only use the programming language provided as input below.
        - For **each language**, output exactly 3 questions.
        - Questions should range in difficulty: 1 basic, 1 intermediate, 1 advanced.
        - Do not include any commentary or extra formatting — only the questions.
        - Do not include any bullet points or numeric points. The questions must be basic strings.

        ### Programming Language:
        {language}

        ### Output Format (strict):
        Questions:
        <qeustion 1><break line>
        <qeustion 2><break line>
        ...

        ### Begin Output:
        """
        )
        all_questions = []
        for keyword in keywords:
            final_prompt = prompt.format(language= [keyword])
            response = self.model.invoke(final_prompt).content.split('Questions:')[-1].strip().split('\n')
            questions = [text.strip() for text in response]
            all_questions.extend(questions)
        state["questions"]["generated_questions"] = all_questions
        return state