"""create post table

Revision ID: 1d54563f69bf
Revises: 
Create Date: 2024-02-12 12:50:24.129909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d54563f69bf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: #handles adding and changing in tables, call by typing alembic upgrade {version number}
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable = False,primary_key = True), sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None: #handles deleting tables, , call by typing alembic downgrade {version number}
    op.drop_table('posts')
    pass
