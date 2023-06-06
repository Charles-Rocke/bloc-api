"""Added model import to migration env.py file

Revision ID: bca055ef21e8
Revises: 016c31085b50
Create Date: 2023-06-05 18:11:50.053764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bca055ef21e8'
down_revision = '016c31085b50'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
