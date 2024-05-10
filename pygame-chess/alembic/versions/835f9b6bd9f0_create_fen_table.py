"""create fen table

Revision ID: 835f9b6bd9f0
Revises: 
Create Date: 2024-05-08 12:50:30.339491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '835f9b6bd9f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'Fen',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('fen', sa.String(75), nullable=False),
    )



def downgrade():
    op.drop_table('Fen')
