from __future__ import annotations

from ._mixin import CreatedUpdatedMixin
from ._model import AbstractModel


class Server(AbstractModel, CreatedUpdatedMixin): ...
