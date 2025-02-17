"""convert Item description to metadata column

Revision ID: 8191c61b75df
Revises: 7f14f9b46f7b
Create Date: 2025-02-08 17:28:59.379950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8191c61b75df'
down_revision: Union[str, None] = '7f14f9b46f7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('jsonld_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=False))
    op.drop_column('item', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('item', 'jsonld_metadata')
    # ### end Alembic commands ###
