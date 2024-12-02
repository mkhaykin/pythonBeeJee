import uuid
from http import HTTPStatus

import email_validator
from email_validator import EmailNotValidError
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_pydantic import validate

import src.database.service as db
from src.api.models import (
    CreateTaskModel,
    EditTaskModel,
    LoginModel,
    ResponseTasksModel,
    TaskModel,
)

bp = Blueprint(
    "api",
    __name__,
    static_folder="static",
    template_folder="templates",
)

RECORDS_PER_PAGE = 3


@bp.route("/tasks", methods=["GET"])
@validate()
def get_tasks() -> tuple[ResponseTasksModel | Response, HTTPStatus]:
    page = request.args.get("page", 1, type=int)
    sort_by = request.args.get("sort_by", -1, type=int)
    order = request.args.get("order", default="asc")

    if order.lower() not in ("asc", "desc"):
        return jsonify({"message": "ошибка порядка сортировки"}), HTTPStatus.BAD_REQUEST

    paginator = db.get_tasks(
        page=page,
        per_page=RECORDS_PER_PAGE,
        sort_by=sort_by,
        order=order,
    )
    return (
        ResponseTasksModel(
            current_page=paginator.page,
            per_page=paginator.per_page,
            pages=paginator.pages,
            tasks=paginator.items,  # type: ignore
        ),
        HTTPStatus.OK,
    )


@bp.route(
    "/task/<task_id>",
    methods=["GET"],
)
@validate()
def get_task(
    task_id: uuid.UUID,
) -> tuple[TaskModel | Response, HTTPStatus]:
    task = db.get_task(str(task_id))
    if not task:
        return jsonify({"error": "Task not found."}), HTTPStatus.NOT_FOUND

    return (
        TaskModel(
            task_id=task.id,
            user_name=task.user_name,
            user_email=task.user_email,
            text=task.text,
            is_completed=task.is_completed,
        ),
        HTTPStatus.OK,
    )


@bp.route("/task", methods=["POST"])
@validate()
def add_task(
    body: CreateTaskModel,
) -> tuple[TaskModel | Response, HTTPStatus]:
    try:
        email_validator.validate_email(
            body.user_email,
            check_deliverability=False,
            allow_smtputf8=False,
        )
    except EmailNotValidError:
        return jsonify({"message": "wrong email"}), HTTPStatus.BAD_REQUEST

    added_task = db.add_task(
        user_name=body.user_name,
        user_email=body.user_email,
        text=body.text,
        is_completed=body.is_completed or False,
    )

    return (
        TaskModel(
            task_id=added_task.id,
            user_name=added_task.user_name,
            user_email=added_task.user_email,
            text=added_task.text,
            is_completed=added_task.is_completed,
        ),
        HTTPStatus.CREATED,
    )


@bp.route("/task/<task_id>", methods=["PUT"])
@jwt_required()
@validate()
def edit_task(
    task_id: str,
    body: EditTaskModel,
) -> tuple[TaskModel | Response, HTTPStatus]:
    edited_task = db.edit_task(
        task_id=task_id,
        new_text=body.text,
        new_is_completed=body.is_completed,
    )

    return (
        TaskModel(
            task_id=edited_task.id,
            user_name=edited_task.user_name,
            user_email=edited_task.user_email,
            text=edited_task.text,
            is_completed=edited_task.is_completed,
        ),
        HTTPStatus.OK,
    )


@bp.route("/task/<task_id>", methods=["DELETE"])
@jwt_required()
def drop_task(
    task_id: str,
) -> tuple[Response, HTTPStatus]:
    db.delete_task(task_id)
    return jsonify({"status": "ok"}), HTTPStatus.OK


@bp.route("/token", methods=["post"])
@validate()
def token(
    body: LoginModel,
) -> tuple[Response, HTTPStatus]:
    username = body.user_name
    password = body.password

    user = db.get_user_by_name(username)

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.name)
        return (
            jsonify({"message": "Login Success", "access-token": access_token}),
            HTTPStatus.OK,
        )
    else:
        return jsonify({"message": "Login Failed"}), HTTPStatus.UNAUTHORIZED
