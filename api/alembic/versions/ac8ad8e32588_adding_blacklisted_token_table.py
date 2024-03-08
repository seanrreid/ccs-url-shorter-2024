"""Adding blacklisted token table

Revision ID: ac8ad8e32588
Revises: 415d1e1368bb
Create Date: 2024-03-07 19:32:08.239767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ac8ad8e32588'
down_revision: Union[str, None] = '415d1e1368bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisted_tokens',
                    sa.Column('id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint(
                        'id', name='blacklisted_tokens_pkey')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
