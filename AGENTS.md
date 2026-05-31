# Aegis Earth Agent Instructions

## Project

Aegis Earth is a disaster intelligence platform.

Tagline: Observe. Analyze. Protect.

Current phase: Sprint 1 - MVP Development.

## Role

Codex acts as Lead Software Engineer.

Responsibilities:

- Implement production-quality code.
- Preserve clean architecture boundaries.
- Keep documentation updated.
- Track progress in `docs/codex-progress.md`.
- Verify work before committing or pushing.

## Scope Rules

MVP includes:

- Location search
- Latitude/longitude search
- Flood detection
- Wildfire detection
- Satellite image analysis
- Risk assessment
- Alert generation
- Map view
- Heat map view
- Difference map view
- Explainability panel
- Confidence indicators

Do not implement future-scope features unless explicitly instructed.

Future-scope features include:

- Cyclones
- Landslides
- Drought prediction
- Drone integration
- Continuous streaming
- Mobile app
- Prediction engine

## Architecture

Keep concerns separated:

- `services/disaster-engine`
- `services/model-interface`
- `services/cache`
- `services/alert-engine`
- `services/visualization`
- `services/geospatial`

Future AI models must remain replaceable through `model-interface`.

## Workflow

Before finishing a work session:

- Update `docs/codex-progress.md`.
- Summarize completed work.
- List blockers.
- List next tasks.
- Run relevant verification commands.

## Git Rules

- Never create another repository.
- Never create another worktree.
- Never delete existing files unless explicitly instructed.
- Verify repository status before pushing.
- Use `main` as the official development branch.

