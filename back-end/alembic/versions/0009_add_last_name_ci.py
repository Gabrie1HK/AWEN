"""add last_name and ci to users and users_management

Revision ID: 0009_add_last_name_ci
Revises: 0008_add_hashed_pass
Create Date: 2026-05-31

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0009_add_last_name_ci"
down_revision = "0008_add_hashed_pass"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_name", sa.String(120), nullable=True))
    op.add_column("users", sa.Column("ci", sa.String(20), nullable=True))
    op.add_column("users_management", sa.Column("last_name", sa.String(120), nullable=True))
    op.add_column("users_management", sa.Column("ci", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "ci")
    op.drop_column("users_management", "last_name")
    op.drop_column("users_management", "ci")
