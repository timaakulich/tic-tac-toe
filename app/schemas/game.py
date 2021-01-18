from datetime import datetime
from typing import List

from pydantic import BaseModel, validator

__all__ = (
    "CreateGameModel",
    "GameModel",
    "GameMoveModel",
    "GameMoveCreateModel",
    "GameMoveCreateResponseModel"
)

from app import settings
from app.game import Mark


class CreateGameModel(BaseModel):
    size: int = settings.MIN_GAME_SIZE
    win_rule: int = settings.MIN_GAME_SIZE

    @validator("size")
    def validate_size(cls, value):
        if value < settings.MIN_GAME_SIZE:
            raise ValueError("Invalid game size")
        return value

    @validator("win_rule")
    def validate_win_rule(cls, value, values):
        if value < settings.MIN_GAME_SIZE:
            raise ValueError("Invalid win rule")
        if value > values["size"]:
            raise ValueError("Win rule can not be more than game size")
        return value


class GameModel(BaseModel):
    id: int
    started_at: datetime
    finished_at: datetime = None
    user_mark: Mark
    winner_mark: Mark = None
    size: int
    win_rule: int

    class Config:
        orm_mode = True


class GameMoveModel(BaseModel):
    id: int
    created_at: datetime
    mark: Mark
    position: List[int]

    class Config:
        orm_mode = True


class GameMoveCreateModel(BaseModel):
    position: List[int]

    @validator("position")
    def validate_position(cls, value):
        if len(value) != 2:
            raise ValueError("Invalid position. Length must be equal to 2")
        if value[0] < 0 or value[1] < 0:
            raise ValueError("Coordinate must be >= 0")
        return value


class GameMoveCreateResponseModel(BaseModel):
    game: GameModel
    game_move: GameMoveModel = None
    winner: Mark = None
