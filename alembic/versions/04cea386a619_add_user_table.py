"""add user table

Revision ID: 04cea386a619
Revises: ca3f65078a41
Create Date: 2023-05-13 13:00:21.111889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04cea386a619'
down_revision = 'ca3f65078a41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_At', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')

                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
