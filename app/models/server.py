from __future__ import annotations

from typing import List, Optional

from pydantic import Field, IPvAnyAddress, field_validator
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._mixin import CreatedUpdatedAtMixin
from ._model import AbstractModel
from ._schema import AbstractSchema


class ServerSchema(AbstractSchema):
    name: str = Field(min_length=5)

    ip_address: IPvAnyAddress

    description: Optional[str]


class Server(AbstractModel, CreatedUpdatedAtMixin):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str]

    ip_address: Mapped[str]

    description: Mapped[str] = mapped_column(nullable=True)

    vlans: Mapped[List["Vlan"]] = relationship(
        "Vlan",
        secondary="servervlans",
    )

    __table_args__ = (UniqueConstraint("name", "ip_address"),)


class VlanSchema(AbstractSchema):
    name: str = Field(min_length=5)

    number: int = Field(max)

    description: Optional[str]

    @field_validator("number")
    def validate_number(cls, v: int) -> int:
        if v < 2:
            raise ValueError("The value cannot be less than 2")
        elif v > 4094:
            raise ValueError("The value cannot be greater than 4094")
        elif v in [0, 1, 4095]:
            raise ValueError("Field must not have value %s", v)
        return v


class Vlan(AbstractModel, CreatedUpdatedAtMixin):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(String)

    number: Mapped[int] = mapped_column(Integer)

    description: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (UniqueConstraint("name", "number"),)


class ServerVlan(AbstractModel):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    server_id: Mapped[int] = mapped_column(ForeignKey(Server.id))

    vlan_id: Mapped[int] = mapped_column(ForeignKey(Vlan.id))

    __table_args__ = (UniqueConstraint("server_id", "vlan_id"),)
