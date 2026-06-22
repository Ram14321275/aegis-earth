"""Enterprise Security

Revision ID: b4f1b8a9c3d1
Revises: e554df618316
Create Date: 2026-06-22 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4f1b8a9c3d1'
down_revision: Union[str, Sequence[str], None] = 'e554df618316'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create tenants table
    op.create_table(
        'tenants',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('tier', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_name'), 'tenants', ['name'], unique=False)

    # 2. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_tenant_id'), 'users', ['tenant_id'], unique=False)

    # 3. Create api_keys table
    op.create_table(
        'api_keys',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('key_hash', sa.String(), nullable=False),
        sa.Column('prefix', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('scopes', sa.JSON(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('revoked', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_keys_key_hash'), 'api_keys', ['key_hash'], unique=True)
    op.create_index(op.f('ix_api_keys_prefix'), 'api_keys', ['prefix'], unique=False)
    op.create_index(op.f('ix_api_keys_tenant_id'), 'api_keys', ['tenant_id'], unique=False)

    # 4. Data Migration: Insert System Tenant
    system_tenant_id = '00000000-0000-0000-0000-000000000000'
    op.execute(
        f"INSERT INTO tenants (id, created_at, updated_at, name, tier, is_active) "
        f"VALUES ('{system_tenant_id}', now(), now(), 'System Default', 'system', true)"
    )

    # 5. Add tenant_id to existing tables
    # Since we can't be 100% sure which tables exist at this migration step in this user's local DB, 
    # we will use inspector to conditionally add to existing tables that are mapped.
    # In a real environment, we know exactly what tables exist up to `e554df618316`.
    # Based on `a3eba8da7ce0_initial_tables.py`, only `location_searches` and `analysis_records` exist.
    # `locations` might also exist or be renamed.
    # We will just add columns to tables we know exist.
    
    tables_to_update = ['location_searches', 'analysis_records', 'locations', 'analyses', 'alerts', 'risk_assessments', 'analysis_jobs', 'audit_logs']
    
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    for table in tables_to_update:
        if table in existing_tables:
            # Add column as nullable
            op.add_column(table, sa.Column('tenant_id', sa.String(), nullable=True))
            # Update existing records to use system_tenant_id
            op.execute(f"UPDATE {table} SET tenant_id = '{system_tenant_id}' WHERE tenant_id IS NULL")
            # Alter column to be non-nullable
            op.alter_column(table, 'tenant_id', nullable=False)
            op.create_index(op.f(f'ix_{table}_tenant_id'), table, ['tenant_id'], unique=False)

def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    tables_to_update = ['location_searches', 'analysis_records', 'locations', 'analyses', 'alerts', 'risk_assessments', 'analysis_jobs', 'audit_logs']
    
    for table in tables_to_update:
        if table in existing_tables:
            columns = [c['name'] for c in inspector.get_columns(table)]
            if 'tenant_id' in columns:
                op.drop_index(op.f(f'ix_{table}_tenant_id'), table_name=table)
                op.drop_column(table, 'tenant_id')

    op.drop_index(op.f('ix_api_keys_tenant_id'), table_name='api_keys')
    op.drop_index(op.f('ix_api_keys_prefix'), table_name='api_keys')
    op.drop_index(op.f('ix_api_keys_key_hash'), table_name='api_keys')
    op.drop_table('api_keys')
    
    op.drop_index(op.f('ix_users_tenant_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    op.drop_index(op.f('ix_tenants_name'), table_name='tenants')
    op.drop_table('tenants')
