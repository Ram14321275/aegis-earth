# Aegis Earth 🌍🛡️

Observe. Analyze. Protect.

Aegis Earth is a next-generation disaster intelligence platform designed to monitor environmental changes using satellite imagery and geospatial intelligence. The platform analyzes Earth observation data to detect floods, wildfires, and other natural hazards, helping communities and decision-makers understand risks through interactive visualizations and actionable insights.

## Key Features

- Flood detection
- Wildfire detection
- Satellite image analysis
- City and coordinate search
- Risk assessment and alert generation
- Interactive map dashboard
- Heat map visualization
- Difference map analysis
- Explainable disaster intelligence
- High-performance caching architecture

## Sprint 1 Scope

- Repository setup
- React/Vite/TypeScript frontend initialization
- FastAPI backend initialization
- PostgreSQL configuration
- Environment configuration
- Documentation setup
- Dark mission-control theme foundation

## Project Layout

```text
frontend/ Reserved official frontend workspace
backend/ Reserved official backend workspace
apps/
  web/      React + Vite + Tailwind frontend
  api/      FastAPI backend
services/  Architecture ownership boundaries
docs/      Sprint, architecture, API, database, and Codex progress docs
infrastructure/ Deployment and infrastructure assets
scripts/ Development workflow scripts
.github/ GitHub workflows and repository automation
```

## Quick Start

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

Backend:

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Copy `.env.example` to `.env` before connecting PostgreSQL or provider credentials.

## Vision

Our mission is to make disaster intelligence accessible, understandable, and actionable by transforming satellite data into meaningful insights that help protect people, infrastructure, and the environment.

Observe. Analyze. Protect.
