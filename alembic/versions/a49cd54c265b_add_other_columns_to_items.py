"""add other columns to items

Revision ID: a49cd54c265b
Revises: 81c52036b7aa
Create Date: 2022-05-04 21:57:34.049513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a49cd54c265b'
down_revision = '81c52036b7aa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('items', sa.Column('row_no', sa.Integer(), nullable=False))
    op.add_column('items', sa.Column('column_no', sa.Integer(), nullable=False))
    op.add_column('items', sa.Column('is_empty', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('items', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('items', 'row_no')
    op.drop_column('items', 'column_no')
    op.drop_column('items', 'is_empty')
    op.drop_column('items', 'created_at')
    pass
