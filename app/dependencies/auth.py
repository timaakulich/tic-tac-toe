from fastapi import Depends, HTTPException
from fastapi import status as statuses
from fastapi.security import OAuth2PasswordBearer

from app.models import User, UserToken


async def get_user_by_token(token) -> User:
    token = await UserToken.load(user=User).query.where(
        UserToken.access_token == token
    ).gino.first()
    if token:
        return token.user


async def get_current_user(token: str = Depends(OAuth2PasswordBearer(
    tokenUrl="/v1/auth/token"
))):
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=statuses.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
