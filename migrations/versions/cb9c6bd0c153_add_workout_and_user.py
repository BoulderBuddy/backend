"""Add workout and user

Revision ID: cb9c6bd0c153
Revises:
Create Date: 2022-05-04 14:36:24.493798

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cb9c6bd0c153"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=256), nullable=True),
        sa.Column("surname", sa.VARCHAR(length=256), nullable=True),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("is_superuser", sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    op.create_index("ix_user_email", "user", ["email"], unique=False)
    op.create_table(
        "workout",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("date", sa.DATE(), nullable=False),
        sa.Column("comment", sa.VARCHAR(), nullable=True),
        sa.Column("user_id", sa.VARCHAR(length=10), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workout_id", "workout", ["id"], unique=False)


def downgrade():
    op.drop_index("ix_workout_id", table_name="workout")
    op.drop_table("workout")
    op.drop_index("ix_user_email", table_name="user")
    op.drop_index("ix_user_id", table_name="user")
    op.drop_table("user")
