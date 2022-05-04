"""create items table

Revision ID: 317b19ab8317
Revises: 
Create Date: 2022-05-04 19:51:51.187768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '317b19ab8317'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('items', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('item_name', sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table('items')
    pass
