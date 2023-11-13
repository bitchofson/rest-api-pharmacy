"""Create availability, pharmacy, available_in_pharmacy tables

Revision ID: d80d2d11f505
Revises: 378c964a738e
Create Date: 2023-11-13 23:49:15.343071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd80d2d11f505'
down_revision: Union[str, None] = '378c964a738e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pharmacy',
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('adress', sa.String(), nullable=False),
    sa.Column('opening', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('availability',
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('drug_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['drug_id'], ['drug.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('drug_id')
    )
    op.create_table('available_in_pharmacy',
    sa.Column('pharmacy_id', sa.Uuid(), nullable=False),
    sa.Column('availability_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['availability_id'], ['availability.id'], ),
    sa.ForeignKeyConstraint(['pharmacy_id'], ['pharmacy.id'], ),
    sa.PrimaryKeyConstraint('pharmacy_id', 'availability_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('available_in_pharmacy')
    op.drop_table('availability')
    op.drop_table('pharmacy')
    # ### end Alembic commands ###
