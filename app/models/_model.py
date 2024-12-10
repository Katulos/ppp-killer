from __future__ import annotations

import sqlite3
import typing as t

from sqlalchemy import (
    Column,
    MetaData,
    event,
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)


class AbstractModel(AsyncAttrs, DeclarativeBase):
    # __abstract__ = True
    # __allow_unmapped__ = True

    _convention = {
        "all_column_names": lambda constraint, table: "_".join(
            [column.name for column in constraint.columns.values()],
        ),
        "ix": "ix__%(table_name)s__%(all_column_names)s",
        "uq": "uq__%(table_name)s__%(all_column_names)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": (
            "fk__%(table_name)s__%(all_column_names)s__"
            "%(referred_table_name)s"
        ),
        "pk": "pk__%(table_name)s",
    }
    metadata = MetaData(naming_convention=_convention)

    @declared_attr.directive
    # ruff: noqa
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        if type(dbapi_connection) is sqlite3.Connection:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    def to_dict(self) -> t.Dict:
        return {
            f"{self.__tablename__}_{col.name}": getattr(self, col.name)
            for col in t.cast(t.List[Column], self.__table__.columns)
        }
