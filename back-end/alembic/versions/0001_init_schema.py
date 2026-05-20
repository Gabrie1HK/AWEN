"""init schema

Revision ID: 0001_init_schema
Revises: 
Create Date: 2026-05-20

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=40), nullable=False),
        sa.Column("branch", sa.String(length=120)),
        sa.Column("phone", sa.String(length=40)),
        sa.Column("address", sa.String(length=200)),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "users_management",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=40), nullable=False),
        sa.Column("branch", sa.String(length=120)),
        sa.Column("phone", sa.String(length=40)),
        sa.Column("address", sa.String(length=200)),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("last_login", sa.String(length=40)),
    )
    op.create_index("ix_users_management_email", "users_management", ["email"], unique=True)

    op.create_table(
        "branches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=200), nullable=False),
        sa.Column("manager", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "parcels",
        sa.Column("id", sa.String(length=20), primary_key=True),
        sa.Column("guide", sa.String(length=40), nullable=False),
        sa.Column("sender", sa.String(length=120), nullable=False),
        sa.Column("sender_id", sa.String(length=40), nullable=False),
        sa.Column("sender_phone", sa.String(length=40), nullable=False),
        sa.Column("recipient", sa.String(length=120), nullable=False),
        sa.Column("recipient_id", sa.String(length=40), nullable=False),
        sa.Column("recipient_phone", sa.String(length=40), nullable=False),
        sa.Column("recipient_address", sa.String(length=200), nullable=False),
        sa.Column("origin_branch", sa.String(length=120), nullable=False),
        sa.Column("destination_branch", sa.String(length=120), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("dimensions", sa.String(length=60), nullable=False),
        sa.Column("declared_value", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.String(length=20), nullable=False),
        sa.Column("updated_at", sa.String(length=20), nullable=False),
        sa.Column("qr_data", sa.String(length=60), nullable=False),
        sa.Column("barcode", sa.String(length=60), nullable=False),
    )
    op.create_index("ix_parcels_guide", "parcels", ["guide"], unique=True)

    op.create_table(
        "tracking_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guide", sa.String(length=40), nullable=False),
        sa.Column("step", sa.String(length=40), nullable=False),
        sa.Column("date", sa.String(length=20)),
        sa.Column("time", sa.String(length=10)),
        sa.Column("location", sa.String(length=200)),
        sa.Column("operator", sa.String(length=120)),
        sa.Column("completed", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_tracking_events_guide", "tracking_events", ["guide"])

    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plate", sa.String(length=20), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("capacity", sa.String(length=40), nullable=False),
        sa.Column("driver", sa.String(length=120)),
    )
    op.create_index("ix_vehicles_plate", "vehicles", ["plate"], unique=True)

    op.create_table(
        "batches",
        sa.Column("id", sa.String(length=20), primary_key=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("vehicle", sa.String(length=20)),
        sa.Column("driver", sa.String(length=120)),
        sa.Column("driver_id", sa.Integer()),
        sa.Column("parcel_count", sa.Integer(), nullable=False),
    )

    op.create_table(
        "batch_parcels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("batch_id", sa.String(length=20), nullable=False),
        sa.Column("parcel_id", sa.String(length=20), nullable=False),
    )
    op.create_index("ix_batch_parcels_batch_id", "batch_parcels", ["batch_id"])
    op.create_index("ix_batch_parcels_parcel_id", "batch_parcels", ["parcel_id"])

    op.create_table(
        "deliveries",
        sa.Column("id", sa.String(length=20), primary_key=True),
        sa.Column("guide", sa.String(length=40), nullable=False),
        sa.Column("recipient", sa.String(length=120), nullable=False),
        sa.Column("driver", sa.String(length=120), nullable=False),
        sa.Column("delivery_date", sa.String(length=20)),
        sa.Column("pod_type", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("signature_data", sa.String(length=500)),
        sa.Column("photo_url", sa.String(length=200)),
        sa.Column("gps", sa.String(length=40)),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.String(length=40), primary_key=True),
        sa.Column("user_id", sa.String(length=40)),
        sa.Column("text", sa.String(length=300), nullable=False),
        sa.Column("time", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.String(length=40), nullable=False),
        sa.Column("read", sa.Boolean(), nullable=False),
        sa.Column("action_type", sa.String(length=40), nullable=False),
        sa.Column("related_id", sa.String(length=40)),
    )


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("deliveries")
    op.drop_index("ix_batch_parcels_parcel_id", table_name="batch_parcels")
    op.drop_index("ix_batch_parcels_batch_id", table_name="batch_parcels")
    op.drop_table("batch_parcels")
    op.drop_table("batches")
    op.drop_index("ix_vehicles_plate", table_name="vehicles")
    op.drop_table("vehicles")
    op.drop_index("ix_tracking_events_guide", table_name="tracking_events")
    op.drop_table("tracking_events")
    op.drop_index("ix_parcels_guide", table_name="parcels")
    op.drop_table("parcels")
    op.drop_table("branches")
    op.drop_index("ix_users_management_email", table_name="users_management")
    op.drop_table("users_management")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
