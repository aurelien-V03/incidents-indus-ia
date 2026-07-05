"""remove business key pk on silver tables

Revision ID: d7a6c78d8bd4
Revises: de63fa565140
Create Date: 2026-07-05 13:23:37.534413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7a6c78d8bd4'
down_revision: Union[str, Sequence[str], None] = 'de63fa565140'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLES = ('silver_machine', 'silver_maintenance', 'silver_releves_incidents', 'silver_telemetry')

OLD_PK_COLUMNS = {
    'silver_machine': ['machine_code'],
    'silver_maintenance': ['maintenance_id'],
    'silver_releves_incidents': ['incident_id'],
    'silver_telemetry': ['machine_id', 'date'],
}


def upgrade() -> None:
    """Upgrade schema."""
    for table in TABLES:
        op.add_column(table, sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False))
        op.drop_constraint(f'{table}_pkey', table, type_='primary')
        op.create_primary_key(f'{table}_pkey', table, ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    for table in TABLES:
        op.drop_constraint(f'{table}_pkey', table, type_='primary')
        op.create_primary_key(f'{table}_pkey', table, OLD_PK_COLUMNS[table])
        op.drop_column(table, 'id')
