import random
from datetime import datetime
from typing import List

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as statuses

from app.db import gino
from app.dependencies.auth import get_current_user
from app.game import Mark, get_winners
from app.models import Game, GameMove, User
from app.schemas.game import (CreateGameModel, GameModel, GameMoveCreateModel,
                              GameMoveCreateResponseModel, GameMoveModel)

__all__ = ("router",)

router = APIRouter()


@router.get("/{game_id}", response_model=GameModel)
async def get_game(game_id: int, user: User = Depends(get_current_user)):
    game = await Game.query.where(
        (Game.id == game_id) & (Game.user_id == user.id)
    ).gino.first()
    if not game:
        raise HTTPException(
            status_code=statuses.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game


@router.get("/", response_model=List[GameModel])
async def get_games(
        user: User = Depends(get_current_user),
        limit: int = Query(10),
        offset: int = Query(0),
):
    return await Game.query.where(
        Game.user_id == user.id
    ).limit(limit).offset(offset).order_by(Game.started_at.desc()).gino.all()


@router.post(
    "/",
    response_model=GameModel,
    status_code=statuses.HTTP_201_CREATED
)
async def create_game(
        data: CreateGameModel,
        user: User = Depends(get_current_user)
):
    game = await Game.create(
        user_id=user.id,
        started_at=datetime.utcnow(),
        size=data.size,
        user_mark=random.choice((Mark.X_MARK, Mark.O_MARK)),
        win_rule=data.win_rule
    )
    if game.user_mark == Mark.O_MARK:
        await GameMove.create(
            game_id=game.id,
            mark=Mark.get_opposite_mark(game.user_mark),
            position=[
                random.randint(0, data.size - 1),
                random.randint(0, data.size - 1),
            ]
        )
    return game


@router.get("/{game_id}/moves/", response_model=List[GameMoveModel])
async def get_moves(
        game_id: int,
        user: User = Depends(get_current_user),
        limit: int = Query(10),
        offset: int = Query(0),
):
    return await GameMove.load(game=Game).query.where(
        (GameMove.game_id == game_id) & (Game.user_id == user.id)
    ).limit(limit).offset(offset).order_by(
        GameMove.created_at.desc()
    ).gino.all()


@router.post(
    "/{game_id}/moves/",
    response_model=GameMoveCreateResponseModel,
    status_code=statuses.HTTP_201_CREATED
)
async def create_move(
        data: GameMoveCreateModel,
        game_id: int,
        user: User = Depends(get_current_user)
):
    # select for update. Prevent race condition
    async with gino.bind.transaction():
        game = await Game.query.with_for_update().where(
            (Game.id == game_id) & (Game.user_id == user.id)
        ).gino.first()
        if not game:
            raise HTTPException(
                status_code=statuses.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        # validate game
        if game.finished_at:
            raise HTTPException(
                status_code=statuses.HTTP_409_CONFLICT,
                detail="Game already finished"
            )
        if data.position[0] >= game.size or data.position[1] >= game.size:
            raise HTTPException(
                status_code=statuses.HTTP_409_CONFLICT,
                detail="Invalid position"
            )
        # get exist moves from db
        game_moves = await GameMove.query.where(
            GameMove.game_id == game.id
        ).with_only_columns([GameMove.position, GameMove.mark]).gino.all()
        exists_moves = {move.position: move.mark for move in game_moves}
        # validate input position
        if tuple(data.position) in exists_moves:
            raise HTTPException(
                status_code=statuses.HTTP_409_CONFLICT,
                detail="Position is not empty"
            )
        await GameMove.create(
            game_id=game.id,
            mark=game.user_mark,
            position=data.position
        )
        # create matrix with marks
        matrix = np.full((game.size, game.size), Mark.EMPTY_MARK.value)
        for exist_position, mark in exists_moves.items():
            matrix[exist_position] = mark.value
        matrix[tuple(data.position)] = game.user_mark.value
        # get available coordinates for ai
        available_choices = tuple(
            zip(*np.where(matrix == Mark.EMPTY_MARK.value)))
        available_choices_len = len(available_choices)
        ai_move = None
        if available_choices:
            # create ai move
            ai_position = random.choice(available_choices)
            matrix[ai_position] = Mark.get_opposite_mark(game.user_mark).value
            ai_move = await GameMove.create(
                game_id=game.id,
                mark=matrix[ai_position],
                position=ai_position
            )
            available_choices_len -= 1
        # get all winners
        winners = set(get_winners(matrix, game.win_rule))
        winner = None
        if winners:
            # if player and ai mark in winners both => player winner,
            # because it moved first
            winner = game.user_mark \
                if game.user_mark in winners \
                else Mark.get_opposite_mark(game.user_mark)
        # check game for end
        if winner or not available_choices_len:
            await game.update(
                finished_at=datetime.utcnow(),
                winner_mark=winner
            ).apply()
        return GameMoveCreateResponseModel(
            game=game,
            game_move=ai_move,
            winner=winner
        )
