"""empty message

Revision ID: a3432c90ed3d
Revises: c6d664f1b1bd
Create Date: 2020-12-05 23:28:47.339894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3432c90ed3d'
down_revision = 'c6d664f1b1bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('booked', 'services_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('booked', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('booked', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('booked', 'services_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
