# Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+
- PostgreSQL 15+

## Environment Setup
Ensure the `.env` file is fully configured inside the root directory. Required parameters include `DATABASE_URL`, `REDIS_URL` (if configured), and `CORS_ORIGINS`.

## Local Development
1. **Database Initialization**: 
   Ensure PostgreSQL is running and the user `postgres` has access to the database target.
2. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Production Deployment (Containerized)
The production system expects the frontend to be statically built and served, while the FastAPI backend runs behind a Uvicorn/Gunicorn worker pool.

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```
2. Build the backend container:
   ```bash
   cd backend
   docker build -t aegis-backend .
   ```
3. Start the cluster using Docker Compose:
   ```bash
   docker-compose up -d
   ```
