from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from jinja2 import pass_context
from starlette.templating import Jinja2Templates

from .config import settings

templates = Jinja2Templates(directory=settings.app.templates_dir)
templates.env.add_extension("jinja2.ext.i18n")


@pass_context
def current_page_with_params(context: dict, params: dict):
    request = context.get("request")  # type:Request
    full_path = request.scope["raw_path"].decode()
    query_params = dict(request.query_params)
    for k, v in params.items():
        query_params[k] = v
    return full_path + "?" + urlencode(query_params)


templates.env.filters["current_page_with_params"] = current_page_with_params


def set_global_env(name: str, value: Any):
    templates.env.globals[name] = value


def add_template_folder(*folders: str):
    for folder in folders:
        templates.env.loader.searchpath.insert(0, folder)
