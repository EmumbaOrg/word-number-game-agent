from langgraph.graph import MessagesState
from typing import Dict, List, Literal, Optional

from app.graphs.states.number import num_init_state
from app.graphs.states.word import word_init_state

class SupervisorState(MessagesState):
    """
        State class for the supervisor managing the number guessing game and word guessing game.
    """
    """
    Below is the state used by the supervisor agent only
    """
    status: Literal["AWAITING_GAME", "NUMEBR_GAME", "WORD_GAME"] = "AWAITING_GAME"
    total_number_games: int = 0
    total_word_games: int = 0
    correct_words: int = 0
    correct_numbers: int = 0
    

    # #state variables used by the number game
    # current_guess: int
    # user_answer: Optional[Literal["yes", "no", "YES", "NO"]] = None
    # low_bound: int
    # upper_bound: int
    # guess_count: int
    # game_in_progress: bool
    # is_number_correct: bool = False

    # # state variables used by the word game
    # word_game_status: Literal["AWAITING_WORD", "ASKING_QUESTIONS", "GUESSING_WORD", "COMPLETED"] = "AWAITING_WORD"
    # word_list: list[str] = ["apple", "chair", "elephant", "guitar", "rocket", "pencil", "pizza", "tiger"]
    # max_questions: int = 5
    # asked_questions: List[Dict[str, str]] = []
    # current_question_index: int = 0
    # final_guess: str = None
    # is_word_correct: bool = False


def init_state() -> SupervisorState:

    # num_state = num_init_state()
    # word_state = word_init_state()
    return SupervisorState(
        # **num_state,  # Unpack the number game state into the supervisor state
        # **word_state,  # Unpack the word game state into the supervisor state
        status="AWAITING_GAME",
        total_number_games=0,
        total_word_games=0,
        correct_words=0,
        correct_numbers=0,    
    )