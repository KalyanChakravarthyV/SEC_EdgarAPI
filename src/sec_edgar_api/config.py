"""Application configuration and settings management."""

from functools import lru_cache

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration."""

    user_agent: str = Field(
        "SEC-EdgarAPI/0.1 (support@example.com)",
        description="User-Agent string sent to SEC endpoints.",
    )
    tickers_url: HttpUrl = Field(
        "https://www.sec.gov/files/company_tickers.json",
        description="Location of the master ticker list published by the SEC.",
    )
    submissions_base_url: HttpUrl = Field(
        "https://data.sec.gov/submissions/",
        description="Base URL for company submission JSON payloads.",
    )
    company_facts_base_url: HttpUrl = Field(
        "https://data.sec.gov/api/xbrl/companyfacts/",
        description="Base URL for the XBRL company facts API.",
    )
    archives_base_url: HttpUrl = Field(
        "https://www.sec.gov/Archives/edgar/data",
        description="Base URL for filing artifacts in EDGAR archives.",
    )
    request_timeout: float = Field(15.0, description="HTTP timeout for SEC requests.")
    max_concurrent_requests: int = Field(
        5,
        ge=1,
        le=10,
        description="Number of concurrent SEC API requests issued when aggregating filings.",
    )

    model_config = SettingsConfigDict(env_prefix="SEC_API_", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
