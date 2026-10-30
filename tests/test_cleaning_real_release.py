"""Part 2 rules, tested against the configured real 2026q3 release."""
from pathlib import Path
import sys

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lookthrough import clean, holdings, load, mapping, paths, reconcile, tables  # noqa: E402

P = paths.load_params(ROOT)
RDIR = paths.release_dir(P, ROOT)


@pytest.fixture(scope="session")
def real_frames():
    sub = load.load_sub(RDIR)
    num = load.load_num(
        RDIR, tags=[reconcile.FV_TAG], custom_fv=True)
    h = tables.load_table(ROOT / "outputs" / "canonical" / "holdings")
    return sub, num, h


def _row(h, adsh, text):
    x = h[
        h["adsh"].eq(adsh)
        & h["identifier"].str.contains(text, case=False, regex=False,
                                       na=False)
    ]
    assert len(x) == 1, (adsh, text, len(x))
    return x.index[0]


def test_transform_current_period_uses_real_sub_period(real_frames):
    sub, _, h = real_frames
    adsh = "0000017313-26-000095"
    sample = h[h["adsh"].eq(adsh)].iloc[0]
    frame = pd.DataFrame({
        "adsh": [adsh, adsh],
        "ddate": ["2026-06-30", "2026-03-31"],
        "period": [pd.NA, pd.NA],
        "identifier": [sample["identifier"], sample["identifier"]],
    })
    out = holdings.split_periods(frame, sub)
    assert list(out["is_current"]) == [True, False]
    assert out.loc[0, "period"] == sub.set_index("adsh").at[adsh, "period"]


def test_transform_axis_identifiers_recovers_real_idless_filing(real_frames):
    sub, _, _ = real_frames
    header = load.soi_header(RDIR)
    tag = load.load_tag(RDIR)
    cm = mapping.map_soi_columns(header, tag)
    soi = load.load_soi(RDIR, mapping.soi_usecols(header, cm))
    soi = soi[soi["adsh"].isin(sub["adsh"])]
    canon = holdings.split_periods(mapping.to_canonical(soi, cm), sub)
    out = clean.recover_axis_identifiers(canon)
    adsh = "0001493152-26-036285"
    x = out[out["adsh"].eq(adsh) & out["is_current"]]
    assert x["identifier"].notna().any()
    assert x.loc[x["identifier"].notna(), "identifier_source"].eq(
        "fallback axis").all()
    assert "ARK Type One Deep Ventures Fund LLC" in set(x["identifier"])


def test_transform_custom_fair_values_fills_real_num_values(real_frames):
    sub, num, h = real_frames
    out = clean.recover_custom_fair_values(
        h[h["is_current"]], num, sub)
    checks = {
        ("0002082559-26-000086",
         "Morgan Stanley Institutional Liquidity Funds"):
            9_637_000.0,
        ("0002082557-26-000059",
         "Morgan Stanley Institutional Liquidity Funds"):
            9_376_000.0,
        ("0001193125-26-342417", "Investments in Money Market Funds"):
            22_597_000.0,
    }
    filled = out[out["fair_value_source"].fillna("").str.startswith("NUM ")]
    assert len(filled) > 0
    for (adsh, text), value in checks.items():
        row = out[
            out["adsh"].eq(adsh)
            & out["identifier"].str.contains(
                text, case=False, regex=False, na=False)
        ]
        assert row["fair_value"].notna().all()
        assert value in set(row["fair_value"])


def test_transform_cleaning_attributes_covers_real_equity_control_unfunded(
        real_frames):
    _, _, h = real_frames
    out = clean.add_cleaning_attributes(h[h["is_current"]])
    warrant = out[
        out["identifier"].str.contains("Warrants", case=False, na=False)]
    equity = out[
        out["identifier"].str.contains("Common Equity", case=False, na=False)]
    controlled = out[out["identifier"].str.contains(
        "Controlled Investments", case=False, na=False)]
    unfunded = out[out["identifier"].str.contains(
        "Unfunded Investments", case=False, na=False)]
    assert (warrant["security_class"] == "warrant").all()
    assert (equity["security_class"] == "equity").any()
    assert "controlled" in set(controlled["affiliation_category"])
    assert unfunded["has_unfunded_commitment"].all()


def test_rule_totals_real_release_and_spares_borrower_names(real_frames):
    _, _, h = real_frames
    drop, _ = clean.rule_totals(h[h["is_current"]])
    cur = h[h["is_current"]]
    assert drop[_row(cur, "0001280784-26-000042", "Total Annex Cloud")]
    assert drop[_row(cur, "0001193125-26-351731", "Net Assets")]
    access = cur[
        cur["adsh"].eq("0001143513-26-000012")
        & cur["identifier"].str.contains(
            "Total Access Elevator", case=False, regex=False, na=False)
    ]
    expert = cur[
        cur["adsh"].eq("0001580345-26-000025")
        & cur["identifier"].str.contains(
            "Total Expert Inc.", case=False, regex=False, na=False)
    ]
    assert len(access) and len(expert)
    assert not drop.loc[access.index].any()
    assert not drop.loc[expert.index].any()


def test_rule_issuer_aggregates_real_control_and_restated_rows(real_frames):
    _, _, h = real_frames
    cur = h[h["is_current"]]
    drop, _ = clean.rule_issuer_aggregates(cur)
    cap = cur[
        cur["adsh"].eq("0000017313-26-000095")
        & cur["identifier"].eq("CapTrin Partners, LLC")
    ].index[0]
    irgse = cur[
        cur["adsh"].eq("0001193125-26-332725")
        & cur["identifier"].eq("IRGSE Holding Corp")
    ].index[0]
    detailed = cur[
        cur["adsh"].eq("0001193125-26-332725")
        & cur["identifier"].str.contains("Class A Units", regex=False,
                                         na=False)
    ].index[0]
    assert drop[cap] and drop[irgse]
    assert not drop[detailed]


def test_rule_cash_real_money_market_and_spares_investments(real_frames):
    _, _, h = real_frames
    cur = h[h["is_current"]]
    drop, _ = clean.rule_cash(cur)
    cash = _row(cur, "0001193125-26-335023", "Money Market")
    holding = _row(cur, "0001280784-26-000042", "Total Annex Cloud")
    assert drop[cash]
    assert not drop[holding]


def test_cleaning_log_has_required_columns_and_real_examples():
    log = pd.read_csv(ROOT / "reports" / "cleaning_log.csv",
                      dtype={"example_adsh": str, "example_soi_row": str})
    assert list(log.columns) == [
        "rule", "artifact", "motivation", "example_adsh",
        "example_soi_row", "rows_affected", "coverage_before",
        "coverage_after",
    ]
    assert (log["rows_affected"] > 0).all()
    header = load.soi_header(RDIR)
    soi = load.load_soi(RDIR, usecols=["adsh"])
    for r in log.itertuples():
        n = int(r.example_soi_row)
        assert n in soi.index
        assert soi.at[n, "adsh"] == r.example_adsh
