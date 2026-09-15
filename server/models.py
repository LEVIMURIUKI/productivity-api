from datetime import datetime

from sqlalchemy.orm import validates

from server.app import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        db.CheckConstraint(
            "length(username) >= 3",
            name="check_username_min_length"
        ),
        db.CheckConstraint(
            "length(email) >= 5",
            name="check_email_min_length"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @validates("username")
    def validate_username(self, key, username):
        if not username or len(username.strip()) < 3:
            raise ValueError(
                "Username must be at least 3 characters long"
            )

        if len(username) > 80:
            raise ValueError(
                "Username must not exceed 80 characters"
            )

        return username.strip()

    @validates("email")
    def validate_email(self, key, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        if len(email) > 120:
            raise ValueError(
                "Email must not exceed 120 characters"
            )

        return email.lower().strip()

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class Task(db.Model):
    __tablename__ = "tasks"

    __table_args__ = (
        db.CheckConstraint(
            "length(title) >= 1",
            name="check_title_min_length"
        ),
        db.CheckConstraint(
            "length(title) <= 120",
            name="check_title_max_length"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(120),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="tasks"
    )

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        if len(title.strip()) > 120:
            raise ValueError(
                "Task title must not exceed 120 characters"
            )

        return title.strip()

    @validates("completed")
    def validate_completed(self, key, completed):
        if not isinstance(completed, bool):
            raise ValueError(
                "Completed must be a boolean"
            )

        return completed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }