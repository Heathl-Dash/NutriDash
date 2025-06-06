"""add last_updated to water_goal

Revision ID: 076cb480b68d
Revises: 
Create Date: 2025-05-29 18:54:04.562938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '076cb480b68d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('water_goals', sa.Column('last_updated', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('water_goals', 'last_updated')
    # ### end Alembic commands ###
