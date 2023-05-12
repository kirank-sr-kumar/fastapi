"""add columns to posts

Revision ID: 8167de2babf6
Revises: c63abf8c5494
Create Date: 2023-05-12 14:39:43.888002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8167de2babf6'
down_revision = 'c63abf8c5494'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False)),

def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
