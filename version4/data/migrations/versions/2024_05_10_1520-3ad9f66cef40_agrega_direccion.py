"""agrega direccion

Revision ID: 3ad9f66cef40
Revises: 70cfd3cb4270
Create Date: 2024-05-10 15:20:19.879611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ad9f66cef40'
down_revision: Union[str, None] = '70cfd3cb4270'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contactos', sa.Column('calle', sa.String(length=80), nullable=True))
    op.add_column('contactos', sa.Column('numero', sa.Integer(), nullable=True))
    op.add_column('contactos', sa.Column('piso', sa.Integer(), nullable=True))
    op.add_column('contactos', sa.Column('depto', sa.String(length=10), nullable=True))
    op.add_column('contactos', sa.Column('localidad_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contactos', 'localidades', ['localidad_id'], ['id'])
    op.drop_column('contactos', 'direccion')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contactos', sa.Column('direccion', sa.VARCHAR(length=120, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'contactos', type_='foreignkey')
    op.drop_column('contactos', 'localidad_id')
    op.drop_column('contactos', 'depto')
    op.drop_column('contactos', 'piso')
    op.drop_column('contactos', 'numero')
    op.drop_column('contactos', 'calle')
    # ### end Alembic commands ###
