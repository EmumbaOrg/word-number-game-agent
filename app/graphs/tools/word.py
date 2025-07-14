from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.messages import ToolMessage
import logging

from app.graphs.states.word import WordToolState
from app.core.chat_model.main import chat_model

logger = logging.getLogger(__name__)

@tool("generate_questions", description="Generate questions for the word guessing game.")
def generate_questions(
    state: Annotated[WordToolState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    Generates the next yes/no question for the word guessing game using an LLM.
    Considers the list of possible words, previously asked questions, and user answers.
    Returns a Command object with the updated state and a ToolMessage containing the next question.
    """
    try:
        prompt = f"""
                You are an AI assistant helping to guess a word from this list:

                {', '.join(state["word_list"])}

                The user has selected **one** word from the list.

                Here are the previous questions and answers:

                {chr(10).join([f"Q{i+1}: {qa['question']} | User: {qa['answer']}" for i, qa in enumerate(state["asked_questions"])]) if state["asked_questions"] else "None yet."}

                

                #### Instructions:
                    - Based on the above, generate the **next yes/no** question.
                    - The question should help **narrow down** the possibilities.
                    - Ask about **characteristics or properties**, not the word itself.
                    - **Do not** repeat previous questions.
                    - Return **only** the new question as a single sentence.

                #### One-Shot Example:
                    - Word list: apple, banana, cherry, orange
                    - Previous:
                    - Q1: Is it a fruit? | User: yes
                    - Q2: Is it red? | User: no
                    - Output: `"Is it yellow?"`

            """

        question = chat_model.invoke(prompt).content.strip()

        return Command(update={
            "asked_questions": state["asked_questions"] + [{"question": question, "answer": None}],
            "current_question_index": state["current_question_index"] + 1,
            "word_game_status": "ASKING_QUESTIONS",
            "messages": [ToolMessage(
                content=f"Next question: {question}",
                tool_call_id=tool_call_id
            )],
        })
    except Exception as e:
        logger.error(f"Error generating question: {e}")
        
        return Command(update={
            "messages": [ToolMessage(
                content="An error occurred while generating the next question.",
                tool_call_id=tool_call_id
            )],
        })

@tool("guess_word", description="Guess the word in the word guessing game.")
def guess_word(
    state: Annotated[WordToolState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    Uses an LLM to guess the user's selected word based on the list of possible words,
    the questions asked, and the user's answers.
    Returns a Command object with the final guess and a ToolMessage containing the guess.
    """
    try:
        prompt = f"""
                You are an AI assistant. The user has selected a word from this list:

                {', '.join(state["word_list"])}



                Here are the five questions and user's responses:

                {chr(10).join([f"Q{i+1}: {qa['question']} | User: {qa['answer']}" for i, qa in enumerate(state["asked_questions"])])}



                #### Instructions:
                    - Based on the above, **guess the user's word**.
                    - Return only the **single word** as your answer.
                    - Do **not** explain or include anything else.

                #### One-Shot Example:
                    - Word list: apple, banana, cherry
                    - Q&A:d
                    - Q1: Is it a fruit? | User: yes
                    - Q2: Is it yellow? | User: yes
                    - ...
                    - Output: `banana`
            """

        guess = chat_model.invoke(prompt).content.strip()
        
        return Command(update={
            "final_guess": guess,
            "word_game_status": "GUESSING_WORD",
            "messages": [ToolMessage(
                content=f"My guess for the word is: {guess}",
                tool_call_id=tool_call_id
            )],
        })
    except Exception as e:
        logger.error(f"Error guessing word: {e}")
        
        return Command(update={
            "messages": [ToolMessage(
                content="An error occurred while guessing the word.",
                tool_call_id=tool_call_id
            )],
        })