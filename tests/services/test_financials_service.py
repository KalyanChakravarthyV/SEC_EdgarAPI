import pytest

from sec_edgar_api.models.filings import CompanySummary
from sec_edgar_api.services.financials_service import FinancialsService


class StubClient:
    def __init__(self) -> None:
        self._summaries = [
            CompanySummary(cik="0000000001", ticker="AAA", title="AAA Corp"),
        ]
        self._facts_payload = {
            "0000000001": {
                "entityName": "AAA Corporation",
                "facts": {
                    "us-gaap": {
                        "Revenues": {
                            "label": "Revenue",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 1000,
                                        "accn": "0000000001-23-000001",
                                    },
                                    {
                                        "fy": 2022,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2023-02-01",
                                        "end": "2022-12-31",
                                        "val": 900,
                                        "accn": "0000000001-22-000001",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "Q1",
                                        "form": "10-Q",
                                        "filed": "2024-05-01",
                                        "end": "2024-03-31",
                                        "val": 1200,
                                        "accn": "0000000001-24-000001",
                                    },
                                ]
                            },
                        },
                        "CostOfRevenue": {
                            "label": "Cost of Revenue",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 400,
                                        "accn": "0000000001-23-000007",
                                    }
                                ]
                            },
                        },
                        "GrossProfit": {
                            "label": "Gross Profit",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 600,
                                        "accn": "0000000001-23-000008",
                                    }
                                ]
                            },
                        },
                        "OperatingExpenses": {
                            "label": "Operating Expenses",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 700,
                                        "accn": "0000000001-23-000002",
                                    }
                                ]
                            },
                        },
                        "Assets": {
                            "label": "Assets",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-01-15",
                                        "end": "2023-12-31",
                                        "val": 5000,
                                        "accn": "0000000001-23-000003",
                                    }
                                ]
                            },
                        },
                        "Liabilities": {
                            "label": "Liabilities",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-01-15",
                                        "end": "2023-12-31",
                                        "val": 2000,
                                        "accn": "0000000001-23-000004",
                                    }
                                ]
                            },
                        },
                        "OperatingIncomeLoss": {
                            "label": "Operating Income",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 300,
                                        "accn": "0000000001-23-000009",
                                    }
                                ]
                            },
                        },
                        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItems": {
                            "label": "Income Before Tax",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 280,
                                        "accn": "0000000001-23-000010",
                                    }
                                ]
                            },
                        },
                        "NetIncomeLoss": {
                            "label": "Net Income",
                            "units": {
                                "USDm": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 150,
                                        "accn": "0000000001-23-000005",
                                    }
                                ]
                            },
                        },
                        "EarningsPerShareBasic": {
                            "label": "EPS Basic",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 2.5,
                                        "accn": "0000000001-23-000011",
                                    }
                                ]
                            },
                        },
                        "EarningsPerShareDiluted": {
                            "label": "EPS Diluted",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 2.4,
                                        "accn": "0000000001-23-000012",
                                    }
                                ]
                            },
                        },
                        "NetCashProvidedByUsedInOperatingActivities": {
                            "label": "Cash From Operations",
                            "units": {
                                "USDm": [
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 120,
                                        "accn": "0000000001-23-000006",
                                    }
                                ]
                            },
                        },
                    }
                },
            }
        }

    async def fetch_company_tickers(self):
        return self._summaries

    async def fetch_company_facts(self, cik: str):
        return self._facts_payload[cik]


@pytest.mark.asyncio
async def test_fetch_financial_snapshot_returns_metrics():
    service = FinancialsService(client=StubClient())
    snapshot = await service.fetch_financial_snapshot("AAA")

    assert snapshot is not None
    assert snapshot.cik == "0000000001"
    assert snapshot.company_name == "AAA Corporation"
    assert snapshot.metrics["revenues"].value == 1200.0
    assert snapshot.metrics["net_income"].unit == "USDm"
    assert snapshot.metrics["equity"].value is None


@pytest.mark.asyncio
async def test_fetch_financial_snapshot_handles_unknown_ticker():
    service = FinancialsService(client=StubClient())
    snapshot = await service.fetch_financial_snapshot("ZZZ")
    assert snapshot is None


@pytest.mark.asyncio
async def test_fetch_income_statement_limits_to_tenk_entries():
    service = FinancialsService(client=StubClient())
    statement = await service.fetch_income_statement("AAA")

    assert statement is not None
    assert statement.filing_form == "10-K"
    assert statement.metrics["revenues"].value == 1000.0
    assert statement.metrics["income_before_tax"].value == 280.0
    assert statement.metrics["eps_diluted"].value == 2.4
    assert statement.metrics["cost_of_revenue"].label == "Cost of Revenue"


@pytest.mark.asyncio
async def test_fetch_income_statement_handles_unknown_ticker():
    service = FinancialsService(client=StubClient())
    statement = await service.fetch_income_statement("ZZZ")
    assert statement is None
