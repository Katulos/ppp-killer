from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AbstractSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
