
import os
from fastapi import APIRouter, Depends
from langsmith import tracing_context

from app.schemas.supervisor import GameHistoryReq, GameStartReq
from app.services.supervisor import SupervisorService


supervisor_router = APIRouter(prefix="/game")

@supervisor_router.get("/status")
async def get_supervisor_status():
    """
    Endpoint to get the status of the supervisor.
    """
    return {"status": "running", "message": "Supervisor is operational."}



@supervisor_router.post("/start")
async def start_game(body: GameStartReq):
    """
    Endpoint to start the number game.
    """
    
    try:
        
        response = await SupervisorService.start_game(body.user_id, body.message)
        return {"message": response}
    except Exception as e:
        # return {"status": "error", "message": str(e)}
        pass

@supervisor_router.post("/history")
async def get_game_history(body: GameHistoryReq, sup_service: SupervisorService = Depends()):
    """
    Endpoint to get the game history for a user.
    """
    # This is a placeholder implementation. Replace with actual logic to retrieve game history.
    # For now, we will return a dummy response.
    response = sup_service.get_game_history(body.user_id)

    return response