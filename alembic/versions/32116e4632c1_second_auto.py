"""Second auto

Revision ID: 32116e4632c1
Revises: 8b01ede63a42
Create Date: 2023-05-13 06:19:07.310614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32116e4632c1'
down_revision = '8b01ede63a42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('endusers')
    op.drop_table('endusercredentials')
    op.drop_table('users')
    op.drop_table('credentials')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('credentials',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_email', sa.INTEGER(), nullable=False),
    sa.Column('credential_id', sa.BLOB(), nullable=False),
    sa.Column('credential_public_key', sa.BLOB(), nullable=False),
    sa.Column('current_sign_count', sa.INTEGER(), nullable=True),
    sa.Column('credential_transport', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uid', sa.VARCHAR(length=40), nullable=True),
    sa.Column('email', sa.VARCHAR(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('endusercredentials',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('end_user_id', sa.INTEGER(), nullable=True),
    sa.Column('credential_id', sa.BLOB(), nullable=False),
    sa.Column('credential_public_key', sa.BLOB(), nullable=False),
    sa.Column('current_sign_count', sa.INTEGER(), nullable=True),
    sa.Column('credential_transport', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['end_user_id'], ['endusers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('endusers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('org', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['org'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
