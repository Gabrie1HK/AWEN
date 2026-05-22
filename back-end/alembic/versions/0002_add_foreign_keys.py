"""add foreign keys

Revision ID: 0002_add_foreign_keys
Revises: 0001_init_schema
Create Date: 2026-05-22

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002_add_foreign_keys"
down_revision = "0001_init_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE notifications SET user_id = NULL WHERE user_id IS NOT NULL AND user_id !~ '^[0-9]+$'")
    op.execute("UPDATE notifications SET user_id = NULL WHERE user_id = ''")

    op.alter_column(
        "notifications",
        "user_id",
        type_=sa.Integer(),
        postgresql_using="NULLIF(user_id, '')::integer",
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_deliveries_guide ON deliveries (guide)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_notifications_user_id ON notifications (user_id)")

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'uq_parcels_guide'
            ) THEN
                ALTER TABLE parcels
                ADD CONSTRAINT uq_parcels_guide
                UNIQUE USING INDEX ix_parcels_guide;
            END IF;
        END $$;
        """
    )

    op.create_foreign_key(
        "fk_tracking_events_guide_parcels_guide",
        "tracking_events",
        "parcels",
        ["guide"],
        ["guide"],
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_deliveries_guide_parcels_guide",
        "deliveries",
        "parcels",
        ["guide"],
        ["guide"],
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_batch_parcels_batch_id_batches_id",
        "batch_parcels",
        "batches",
        ["batch_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_batch_parcels_parcel_id_parcels_id",
        "batch_parcels",
        "parcels",
        ["parcel_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_notifications_user_id_users_id",
        "notifications",
        "users",
        ["user_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_notifications_user_id_users_id", "notifications", type_="foreignkey")
    op.drop_constraint("fk_batch_parcels_parcel_id_parcels_id", "batch_parcels", type_="foreignkey")
    op.drop_constraint("fk_batch_parcels_batch_id_batches_id", "batch_parcels", type_="foreignkey")
    op.drop_constraint("fk_deliveries_guide_parcels_guide", "deliveries", type_="foreignkey")
    op.drop_constraint("fk_tracking_events_guide_parcels_guide", "tracking_events", type_="foreignkey")

    op.drop_constraint("uq_parcels_guide", "parcels", type_="unique")
    op.create_index("ix_parcels_guide", "parcels", ["guide"], unique=True)

    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_index("ix_deliveries_guide", table_name="deliveries")

    op.alter_column(
        "notifications",
        "user_id",
        type_=sa.String(length=40),
        postgresql_using="user_id::text",
    )
