from flask import Blueprint, Response

bp = Blueprint(
    "api",
    __name__,
    static_folder="static",
    template_folder="templates",
)


@bp.route("/")
def get() -> Response:
    return Response("Hi, API's here ...")
