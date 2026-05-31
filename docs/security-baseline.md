# Security Baseline

## Aegis Earth MVP

Date: 2026-05-31

This document defines the minimum security rules for the Aegis Earth MVP repository and development workflow.

## Audit Summary

### Current Status

- `.gitignore` protects local environment files, secret files, Python cache files, Node dependencies, logs, OS files, IDE folders, and build outputs.
- `.env.example` is the only tracked environment file.
- No real `.env`, `.env.local`, `.env.development`, `credentials.json`, or `service-account.json` files were found locally during this audit.
- No tracked private key, certificate, or credential JSON files were found.
- Secret keyword scan found only expected references in configuration, docs, and ignore rules.
- Production npm dependency audit reported zero known vulnerabilities.

### Current Risks

- The repository is public, so every committed file must be treated as permanently visible.
- `scripts/push.sh` stages all files with `git add .`; developers must verify `git status` before using it.
- `DATABASE_URL` in `.env.example` uses demo local credentials only. Real database credentials must never be committed.
- `allow_credentials=True` is enabled in FastAPI CORS configuration. This is acceptable only with explicit trusted origins, never wildcard origins.
- Satellite provider credentials for Google Earth Engine, Sentinel access, and future cloud services must stay outside Git.

## Repository Security Rules

### Ignore Rules

The repository must ignore:

- `.env`
- `.env.*`
- Private keys: `*.pem`, `*.key`, `*.crt`
- Provider credential files: `credentials.json`, `service-account.json`
- Python caches: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- Virtual environments: `.venv/`, `venv/`
- Node dependencies: `node_modules/`
- Logs: `*.log`
- OS files: `.DS_Store`, `Thumbs.db`
- IDE folders: `.vscode/`, `.idea/`
- Build outputs: `dist/`, `build/`, `.vite/`, `*.tsbuildinfo`

`.env.example` must remain tracked and must contain only safe placeholder values.

## Environment Variables

### Allowed in `.env.example`

- Localhost URLs
- Empty provider placeholders
- Non-secret configuration defaults
- Clearly fake or local-only credentials

### Forbidden in Git

- Production `DATABASE_URL`
- API keys
- OAuth secrets
- JWT signing secrets
- Google Earth Engine service account files
- Cloud provider keys
- Private certificates
- User data exports
- Raw satellite provider tokens

## Secret Handling

Secrets must be stored in one of:

- Local `.env` files ignored by Git
- Deployment platform secret storage
- CI/CD secret storage
- Cloud secret manager

Secrets must never be copied into:

- Source files
- Markdown documentation
- Issue templates
- Commit messages
- Screenshots
- Logs
- Test fixtures

If a secret is committed, rotate it immediately and treat the Git history as exposed.

## Public Repository Rules

Before every push:

1. Run `git status`.
2. Review staged changes with `git diff --cached`.
3. Check for secrets with `rg` or equivalent.
4. Confirm no `.env`, key, certificate, or provider credential files are staged.
5. Confirm docs do not contain real access tokens, endpoints with credentials, or private infrastructure details.

Recommended scan:

```bash
rg -n --hidden --glob '!node_modules/**' --glob '!dist/**' --glob '!build/**' --glob '!.git/**' "(api[_-]?key|secret|token|password|private[_-]?key|service[_-]?account|credentials|BEGIN .*PRIVATE KEY)"
```

## Backend Security Baseline

- Use explicit CORS origins only.
- Never combine wildcard origins with credentialed CORS.
- Validate all API request payloads with Pydantic schemas.
- Keep provider integrations behind service boundaries.
- Do not expose stack traces in production responses.
- Do not log secrets, full database URLs, provider tokens, or raw credentials.
- Keep database migrations and access models reviewable.
- Use least-privilege database users in non-local environments.

## Frontend Security Baseline

- Only expose values prefixed with `VITE_` when they are safe for browsers.
- Treat all frontend environment values as public.
- Never place API keys or provider secrets in frontend code.
- Sanitize and validate user-provided search input before backend processing.
- Keep map tile and provider URLs free of embedded credentials.

## Data Security Baseline

The MVP must not store sensitive personal data unless explicitly approved.

Allowed MVP data:

- Location names
- Latitude and longitude
- Risk scores
- Confidence values
- Generated alert metadata
- Evidence layer metadata

Restricted data:

- Personal identifiers
- Private addresses tied to users
- Authentication tokens
- Provider credentials
- Raw private imagery exports

## Incident Response

If secret exposure is suspected:

1. Stop pushing new commits.
2. Identify the exposed value and affected services.
3. Rotate the credential immediately.
4. Remove the secret from the working tree.
5. Add or fix ignore rules.
6. Document the incident in `docs/development-log.md`.
7. Review whether Git history cleanup is required.

## Verification Performed

- Reviewed `.gitignore`.
- Confirmed `.env`, `.env.local`, `.env.development`, `credentials.json`, and `service-account.json` were absent locally and ignored.
- Confirmed only `.env.example` is tracked among environment-style files.
- Scanned repository text for common secret indicators.
- Reviewed public URL and credential-related code references.
- Ran production npm dependency audit.

