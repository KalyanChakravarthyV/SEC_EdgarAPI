"""FastAPI dependency wiring."""

from __future__ import annotations

import httpx
from fastapi import Depends

from .clients.sec_client import SECEdgarClient
from .config import Settings, get_settings
from .services.financials_service import FinancialsService
from .services.tenk_service import TenKService

_http_client: httpx.AsyncClient | None = None
_tenk_service: TenKService | None = None
_financials_service: FinancialsService | None = None


async def get_http_client(settings: Settings = Depends(get_settings)) -> httpx.AsyncClient:
    """Provide a shared AsyncClient instance."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            headers={
                "User-Agent": settings.user_agent,
                "Accept-Encoding": "gzip, deflate",
            },
            timeout=settings.request_timeout,
        )
    return _http_client


async def get_sec_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
    settings: Settings = Depends(get_settings),
) -> SECEdgarClient:
    return SECEdgarClient(http_client=http_client, settings=settings)


async def get_tenk_service(
    settings: Settings = Depends(get_settings),
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> TenKService:
    global _tenk_service
    if _tenk_service is None:
        client = SECEdgarClient(http_client=http_client, settings=settings)
        _tenk_service = TenKService(client=client, settings=settings)
    return _tenk_service


async def get_financials_service(
    settings: Settings = Depends(get_settings),
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> FinancialsService:
    global _financials_service
    if _financials_service is None:
        client = SECEdgarClient(http_client=http_client, settings=settings)
        _financials_service = FinancialsService(client=client)
    return _financials_service


async def close_http_client() -> None:
    """Close the shared HTTP client."""
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None
        global _tenk_service, _financials_service
        _tenk_service = None
        _financials_service = None
