"""Initial tables

Revision ID: a3eba8da7ce0
Revises: 
Create Date: 2026-05-31 14:08:34.549970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3eba8da7ce0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'location_searches',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('query', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('state_province', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_location_searches_created_at', 'location_searches', ['created_at'], unique=False)
    op.create_index(op.f('ix_location_searches_query'), 'location_searches', ['query'], unique=False)

    op.create_table(
        'analysis_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('location_id', sa.String(), nullable=False),
        sa.Column('hazard_type', sa.String(), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('analysis_version', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_records_hazard_type'), 'analysis_records', ['hazard_type'], unique=False)
    op.create_index(op.f('ix_analysis_records_severity'), 'analysis_records', ['severity'], unique=False)
    op.create_index(op.f('ix_analysis_records_generated_at'), 'analysis_records', ['generated_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_analysis_records_generated_at'), table_name='analysis_records')
    op.drop_index(op.f('ix_analysis_records_severity'), table_name='analysis_records')
    op.drop_index(op.f('ix_analysis_records_hazard_type'), table_name='analysis_records')
    op.drop_table('analysis_records')
    
    op.drop_index(op.f('ix_location_searches_query'), table_name='location_searches')
    op.drop_index('ix_location_searches_created_at', table_name='location_searches')
    op.drop_table('location_searches')
