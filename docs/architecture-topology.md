# Aegis Earth Architecture Topology

This document visualizes the infrastructure and deployment topography of the Aegis Earth platform.

## Infrastructure Flow

```mermaid
graph TD
    subgraph "External"
        Users((Users))
        Providers[Satellite Providers\nGEE, Sentinel]
    end

    subgraph "Cloud Load Balancing (Ingress)"
        GLB[Nginx Ingress Controller]
    end

    subgraph "Kubernetes Cluster (GKE)"
        subgraph "Frontend Namespace"
            FE[Frontend Deployment\nReact / Vite]
            FESvc[Frontend Service]
        end

        subgraph "Backend Namespace"
            BE[Backend Deployment\nFastAPI]
            BESvc[Backend Service]
            Workers[Background Workers\nAnyIO / APScheduler]
        end
    end

    subgraph "Managed Services (Cloud)"
        DB[(Cloud SQL\nPostgreSQL)]
        Cache[(MemoryStore\nRedis HA)]
    end

    %% Traffic Routing
    Users -->|HTTPS| GLB
    GLB -->|Path: /| FESvc
    GLB -->|Path: /api| BESvc
    
    FESvc --> FE
    BESvc --> BE

    %% Backend Dependencies
    BE -->|SQL/ORM| DB
    BE -->|PubSub / Queues| Cache
    Workers -->|SQL/ORM| DB
    Workers -->|Job Polling| Cache

    %% External Comm
    Workers -->|API Requests| Providers
    BE -->|Metadata Requests| Providers
```

## Scaling Dimensions
1. **Frontend**: Scales via HPA based on CPU (static asset delivery).
2. **Backend**: Scales via HPA based on CPU/HTTP connection load.
3. **Workers**: Scales horizontally consuming queue length metrics.
4. **Database**: Scaled vertically (Compute/RAM) and isolated from application clusters.
5. **Redis**: Scaled vertically, operating in High Availability mode.
