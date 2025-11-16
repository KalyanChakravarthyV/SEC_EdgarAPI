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
                                        "fy": 2013,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2014-02-01",
                                        "end": "2013-12-31",
                                        "val": 400,
                                        "accn": "0000000001-13-000001",
                                    }
                                ],
                                "USDm": [
                                    {
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "",
                                        "end": "2025-12-31",
                                        "val": 1500,
                                        "accn": "0000000001-25-000001",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "",
                                        "end": "2024-12-31",
                                        "val": 1200,
                                        "accn": "0000000001-24-000001",
                                    },
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
                                        "fy": 2021,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2022-02-01",
                                        "end": "2021-12-31",
                                        "val": 850,
                                        "accn": "0000000001-21-000001",
                                    },
                                ],
                            },
                        },
                        "RevenueFromContractWithCustomerExcludingAssessedTax": {
                            "label": "Revenue from contract with customer",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "",
                                        "end": "2025-12-31",
                                        "val": 1500,
                                        "accn": "0000000001-25-000101",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 1200,
                                        "accn": "0000000001-24-000101",
                                    },
                                    {
                                        "fy": 2023,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2024-02-01",
                                        "end": "2023-12-31",
                                        "val": 1000,
                                        "accn": "0000000001-23-000101",
                                    },
                                ]
                            },
                        },
                        "CostOfRevenue": {
                            "label": "Cost of Revenue",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 520,
                                        "accn": "0000000001-25-000007",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 480,
                                        "accn": "0000000001-24-000007",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 980,
                                        "accn": "0000000001-25-000008",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 720,
                                        "accn": "0000000001-24-000008",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 720,
                                        "accn": "0000000001-25-000002",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 700,
                                        "accn": "0000000001-24-000002",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-01-15",
                                        "end": "2025-12-31",
                                        "val": 5500,
                                        "accn": "0000000001-25-000003",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-01-15",
                                        "end": "2024-12-31",
                                        "val": 5300,
                                        "accn": "0000000001-24-000003",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-01-15",
                                        "end": "2025-12-31",
                                        "val": 2100,
                                        "accn": "0000000001-25-000004",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-01-15",
                                        "end": "2024-12-31",
                                        "val": 2050,
                                        "accn": "0000000001-24-000004",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 430,
                                        "accn": "0000000001-25-000009",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 410,
                                        "accn": "0000000001-24-000009",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "",
                                        "end": "2025-12-31",
                                        "val": 390,
                                        "accn": "0000000001-25-000010",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 360,
                                        "accn": "0000000001-24-000010",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 180,
                                        "accn": "0000000001-25-000005",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 165,
                                        "accn": "0000000001-24-000005",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 2.8,
                                        "accn": "0000000001-25-000011",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 2.6,
                                        "accn": "0000000001-24-000011",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 2.6,
                                        "accn": "0000000001-25-000012",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 2.5,
                                        "accn": "0000000001-24-000012",
                                    },
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
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 140,
                                        "accn": "0000000001-25-000006",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 130,
                                        "accn": "0000000001-24-000006",
                                    },
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


class FallbackRevenueStub:
    def __init__(self) -> None:
        self._summaries = [
            CompanySummary(cik="0000000002", ticker="REV", title="Revenue Co"),
        ]
        self._facts_payload = {
            "0000000002": {
                "entityName": "Revenue Co",
                "facts": {
                    "us-gaap": {
                        "SalesRevenueNet": {
                            "label": "Net Sales",
                            "units": {
                                "USD": [
                                    {
                                        "fy": 2025,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2026-02-01",
                                        "end": "2025-12-31",
                                        "val": 222,
                                        "accn": "0000000002-25-000001",
                                    },
                                    {
                                        "fy": 2024,
                                        "fp": "FY",
                                        "form": "10-K",
                                        "filed": "2025-02-01",
                                        "end": "2024-12-31",
                                        "val": 111,
                                        "accn": "0000000002-24-000001",
                                    },
                                ]
                            },
                        }
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
    revenues = snapshot.metrics["revenues"]
    assert len(revenues.entries) == 3
    assert [entry.value for entry in revenues.entries] == [1500.0, 1200.0, 1000.0]
    assert all(
        entry.concept == "RevenueFromContractWithCustomerExcludingAssessedTax"
        for entry in revenues.entries
    )
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
    revenues = statement.metrics["revenues"]
    assert len(revenues.entries) == 3
    assert [entry.value for entry in revenues.entries] == [1500.0, 1200.0, 1000.0]
    assert revenues.entries[0].concept == "RevenueFromContractWithCustomerExcludingAssessedTax"
    assert statement.metrics["income_before_tax"].value == 390.0
    assert statement.metrics["eps_diluted"].value == 2.6
    assert statement.metrics["cost_of_revenue"].label == "Cost of Revenue"


@pytest.mark.asyncio
async def test_fetch_income_statement_handles_unknown_ticker():
    service = FinancialsService(client=StubClient())
    statement = await service.fetch_income_statement("ZZZ")
    assert statement is None


@pytest.mark.asyncio
async def test_revenue_concept_falls_back_to_sales_revenue():
    service = FinancialsService(client=FallbackRevenueStub())
    snapshot = await service.fetch_financial_snapshot("REV")
    assert snapshot is not None
    revenues = snapshot.metrics["revenues"]
    assert [entry.value for entry in revenues.entries] == [222.0, 111.0]
    assert all(entry.concept == "SalesRevenueNet" for entry in revenues.entries)
