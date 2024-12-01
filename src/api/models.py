import uuid

from pydantic import BaseModel


class TaskModel(BaseModel):
    task_id: uuid.UUID
    user_name: str
    user_email: str
    text: str
    is_completed: bool


class CreateTaskModel(BaseModel):
    user_name: str
    user_email: str
    text: str
    is_completed: bool | None = False


class EditTaskModel(BaseModel):
    text: str
    is_completed: bool


class ResponseTasksModel(BaseModel):
    current_page: int
    pages: int
    per_page: int
    tasks: list[TaskModel]


class LoginModel(BaseModel):
    user_name: str
    password: str
