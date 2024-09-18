"""agrega localidades y provincias

Revision ID: 70cfd3cb4270
Revises: b49152c06357
Create Date: 2024-04-30 23:51:13.149745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70cfd3cb4270'
down_revision: Union[str, None] = 'b49152c06357'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('provincias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('pais', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('localidades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('provincia_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['provincia_id'], ['provincias.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('localidades')
    op.drop_table('provincias')
    # ### end Alembic commands ###