"""create phone number

Revision ID: d593096dcd02
Revises: 
Create Date: 2025-08-26 16:59:52.100569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd593096dcd02'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
