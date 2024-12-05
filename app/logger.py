from __future__ import annotations

import logging
import os
import pathlib
from typing import Any, Dict

from .config import settings

if settings.app.debug:
    _log_level = logging.DEBUG
else:
    _log_level = logging.INFO

_enable_handlers = ["default"]

LOGGING_CONFIG: Dict[str, Any] = {}

if os.name == "posix" and pathlib.Path("/dev/log").exists():
    _enable_handlers.append("syslog")


LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
        "syslog": {
            "format": "%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - '%(message)s'",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        # "syslog": {
        #     "address": "/dev/log",
        #     "level": "INFO",
        #     "facility": "daemon",
        #     "formatter": "syslog",
        #     "class": "logging.handlers.SysLogHandler",
        # },
    },
    "loggers": {
        "": {  # root logger
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
        "tortoise": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
        "tortoise.db_client": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
        "__main__": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": True,
        },
        "uvicorn.asgi": {
            "handlers": _enable_handlers,
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
# logging.config.dictConfig(LOGGING_CONFIG)
# logger = logging.getLogger(__name__)
