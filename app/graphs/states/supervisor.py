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
    status: Literal["AWAITING_GAME", "NUMBER_GAME", "WORD_GAME"] = "AWAITING_GAME"
    total_number_games: int = 0
    total_word_games: int = 0
    correct_words: int = 0
    correct_numbers: int = 0
    

def init_state() -> SupervisorState:
    return SupervisorState(
        status="AWAITING_GAME",
        total_number_games=0,
        total_word_games=0,
        correct_words=0,
        correct_numbers=0,    
    )