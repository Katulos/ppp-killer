from __future__ import annotations

from sqlalchemy import create_engine
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette_admin import CustomView, I18nConfig
from starlette_admin.contrib.sqla import Admin

from .config import settings
from .models import AbstractModel, Server, ServerSchema, Vlan, VlanSchema
from .provider import UsernameAndPasswordProvider
from .views import ServerView, VlanView

engine = create_engine(
    settings.db.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.app.debug,
)

AbstractModel.metadata.create_all(engine)

middlewares = [
    Middleware(SessionMiddleware, secret_key=settings.app.secret),
    Middleware(GZipMiddleware),
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.app.allowed_hosts,
    ),
]

routes = [
    Mount(
        "/static",
        app=StaticFiles(directory=settings.app.static_dir),
        name="static",
    ),
]

admin = Admin(
    engine,
    title="PPP Killer",
    auth_provider=UsernameAndPasswordProvider(),
    middlewares=middlewares,
    base_url="/",
    statics_dir=settings.app.static_dir,
    templates_dir=settings.app.templates_dir,
    logo_url="https://preview.tabler.io/static/logo-white.svg",
    login_logo_url="https://preview.tabler.io/static/logo.svg",
    index_view=CustomView(
        label="Dashboard",
        icon="fa fa-dashboard",
        template_path="dashboard.html",
    ),
    i18n_config=I18nConfig(
        default_locale="ru",
        language_switcher=["en", "ru"],
    ),
    debug=settings.app.debug,
)

admin.add_view(
    ServerView(Server, icon="fa fa-server", pydantic_model=ServerSchema),
)
admin.add_view(
    VlanView(Vlan, icon="fa fa-network-wired", pydantic_model=VlanSchema),
)

app = Starlette(routes=routes)

admin.mount_to(app)


def get_application() -> Starlette:
    return app
