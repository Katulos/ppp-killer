from __future__ import annotations

import logging.config
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.starlette import register_tortoise

from .config import settings
from .exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from .logger import LOGGING_CONFIG
from .middlewares import language_processor

logging.config.dictConfig(LOGGING_CONFIG)


routes = [
    Mount(
        "/static",
        app=StaticFiles(directory=settings.app.static_dir),
        name="static",
    ),
]


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(BaseHTTPMiddleware, dispatch=language_processor),
]


@asynccontextmanager
async def lifespan(app: Starlette):
    yield


def get_application() -> Starlette:
    app = Starlette(
        debug=settings.app.debug,
        routes=routes,
        middleware=middleware,
    )
    app.add_exception_handler(
        HTTP_500_INTERNAL_SERVER_ERROR,
        server_error_exception,
    )
    app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    app.add_exception_handler(
        HTTP_401_UNAUTHORIZED,
        unauthorized_error_exception,
    )

    register_tortoise(
        app,
        db_url=settings.db.database_url,
        modules={"models": ["app.models"]},
        generate_schemas=True,
    )

    return app
