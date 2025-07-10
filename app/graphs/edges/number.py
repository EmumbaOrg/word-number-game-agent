from typing import Literal
from app.graphs.states.number import NumberGameState


def end_number_game_edge(state: NumberGameState) -> Literal["final_number_guess", "number_question_user"]:
    """
    Edge function to determine the next step in the number guessing game based on the game state.
    If the game is over, it returns a command to end the game. Otherwise, it continues the game.
    
    Args:
        state (NumberGameState): The current state of the number guessing game.
        
    Returns:
        str: The next node to transition to based on the game state.
    """
    
    if not state["game_in_progress"]:
        return "final_number_guess"
    return "number_question_user"