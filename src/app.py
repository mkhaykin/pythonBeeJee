from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_wtf.csrf import CSRFProtect

from src.database.connection.connection import SQLALCHEMY_DATABASE_URL
from src.database.connection.utils import create_tables

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager: LoginManager = LoginManager()


def create_app() -> Flask:
    from src.api.routes import bp as bp_api
    from src.database.model.users import User
    from src.database.service import create_user, get_user_by_name
    from src.settings import settings
    from src.web.routes import bp as bp_web

    create_tables()

    app = Flask(__name__)

    app.config.update(**settings.__dict__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL

    csrf.init_app(app)
    db.init_app(app)

    login_manager.login_view = "web.login"
    login_manager.login_message = "You have to log in to access this page."
    login_manager.user_loader(lambda user_id: db.session.get(User, user_id))
    login_manager.init_app(app)

    app.register_blueprint(bp_web, url_prefix="")

    bp_swagger = get_swaggerui_blueprint(
        base_url="/api/docs",
        api_url="/static/swagger.jaml",
    )
    app.register_blueprint(bp_swagger, url_prefix="/api/docs")

    CORS(bp_api)
    app.register_blueprint(bp_api, url_prefix="/api")
    csrf.exempt(bp_api)

    JWTManager(app)

    with app.app_context():
        if not get_user_by_name("admin"):
            create_user("admin", "123")

    return app
