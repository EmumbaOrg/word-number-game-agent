from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.messages import ToolMessage

from app.graphs.states.word import WordToolState
from app.core.chat_model.main import chat_model

@tool("generate_questions", description="Generate questions for the word guessing game.")
def generate_questions(state: Annotated[WordToolState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    Uses the LLM to generate the next yes/no question, considering the list of possible words,
    the questions already asked, and the user's answers.
    """


    # Prepare the prompt for the LLM
    try:
        prompt = f"""
                You are an AI assistant helping to guess a word from this list: {', '.join(state["word_list"])}.
                The user has selected one word from this list.

                Here are the previous questions and answers:
                    {chr(10).join([f"Q{i+1}: {qa['question']} | User: {qa['answer']}" for i, qa in enumerate(state["asked_questions"])]) if state["asked_questions"] else "None yet."}

                Based on the above, generate the next yes/no question that will best narrow down the possible words. 
                Do not repeat previous questions. Only return the next question as a single sentence.
            """

        # Call the LLM
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
        print(f"Error generating question: {e}")

@tool("guess_word", description="Guess the word in the word guessing game.")
def guess_word(state: Annotated[WordToolState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    Uses the LLM to guess the user's word, considering the list of possible words,
    the questions asked, and the user's answers.
    """

    try:
        prompt = f"""
                You are an AI assistant. The user has selected a word from this list: {', '.join(state["word_list"])}.

                Here are the five questions asked and the user's answers:
                    {chr(10).join([f"Q{i+1}: {qa['question']} | User: {qa['answer']}" for i, qa in enumerate(state["asked_questions"])])}

                Based on the above, guess which word the user selected. 
                Only return the single word as your answer.
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
        print(f"Error guessing word: {e}")