"""add hashed_password to users_management

Revision ID: 0008_add_hashed_pass
Revises: 0007_add_note_visibility
Create Date: 2026-05-29

"""
from alembic import op
import sqlalchemy as sa


revision = "0008_add_hashed_pass"
down_revision = "0007_add_note_visibility"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users_management", sa.Column("hashed_password", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users_management", "hashed_password")
