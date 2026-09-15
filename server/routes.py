from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from marshmallow import ValidationError

from server.app import db, bcrypt
from server.models import User, Task
from server.schemas import (
    RegisterSchema,
    LoginSchema,
    TaskSchema,
    TaskUpdateSchema
)

def register():
    data = request.get_json() or {}

    try:
        data = RegisterSchema().load(data)
    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    username = data["username"]
    email = data["email"]
    password = data["password"]

    if User.query.filter_by(username=username).first():
        return jsonify({
            "error": "Username already exists"
        }), 409

    if User.query.filter_by(email=email).first():
        return jsonify({
            "error": "Email already exists"
        }), 409

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


def login():
    data = request.get_json() or {}

    try:
        data = LoginSchema().load(data)
    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@jwt_required()
def me():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(user.to_dict()), 200


@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 10

    if per_page > 100:
        per_page = 100

    pagination = Task.query.filter_by(
        user_id=user_id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "tasks": [
            task.to_dict()
            for task in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    }), 200


@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())

    data = request.get_json() or {}

    try:
        data = TaskSchema().load(data)
    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        completed=data.get("completed", False),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify(task.to_dict()), 200


@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    data = request.get_json() or {}

    try:
        data = TaskUpdateSchema().load(data)
    except ValidationError as error:
        return jsonify({
            "errors": error.messages
        }), 400

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()

    return jsonify(task.to_dict()), 200


@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200