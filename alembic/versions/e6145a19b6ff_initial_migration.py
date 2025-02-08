"""Initial migration

Revision ID: e6145a19b6ff
Revises:
Create Date: 2025-01-28 20:16:40.229393

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "e6145a19b6ff"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        "item",
        sa.Column(
            "item_uuid",
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "date_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("item_uuid"),
    )
    op.create_index(op.f("ix_item_item_uuid"), "item", ["item_uuid"], unique=False)
    op.create_index(op.f("ix_item_title"), "item", ["title"], unique=False)

    # Create trigger function for updating date_updated
    op.execute("""
        CREATE OR REPLACE FUNCTION update_date_updated_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.date_updated = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """)

    # Create the trigger that calls the function on updates
    op.execute("""
        CREATE TRIGGER update_item_date_updated
        BEFORE UPDATE ON item
        FOR EACH ROW
        EXECUTE FUNCTION update_date_updated_column();
        """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_item_date_updated ON item;")
    op.execute("DROP FUNCTION IF EXISTS update_date_updated_column;")
    op.drop_index(op.f("ix_item_title"), table_name="item")
    op.drop_index(op.f("ix_item_item_uuid"), table_name="item")
    op.drop_table("item")
