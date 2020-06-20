"""calls

Revision ID: 051b400f7f55
Revises: 89630777d5b5
Create Date: 2020-06-20 06:03:25.717735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '051b400f7f55'
down_revision = 'a1790f3645e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('call',
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('community_id', sa.BigInteger(), nullable=False),
    sa.Column('manager_id', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('call')
    # ### end Alembic commands ###
