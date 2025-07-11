from fastapi import APIRouter, Depends, HTTPException
from app.schemas.supervisor import GameHistoryReq, GameStartReq
from app.services.supervisor import SupervisorService

supervisor_router = APIRouter(prefix="/game")

@supervisor_router.post("/start")
async def start_game(body: GameStartReq):
    """
    Endpoint to start the number game.
    """
    try:
        response = await SupervisorService.start_game(body.user_id, body.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to start the game.")

@supervisor_router.post("/history")
async def get_game_history(body: GameHistoryReq, sup_service: SupervisorService = Depends()):
    """
    Endpoint to retrieve the game history for a specific user.
    """
    try:
        response = sup_service.get_game_history(body.user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve game history.")
        