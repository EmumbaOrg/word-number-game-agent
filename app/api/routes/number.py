from fastapi import APIRouter, Depends, HTTPException
from app.schemas.number import UserWillRequest, UserAnswerRequest
from app.services.number import NumberGameService

number_router = APIRouter(prefix="/number")

@number_router.post("/select")
async def number_selected(
    body: UserWillRequest,
    number_game_service: NumberGameService = Depends()
):
    """
    Endpoint to handle the user's selection in the number game.
    """
    try:
        response = await number_game_service.number_selected(body.user_will, body.user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong while selecting the number.")

@number_router.post("/guess")
async def guess_number(
    body: UserAnswerRequest,
    number_game_service: NumberGameService = Depends()
):
    """
    Endpoint to handle the user's guess in the number guessing game.
    """
    try:
        response = await number_game_service.guess_number(body.user_answer, body.user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to process your guess at the moment.")
