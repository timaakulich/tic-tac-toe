from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY

from app.db import gino
from app.db.base_model import BaseModel

__all__ = (
    "Game",
    "GameMove"
)

from app.game import Mark


class Game(BaseModel):
    id = gino.Column(gino.Integer, primary_key=True)
    user_id = gino.Column(
        gino.Integer,
        gino.ForeignKey("users.id")
    )
    started_at = gino.Column(gino.DateTime, nullable=False, index=True)
    finished_at = gino.Column(gino.DateTime)
    user_mark = gino.Column(gino.Enum(Mark), nullable=False)
    winner_mark = gino.Column(gino.Enum(Mark))
    size = gino.Column(gino.Integer, nullable=False)
    win_rule = gino.Column(gino.Integer, nullable=False)


class GameMove(BaseModel):
    id = gino.Column(gino.Integer, primary_key=True)
    game_id = gino.Column(
        gino.Integer,
        gino.ForeignKey("games.id")
    )
    created_at = gino.Column(
        gino.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )
    mark = gino.Column(gino.Enum(Mark))
    position = gino.Column(ARRAY(gino.Integer, as_tuple=True))
