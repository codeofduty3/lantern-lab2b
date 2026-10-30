"""Export the read-only LANTERN app data from the completed pipeline.

The exporter copies values from the panel and reports. It never recreates
cleaning or reconciliation logic and is intentionally separate from ``dvc.yaml``.

Usage:
    python scripts/export_app_data.py
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
APP_DATA = ROOT / "app" / "data"
COVERAGE = ROOT / "reports" / "coverage.csv"
COVERAGE_METRICS = ROOT / "reports" / "coverage.json"
TRIAGE_NOTES = ROOT / "docs" / "triage_notes.csv"
CLEANING_LOG = ROOT / "reports" / "cleaning_log.csv"
PANEL = ROOT / "outputs" / "panel" / "holdings.parquet"

TRIAGE_CATEGORIES = {
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

HOLDING_FIELDS = [
    "identifier",
    "investment_type",
    "industry",
    "affiliation",
    "principal",
    "cost",
    "fair_value",
    "interest_rate",
    "spread",
    "pik_rate",
    "maturity",
    "pct_net_assets",
    "source_rows",
    "n_rows",
    "n_conflicts",
    "identifier_source",
    "fair_value_source",
    "security_class",
    "affiliation_category",
    "has_unfunded_commitment",
    "shares",
    "unfunded_commitment",
]

FILING_FIELDS = [
    "adsh",
    "cik",
    "name",
    "form",
    "period",
    "n_holdings",
    "holdings_fv",
    "missing_fv",
    "filed_fv",
    "gap_pct",
    "admitted",
    "triage_category",
]


def _value(value):
    """Convert pandas/numpy scalars to strict JSON values."""
    if value is None or (not isinstance(value, (list, dict)) and pd.isna(value)):
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _records(frame: pd.DataFrame, fields: list[str]) -> list[dict]:
    available = [field for field in fields if field in frame.columns]
    return [
        {field: _value(row[field]) for field in available}
        for _, row in frame[available].iterrows()
    ]


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _edgar_url(row: pd.Series) -> str:
    cik = str(row["cik"]).lstrip("0")
    accession = str(row["adsh"]).replace("-", "")
    return (
        "https://www.sec.gov/Archives/edgar/data/"
        f"{cik}/{accession}/{row['adsh']}-index.html"
    )


def _check_coverage(coverage: pd.DataFrame, metrics: dict) -> None:
    admitted = coverage[coverage["admitted"]]
    checks = {
        "filings_attempted": len(coverage),
        "filings_admitted": len(admitted),
        "share_of_filings": round(
            len(admitted) / len(coverage) if len(coverage) else 0.0, 3
        ),
        "filed_fv_attempted": float(coverage["filed_fv"].sum()),
        "filed_fv_admitted": float(admitted["filed_fv"].sum()),
        "share_of_dollars": round(
            float(admitted["filed_fv"].sum() / coverage["filed_fv"].sum()), 3
        ),
        "filings_without_soi_rows": metrics["filings_without_soi_rows"],
    }
    if checks != metrics:
        raise AssertionError(
            "Exported filing totals disagree with reports/coverage.json: "
            f"{checks!r} != {metrics!r}"
        )


def _check_panel(panel: pd.DataFrame, admitted: pd.DataFrame) -> None:
    panel_totals = (
        panel.groupby("adsh", as_index=False)["fair_value"]
        .sum()
        .rename(columns={"fair_value": "panel_fv"})
    )
    compared = admitted[["adsh", "holdings_fv"]].merge(
        panel_totals, on="adsh", how="outer", indicator=True
    )
    if not compared["_merge"].eq("both").all():
        raise AssertionError("Admitted filings and the panel have different filing keys")
    difference = compared["panel_fv"] - compared["holdings_fv"]
    if difference.abs().max() > 0.5:
        bad = compared.loc[difference.abs() > 0.5]
        raise AssertionError(
            "Panel total differs from reports/coverage.csv:\n"
            + bad.to_string(index=False)
        )
    if not math.isclose(
        float(panel["fair_value"].sum()),
        float(admitted["holdings_fv"].sum()),
        abs_tol=0.5,
    ):
        raise AssertionError("Panel grand total differs from admitted coverage total")


def main() -> None:
    metrics = json.loads(COVERAGE_METRICS.read_text(encoding="utf-8"))
    coverage = pd.read_csv(COVERAGE, dtype={"adsh": str, "cik": str})
    triage_notes = pd.read_csv(TRIAGE_NOTES, dtype=str, keep_default_na=False)
    cleaning = pd.read_csv(CLEANING_LOG)
    panel = pd.read_parquet(PANEL)

    _check_coverage(coverage, metrics)
    admitted = coverage[coverage["admitted"]].copy()
    _check_panel(panel, admitted)

    missing_notes = set(coverage.loc[~coverage["admitted"], "adsh"]) - set(
        triage_notes["adsh"]
    )
    invalid_categories = set(triage_notes["triage_category"]) - TRIAGE_CATEGORIES
    if missing_notes or invalid_categories:
        raise AssertionError(
            f"Invalid triage export; missing={sorted(missing_notes)!r}, "
            f"categories={sorted(invalid_categories)!r}"
        )

    if APP_DATA.exists():
        shutil.rmtree(APP_DATA)
    APP_DATA.mkdir(parents=True)

    copy_metrics = json.loads(COVERAGE_METRICS.read_text(encoding="utf-8"))
    _write_json(APP_DATA / "coverage.json", copy_metrics)

    filings = []
    for _, row in coverage.iterrows():
        filing = {field: _value(row[field]) for field in FILING_FIELDS}
        filing["edgar_url"] = _edgar_url(row)
        filings.append(filing)
    _write_json(APP_DATA / "filings.json", {"filings": filings})

    notes = triage_notes.set_index("adsh")
    excluded = coverage.loc[~coverage["admitted"]].copy()
    triage = []
    for _, row in excluded.iterrows():
        note = notes.loc[row["adsh"]]
        triage.append(
            {
                "adsh": row["adsh"],
                "name": row["name"],
                "form": row["form"],
                "period": row["period"],
                "holdings_fv": _value(row["holdings_fv"]),
                "filed_fv": _value(row["filed_fv"]),
                "gap_pct": _value(row["gap_pct"]),
                "triage_category": note["triage_category"],
                "evidence": note["evidence"],
                "example": note["example"],
                "fix": note["fix"],
                "edgar_url": _edgar_url(row),
            }
        )
    _write_json(APP_DATA / "triage.json", {"triage": triage})
    _write_json(
        APP_DATA / "cleaning_rules.json",
        {"rules": _records(cleaning, list(cleaning.columns))},
    )

    holdings_dir = APP_DATA / "holdings"
    holdings_dir.mkdir()
    for row in admitted.itertuples():
        filing_panel = panel.loc[panel["adsh"].eq(row.adsh)]
        filing_total = float(filing_panel["fair_value"].sum())
        if not math.isclose(filing_total, float(row.holdings_fv), abs_tol=0.5):
            raise AssertionError(f"{row.adsh}: holdings do not sum to coverage.csv")
        _write_json(
            holdings_dir / f"{row.adsh}.json",
            {
                "adsh": row.adsh,
                "holdings_fv": _value(row.holdings_fv),
                "holdings": _records(filing_panel, HOLDING_FIELDS),
            },
        )

    total_bytes = sum(path.stat().st_size for path in APP_DATA.rglob("*.json"))
    print(f"Exported {len(filings)} filings ({len(admitted)} with holdings) to {APP_DATA}")
    print(f"Export size: {total_bytes / 1024 / 1024:.1f} MiB")


if __name__ == "__main__":
    main()
