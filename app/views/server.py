from __future__ import annotations

from starlette.requests import Request
from starlette_admin.contrib.sqla.ext.pydantic import ModelView


class ServerView(ModelView):
    fields = [
        "name",
        "ip_address",
        "vlans",
        "description",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list = [
        "id",
        "ip_address",
        "description",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]

    # async def validate(self, request: Request, data: Dict[str, Any]) -> None:
    #     errors: Dict[str, str] = {}
    #     session: Session = request.state.session
    #
    #     server_exists = (
    #         session.query(self.model.id)
    #         .filter_by(ip_address=data["ip_address"])
    #         .first()
    #         is not None
    #     )
    #     if server_exists and data.get("id"):
    #         errors["ip_address"] = "Must be unique"
    #     if len(errors) > 0:
    #         raise FormValidationError(errors)
    #     return await super().validate(request, data)

    def can_view_details(self, request: Request) -> bool:
        return "read" in request.state.user["roles"]

    def can_create(self, request: Request) -> bool:
        return "create" in request.state.user["roles"]

    def can_edit(self, request: Request) -> bool:
        return "edit" in request.state.user["roles"]

    def can_delete(self, request: Request) -> bool:
        return "delete" in request.state.user["roles"]

    async def is_action_allowed(self, request: Request, name: str) -> bool:
        return await super().is_action_allowed(request, name)


class VlanView(ModelView):
    exclude_fields_from_list = ["id", "created_at", "updated_at"]
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]
    #
    #     async def validate(self, request: Request, data: Dict[str, Any]) -> None:
    #         errors: Dict[str, str] = {}
    #         session: Session = request.state.session
    #
    #         name_exists = (
    #             session.query(self.model.id).filter_by(name=data["name"]).first()
    #             is not None
    #         )
    #         number_exists = (
    #             session.query(self.model.id)
    #             .filter_by(number=data["number"])
    #             .first()
    #             is not None
    #         )
    #         if name_exists:
    #             errors["name"] = "Must be unique"
    #         if number_exists:
    #             errors["number"] = "Must be unique"
    #         if len(errors) > 0:
    #             raise FormValidationError(errors)
    #         return await super().validate(request, data)

    def can_view_details(self, request: Request) -> bool:
        return "read" in request.state.user["roles"]

    def can_create(self, request: Request) -> bool:
        return "create" in request.state.user["roles"]

    def can_edit(self, request: Request) -> bool:
        return "edit" in request.state.user["roles"]

    def can_delete(self, request: Request) -> bool:
        return "delete" in request.state.user["roles"]

    async def is_action_allowed(self, request: Request, name: str) -> bool:
        return await super().is_action_allowed(request, name)
