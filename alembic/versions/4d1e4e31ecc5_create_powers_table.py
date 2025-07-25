"""create powers table

Revision ID: 4d1e4e31ecc5
Revises: 
Create Date: 2025-07-07 12:34:01.446759

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d1e4e31ecc5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('powers',
    sa.Column('power_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('power_damage', sa.Integer(), nullable=False),
    sa.Column('power_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('power_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('powers')
    # ### end Alembic commands ###
