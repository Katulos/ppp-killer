from __future__ import annotations

from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from .config import settings

users = {
    "admin": {
        "name": "Administrator",
        "avatar": "avatar.png",
        # "company_logo_url": "logo.png",
        "roles": [
            "read",
            "create",
            "edit",
            "delete",
        ],
    },
}


class UsernameAndPasswordProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"},
            )

        if username in users and password == settings.app.admin_password:
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            request.state.user = users.get(request.session["username"])
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user
        custom_app_title = "Hello, " + user["name"] + "!"
        custom_logo_url = None
        if user.get("company_logo_url", None):
            custom_logo_url = request.url_for(
                "static",
                path=user["company_logo_url"],
            )
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        if user["avatar"] is not None:
            photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
