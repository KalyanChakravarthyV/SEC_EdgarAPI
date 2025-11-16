# Repository Guidelines

This repository hosts the in-house SEC EDGAR ingestion API. Keep the layout predictable, automate everything you can, and document assumptions in-line so other agents can pick up your branch without context.

## Project Structure & Module Organization
- `src/sec_edgar_api/` holds runtime code. Keep request/response models in `models/`, EDGAR HTTP utilities in `clients/`, and per-feature orchestration under `services/`.
- `scripts/` is reserved for operational helpers (data refreshers, schema syncs); ship executable examples with docstrings plus `--help`.
- `tests/` mirrors the `src/` tree (`tests/clients/test_submission_client.py`, etc.). Keep fixtures in `tests/fixtures/`.
- Store sample filings or mock payloads in `data/samples/` and reference them via relative paths so tests remain deterministic.

## Build, Test, and Development Commands
- `poetry install` — install dependencies, creating the locked virtual environment expected by CI.
- `poetry run uvicorn sec_edgar_api.app:app --reload` — run the local API with hot reload to exercise endpoints quickly.
- `poetry run pytest` — execute the entire test suite; required before any push.
- `poetry run ruff check src tests` and `poetry run ruff format src tests` — lint + format; CI enforces both.
- `poetry run mypy src` — ensure typing remains sound around the EDGAR payload contracts.

## Coding Style & Naming Conventions
Target Python 3.11 with 4-space indentation. Prefer dataclasses or Pydantic models for data carriers and snake_case module names. End files with typing guards (`if __name__ == "__main__":`). Import ordering follows Ruff defaults (stdlib, third-party, local). Keep functions under 40 lines; break workflows into composable services. When adding new API routes, place FastAPI routers under `src/sec_edgar_api/routes/` and name files `filings.py`, `submissions.py`, etc.

## Testing Guidelines
Use pytest with `pytest.mark.asyncio` for async clients. Test filenames follow `test_<module>.py` and each test name states the scenario (`test_fetch_filings_handles_404`). Maintain ≥90% branch coverage; run `poetry run pytest --cov=sec_edgar_api --cov-report=term-missing` before submitting. Provide factories for EDGAR payload stubs in `tests/factories.py` to keep assertions readable.

## Commit & Pull Request Guidelines
Use Conventional Commits (`feat: add submission parser`, `fix: handle rate limit`). Each PR should link the relevant issue, describe schema or endpoint changes, and include before/after notes for API responses or CLI output. Add screenshots or sample JSON when modifying user-facing behavior. Request reviews only after CI is green and lint/test commands have been pasted into the PR checklist.

## Security & Configuration Tips
Never commit secrets; copy `.env.example` to `.env` locally and keep API keys in your shell keychain. Rotate temporary EDGAR session cookies every 12 hours. Limit outbound HTTP clients to `sec_edgar_api/clients/session.py` so instrumentation and retry policies stay centralized.
