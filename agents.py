from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from state import MessageState

class Interviewer:
    def __init__(self, model_name: str, temperature: float, prompts: dict):
        self.model = ChatOllama(model=model_name, temperature=temperature)
        self.prompts = prompts

    def fetch_keyword(self, state: MessageState) -> MessageState:
        input_text = state.get("cv_data").get("text")
        prompt = PromptTemplate.from_template(self.prompts.get("fetch_keyword"))
        final_prompt = prompt.format(text= input_text)
        response = self.model.invoke(final_prompt).content.split('Output:')[-1].strip().split(',')
        keywords = [text.strip() for text in response]
        state["cv_data"]["keywords"] = keywords
        return state

    def generate_question(self, state: MessageState) -> MessageState:
        keywords = state.get("cv_data").get("keywords")
        prompt = PromptTemplate.from_template(self.prompts.get("generate_question"))
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
            return "end"
        current_index = state.get("current_index")
        interview_question = state["questions"].get("generated_questions")[current_index]
        candidate_response = state.get("answers").get("candidate_answers")[-1]
        prompt = PromptTemplate.from_template(self.prompts.get("decider_node"))
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
        prompt = PromptTemplate.from_template(self.prompts.get("clarification_node"))
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
    