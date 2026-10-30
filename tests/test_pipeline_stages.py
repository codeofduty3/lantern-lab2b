"""Pipeline wiring and admission invariants for Part 5."""
from pathlib import Path
import sys

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lookthrough import reconcile  # noqa: E402


def test_dvc_pipeline_has_five_script_stages_and_metric():
    config = yaml.safe_load((ROOT / "dvc.yaml").read_text())
    stages = config["stages"]
    assert list(stages) == ["acquire", "parse", "clean", "reconcile", "report"]
    assert all(
        stages[name]["cmd"] == f"python scripts/{name}.py"
        for name in stages
    )
    def out_names(stage):
        return {
            next(iter(item)) if isinstance(item, dict) else item
            for item in stage["outs"]
        }

    assert "data/raw" in out_names(stages["acquire"])
    assert "outputs/panel/holdings.parquet" in out_names(stages["report"])
    assert "reconcile.tolerance" in stages["clean"]["params"]
    assert "reconcile.tolerance" in stages["reconcile"]["params"]
    metric = next(
        item for item in stages["report"]["metrics"]
        if isinstance(item, dict) and "reports/coverage.json" in item)
    assert metric["reports/coverage.json"]["cache"] is False


def _one_filing_gap():
    current = pd.DataFrame({
        "adsh": ["x"],
        "identifier": ["holding"],
        "fair_value": [100.0],
    })
    sub = pd.DataFrame({
        "adsh": ["x"],
        "cik": ["1"],
        "name": ["TEST BDC"],
        "form": ["10-Q"],
        "period": ["2026-06-30"],
    })
    filed = pd.DataFrame({"adsh": ["x"], "filed_fv": [102.0]})
    return current, filed, sub


def test_tolerance_parameter_controls_admission():
    current, filed, sub = _one_filing_gap()
    strict = reconcile.reconcile(
        current, filed, sub, 0.01, soi_adsh={"x"})
    loose = reconcile.reconcile(
        current, filed, sub, 0.03, soi_adsh={"x"})
    assert not bool(strict.loc[0, "admitted"])
    assert bool(loose.loc[0, "admitted"])


def test_no_filing_with_soi_rows_is_silently_dropped():
    current, filed, sub = _one_filing_gap()
    sub = pd.concat([
        sub,
        pd.DataFrame({
            "adsh": ["z"],
            "cik": ["2"],
            "name": ["NO HOLDINGS BDC"],
            "form": ["10-Q"],
            "period": ["2026-06-30"],
        }),
    ], ignore_index=True)
    filed = pd.concat([
        filed,
        pd.DataFrame({"adsh": ["z"], "filed_fv": [10.0]}),
    ], ignore_index=True)
    rec = reconcile.reconcile(
        current, filed, sub, 0.01, soi_adsh={"x", "z"})
    empty = rec.set_index("adsh").loc["z"]
    assert int(empty["n_holdings"]) == 0
    assert not bool(empty["admitted"])
