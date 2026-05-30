"""add parcel_notes table

Revision ID: 0005_add_parcel_notes
Revises: 0004_add_parcel_coordinates
Create Date: 2026-05-28

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0005_add_parcel_notes"
down_revision = "0004_add_parcel_coordinates"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "parcel_notes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("guide", sa.String(length=40), nullable=False, index=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("parcel_notes")
