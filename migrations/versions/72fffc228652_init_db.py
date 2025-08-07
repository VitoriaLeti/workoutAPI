"""init db

Revision ID: 72fffc228652
Revises: 251b5cafdc8b
Create Date: 2025-07-31 14:07:06.634736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72fffc228652'
down_revision: Union[str, Sequence[str], None] =  None

branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # Criação da tabela categorias
    op.create_table(
        'categorias',
        sa.Column('pk_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=50), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('pk_id'),
        sa.UniqueConstraint('nome')
    )

    # Criação da tabela centros_treinamento
    op.create_table(
        'centros_treinamento',
        sa.Column('pk_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=50), nullable=False),
        sa.Column('endereco', sa.String(length=60), nullable=False),
        sa.Column('proprietario', sa.String(length=30), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('pk_id'),
        sa.UniqueConstraint('nome')
    )

    # Criação da tabela atletas
    op.create_table(
        'atletas',
        sa.Column('pk_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=50), nullable=False),
        sa.Column('cpf', sa.String(length=14), nullable=False),
        sa.Column('idade', sa.Integer(), nullable=False),
        sa.Column('peso', sa.Float(), nullable=False),
        sa.Column('altura', sa.Float(), nullable=False),
        sa.Column('sexo', sa.String(length=1), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('categoria_id', sa.Integer(), nullable=False),
        sa.Column('centro_treinamento_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['categoria_id'], ['categorias.pk_id']),
        sa.ForeignKeyConstraint(['centro_treinamento_id'], ['centros_treinamento.pk_id']),
        sa.PrimaryKeyConstraint('pk_id'),
        sa.UniqueConstraint('cpf')
    )
