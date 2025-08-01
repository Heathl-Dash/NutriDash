"""alter last_updated column to timestamptz

Revision ID: 8457838ec650
Revises: 076cb480b68d
Create Date: 2025-05-29 20:55:54.107138

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8457838ec650"
down_revision: Union[str, None] = "076cb480b68d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "water_goals",
        "last_updated",
        type_=sa.DateTime(timezone=True),
        postgresql_using="last_updated::timestamptz",
        existing_nullable=True,
        nullable=False,
        server_default=sa.func.now(),
    )


def downgrade() -> None:
    op.alter_column(
        "water_goals",
        "last_updated",
        type_=sa.DateTime(timezone=False),
        postgresql_using="last_updated::timestamp",
        existing_nullable=False,
        nullable=True,
        server_default=None,
    )
