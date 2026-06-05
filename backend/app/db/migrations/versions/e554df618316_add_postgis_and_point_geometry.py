"""Add PostGIS and point_geometry

Revision ID: e554df618316
Revises: a3eba8da7ce0
Create Date: 2026-06-04 15:26:52.367124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e554df618316'
down_revision: Union[str, Sequence[str], None] = 'a3eba8da7ce0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    import geoalchemy2
    
    # Add point_geometry column to locations table
    op.add_column(
        'locations',
        sa.Column(
            'point_geometry',
            geoalchemy2.types.Geography(
                geometry_type='POINT', 
                srid=4326, 
                from_text='ST_GeogFromText', 
                name='geography',
                spatial_index=True
            ),
            nullable=True
        )
    )


def downgrade() -> None:
    op.drop_column('locations', 'point_geometry')
    op.execute("DROP EXTENSION IF EXISTS postgis;")
