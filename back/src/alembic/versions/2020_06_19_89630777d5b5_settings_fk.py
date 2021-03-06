"""settings fk

Revision ID: 89630777d5b5
Revises: 77870ae5b560
Create Date: 2020-06-19 21:52:42.306259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89630777d5b5'
down_revision = '77870ae5b560'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'setting', 'community', ['community_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'setting', type_='foreignkey')
    # ### end Alembic commands ###
