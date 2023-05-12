"""add user table

Revision ID: eb7b5f59f1bb
Revises: f9f3407177b9
Create Date: 2023-05-12 14:11:42.189209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb7b5f59f1bb'
down_revision = 'f9f3407177b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",sa.Column('id',sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table("users")
