"""Adicionando tabela Ação

Revision ID: aa257488d6bd
Revises: b567784e5bd3
Create Date: 2024-11-12 11:06:05.292928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa257488d6bd'
down_revision: Union[str, None] = 'b567784e5bd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('acoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo_acao', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('anexo', sa.Integer(), nullable=False),
    sa.Column('dotacao', sa.Float(), nullable=False),
    sa.Column('uo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['uo_id'], ['uos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('acoes')
    # ### end Alembic commands ###
