from flask import abort
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import delete, select

from src.app import db
from src.database.model.tasks import Task
from src.database.model.users import User


def get_user_by_name(name: str) -> User | None:
    stmt = select(User).where(User.name == name)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user


def get_tasks(page: int = 1, per_page: int = 3) -> Pagination:
    stmt = select(Task)
    tasks = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    return tasks


def get_task(task_id: str) -> Task | None:
    user = db.session.get(Task, task_id)
    return user


def add_task(
    user_name: str,
    user_email: str,
    text: str,
) -> Task:
    task = Task(
        user_name=user_name.lower().strip(),
        user_email=user_email.lower().strip(),
        text=text,
        is_completed=False,
    )

    db.session.add(task)
    db.session.commit()

    return task


def edit_task(
    task_id: str,
    new_text: str,
    new_is_completed: bool,
) -> Task:
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404, "No such task")

    task.text = new_text
    task.is_completed = new_is_completed

    db.session.commit()

    return task


def delete_task(
    task_id: str,
) -> None:
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404, "No such task")

    delete(Task).where(Task.id == task_id)
    db.session.commit()
