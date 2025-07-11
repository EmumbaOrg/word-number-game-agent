from fastapi import APIRouter, Depends, HTTPException

from app.schemas.number import UserAnswerRequest, UserWillRequest
from app.services.word import WordGameService


word_router = APIRouter(prefix="/word")
@word_router.post("/select")
async def select_word(body: UserWillRequest, word_game_service: WordGameService = Depends()):
    """
    Endpoint to select a word for the word guessing game.
    """
    try:
        response = await word_game_service.word_selected(body.user_will, body.user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to select word for the game.")

@word_router.post("/guess")
async def guess_word(body: UserAnswerRequest, word_game_service: WordGameService = Depends()):
    """
    Endpoint to handle the user's guess in the word guessing game.
    """
    try:
        response = await word_game_service.guess_word(body.user_answer, body.user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process word guess.")
