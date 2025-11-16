"""API routes for company financial metrics."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_financials_service
from ..models.financials import CompanyFinancialSnapshot, CompanyIncomeStatement
from ..services.financials_service import FinancialsService

router = APIRouter(prefix="/financials", tags=["financials"])


@router.get("/{ticker}", response_model=CompanyFinancialSnapshot)
async def get_company_financials(
    ticker: str,
    financials_service: FinancialsService = Depends(get_financials_service),
) -> CompanyFinancialSnapshot:
    """Return the latest financial metrics for the requested ticker."""
    snapshot = await financials_service.fetch_financial_snapshot(ticker=ticker)
    if snapshot is None:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found.")
    return snapshot


@router.get("/{ticker}/income-statement", response_model=CompanyIncomeStatement)
async def get_income_statement(
    ticker: str,
    financials_service: FinancialsService = Depends(get_financials_service),
) -> CompanyIncomeStatement:
    """Return key income-statement metrics sourced from the latest 10-K."""
    statement = await financials_service.fetch_income_statement(ticker=ticker)
    if statement is None:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found.")
    return statement
