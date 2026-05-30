"""add client_number to users

Revision ID: 0006_add_client_number
Revises: 0005_add_parcel_notes
Create Date: 2026-05-29

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0006_add_client_number"
down_revision = "0005_add_parcel_notes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("client_number", sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE users
        SET client_number = sub.row_num
        FROM (
            SELECT id, row_number() OVER (ORDER BY id) AS row_num
            FROM users
        ) sub
        WHERE users.id = sub.id
        """
    )
    op.alter_column("users", "client_number", nullable=False)
    op.create_unique_constraint("uq_users_client_number", "users", ["client_number"])


def downgrade() -> None:
    op.drop_constraint("uq_users_client_number", "users", type_="unique")
    op.drop_column("users", "client_number")
