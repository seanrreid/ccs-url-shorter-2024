"""Changing Hashed Password type back to a String

Revision ID: 415d1e1368bb
Revises: a5326c831d5c
Create Date: 2024-03-04 20:18:36.484181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '415d1e1368bb'
down_revision: Union[str, None] = 'a5326c831d5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=postgresql.BYTEA(),
               type_=sa.String,
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String,
               type_=postgresql.BYTEA(),
               existing_nullable=True)
    # ### end Alembic commands ###
