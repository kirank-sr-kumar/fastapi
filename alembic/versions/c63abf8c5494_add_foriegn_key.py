"""add foriegn key

Revision ID: c63abf8c5494
Revises: eb7b5f59f1bb
Create Date: 2023-05-12 14:22:19.580333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c63abf8c5494'
down_revision = 'eb7b5f59f1bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='posts')
