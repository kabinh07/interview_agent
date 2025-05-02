from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
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
        - Do not include the language name in output segment.
        - Do not provide any answers.
        - Do not provide any choices.

        ### Programming Language:
        {language}

        ### Output Format (strict):
        Output:
        <qeustion 1><break line>
        <qeustion 2><break line>
        ...

        Output:
        """
        )
        all_questions = []
        for keyword in keywords:
            final_prompt = prompt.format(language= [keyword])
            response = self.model.invoke(final_prompt).content.split('Questions:')[-1].strip().split('\n')
            questions = [text.strip() for text in response if not text.strip() == "" and "?" in text.strip()]
            all_questions.extend(questions)
        state["questions"]["generated_questions"] = all_questions
        return state

    def ask_questions(self, state: MessageState) -> MessageState:
        current_index = state.get("current_index")
        interview_question = state["questions"].get("generated_questions")[current_index]
        ai_message = AIMessage(content=interview_question)
        history = []
        ai_message.pretty_print()
        history.append(ai_message)
        temp_human_message = HumanMessage(content="")
        temp_human_message.pretty_print()
        input_message = input()
        human_message = HumanMessage(content=input_message)
        history.append(human_message)
        state["chat_history"] = history
        current_index += 1
        state["current_index"] = current_index
        state["answers"]["candidate_answers"] = [input_message]
        return state
    
    def decider_node(self, state: MessageState):
        if state.get("current_index") >= len(state.get("questions").get("generated_questions")):
            print("ENDDDDDDDDDD")
            return "end"
        current_index = state.get("current_index")
        interview_question = state["questions"].get("generated_questions")[current_index]
        candidate_response = state.get("answers").get("candidate_answers")[-1]
        prompt = """
        You are a strict classifier that decides whether a candidate's input is a quesiton or an answer to a given interview question.

        ### Instructions:
        - Output **only one word**: either `clarification` or `answer`.

        ### Examples:
        Interview Question: What is a Python dictionary?
        Candidate Input: What do you mean by dictionary?
        Output: question

        Interview Question: What is a Python dictionary?
        Candidate Input: It's used to store key-value pairs.
        Output: answer

        ### Rules:
        - Provide only a single word (e.g: question, answer)
        - No explaination
        ---

        Interview Question:
        {interview_question}

        Candidate Input:
        {user_input}

        Output:

        """
        final_prompt = prompt.format(interview_question = interview_question, user_input = candidate_response)
        response = self.model.invoke(final_prompt).content
        print(response)
        return "confusion" if "question" == response else "next"
    
    def clarification_node(self, state: MessageState) -> MessageState:
        current_index = state.get("current_index") - 1
        question = state.get("questions").get("generated_questions")[current_index]
        candidate_question = state.get("answers").get("candidate_answers").pop()
        state["questions"]["candidate_questions"] = candidate_question
        history = []

        prompt = """
        You are a interviewer

        A question was asked to a candidate, Now you have to clear the confusion. The asked question and the confusion is given below

        ### Instructions:
        - Clear the confusion but don't answer the question.

        Question:
        {quesiton}

        Confusion:
        {confusion}

        Answer:
        """
        final_prompt = prompt.format(quesiton=question, confusion=candidate_question)
        thinking_message = AIMessage(content="Thinking...")
        thinking_message.pretty_print()
        response = self.model.invoke(final_prompt).content
        ai_message = AIMessage(content=response)
        ai_message.pretty_print()
        history.append(ai_message)
        temp_human_message = HumanMessage(content="")
        temp_human_message.pretty_print()
        input_message = input()
        human_message = HumanMessage(content=input_message)
        history.append(human_message)
        state["chat_history"] = history
        state["answers"]["candidate_answers"] = [input_message]
        return state
    