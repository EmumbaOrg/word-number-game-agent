from typing import Literal
from app.graphs.states.word import WordGameState


def make_final_guess(state: WordGameState) -> Literal["final_guess", "word_question_user"]:
    """
    Determines whether to present the agent's final guess to the user or continue asking questions.

    Args:
        state (WordGameState): The current state of the word guessing game.

    Returns:
        Literal["final_guess", "word_question_user"]: Returns "final_guess" if a final guess is available,
        otherwise returns "word_question_user" to continue the questioning process.
    """
    guess = state.get("final_guess", None)
    if guess:
        return "final_guess"
    else:
        return "word_question_user"
