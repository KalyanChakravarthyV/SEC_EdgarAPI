"""FastAPI application wiring."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .dependencies import close_http_client
from .routes import filings, financials


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup/shutdown events."""
    yield
    await close_http_client()


def create_app() -> FastAPI:
    """Application factory."""
    application = FastAPI(
        title="SEC EDGAR 10-K Aggregator",
        description="Aggregates 10-K filings for publicly traded companies via the SEC EDGAR API.",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(filings.router)
    application.include_router(financials.router)

    @application.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
