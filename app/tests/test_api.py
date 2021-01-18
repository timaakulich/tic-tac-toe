from datetime import datetime, timedelta

import pytest

from app.game import Mark
from app.models import User, UserToken


@pytest.mark.asyncio
async def test_api(bind, client):
    response = await client.get("/v1/ping/")
    assert response.status_code == 200

    user = await User.create(
        username="test",
        password_hash="test"
    )
    await UserToken.create(
        user_id=user.id,
        access_token="access_token",
        expire_at=datetime.utcnow() + timedelta(seconds=600)
    )
    headers = {
        "Authorization": "Bearer access_token"
    }

    # get games
    response = await client.get("/v1/games/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []
    response = await client.post("/v1/games/", headers=headers, json={
        "size": 3,
        "win_rule": 4
    })
    assert response.status_code == 422

    response = await client.post("/v1/games/", headers=headers, json={
        "size": 3,
        "win_rule": 3
    })
    assert response.status_code == 201
    game_id = response.json()["id"]
    user_mark = response.json()["user_mark"]
    assert game_id == 1

    response = await client.get("/v1/games/", headers=headers)
    assert len(response.json()) == 1

    response = await client.get(f"/v1/games/{game_id}/moves/", headers=headers)
    moves_len = 0 if user_mark == Mark.X_MARK else 1  # noqa not (user_mark == Mark.X_MARK)
    assert len(response.json()) == moves_len
    if not moves_len:
        position = [0, 0]
    else:
        position = response.json()[0]["position"]
        position = [(position[0] + 1) % 3, (position[0] + 1) % 3]

    response = await client.post(
        f"/v1/games/{game_id}/moves/",
        headers=headers,
        json={
            "position": position
        }
    )
    assert response.status_code == 201
    response = await client.post(
        f"/v1/games/{game_id}/moves/",
        headers=headers,
        json={
            "position": position
        }
    )
    assert response.status_code == 409
