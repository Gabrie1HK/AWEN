"""add is_public to parcel_notes

Revision ID: 0007_add_note_visibility
Revises: 0006_add_client_number
Create Date: 2026-05-29

"""
from alembic import op
import sqlalchemy as sa


revision = "0007_add_note_visibility"
down_revision = "0006_add_client_number"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("parcel_notes", sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.alter_column("parcel_notes", "is_public", server_default=None)


def downgrade() -> None:
    op.drop_column("parcel_notes", "is_public")
