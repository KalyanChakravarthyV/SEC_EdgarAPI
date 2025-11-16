"""Service responsible for assembling financial metrics from company facts."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Iterable, Mapping, Sequence

from ..clients.sec_client import SECEdgarClient
from ..models.financials import (
    CompanyFinancialSnapshot,
    CompanyIncomeStatement,
    FinancialMetric,
    FinancialMetricSeries,
)
from ..models.filings import CompanySummary


class FinancialsService:
    """Provides derived financial information for a given company."""

    FINANCIAL_CONCEPTS: dict[str, Sequence[str]] = {
        "revenues": (
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
            "SalesRevenueNet",
            "SalesRevenueGoodsNet",
            "NetSales",
            "TotalRevenue",
            "OperatingRevenue",
            "Revenues",
        ),
        "operating_expenses": "OperatingExpenses",
        "assets": "Assets",
        "liabilities": "Liabilities",
        "equity": "StockholdersEquity",
        "net_income": "NetIncomeLoss",
        "cash_from_operations": "NetCashProvidedByUsedInOperatingActivities",
    }
    INCOME_STATEMENT_CONCEPTS: dict[str, Sequence[str]] = {
        "revenues": (
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
            "SalesRevenueNet",
            "SalesRevenueGoodsNet",
            "NetSales",
            "TotalRevenue",
            "OperatingRevenue",
            "Revenues",
        ),
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
        metrics = self._extract_metrics(
            facts_payload,
            concepts=self.FINANCIAL_CONCEPTS,
            history_lengths={"revenues": 3},
            series_form_filters={"revenues": "10-K"},
        )
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
            history_lengths={"revenues": 3},
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
        concepts: Mapping[str, Sequence[str] | str],
        form_filter: str | None = None,
        history_lengths: Mapping[str, int] | None = None,
        series_form_filters: Mapping[str, str | None] | None = None,
    ) -> dict[str, FinancialMetric | FinancialMetricSeries]:
        results: dict[str, FinancialMetric | FinancialMetricSeries] = {}
        series_form_filters = series_form_filters or {}
        us_gaap = payload.get("facts", {}).get("us-gaap", {})
        for alias, concept in concepts.items():
            selected_concept, fact_payload = self._resolve_concept_payload(us_gaap, concept)
            history_length = (history_lengths or {}).get(alias)
            if history_length and history_length > 1:
                alias_form_filter = series_form_filters.get(alias, form_filter)
                results[alias] = self._build_metric_series(
                    concept=selected_concept or self._first_concept_name(concept),
                    payload=fact_payload,
                    form_filter=alias_form_filter,
                    history_length=history_length,
                )
            else:
                alias_form_filter = series_form_filters.get(alias, form_filter)
                results[alias] = self._build_metric(
                    concept=selected_concept or self._first_concept_name(concept),
                    payload=fact_payload,
                    form_filter=alias_form_filter,
                )
        return results

    def _resolve_concept_payload(
        self,
        us_gaap: Mapping[str, Any],
        concept: Sequence[str] | str,
    ) -> tuple[str | None, Mapping[str, Any] | None]:
        concept_names: Iterable[str]
        if isinstance(concept, str):
            concept_names = (concept,)
        else:
            concept_names = concept

        for name in concept_names:
            payload = us_gaap.get(name)
            if payload:
                return name, payload
        return None, None

    @staticmethod
    def _first_concept_name(concept: Sequence[str] | str) -> str:
        if isinstance(concept, str):
            return concept
        return next(iter(concept), "")

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

        label = payload.get("label") or concept
        units: Mapping[str, list[Mapping[str, Any]]] = payload.get("units") or {}
        selected_unit, entries = self._select_entries(units, form_filter=form_filter)
        if not entries:
            return FinancialMetric(
                concept=concept,
                label=label,
                value=None,
                unit=None,
                fiscal_year=None,
                fiscal_period=None,
                end_date=None,
                filing_date=None,
                accession_number=None,
            )

        entry = max(entries, key=self._entry_sort_key)
        return self._build_metric_from_entry(
            concept=concept,
            label=label,
            entry=entry,
            unit=selected_unit,
        )

    def _build_metric_series(
        self,
        *,
        concept: str,
        payload: Mapping[str, Any] | None,
        form_filter: str | None,
        history_length: int,
    ) -> FinancialMetricSeries:
        if not payload:
            return FinancialMetricSeries(concept=concept, label=concept, entries=[])

        label = payload.get("label") or concept
        units: Mapping[str, list[Mapping[str, Any]]] = payload.get("units") or {}
        selected_unit, entries = self._select_entries(units, form_filter=form_filter)
        if not entries:
            return FinancialMetricSeries(concept=concept, label=label, entries=[])

        sorted_entries = sorted(entries, key=self._entry_sort_key, reverse=True)
        limited = sorted_entries[:history_length]
        observations = [
            self._build_metric_from_entry(
                concept=concept,
                label=label,
                entry=entry,
                unit=selected_unit,
            )
            for entry in limited
        ]
        return FinancialMetricSeries(concept=concept, label=label, entries=observations)

    def _build_metric_from_entry(
        self,
        *,
        concept: str,
        label: str,
        entry: Mapping[str, Any],
        unit: str | None,
    ) -> FinancialMetric:
        numeric_value = entry.get("val")
        value = float(numeric_value) if isinstance(numeric_value, (int, float)) else None
        return FinancialMetric(
            concept=concept,
            label=label,
            value=value,
            unit=unit,
            fiscal_year=entry.get("fy"),
            fiscal_period=entry.get("fp"),
            end_date=self._parse_date(entry.get("end")),
            filing_date=self._parse_date(entry.get("filed")),
            accession_number=entry.get("accn"),
        )

    def _select_entries(
        self,
        units: Mapping[str, list[Mapping[str, Any]]],
        *,
        form_filter: str | None = None,
    ) -> tuple[str | None, list[Mapping[str, Any]]]:
        if not units:
            return None, []

        candidates: list[tuple[str, list[Mapping[str, Any]], Mapping[str, Any]]] = []
        for unit, raw_entries in units.items():
            if not raw_entries:
                continue
            filtered_entries = self._filter_by_form(raw_entries, form_filter=form_filter)
            if not filtered_entries:
                continue
            freshest_entry = max(filtered_entries, key=self._entry_sort_key)
            candidates.append((unit, filtered_entries, freshest_entry))

        if not candidates:
            return None, []

        def unit_priority(unit: str) -> int:
            if unit in self._PREFERRED_UNITS:
                # Higher priority for earlier entries in the preference list.
                return len(self._PREFERRED_UNITS) - self._PREFERRED_UNITS.index(unit)
            return 0

        selected_unit, selected_entries, _ = max(
            candidates,
            key=lambda item: (self._entry_sort_key(item[2]), unit_priority(item[0])),
        )
        return selected_unit, selected_entries

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

    def _entry_sort_key(self, entry: Mapping[str, Any]) -> tuple[int, date, date]:
        fiscal_year_raw = entry.get("fy")
        if isinstance(fiscal_year_raw, str):
            try:
                fiscal_year = int(fiscal_year_raw)
            except ValueError:
                fiscal_year = 0
        elif isinstance(fiscal_year_raw, int):
            fiscal_year = fiscal_year_raw
        else:
            fiscal_year = 0
        filed = self._parse_date(entry.get("filed")) or date.min
        period_end = self._parse_date(entry.get("end")) or date.min
        return fiscal_year, filed, period_end

    @staticmethod
    def _parse_date(value: str | None) -> date | None:
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
