"""API contract and copied-value tests for the read-only LANTERN app."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
APP_DATA = ROOT / "app" / "data"
sys.path.insert(0, str(ROOT))

pytest.importorskip("fastapi", reason="Install FastAPI to run the app tests")
if not (APP_DATA / "coverage.json").exists():
    pytest.skip(
        "Run `python scripts/export_app_data.py` before the app tests",
        allow_module_level=True,
    )

from fastapi.testclient import TestClient  # noqa: E402

from app.api.main import app  # noqa: E402


VALID_TRIAGE = {
    "comparative_leakage",
    "totals_counted",
    "cash_lines",
    "restated_copies",
    "unfunded_commitments",
    "custom_tags",
    "no_identified_holdings",
    "affiliate_split",
    "no_filed_total",
    "other",
}


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


def test_health_and_swagger(client: TestClient) -> None:
    assert client.get("/health").json() == {
        "status": "ok",
        "release": "2026q3",
        "read_only": True,
    }
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert set(paths) == {
        "/health",
        "/coverage",
        "/filings",
        "/filings/{adsh}",
        "/filings/{adsh}/holdings",
        "/triage",
        "/cleaning-rules",
    }
    assert client.get("/docs").status_code == 200


def test_coverage_matches_report(client: TestClient) -> None:
    expected = json.loads(
        (ROOT / "reports" / "coverage.json").read_text(encoding="utf-8")
    )
    response = client.get("/coverage")
    assert response.status_code == 200
    assert response.json() == expected


def test_filings_returns_every_attempt(client: TestClient) -> None:
    import pandas as pd

    expected = pd.read_csv(
        ROOT / "reports" / "coverage.csv", dtype={"adsh": str, "cik": str}
    )
    response = client.get("/filings")
    assert response.status_code == 200
    filings = response.json()["filings"]
    assert len(filings) == len(expected)
    assert {item["adsh"] for item in filings} == set(expected["adsh"])


def test_every_excluded_filing_has_valid_triage(client: TestClient) -> None:
    import pandas as pd

    coverage = pd.read_csv(
        ROOT / "reports" / "coverage.csv", dtype={"adsh": str}
    )
    excluded = set(coverage.loc[~coverage["admitted"], "adsh"])
    triage = client.get("/triage").json()["triage"]
    assert {item["adsh"] for item in triage} == excluded
    assert all(item["triage_category"] in VALID_TRIAGE for item in triage)
    assert all(
        item["evidence"] and item["example"]
        for item in triage
    )


def test_admitted_holdings_sum_to_panel_and_coverage(client: TestClient) -> None:
    import pandas as pd

    panel = pd.read_parquet(ROOT / "outputs" / "panel" / "holdings.parquet")
    panel_totals = panel.groupby("adsh")["fair_value"].sum()
    coverage = pd.read_csv(
        ROOT / "reports" / "coverage.csv", dtype={"adsh": str}
    )
    admitted = coverage[coverage["admitted"]]
    assert len(admitted) == panel["adsh"].nunique()

    for row in admitted.itertuples():
        response = client.get(f"/filings/{row.adsh}/holdings")
        assert response.status_code == 200, row.adsh
        document = response.json()
        exported_total = sum(
            holding["fair_value"] or 0.0 for holding in document["holdings"]
        )
        assert math.isclose(exported_total, row.holdings_fv, abs_tol=0.5)
        assert math.isclose(
            exported_total, panel_totals.loc[row.adsh], abs_tol=0.5
        )
        assert math.isclose(document["holdings_fv"], row.holdings_fv, abs_tol=0.5)


def test_excluded_holdings_endpoint_is_explicit(client: TestClient) -> None:
    excluded = client.get("/triage").json()["triage"][0]["adsh"]
    response = client.get(f"/filings/{excluded}/holdings")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "not_found"
