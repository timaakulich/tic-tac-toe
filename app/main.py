import os  # isort:skip
import sys  # isort:skip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa

from fastapi import FastAPI

from app import settings
from app.db import init_db, pop_bind, set_bind

__all__ = ("app", )


app = FastAPI(title=settings.PROJECT)

gino = init_db()
gino.init_app(app)

from app.api.v1 import api_router as api_v1 # noqa isort:skip
app.include_router(api_v1, prefix="/v1")


@app.on_event("startup")
async def startup():
    await set_bind()


@app.on_event("shutdown")
async def shutdown():
    await pop_bind()
