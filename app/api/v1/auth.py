import uuid
from datetime import datetime, timedelta

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as statuses
from fastapi.security import OAuth2PasswordRequestForm

from app import settings
from app.models import User, UserToken
from app.schemas.auth import CreateUserModel, TokenModel
from app.utils import get_password_hash

router = APIRouter()


async def _create_token(user_id: int) -> UserToken:
    return await UserToken.create(
        user_id=user_id,
        access_token=str(uuid.uuid4()),
        expire_at=datetime.utcnow() + timedelta(seconds=settings.TOKEN_TTL)
    )


@router.post("/users", response_model=TokenModel)
async def create_user(data: CreateUserModel):
    try:
        user = await User.create(
            username=data.username,
            password_hash=get_password_hash(data.password)
        )
    except UniqueViolationError:
        raise HTTPException(
            statuses.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    else:
        return await _create_token(user.id)


@router.post("/token", response_model=TokenModel, name="get_token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.query.where(
        User.username == form_data.username
    ).gino.first()
    if not user or user.password_hash != get_password_hash(form_data.password):
        raise HTTPException(
            status_code=statuses.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    return await _create_token(user.id)
