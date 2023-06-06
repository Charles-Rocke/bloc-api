"""Deleted all models so alembic can see

Revision ID: cdc7d076e097
Revises: a2bba0c903bd
Create Date: 2023-06-05 18:06:50.072136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdc7d076e097'
down_revision = 'a2bba0c903bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
