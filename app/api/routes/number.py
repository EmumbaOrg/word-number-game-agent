from fastapi import APIRouter, Depends

from app.schemas.number import UserWillRequest, UserAnswerRequest
from app.services.number import NumberGameService

number_router = APIRouter(prefix="/number")

@number_router.get("/status")
async def get_number_status():
    """
    Endpoint to get the status of the number module.
    """
    return {"status": "running", "message": "Number module is operational."}


@number_router.post("/select")
async def number_selected(body: UserWillRequest, number_game_service: NumberGameService = Depends()):
    
    response = await number_game_service.number_slected(body.user_will, body.user_id)
    return response

@number_router.post("/guess")
async def guess_number(body: UserAnswerRequest, number_game_service: NumberGameService = Depends()):
    """
    Endpoint to handle the user's guess in the number guessing game.
    """
    response = await number_game_service.guess_number(body.user_answer, body.user_id)
    
    if isinstance(response, dict) and "message" in response:
        return response
    
    return {"status": "success", "message": "Guess processed successfully."}