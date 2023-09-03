"""Empty Init

Revision ID: a44e22de909e
Revises: 72ebacf6ab54
Create Date: 2023-09-03 12:49:36.257715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a44e22de909e'
down_revision: Union[str, None] = '72ebacf6ab54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
