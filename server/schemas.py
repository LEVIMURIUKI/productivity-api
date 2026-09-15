from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80)
    )

    email = fields.Email(
        required=True
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=6)
    )


class LoginSchema(Schema):
    username = fields.Str(
        required=True
    )

    password = fields.Str(
        required=True
    )


class TaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=120)
    )

    description = fields.Str(
        allow_none=True
    )

    completed = fields.Bool(
        load_default=False
    )


class TaskUpdateSchema(Schema):
    title = fields.Str(
        validate=validate.Length(min=1, max=120)
    )

    description = fields.Str(
        allow_none=True
    )

    completed = fields.Bool()