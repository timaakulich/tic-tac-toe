import os  # isort:skip
import sys  # isort:skip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa


import pytest  # noqa
import sqlalchemy
from async_asgi_testclient import TestClient
from async_generator import async_generator, yield_

from app import settings
from app.db import get_database_url, init_db
from app.main import app

settings.DB_NAME = f"{settings.DB_NAME}_test"  # monkey patching

gino = init_db()


@pytest.fixture(scope="module")
def sa_engine():
    rv = sqlalchemy.create_engine(get_database_url())
    gino.create_all(rv)
    yield rv
    gino.drop_all(rv)
    rv.dispose()


@pytest.fixture
@async_generator
async def bind(sa_engine):
    async with gino.with_bind(get_database_url()) as e:
        await yield_(e)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
