"""add foreign key to post table

Revision ID: 8681bdac62bb
Revises: 04cea386a619
Create Date: 2023-05-13 13:10:48.464150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8681bdac62bb'
down_revision = '04cea386a619'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
