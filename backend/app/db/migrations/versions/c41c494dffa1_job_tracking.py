"""job_tracking

Revision ID: c41c494dffa1
Revises: b4f1b8a9c3d1
Create Date: 2026-06-22 10:05:33.314018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c41c494dffa1'
down_revision: Union[str, Sequence[str], None] = 'b4f1b8a9c3d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update analysis_jobs table
    op.add_column('analysis_jobs', sa.Column('correlation_id', sa.String(), nullable=True))
    op.add_column('analysis_jobs', sa.Column('hazard_type', sa.String(), nullable=True))
    op.add_column('analysis_jobs', sa.Column('failure_reason', sa.String(), nullable=True))
    op.add_column('analysis_jobs', sa.Column('execution_duration_ms', sa.Float(), nullable=True))
    
    op.create_index(op.f('ix_analysis_jobs_correlation_id'), 'analysis_jobs', ['correlation_id'], unique=False)
    op.create_index(op.f('ix_analysis_jobs_hazard_type'), 'analysis_jobs', ['hazard_type'], unique=False)

    # Note: SQLite doesn't support dropping columns easily, but we assume Postgres based on earlier errors.
    # The previous columns error_message and execution_time_ms were renamed.
    # To be safe and backward compatible with running services, we will just add the new columns
    # and not drop the old ones immediately, or we can drop them if we are sure.
    op.drop_column('analysis_jobs', 'error_message')
    op.drop_column('analysis_jobs', 'execution_time_ms')

    # Create job_attempts table
    op.create_table('job_attempts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('attempt_number', sa.Integer(), nullable=False),
        sa.Column('worker_id', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('logs', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['analysis_jobs.job_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_attempts_job_id'), 'job_attempts', ['job_id'], unique=False)
    op.create_index(op.f('ix_job_attempts_tenant_id'), 'job_attempts', ['tenant_id'], unique=False)

    # Create job_failures table
    op.create_table('job_failures',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('attempt_number', sa.Integer(), nullable=False),
        sa.Column('failure_reason', sa.String(), nullable=False),
        sa.Column('stack_trace', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['analysis_jobs.job_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_failures_job_id'), 'job_failures', ['job_id'], unique=False)
    op.create_index(op.f('ix_job_failures_tenant_id'), 'job_failures', ['tenant_id'], unique=False)

    # Create idempotency_records table
    op.create_table('idempotency_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('idempotency_key', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('response_payload', sa.JSON(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_idempotency_records_idempotency_key'), 'idempotency_records', ['idempotency_key'], unique=True)
    op.create_index(op.f('ix_idempotency_records_job_id'), 'idempotency_records', ['job_id'], unique=False)
    op.create_index(op.f('ix_idempotency_records_tenant_id'), 'idempotency_records', ['tenant_id'], unique=False)

    # Create deduplication_locks table
    op.create_table('deduplication_locks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('fingerprint', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deduplication_locks_fingerprint'), 'deduplication_locks', ['fingerprint'], unique=True)
    op.create_index(op.f('ix_deduplication_locks_job_id'), 'deduplication_locks', ['job_id'], unique=False)
    op.create_index(op.f('ix_deduplication_locks_tenant_id'), 'deduplication_locks', ['tenant_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_deduplication_locks_tenant_id'), table_name='deduplication_locks')
    op.drop_index(op.f('ix_deduplication_locks_job_id'), table_name='deduplication_locks')
    op.drop_index(op.f('ix_deduplication_locks_fingerprint'), table_name='deduplication_locks')
    op.drop_table('deduplication_locks')

    op.drop_index(op.f('ix_idempotency_records_tenant_id'), table_name='idempotency_records')
    op.drop_index(op.f('ix_idempotency_records_job_id'), table_name='idempotency_records')
    op.drop_index(op.f('ix_idempotency_records_idempotency_key'), table_name='idempotency_records')
    op.drop_table('idempotency_records')

    op.drop_index(op.f('ix_job_failures_tenant_id'), table_name='job_failures')
    op.drop_index(op.f('ix_job_failures_job_id'), table_name='job_failures')
    op.drop_table('job_failures')

    op.drop_index(op.f('ix_job_attempts_tenant_id'), table_name='job_attempts')
    op.drop_index(op.f('ix_job_attempts_job_id'), table_name='job_attempts')
    op.drop_table('job_attempts')

    op.add_column('analysis_jobs', sa.Column('execution_time_ms', sa.Float(), nullable=True))
    op.add_column('analysis_jobs', sa.Column('error_message', sa.String(), nullable=True))
    
    op.drop_index(op.f('ix_analysis_jobs_hazard_type'), table_name='analysis_jobs')
    op.drop_index(op.f('ix_analysis_jobs_correlation_id'), table_name='analysis_jobs')
    
    op.drop_column('analysis_jobs', 'execution_duration_ms')
    op.drop_column('analysis_jobs', 'failure_reason')
    op.drop_column('analysis_jobs', 'hazard_type')
    op.drop_column('analysis_jobs', 'correlation_id')
