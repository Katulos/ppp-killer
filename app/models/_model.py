from __future__ import annotations

from tortoise import Model


class AbstractModel(Model):
    class Meta:
        abstract = True
