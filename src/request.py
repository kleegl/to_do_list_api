from base import BaseSchema
from models import TaskStatus


class UserCreateRequest(BaseSchema):
    name: str
    password: str


class UserUpdateRequest(BaseSchema):
    name: str | None = None
    password: str | None = None


class TaskCreateRequest(BaseSchema):
    title: str
    content: str | None = None
    status: TaskStatus


class TaskUpdateRequest(BaseSchema):
    title: str | None = None
    content: str | None = None
    status: TaskStatus | None = None
