"""Delete unique drug_id

Revision ID: 5bfbea9f4a40
Revises: f38f67bfa0ad
Create Date: 2023-11-28 18:41:23.847994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bfbea9f4a40'
down_revision: Union[str, None] = 'f38f67bfa0ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('availability_drug_id_key', 'availability', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('availability_drug_id_key', 'availability', ['drug_id'])
    # ### end Alembic commands ###
