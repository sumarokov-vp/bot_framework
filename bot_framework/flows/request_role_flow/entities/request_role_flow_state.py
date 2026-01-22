from pydantic import BaseModel


class RequestRoleFlowState(BaseModel):
    requester_user_id: int
    selected_role_id: int | None = None
