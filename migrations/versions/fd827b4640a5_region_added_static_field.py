"""Region added static field

Revision ID: fd827b4640a5
Revises: 
Create Date: 2023-02-27 18:07:06.877634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd827b4640a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('regions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('static', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('regions', schema=None) as batch_op:
        batch_op.drop_column('static')

    # ### end Alembic commands ###