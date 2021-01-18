from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "CreateUserModel",
    "TokenModel",
)


class CreateUserModel(BaseModel):
    username: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expire_at: datetime

    class Config:
        orm_mode = True
