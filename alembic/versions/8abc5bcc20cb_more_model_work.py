"""More Model work

Revision ID: 8abc5bcc20cb
Revises: 88c5db0dbc7b
Create Date: 2023-06-07 01:06:39.508086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8abc5bcc20cb'
down_revision = '88c5db0dbc7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('endusers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_org', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('origin', sa.String(), nullable=True))
        # batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_endusers_parent_org_users'), 'users', ['parent_org'], ['id'])
        batch_op.drop_column('org')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timezone', sa.String(length=50), nullable=True))
        batch_op.drop_constraint('unique_api_key', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_users_api_key'), ['api_key'])
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_users_uid'), ['uid'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_uid'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_users_api_key'), type_='unique')
        batch_op.create_unique_constraint('unique_api_key', ['api_key'])
        batch_op.drop_column('timezone')

    with op.batch_alter_table('endusers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('org', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_endusers_parent_org_users'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['org'], ['id'])
        batch_op.drop_column('origin')
        batch_op.drop_column('parent_org')

    # ### end Alembic commands ###