from pydantic import BaseModel, Field


class UserCreateReq(BaseModel):
    name: str = Field(..., description="The name of the user to be created")

class UserCreateResp(UserCreateReq):
    user_id: str = Field(..., description="The unique identifier of the created user")
