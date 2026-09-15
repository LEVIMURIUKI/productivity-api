"""add model validation constraints

Revision ID: 55f89646d9b1
Revises: 4def256249ae
Create Date: 2026-09-15 15:34:20.017982

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "55f89646d9b1"
down_revision = "4def256249ae"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_check_constraint(
            "check_username_min_length",
            "length(username) >= 3"
        )
        batch_op.create_check_constraint(
            "check_email_min_length",
            "length(email) >= 5"
        )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.create_check_constraint(
            "check_title_min_length",
            "length(title) >= 1"
        )
        batch_op.create_check_constraint(
            "check_title_max_length",
            "length(title) <= 120"
        )


def downgrade():
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint(
            "check_title_max_length",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_title_min_length",
            type_="check"
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint(
            "check_email_min_length",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_username_min_length",
            type_="check"
        )
