"""Write the Case Study 2B outputs: the panel, coverage, triage and cleaning log."""
import json

import pandas as pd

from . import reconcile, tables

PANEL_COLS = ["adsh", "cik", "name", "period", "identifier", "investment_type", "industry", "affiliation",
              "principal", "cost", "fair_value", "interest_rate", "spread", "pik_rate", "maturity",
              "pct_net_assets", "source_rows", "n_rows", "n_conflicts"]


def write_outputs(kept: pd.DataFrame, rec: pd.DataFrame, diag: pd.DataFrame, log: pd.DataFrame, root, P,
                  triage: pd.DataFrame = None, no_soi: pd.DataFrame = None) -> dict:
    """triage: one row per excluded filing (adsh, triage_category, example, evidence, fix), written into
    coverage.csv and triage.md; an excluded filing without a row stays 'to_triage'.
    no_soi: filings in SUB with no SOI rows at all, reported separately."""
    out = root / P["outputs"]["panel"]; rep = root / P["outputs"]["reports"]
    rep.mkdir(parents=True, exist_ok=True)
    admitted = set(rec.loc[rec["admitted"], "adsh"])
    panel = kept[kept["adsh"].isin(admitted)][[c for c in PANEL_COLS if c in kept]]
    panel_path = tables.save_table(panel, out / "holdings")
    notes = triage.set_index("adsh") if triage is not None else pd.DataFrame(columns=["triage_category"])
    cov = rec.copy()
    cov["triage_category"] = ["" if a else notes["triage_category"].get(d, "to_triage")
                              for a, d in zip(cov["admitted"], cov["adsh"])]
    cov.to_csv(rep / "coverage.csv", index=False)
    metrics = reconcile.coverage(rec)
    if no_soi is not None:
        metrics["filings_without_soi_rows"] = int(len(no_soi))
    (rep / "coverage.json").write_text(json.dumps(metrics, indent=2))   # DVC metric
    a = cov[cov["admitted"]]
    share = lambda part, whole: f"{part / whole:.1%}" if whole else "n/a"
    lines = ["# Coverage report", "",
             f"Filings attempted: {len(cov)}; admitted: {len(a)} ({len(a) / max(len(cov), 1):.0%}).",
             f"Filed fair value attempted: ${cov['filed_fv'].sum():,.0f}; admitted: ${a['filed_fv'].sum():,.0f} "
             f"({a['filed_fv'].sum() / max(cov['filed_fv'].sum(), 1):.0%}).", ""]
    x = cov[~cov["admitted"]]
    if len(x):
        lines += ["## Excluded filings by triage category", "",
                  "| Category | Filings | Share of filings | Filed FV | Share of filed FV |", "|---|---:|---:|---:|---:|"]
        for cat, g in x.groupby("triage_category"):
            lines.append(f"| {cat} | {len(g)} | {share(len(g), len(cov))} | {g['filed_fv'].sum():,.0f} "
                         f"| {share(g['filed_fv'].sum(), cov['filed_fv'].sum())} |")
        lines.append("")
    if no_soi is not None:
        lines += ["## Filings in SUB with no SOI rows (reported separately, not attempted)", ""]
        lines += [f"- {r.name} ({r.adsh}), {r.form}, period {r.period}" for r in no_soi.itertuples()] or ["- none"]
        lines.append("")
    lines += ["## Filings attempted", "",
              "| BDC | Holdings | Holdings FV | Filed FV | Gap | Admitted |", "|---|---:|---:|---:|---:|---|"]
    money = lambda x: "n/a" if pd.isna(x) else f"{x:,.0f}"
    pct = lambda x: "n/a" if pd.isna(x) else f"{x:+.2%}"
    lines += [f"| {r.name} | {r.n_holdings} | {money(r.holdings_fv)} | {money(r.filed_fv)} | {pct(r.gap_pct)} | {r.admitted} |"
              for r in cov.itertuples()]
    (rep / "coverage.md").write_text("\n".join(lines) + "\n")
    tri = ["# Triage of non-admitted filings", "",
           "For each filing: the evidence, the root-cause category, an example (accession number and SOI row), and the fix you applied or why none is possible.", ""]
    note = lambda adsh, c: notes[c].get(adsh, "_to fill in_") if c in notes else "_to fill in_"
    for r in diag.itertuples():
        tri += [f"## {r.name} ({r.adsh})", "", f"- Gap: {pct(r.gap_pct)}",
                f"- Holdings identified: {r.n_holdings}; current SOI rows without an identifier: {r.rows_without_identifier}",
                f"- Holdings with missing fair value: {r.missing_fv_rows}",
                f"- No filed total in NUM: {r.no_filed_total}",
                f"- Custom tag used in the SOI: {r.custom_tag_in_soi}; custom fair-value facts in NUM: {r.custom_fv_facts_in_num}",
                f"- Negative fair value tagged by investment type in NUM: {r.negative_type_level_fv:,.0f}",
                f"- **Evidence:** {note(r.adsh, 'evidence')}",
                f"- **Root-cause category:** {note(r.adsh, 'triage_category')}",
                f"- **Example:** {note(r.adsh, 'example')}",
                f"- **Fix or reason:** {note(r.adsh, 'fix')}", ""]
    (rep / "triage.md").write_text("\n".join(tri))
    log.to_csv(rep / "cleaning_log.csv", index=False)
    return {"panel": panel_path, "coverage": rep / "coverage.csv", "triage": rep / "triage.md"}
