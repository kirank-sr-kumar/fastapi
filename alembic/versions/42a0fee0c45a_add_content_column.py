"""add content column

Revision ID: 42a0fee0c45a
Revises: 25134142c072
Create Date: 2023-05-12 15:44:43.443250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42a0fee0c45a'
down_revision = '238acaba5127'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
