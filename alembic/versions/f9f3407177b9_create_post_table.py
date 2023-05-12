"""create post table

Revision ID: f9f3407177b9
Revises: 
Create Date: 2023-05-12 13:58:06.097032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9f3407177b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('title',sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
