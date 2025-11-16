"""API routes for fetching 10-K filings."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ..services.tenk_service import TenKService
from ..models.filings import AggregatedFilings, Filing
from ..dependencies import get_tenk_service

router = APIRouter(prefix="/filings", tags=["filings"])


@router.get("/10-k", response_model=AggregatedFilings)
async def get_aggregated_tenk_filings(
    max_companies: int | None = Query(
        None,
        ge=1,
        description=(
            "Limit the number of tickers scanned. Leave unset to iterate the entire SEC list. "
            "Use smaller values when testing locally to avoid hitting SEC rate limits."
        ),
    ),
    limit_per_company: int = Query(
        1,
        ge=1,
        le=10,
        description="Maximum number of recent 10-Ks returned per company.",
    ),
    tenk_service: TenKService = Depends(get_tenk_service),
) -> AggregatedFilings:
    """Return aggregated 10-K filings across companies."""
    return await tenk_service.fetch_all_filings(
        limit_per_company=limit_per_company,
        max_companies=max_companies,
    )


@router.get("/10-k/{ticker}", response_model=list[Filing])
async def get_company_tenk_filings(
    ticker: str,
    limit: int = Query(3, ge=1, le=10),
    tenk_service: TenKService = Depends(get_tenk_service),
) -> list[Filing]:
    filings = await tenk_service.fetch_company_filings(ticker=ticker, limit=limit)
    if not filings:
        raise HTTPException(status_code=404, detail=f"No 10-K filings found for ticker '{ticker}'.")
    return filings
