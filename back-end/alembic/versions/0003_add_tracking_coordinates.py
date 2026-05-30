"""add tracking coordinates

Revision ID: 0003_add_tracking_coordinates
Revises: 0002_add_foreign_keys
Create Date: 2026-05-28

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0003_add_tracking_coordinates"
down_revision = "0002_add_foreign_keys"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tracking_events", sa.Column("lat", sa.Float(), nullable=True))
    op.add_column("tracking_events", sa.Column("lng", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("tracking_events", "lng")
    op.drop_column("tracking_events", "lat")
