from datetime import datetime
from typing import List
from base import BaseSchema
from models import TaskStatus


class TaskResponse(BaseSchema):
    id: int
    title: str
    content: str | None = None
    created_at: datetime
    updated_at: datetime
    status: TaskStatus
    user_id: int


class UserBaseResponse(BaseSchema):
    id: int
    name: str
    is_admin: bool


class UserResponse(BaseSchema):
    id: int
    name: str
    tasks: List[TaskResponse] | None = None
