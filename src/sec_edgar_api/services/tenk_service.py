"""Service responsible for orchestrating large-scale 10-K retrieval."""

from __future__ import annotations

import asyncio
from datetime import date
from typing import Iterable

from ..clients.sec_client import SECEdgarClient
from ..config import Settings
from ..models.filings import AggregatedFilings, CompanySummary, Filing


class TenKService:
    """Coordinates fetching 10-K filings across all publicly traded companies."""

    def __init__(self, client: SECEdgarClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings
        self._semaphore = asyncio.Semaphore(settings.max_concurrent_requests)

    async def fetch_company_filings(self, ticker: str, limit: int = 5) -> list[Filing]:
        """Fetch the latest 10-K filings for a single ticker."""
        summaries = await self._client.fetch_company_tickers()
        summary = next((item for item in summaries if item.ticker == ticker.upper()), None)
        if not summary:
            return []
        filings = await self._client.fetch_recent_filings(summary.cik)
        filtered = [filing for filing in filings if filing.form_type.startswith("10-K")]
        return filtered[:limit]

    async def fetch_all_filings(
        self, *, limit_per_company: int = 1, max_companies: int | None = None
    ) -> AggregatedFilings:
        """Fetch 10-K filings for the desired span of companies."""
        companies = await self._client.fetch_company_tickers()
        if max_companies is not None:
            companies = companies[:max_companies]

        filings = await self._gather_filings(companies, limit_per_company)
        flattened = [filing for company_filings in filings for filing in company_filings]
        flattened.sort(key=lambda filing: filing.filing_date or date.min, reverse=True)
        return AggregatedFilings(
            companies_examined=len(companies),
            total_filings=len(flattened),
            form_type="10-K",
            filings=flattened,
        )

    async def _gather_filings(
        self, companies: Iterable[CompanySummary], limit_per_company: int
    ) -> list[list[Filing]]:
        async def fetch_company(summary: CompanySummary) -> list[Filing]:
            async with self._semaphore:
                filings = await self._client.fetch_recent_filings(summary.cik)
            tenk_filings = [filing for filing in filings if filing.form_type.startswith("10-K")]
            return tenk_filings[:limit_per_company]

        tasks = [asyncio.create_task(fetch_company(summary)) for summary in companies]
        return await asyncio.gather(*tasks)
