from datetime import date

import pytest

from sec_edgar_api.config import Settings
from sec_edgar_api.models.filings import CompanySummary, Filing
from sec_edgar_api.services.tenk_service import TenKService


class StubClient:
    def __init__(self) -> None:
        self._summaries = [
            CompanySummary(cik="0000000001", ticker="AAA", title="AAA Corp"),
            CompanySummary(cik="0000000002", ticker="BBB", title="BBB Corp"),
        ]
        self._filings_by_cik = {
            "0000000001": [
                Filing(
                    cik="0000000001",
                    ticker="AAA",
                    company_name="AAA Corp",
                    form_type="10-K",
                    filing_date=date(2023, 1, 31),
                    report_period=date(2022, 12, 31),
                    accession_number="0000000001-23-000001",
                    primary_document_url=None,
                ),
                Filing(
                    cik="0000000001",
                    ticker="AAA",
                    company_name="AAA Corp",
                    form_type="8-K",
                    filing_date=date(2023, 2, 1),
                    report_period=None,
                    accession_number="0000000001-23-000002",
                    primary_document_url=None,
                ),
            ],
            "0000000002": [
                Filing(
                    cik="0000000002",
                    ticker="BBB",
                    company_name="BBB Corp",
                    form_type="10-K",
                    filing_date=date(2023, 3, 15),
                    report_period=date(2022, 12, 31),
                    accession_number="0000000002-23-000001",
                    primary_document_url=None,
                )
            ],
        }

    async def fetch_company_tickers(self) -> list[CompanySummary]:
        return self._summaries

    async def fetch_recent_filings(self, cik: str) -> list[Filing]:
        return self._filings_by_cik[cik]


@pytest.mark.asyncio
async def test_fetch_company_filings_filters_by_ticker():
    service = TenKService(client=StubClient(), settings=Settings())
    filings = await service.fetch_company_filings("AAA", limit=5)
    assert len(filings) == 1
    assert filings[0].form_type == "10-K"


@pytest.mark.asyncio
async def test_fetch_all_filings_limits_per_company():
    service = TenKService(client=StubClient(), settings=Settings(max_concurrent_requests=2))
    aggregated = await service.fetch_all_filings(limit_per_company=1, max_companies=1)
    assert aggregated.companies_examined == 1
    assert aggregated.total_filings == 1
    assert aggregated.filings[0].ticker == "AAA"
