from datetime import datetime

from fastapi import APIRouter

from app.schemas.ping import PingModel

__all__ = ("router",)

router = APIRouter()


@router.get("/", response_model=PingModel)
async def ping():
    return {"pong": datetime.utcnow().isoformat()}
