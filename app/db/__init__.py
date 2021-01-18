from gino_starlette import Gino

from app import settings

__all__ = (
    "gino",
    "init_db",
    "get_db",
    "set_bind",
    "pop_bind",
    "get_database_url"
)


def get_database_url():
    return "postgresql://{user}:{password}@{host}:{port}/{db}".format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        db=settings.DB_NAME,
    )


gino: Gino = None


def init_db():
    global gino
    if gino is None:
        gino = Gino(
            dsn=get_database_url(),
            pool_min_size=getattr(settings, "DB_POOL_MIN_SIZE", 1),
            pool_max_size=getattr(settings, "DB_POOL_MAX_SIZE", 10),
            echo=getattr(settings, "DB_ECHO", False),
            ssl=getattr(settings, "DB_SSL", None),
            use_connection_for_request=getattr(
                settings, "DB_USE_CONNECTION_FOR_REQUEST", True),  # noqa
            retry_limit=getattr(settings, "DB_RETRY_LIMIT", 32,),
            retry_interval=getattr(settings, "DB_RETRY_INTERVAL", 1)
        )
    return gino


def get_db():
    global gino
    if gino is None:
        raise Exception("Call 'init_db' first")
    return gino


async def set_bind():
    global gino
    await gino.set_bind(get_database_url())


async def pop_bind():
    global gino
    await gino.pop_bind().close()
