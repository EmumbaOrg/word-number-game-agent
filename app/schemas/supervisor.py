from pydantic import BaseModel, Field

class GameStartReq(BaseModel):
    user_id: str = Field(
        ...,
        description="The unique identifier for the user starting the game.",
        example="12345",
    )
    message: str = Field(
        ...,
        description="The initial message or command to start the game.",
        example="Start the number guessing game",
    )

class GameHistoryReq(BaseModel):
    user_id: str = Field(
        ...,
        description="The unique identifier for the user whose game history is being requested.",
        example="12345",
    )