from fastapi import APIRouter, Depends

from app.schemas.number import UserAnswerRequest, UserWillRequest
from app.services.word import WordGameService

word_router = APIRouter(prefix="/word")

@word_router.get("/status")
async def get_word_status():
    """
    Endpoint to get the status of the word module.
    """
    return {"status": "running", "message": "Word module is operational."}


@word_router.post("/select")
async def select_word(body: UserWillRequest, word_game_service: WordGameService = Depends()):
    """
    Endpoint to select a word for the word guessing game.
    """
    response = await word_game_service.word_selected(body.user_will, body.user_id)
    return response
    
@word_router.post("/guess")
async def guess_word(body: UserAnswerRequest, word_game_service: WordGameService = Depends()):
    """
    Endpoint to handle the user's guess in the word guessing game.
    """
    response = await word_game_service.guess_word(body.user_answer, body.user_id)
    
    return response
    
