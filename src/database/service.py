from flask import abort
from sqlalchemy import asc, case, delete, desc, select, text
from sqlalchemy.sql.functions import count

from src.api.models import TaskModel
from src.app import db
from src.database.model.tasks import Task
from src.database.model.users import User
from src.web.utils import MyPaginator


def get_user_by_name(name: str) -> User | None:
    stmt = select(User).where(User.name == name)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user


def get_tasks(
    page: int = 1,
    per_page: int = 3,
    sort_by: int = 4,
    order: str = "asc",
) -> MyPaginator:
    func_sort = {"asc": asc, "desc": desc}.get(order, asc)
    if sort_by <= 0:
        sort_by = 1
    stmt = select(
        Task.id.label("id"),
        Task.user_name.label("user_name"),
        Task.user_email.label("user_email"),
        Task.text.label("text"),
        Task.is_completed.label("is_completed"),
        case(
            (Task.updated_at != None, "updated"),  # noqa
            else_="",
        ).label("status"),
    )
    stmt_count = select(count()).select_from(Task)
    counts = db.session.execute(stmt_count).scalar()
    result_stmt = (
        stmt.offset((page - 1) * per_page)
        .limit(per_page)
        .order_by(func_sort(text(str(sort_by))))
    )
    tasks = db.session.execute(result_stmt)
    return MyPaginator(
        page=page,
        per_page=per_page,
        total=counts or 0,
        items=[
            TaskModel(
                task_id=task.id,
                user_name=task.user_name,
                user_email=task.user_email,
                text=task.text,
                is_completed=task.is_completed,
                status=task.status,
            )
            for task in tasks
        ],
    )


def get_task(task_id: str) -> Task | None:
    task = db.session.get(Task, task_id)
    return task


def add_task(
    user_name: str,
    user_email: str,
    text: str,
    is_completed: bool = False,
) -> Task:
    task = Task(
        user_name=user_name.lower().strip(),
        user_email=user_email.lower().strip(),
        text=text,
        is_completed=is_completed,
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

    stmt = delete(Task).where(Task.id == task_id)
    db.session.execute(stmt)
    db.session.commit()


def get_user(user_name: str) -> User | None:
    stmt = select(User).where(User.name == user_name)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user


def create_user(
    user_name: str,
    password: str,
) -> None:
    user = User(name=user_name)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
