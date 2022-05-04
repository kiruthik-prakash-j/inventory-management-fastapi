"""add quantity column to post

Revision ID: b9c0b6e10e7e
Revises: 317b19ab8317
Create Date: 2022-05-04 20:06:27.345918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c0b6e10e7e'
down_revision = '317b19ab8317'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("items", sa.Column("quantity", sa.Integer(), nullable=False, server_default='0'))
    pass


def downgrade():
    op.drop_column("items", "quantity")
    pass
