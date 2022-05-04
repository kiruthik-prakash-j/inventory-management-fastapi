"""add foreign key to items

Revision ID: 81c52036b7aa
Revises: 31d0f52dec3d
Create Date: 2022-05-04 21:51:04.427238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81c52036b7aa'
down_revision = '31d0f52dec3d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('items', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('items_users_fk', 
        source_table="items", 
        referent_table="users", 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('items_users_fk', table_name="items")
    op.drop_column('items', 'owner_id')
    pass
