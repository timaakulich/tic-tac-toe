from gino.declarative import ModelType

from app.db import init_db

__all__ = (
    "BaseModel",
)

db = init_db()


class _BaseMeta(ModelType):
    def __new__(mcs, name, bases, attrs):
        if not attrs.get("__abstract__"):
            attrs["__tablename__"] = f"{name.lower()}s"
        return ModelType.__new__(mcs, name, bases, attrs)


class BaseModel(db.Model, metaclass=_BaseMeta):
    __abstract__ = True
