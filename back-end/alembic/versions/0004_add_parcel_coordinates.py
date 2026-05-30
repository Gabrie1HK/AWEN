"""add parcel coordinates

Revision ID: 0004_add_parcel_coordinates
Revises: 0003_add_tracking_coordinates
Create Date: 2026-05-28

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0004_add_parcel_coordinates"
down_revision = "0003_add_tracking_coordinates"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("parcels", sa.Column("origin_address", sa.String(length=200), nullable=True))
    op.add_column("parcels", sa.Column("origin_lat", sa.Float(), nullable=True))
    op.add_column("parcels", sa.Column("origin_lng", sa.Float(), nullable=True))
    op.add_column("parcels", sa.Column("destination_address", sa.String(length=200), nullable=True))
    op.add_column("parcels", sa.Column("destination_lat", sa.Float(), nullable=True))
    op.add_column("parcels", sa.Column("destination_lng", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("parcels", "destination_lng")
    op.drop_column("parcels", "destination_lat")
    op.drop_column("parcels", "destination_address")
    op.drop_column("parcels", "origin_lng")
    op.drop_column("parcels", "origin_lat")
    op.drop_column("parcels", "origin_address")
