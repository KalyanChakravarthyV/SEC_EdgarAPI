"""Pydantic models describing filings and related payloads."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, HttpUrl


class CompanySummary(BaseModel):
    """Minimal information about a publicly traded company."""

    cik: str
    ticker: str
    title: str


class Filing(BaseModel):
    """Representation of a single SEC filing."""

    cik: str
    ticker: str
    company_name: str
    form_type: str
    filing_date: Optional[date]
    report_period: Optional[date]
    accession_number: str
    primary_document_url: Optional[HttpUrl]


class AggregatedFilings(BaseModel):
    """Container returned by the aggregated filings endpoint."""

    companies_examined: int
    total_filings: int
    form_type: str
    filings: list[Filing]
