"""Async client for interacting with the SEC EDGAR API."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

import httpx

from ..config import Settings
from ..models.filings import CompanySummary, Filing


class SECEdgarClient:
    """HTTP client that wraps SEC endpoints."""

    def __init__(self, http_client: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http_client
        self._settings = settings

    async def fetch_company_tickers(self) -> list[CompanySummary]:
        """Download the SEC master ticker list."""
        response = await self._http.get(str(self._settings.tickers_url))
        response.raise_for_status()
        payload: Mapping[str, Any] = response.json()
        summaries: list[CompanySummary] = []
        for item in payload.values():
            cik = str(item["cik_str"]).zfill(10)
            summaries.append(
                CompanySummary(
                    cik=cik,
                    ticker=item["ticker"],
                    title=item["title"],
                )
            )
        # The SEC file ships as numeric keys, already ordered by CIK.
        return summaries

    async def fetch_recent_filings(self, cik: str) -> list[Filing]:
        """Retrieve the recent filings for a single company."""
        submissions_url = f"{self._settings.submissions_base_url}CIK{cik}.json"
        response = await self._http.get(submissions_url)
        response.raise_for_status()
        payload = response.json()
        return self._parse_recent_filings(payload)

    async def fetch_company_facts(self, cik: str) -> Mapping[str, Any]:
        """Retrieve the company facts payload for a single company."""
        facts_url = f"{self._settings.company_facts_base_url}CIK{cik}.json"
        response = await self._http.get(facts_url)
        response.raise_for_status()
        return response.json()

    def _parse_recent_filings(self, payload: Mapping[str, Any]) -> list[Filing]:
        filings: list[Filing] = []
        recent = payload.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        accession_numbers = recent.get("accessionNumber", [])
        filing_dates = recent.get("filingDate", [])
        report_periods = recent.get("reportDate", [])
        primary_docs = recent.get("primaryDocument", [])
        company_name = payload.get("name")
        ticker = (payload.get("tickers") or [""])[0]
        cik = str(payload.get("cik", "")).zfill(10)

        record_count = min(
            len(forms),
            len(accession_numbers),
            len(filing_dates),
        )
        for idx in range(record_count):
            form_type = forms[idx]
            filings.append(
                Filing(
                    cik=cik,
                    ticker=ticker,
                    company_name=company_name,
                    form_type=form_type,
                    filing_date=self._safe_parse_date(filing_dates, idx),
                    report_period=self._safe_parse_date(report_periods, idx),
                    accession_number=accession_numbers[idx],
                    primary_document_url=self._build_primary_document_url(
                        cik=cik,
                        accession=accession_numbers[idx],
                        document=primary_docs[idx] if idx < len(primary_docs) else None,
                    ),
                )
            )
        return filings

    def _build_primary_document_url(
        self, cik: str, accession: str, document: str | None
    ) -> str | None:
        if not document:
            return None
        sanitized_cik = cik.lstrip("0")
        accession_fragment = accession.replace("-", "")
        return (
            f"{self._settings.archives_base_url}/{sanitized_cik}/{accession_fragment}/{document}"
        )

    @staticmethod
    def _safe_parse_date(values: list[str], index: int) -> date | None:
        if index >= len(values) or not values[index]:
            return None
        return datetime.strptime(values[index], "%Y-%m-%d").date()
