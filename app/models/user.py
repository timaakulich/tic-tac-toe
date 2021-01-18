from app.db import gino
from app.db.base_model import BaseModel

__all__ = (
    "User",
    "UserToken"
)


class User(BaseModel):
    id = gino.Column(gino.Integer, primary_key=True)
    username = gino.Column(gino.String, nullable=False, unique=True)
    password_hash = gino.Column(gino.String, nullable=False)


class UserToken(BaseModel):
    id = gino.Column(gino.Integer, primary_key=True)
    user_id = gino.Column(
        gino.Integer,
        gino.ForeignKey("users.id")
    )
    access_token = gino.Column(gino.String(36), nullable=False, unique=True)
    expire_at = gino.Column(gino.DateTime, nullable=False)
