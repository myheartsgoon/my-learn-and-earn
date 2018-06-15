"""empty message

Revision ID: 7aacb05e6bc0
Revises: 5d63607a3f6c
Create Date: 2018-06-15 15:37:44.190679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aacb05e6bc0'
down_revision = '5d63607a3f6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('descp', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'descp')
    # ### end Alembic commands ###
