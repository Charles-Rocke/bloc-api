"""Adding end user fields to generate fresh migration

Revision ID: 708e50098ec2
Revises: 484dd0c2d20f
Create Date: 2023-06-07 17:38:54.447985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708e50098ec2'
down_revision = '484dd0c2d20f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('endusers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_org', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('origin', sa.String(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_endusers_parent_org_users'), 'users', ['parent_org'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('endusers', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_endusers_parent_org_users'), type_='foreignkey')
        batch_op.drop_column('origin')
        batch_op.drop_column('email')
        batch_op.drop_column('parent_org')

    # ### end Alembic commands ###
