"""adding rest of columns

Revision ID: 6a206db2f982
Revises: dc14f874cbfd
Create Date: 2024-02-12 13:29:34.384383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

#alembic current -- in terminal to check which database version you're currently on

# revision identifiers, used by Alembic.
revision: str = '6a206db2f982'
down_revision: Union[str, None] = 'dc14f874cbfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default = 'TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('NOW()')))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
