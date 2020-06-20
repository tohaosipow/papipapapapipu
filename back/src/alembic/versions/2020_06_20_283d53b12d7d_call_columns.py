"""call columns

Revision ID: 283d53b12d7d
Revises: 051b400f7f55
Create Date: 2020-06-20 11:11:55.682760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283d53b12d7d'
down_revision = 'fbc121875bdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('call', sa.Column('answered', sa.Boolean(), nullable=False))
    op.add_column('call', sa.Column('hidden', sa.Boolean(), nullable=False))
    op.add_column('call', sa.Column('client_phone', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('call', 'client_phone')
    op.drop_column('call', 'hidden')
    op.drop_column('call', 'answered')
    # ### end Alembic commands ###
