from typing import Literal, List, Dict
from langgraph.graph import MessagesState
from langgraph.prebuilt.chat_agent_executor import AgentState


class WordGameState(MessagesState):
    """
    State class for the word guessing game.
    Inherits from MessagesState to manage conversation history.
    """
    word_game_status: Literal["AWAITING_WORD", "ASKING_QUESTIONS", "GUESSING_WORD", "COMPLETED"] = "AWAITING_WORD"
    word_list: list[str] = ["apple", "chair", "elephant", "guitar", "rocket", "pencil", "pizza", "tiger"]
    max_questions: int = 5
    asked_questions: List[Dict[str, str]] = []
    current_question_index: int = 0
    final_guess: str = None
    is_guess_correct: bool = False

class WordToolState(AgentState, WordGameState):
    """
    State class for the word guessing game tool.
    Inherits from MessagesState and WordGameState to manage game state and conversation history.
    """
    pass

def word_init_state() -> WordGameState:
    """
    Initializes the state for the word guessing game.
    Sets the initial status and prepares the word list.
    Returns:
        WordGameState: The initial state of the word guessing game.
    """
    return WordGameState(
        word_game_status = "AWAITING_WORD",
        word_list = ["apple", "chair", "elephant", "guitar", "rocket", "pencil", "pizza", "tiger"],
        max_questions = 5,
        asked_questions = [],
        current_question_index = 0,
        final_guess = "",
        is_guess_correct = False
    )