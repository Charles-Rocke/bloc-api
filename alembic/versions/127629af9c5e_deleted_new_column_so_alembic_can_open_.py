"""deleted new column so alembic can open its fucking eyes

Revision ID: 127629af9c5e
Revises: 4eb4931200c0
Create Date: 2023-06-05 17:36:23.640760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '127629af9c5e'
down_revision = '4eb4931200c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
