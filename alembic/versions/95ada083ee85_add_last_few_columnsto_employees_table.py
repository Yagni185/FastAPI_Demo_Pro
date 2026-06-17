"""add last few columnsto employees table

Revision ID: 95ada083ee85
Revises: 865687e3fd9b
Create Date: 2026-06-16 11:31:40.678557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95ada083ee85'
down_revision: Union[str, Sequence[str], None] = '865687e3fd9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('employees', sa.Column('dprt',sa.String(), nullable = True, server_default = 'Admin'))
    op.add_column('employees', sa.Column('is_active',sa.Boolean(), nullable = True, server_default = 'true'))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('employees','dprt')
    op.drop_column('employees','is_active')
