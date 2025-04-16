"""more titles

Revision ID: 9ce0def73b09
Revises: 8288ec79df35
Create Date: 2025-04-16 09:33:48.300343

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ce0def73b09"
down_revision: Union[str, None] = "8288ec79df35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("invoices", sa.Column("title", sa.String(), nullable=True))
    op.add_column(
        "product_plans",
        sa.Column(
            "name",
            sa.String(),
            nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_plans", "name")
    op.drop_column("invoices", "title")
    # ### end Alembic commands ###
