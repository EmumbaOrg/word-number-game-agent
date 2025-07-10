from typing import Literal
from pydantic import BaseModel, Field


class UserWillRequest(BaseModel):
    user_will: Literal["NUMBER_SELECTED", "WORD_SELECTED", "EXIT_GAME"] = Field(
        description="Specifies if the user wants to select a number to be guessed or exit the game.",
    )
    user_id: str = Field(
        description="Unique identifier for the user, used to track the game state.",
    )

class UserAnswerRequest(BaseModel):
    user_answer: Literal["yes", "no"] = Field(
        description="User's response to the guess. 'yes' if the guessed number is greater than the user's number, 'no' otherwise.",
    )
    user_id: str = Field(
        description="Unique identifier for the user, used to track the game state.",
    )