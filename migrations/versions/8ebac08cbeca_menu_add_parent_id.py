"""menu add parent_id

Revision ID: 8ebac08cbeca
Revises: 2bdde1bca83d
Create Date: 2022-05-21 22:43:11.368341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ebac08cbeca'
down_revision = '2bdde1bca83d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menu_menu', sa.Column('parent_id', sa.Integer(), nullable=False, comment='父菜单id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menu_menu', 'parent_id')
    # ### end Alembic commands ###
