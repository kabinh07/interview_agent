# Interview Agent

An intelligent interview simulation system powered by LLMs that automatically generates relevant questions based on a candidate's CV, conducts interviews, and handles clarifications when needed.

## Overview

This project implements an automated interview agent using LangChain and LangGraph. The system analyzes a candidate's CV to extract keywords, generates tailored interview questions, and conducts a natural conversation flow with clarification capabilities.

## Features

- **Keyword Extraction**: Automatically identifies key skills and experiences from CV text
- **Dynamic Question Generation**: Creates relevant technical questions based on extracted keywords
- **Interactive Interview Flow**: Simulates a real interview experience with follow-up questions
- **Clarification Handling**: Intelligently responds when candidates ask for clarification
- **Conversation Management**: Maintains context throughout the interview process

## Architecture

The system is built as a state machine using LangGraph with the following components:

- **State Management**: Tracks CV data, questions, answers, and conversation history
- **Interviewer Agent**: Handles keyword extraction, question generation, and conversation flow
- **Decision Logic**: Determines whether to continue asking questions, provide clarification, or end the interview

A visualization of the graph workflow is generated as `graph.png` when running the application.

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables in a `.env` file

## Usage

1. Ensure you have Ollama installed and the required LLM model (llama3.2:1b) available
2. Create prompt files in the `prompts/` directory:
   - `clarification_node.txt`
   - `decider_node.txt`
   - `fetch_keyword.txt`
   - `generate_question.txt`
3. Run the application:
   ```bash
   python main.py
   ```

## Customization

You can customize the interview agent by:

1. Modifying the CV data in `main.py`
2. Adjusting the prompt templates in the `prompts/` directory
3. Changing the LLM model in the `Interviewer` initialization

## Requirements

- Python 3.8+
- LangChain and LangGraph libraries
- Ollama for local LLM inference
- Additional dependencies listed in `requirements.txt`

## License

This project is open source and available under the MIT License.