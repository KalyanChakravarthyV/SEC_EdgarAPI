"""Service responsible for assembling financial metrics from company facts."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Mapping

from ..clients.sec_client import SECEdgarClient
from ..models.financials import (
    CompanyFinancialSnapshot,
    CompanyIncomeStatement,
    FinancialMetric,
)
from ..models.filings import CompanySummary


class FinancialsService:
    """Provides derived financial information for a given company."""

    FINANCIAL_CONCEPTS: dict[str, str] = {
        "revenues": "Revenues",
        "operating_expenses": "OperatingExpenses",
        "assets": "Assets",
        "liabilities": "Liabilities",
        "equity": "StockholdersEquity",
        "net_income": "NetIncomeLoss",
        "cash_from_operations": "NetCashProvidedByUsedInOperatingActivities",
    }
    INCOME_STATEMENT_CONCEPTS: dict[str, str] = {
        "revenues": "Revenues",
        "cost_of_revenue": "CostOfRevenue",
        "gross_profit": "GrossProfit",
        "operating_expenses": "OperatingExpenses",
        "operating_income": "OperatingIncomeLoss",
        "income_before_tax": (
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItems"
        ),
        "net_income": "NetIncomeLoss",
        "eps_basic": "EarningsPerShareBasic",
        "eps_diluted": "EarningsPerShareDiluted",
    }
    _PREFERRED_UNITS = ("USD", "USDm", "USDmm", "USDMillions")

    def __init__(self, client: SECEdgarClient) -> None:
        self._client = client

    async def fetch_financial_snapshot(self, ticker: str) -> CompanyFinancialSnapshot | None:
        """Return the latest financial metrics for the requested ticker."""
        summary = await self._resolve_company(ticker)
        if summary is None:
            return None
        facts_payload = await self._client.fetch_company_facts(summary.cik)
        metrics = self._extract_metrics(facts_payload, concepts=self.FINANCIAL_CONCEPTS)
        company_name = facts_payload.get("entityName") or summary.title

        return CompanyFinancialSnapshot(
            cik=summary.cik,
            ticker=summary.ticker,
            company_name=company_name,
            metrics=metrics,
        )

    async def fetch_income_statement(self, ticker: str) -> CompanyIncomeStatement | None:
        """Return the latest income statement metrics constrained to 10-K filings."""
        summary = await self._resolve_company(ticker)
        if summary is None:
            return None
        facts_payload = await self._client.fetch_company_facts(summary.cik)
        metrics = self._extract_metrics(
            facts_payload,
            concepts=self.INCOME_STATEMENT_CONCEPTS,
            form_filter="10-K",
        )
        company_name = facts_payload.get("entityName") or summary.title
        return CompanyIncomeStatement(
            cik=summary.cik,
            ticker=summary.ticker,
            company_name=company_name,
            filing_form="10-K",
            metrics=metrics,
        )

    async def _resolve_company(self, ticker: str) -> CompanySummary | None:
        summaries = await self._client.fetch_company_tickers()
        ticker_upper = ticker.upper()
        return next((summary for summary in summaries if summary.ticker == ticker_upper), None)

    def _extract_metrics(
        self,
        payload: Mapping[str, Any],
        *,
        concepts: Mapping[str, str],
        form_filter: str | None = None,
    ) -> dict[str, FinancialMetric]:
        results: dict[str, FinancialMetric] = {}
        us_gaap = payload.get("facts", {}).get("us-gaap", {})
        for alias, concept in concepts.items():
            fact_payload = us_gaap.get(concept)
            results[alias] = self._build_metric(
                concept=concept,
                payload=fact_payload,
                form_filter=form_filter,
            )
        return results

    def _build_metric(
        self,
        *,
        concept: str,
        payload: Mapping[str, Any] | None,
        form_filter: str | None = None,
    ) -> FinancialMetric:
        if not payload:
            return FinancialMetric(
                concept=concept,
                label=concept,
                value=None,
                unit=None,
                fiscal_year=None,
                fiscal_period=None,
                end_date=None,
                filing_date=None,
                accession_number=None,
            )

        units: Mapping[str, list[Mapping[str, Any]]] = payload.get("units") or {}
        selected_unit, entry = self._select_entry(units, form_filter=form_filter)
        if entry is None:
            return FinancialMetric(
                concept=concept,
                label=payload.get("label") or concept,
                value=None,
                unit=None,
                fiscal_year=None,
                fiscal_period=None,
                end_date=None,
                filing_date=None,
                accession_number=None,
            )

        numeric_value = entry.get("val")
        value = float(numeric_value) if isinstance(numeric_value, (int, float)) else None
        return FinancialMetric(
            concept=concept,
            label=payload.get("label") or concept,
            value=value,
            unit=selected_unit,
            fiscal_year=entry.get("fy"),
            fiscal_period=entry.get("fp"),
            end_date=self._parse_date(entry.get("end")),
            filing_date=self._parse_date(entry.get("filed")),
            accession_number=entry.get("accn"),
        )

    def _select_entry(
        self,
        units: Mapping[str, list[Mapping[str, Any]]],
        *,
        form_filter: str | None = None,
    ) -> tuple[str | None, Mapping[str, Any] | None]:
        if not units:
            return None, None

        selected_unit: str | None = None
        entries: list[Mapping[str, Any]] | None = None
        for unit in self._PREFERRED_UNITS:
            unit_entries = units.get(unit)
            if unit_entries:
                selected_unit = unit
                entries = unit_entries
                break

        if not entries:
            for unit, unit_entries in units.items():
                if unit_entries:
                    selected_unit = unit
                    entries = unit_entries
                    break

        if not entries:
            return None, None

        filtered_entries = self._filter_by_form(entries, form_filter=form_filter)
        entry = max(filtered_entries, key=self._entry_sort_key)
        return selected_unit, entry

    def _filter_by_form(
        self,
        entries: list[Mapping[str, Any]],
        *,
        form_filter: str | None,
    ) -> list[Mapping[str, Any]]:
        if not form_filter:
            return entries
        matching = [
            entry
            for entry in entries
            if isinstance(entry.get("form"), str) and entry["form"].upper().startswith(form_filter.upper())
        ]
        return matching or entries

    def _entry_sort_key(self, entry: Mapping[str, Any]) -> tuple[date, date]:
        filed = self._parse_date(entry.get("filed")) or date.min
        period_end = self._parse_date(entry.get("end")) or date.min
        return filed, period_end

    @staticmethod
    def _parse_date(value: str | None) -> date | None:
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
