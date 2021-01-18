from pydantic import BaseModel

__all__ = ("PingModel",)


class PingModel(BaseModel):
    pong: str
