from flask import (  # Response,
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug import Response

import src.database.service as db
from src.web.forms.login_forms import LoginForm
from src.web.forms.task_form import TaskAddForm, TaskDropForm, TaskEditForm
from src.web.forms.utils import disable_form_items

bp = Blueprint(
    "web",
    __name__,
    static_folder="static",
    template_folder="templates",
)


@bp.route("/favicon.ico")
def favicon() -> str:
    return url_for("static", filename="favicon.ico")


@bp.route("/")
def index() -> str:
    page = request.args.get("page", 1, type=int)
    tasks = db.get_tasks(page=page)
    return render_template(
        "index.html",
        tasks=tasks.items,
        pagination=tasks,
    )


@bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """login page"""
    if current_user.is_authenticated:
        return redirect(url_for("web.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_name(request.form.get("user_name", ""))

        if user and user.check_password(password=form.password.data):
            login_user(user, remember=form.remember.data, force=True)
            flash("You have been logged in!", "success")
            return redirect(request.args.get("next") or url_for("web.index"))
        else:
            flash(
                "Login Unsuccessful. Please check username and password",
                "danger",
            )

    return render_template("login.html", title="Login", form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout() -> Response:
    logout_user()
    return redirect(url_for("web.index"))


@bp.route("/add", methods=["GET", "POST"])
def add_task() -> str | Response:
    """add task page"""

    form = TaskAddForm()
    if form.validate_on_submit():
        db.add_task(
            request.form.get("user_name", ""),
            request.form.get("user_email", ""),
            request.form.get("text", ""),
        )
        flash(
            "Task added.",
            "success",
        )
        return redirect(url_for("web.index"))

    return render_template("task.html", title="Create task", form=form)


@bp.route("/edit/<task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id: str) -> str | Response:
    """edit task page"""

    task = db.get_task(task_id)
    if task is None:
        abort(404, "No such task")

    form = TaskEditForm(
        user_name=task.user_name,
        user_email=task.user_email,
        text=task.text,
        is_completed=task.is_completed,
    )
    disable_form_items(
        form.user_name,
        form.user_email,
    )

    if form.validate_on_submit():
        db.edit_task(
            task_id,
            request.form.get("text", ""),
            bool(request.form.get("is_completed", False)),
        )
        flash(
            "Task edited.",
            "success",
        )
        return redirect(url_for("web.index"))

    return render_template("task.html", title="Edit task", form=form, action="edit")


@bp.route("/drop/<task_id>", methods=["GET", "POST"])
@login_required
def drop_task(task_id: str) -> str | Response:
    """edit task page"""

    task = db.get_task(task_id)
    if task is None:
        abort(404, "No such task")

    form = TaskDropForm(
        user_name=task.user_name,
        user_email=task.user_email,
        text=task.text,
        is_completed=task.is_completed,
    )
    disable_form_items(
        form.user_name,
        form.user_email,
        form.text,
        form.is_completed,
    )

    if form.validate_on_submit():
        if bool(request.form.get("confirm_deletion", False)):
            db.delete_task(
                task_id,
            )
            flash(
                "Task deleted.",
                "success",
            )
            return redirect(url_for("web.index"))
        else:
            flash(
                "To delete a task, check the 'Confirm deletion' box.",
                "warning",
            )

    return render_template("task.html", title="Delete task", form=form, action="edit")
