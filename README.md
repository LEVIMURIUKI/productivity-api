# Productivity API

A secure Flask REST API for managing personal productivity tasks.

Each authenticated user can create, view, update, and delete their own tasks. JWT authentication is used to protect the API and ensure users cannot access another user's tasks.

## Features

- User registration
- Secure password hashing with Flask-Bcrypt
- JWT-based authentication
- Protected API routes
- User-specific task ownership
- Full CRUD operations for tasks
- Pagination for task listings
- Marshmallow request validation
- SQLAlchemy database models
- Flask-Migrate database migrations
- Automated pytest test suite
- Database and model-level validation

## Technologies

- Python
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 4.0.0
- Flask-Bcrypt 1.0.1
- Flask-JWT-Extended
- Marshmallow 3.20.1
- Flask-RESTful
- SQLite
- Pytest 7.2.0
- Pipenv

## Project Structure

```text
productivity-api/
├── migrations/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── seed.py
├── tests/
│   ├── test_api.py
│   └── test_models.py
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── pytest.ini
└── README.md
