# Disaster Recovery & Reliability Architecture

This document outlines the operational resilience strategies for the Aegis Earth Production Infrastructure.

## 1. PostgreSQL Recovery Strategy

Cloud SQL (PostgreSQL) is the primary state store.
- **Backups**: Automated daily backups are enabled in Terraform (`db.tf`) starting at 02:00 UTC.
- **Point-in-Time Recovery (PITR)**: Enabled. Archiving Write-Ahead Logs (WAL) allows restoring the database to any specific timestamp within the retention window (default 7 days).
- **Failover**: Configured for Regional High Availability. In the event of an availability zone failure, Cloud SQL automatically fails over to the standby replica with zero data loss.

## 2. Redis Persistence Strategy

Redis handles high-speed caching, distributed locking, and job queueing.
- **Durability**: Configured with `save 60 1` (AOF/RDB mixed persistence). Data loss is bounded to a maximum of 60 seconds of unwritten cache states.
- **Failover**: Configured as `STANDARD_HA` in Terraform, which provisions a primary and a replica in different zones. Failovers are managed automatically by MemoryStore with minimal application disruption.
- **Job Recovery**: If Redis fails, background workers listening to the queue will reconnect upon recovery. Orphaned jobs are moved back to `PENDING` via the internal Scheduler Heartbeat mechanism.

## 3. Deployment Rollback Procedures

Deployment reliability is strictly managed via GitHub Actions and Helm.
- **Zero-Downtime**: Kubernetes `RollingUpdate` strategies are enforced. A new pod must report `Ready` via the `/api/v1/system/health` probe before the old pod is terminated.
- **Automatic Rollback**: If a Helm deployment fails or times out, the GitHub Actions pipeline will automatically trigger `helm rollback`.
- **Manual Rollback**: 
  ```bash
  helm history aegis-earth -n production
  helm rollback aegis-earth <REVISION_NUMBER> -n production
  ```

## 4. Websocket & Stream Recovery

Websocket connections (`/ws/intelligence`) are stateful.
- **Client Reconnection**: Frontend clients implement exponential backoff reconnection.
- **Server Termination**: When a backend pod is terminated (e.g., during scaling or deployment), the `SIGTERM` signal triggers a graceful disconnect for all active websockets. Clients will automatically reconnect to healthy, surviving pods.
- **Redis Pub/Sub**: Stream continuity is maintained by Redis. Dropped consumers will resume from their last acknowledged stream ID.

## 5. Regional Outage Assumptions

Currently, the infrastructure is bound to a single region (e.g., `us-central1`) with multi-zone high availability.
- A single zone failure will automatically trigger pod rescheduling and database failovers within seconds.
- A total regional failure (entire `us-central1` goes offline) will result in system downtime. Future checkpoints will introduce multi-region Global Load Balancing to mitigate this.
