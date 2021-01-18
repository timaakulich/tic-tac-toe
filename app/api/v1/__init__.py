from fastapi import APIRouter

from app.api.v1 import auth, game, ping

api_router = APIRouter()

api_router.include_router(
    ping.router,
    tags=["ping"],
    prefix="/ping"
)
api_router.include_router(
    auth.router,
    tags=["auth"],
    prefix="/auth"
)
api_router.include_router(
    game.router,
    tags=["game"],
    prefix="/games"
)
