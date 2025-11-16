"""Pydantic models describing derived financial metrics."""

from __future__ import annotations

from datetime import date

from typing import Union

from pydantic import BaseModel


class FinancialMetric(BaseModel):
    """Represents the most recent value for a single financial concept."""

    concept: str
    label: str
    value: float | None
    unit: str | None
    fiscal_year: int | None
    fiscal_period: str | None
    end_date: date | None
    filing_date: date | None
    accession_number: str | None


class CompanyFinancialSnapshot(BaseModel):
    """Collection of financial metrics for a company."""

    cik: str
    ticker: str
    company_name: str | None
    metrics: dict[str, "MetricValue"]


class CompanyIncomeStatement(BaseModel):
    """Income statement-focused metrics sourced from a 10-K filing."""

    cik: str
    ticker: str
    company_name: str | None
    filing_form: str
    metrics: dict[str, "MetricValue"]


class FinancialMetricSeries(BaseModel):
    """Collection of observations for a metric concept."""

    concept: str
    label: str
    entries: list[FinancialMetric]


MetricValue = Union[FinancialMetric, FinancialMetricSeries]
