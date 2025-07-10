import uuid

from fastapi import APIRouter

from app.schemas.user import UserCreateReq, UserCreateResp
from app.core import session

user_router = APIRouter(prefix="/users")

@user_router.post("/")
async def create_user(body: UserCreateReq) -> UserCreateResp:
    """
    Endpoint to create a new user.
    """
    # Simulate user creation logic
    user_id = str(uuid.uuid4())
    session.create_user(user_id, body.name)
    return UserCreateResp(user_id=user_id, name=body.name)

