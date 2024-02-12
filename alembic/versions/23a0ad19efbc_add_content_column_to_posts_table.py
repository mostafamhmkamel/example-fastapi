"""add content column to posts table

Revision ID: 23a0ad19efbc
Revises: 1d54563f69bf
Create Date: 2024-02-12 13:05:36.013501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# almebic upgrade head -- used to upgrade to newest version
#alembic downgrade -1 -- used to go to one revision earlier

# revision identifiers, used by Alembic.
revision: str = '23a0ad19efbc'
down_revision: Union[str, None] = '1d54563f69bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
