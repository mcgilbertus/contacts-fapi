"""contacto

Revision ID: fb83fef634aa
Revises: 
Create Date: 2024-04-02 21:50:31.855272

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fb83fef634aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contactos3',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nombre', sa.String(length=80), nullable=False),
                    sa.Column('direccion', sa.String(length=120), nullable=True),
                    sa.Column('telefonos', sa.String(length=50), nullable=True),
                    sa.Column('fecha_nac', sa.Date(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('contactos3')
