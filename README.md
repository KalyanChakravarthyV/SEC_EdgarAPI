# SEC EDGAR FastAPI Service

This project exposes a FastAPI service that aggregates 10-K filings for publicly traded companies using the official SEC EDGAR REST endpoints. The service respects SEC rate limits by throttling outbound calls and always sends a custom `User-Agent`.

## Getting Started

```bash
poetry install
poetry run uvicorn sec_edgar_api.app:app --reload
```

## Example Usage

- `GET /health` — service heartbeat.
- `GET /filings/10-k?max_companies=25&limit_per_company=2` — aggregate up to 25 companies' most recent 10-K filings.
- `GET /companies/AAPL/10-k?limit=3` — fetch Apple Inc.'s three latest 10-K reports.
- `GET /financials/AAPL` — return the latest Revenues, Operating Expenses, Assets, Liabilities, Equity, and other core metrics extracted from the EDGAR company facts API.
- `GET /financials/AAPL/income-statement` — surface Revenues, Operating Expenses, Income Before Tax, EPS, and related income statement metrics sourced from the latest 10-K.

Set `SEC_API_USER_AGENT` in your environment (or `.env`) before running the server to comply with SEC requirements.
