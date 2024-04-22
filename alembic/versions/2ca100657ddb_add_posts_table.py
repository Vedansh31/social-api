"""Add posts table

Revision ID: 2ca100657ddb
Revises: 
Create Date: 2024-04-12 14:28:14.181625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ca100657ddb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.column('id', sa.Integer(), primary_key = True),
                    sa.column('title', sa.String(), nnullable = False), sa.column('content', sa.String(), nullable = False),
                    sa.column('published', sa.Boolean(), nullable = False, server_default = 'TRUE'), sa.column('created_at', sa.TIMESTAMP(timezone= True), nullable = False, server_default = sa.text('NOW()')))
    pass


def downgrade():
    op.drop_table('posts')
    pass
