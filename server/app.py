import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "development-secret-key"
)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import models so Flask-Migrate can detect them
    from server import models

    # Import routes
    from server.routes import (
        register,
        login,
        me,
        get_tasks,
        create_task,
        get_task,
        update_task,
        delete_task
    )

    # Authentication routes
    app.add_url_rule(
        "/register",
        view_func=register,
        methods=["POST"]
    )

    app.add_url_rule(
        "/login",
        view_func=login,
        methods=["POST"]
    )

    app.add_url_rule(
        "/me",
        view_func=me,
        methods=["GET"]
    )

    # Task routes
    app.add_url_rule(
        "/tasks",
        view_func=get_tasks,
        methods=["GET"]
    )

    app.add_url_rule(
        "/tasks",
        view_func=create_task,
        methods=["POST"]
    )

    app.add_url_rule(
        "/tasks/<int:task_id>",
        view_func=get_task,
        methods=["GET"]
    )

    app.add_url_rule(
        "/tasks/<int:task_id>",
        view_func=update_task,
        methods=["PATCH"]
    )

    app.add_url_rule(
        "/tasks/<int:task_id>",
        view_func=delete_task,
        methods=["DELETE"]
    )

    return app


app = create_app()