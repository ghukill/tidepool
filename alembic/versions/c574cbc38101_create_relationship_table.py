"""create relationship table

Revision ID: c574cbc38101
Revises: e6145a19b6ff
Create Date: 2025-01-29 08:47:24.359702

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c574cbc38101"
down_revision: Union[str, None] = "e6145a19b6ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "relationship",
        sa.Column("relationship_uuid", sa.UUID(), nullable=False),
        sa.Column("subject", sa.String(), nullable=True),
        sa.Column("predicate", sa.String(), nullable=True),
        sa.Column("object", sa.String(), nullable=True),
        sa.Column(
            "date_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("relationship_uuid"),
    )
    op.create_index(
        op.f("ix_relationship_object"), "relationship", ["object"], unique=False
    )
    op.create_index(
        op.f("ix_relationship_predicate"), "relationship", ["predicate"], unique=False
    )
    op.create_index(
        op.f("ix_relationship_relationship_uuid"),
        "relationship",
        ["relationship_uuid"],
        unique=False,
    )
    op.create_index(
        op.f("ix_relationship_subject"), "relationship", ["subject"], unique=False
    )
    # ### end Alembic commands ###

    # Create the trigger that calls the function on updates
    op.execute("""
    CREATE TRIGGER update_relationship_date_updated
    BEFORE UPDATE ON relationship
    FOR EACH ROW
    EXECUTE FUNCTION update_date_updated_column();
    """)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TRIGGER IF EXISTS update_relationship_date_updated ON item;")
    op.drop_index(op.f("ix_relationship_subject"), table_name="relationship")
    op.drop_index(op.f("ix_relationship_relationship_uuid"), table_name="relationship")
    op.drop_index(op.f("ix_relationship_predicate"), table_name="relationship")
    op.drop_index(op.f("ix_relationship_object"), table_name="relationship")
    op.drop_table("relationship")
    # ### end Alembic commands ###
