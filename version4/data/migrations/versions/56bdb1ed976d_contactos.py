"""contactos

Revision ID: 56bdb1ed976d
Revises: 
Create Date: 2024-04-02 21:09:58.103572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56bdb1ed976d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contactos2',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nombre', sa.String(length=80), nullable=False),
                    sa.Column('direccion', sa.String(length=120), nullable=True),
                    sa.Column('telefonos', sa.String(length=50), nullable=True),
                    sa.Column('fecha_nac', sa.Date(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contactos2')
    # ### end Alembic commands ###
