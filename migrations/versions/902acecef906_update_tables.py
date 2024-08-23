"""update  tables

Revision ID: 902acecef906
Revises: b4bc821294c3
Create Date: 2024-08-23 11:39:46.309230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '902acecef906'
down_revision: Union[str, None] = 'b4bc821294c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Adicionar novo campo e remover constraints usando batch mode
    with op.batch_alter_table('clinical_examinations', schema=None) as batch_op:
        batch_op.drop_column('user_id')  # Remover a coluna se necessário

    with op.batch_alter_table('clinical_histories', schema=None) as batch_op:
        batch_op.drop_column('user_id')  # Remover a coluna se necessário

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_column('user_id')  # Remover a coluna se necessário

def downgrade():
    # Reverter as alterações na migração
    with op.batch_alter_table('clinical_examinations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        # Recriar constraint se necessário
        # batch_op.create_foreign_key('fk_user_id', 'user', ['user_id'], ['id'])

    with op.batch_alter_table('clinical_histories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        # Recriar constraint se necessário
        # batch_op.create_foreign_key('fk_user_id', 'user', ['user_id'], ['id'])

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        # Recriar constraint se necessário
        # batch_op.create_foreign_key('fk_user_id', 'user', ['user_id'], ['id'])