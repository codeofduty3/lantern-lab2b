"""Stage 3 (reconcile): Part 3, reconciliation and coverage.

1. Take the current-period holdings from the parse stage and apply the cleaning rules.
2. Compare each filing's holdings with its filed total (the undimensioned
   InvestmentOwnedAtFairValue fact at the period end in SUB) and admit filings
   within reconcile.tolerance. Every current filing with SOI rows is attempted;
   filings in SUB with no SOI rows are reported separately.
3. Triage every filing not admitted, from docs/triage_notes.csv (category, example,
   evidence, fix). An excluded filing without a note stays 'to_triage', so the
   self-check fails until it is triaged.

Writes:
  outputs/panel/holdings.parquet   admitted filings only, current period, one row per holding
  reports/coverage.csv, coverage.md, coverage.json (DVC metric), triage.md, cleaning_log.csv

Run from the repo root after scripts/parse.py:  python scripts/reconcile.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import clean, holdings, load, mapping, paths, reconcile, report, tables  # noqa: E402

# Structural rules in deliberate semantic order; coverage is measured only
# after the rule definitions and order have been fixed.
RULES = clean.CLEANING_RULES

P = paths.load_params(ROOT)
rdir = paths.release_dir(P, ROOT)
tol = float(P["reconcile"]["tolerance"])

# Inputs: SUB, NUM fair-value facts, SOI rows (for the attempted set and the triage evidence)
sub, tag = load.load_sub(rdir), load.load_tag(rdir)
header = load.soi_header(rdir)
colmap = mapping.map_soi_columns(header, tag)
soi = load.load_soi(rdir, mapping.soi_usecols(header, colmap))
soi = soi[soi["adsh"].isin(sub["adsh"])]
canon = holdings.split_periods(mapping.to_canonical(soi, colmap), sub)
canon = clean.recover_axis_identifiers(canon)
num = load.load_num(rdir, tags=[reconcile.FV_TAG], custom_fv=True)
h_all = tables.load_table(ROOT / "outputs" / "canonical" / "holdings")

# 1. Clean the current period
filed = reconcile.filed_totals(num, sub)
attempted = set(soi["adsh"])
h = h_all[h_all["is_current"]].copy()
base_cov = clean.coverage_value(h, filed, sub, tol, attempted)

# Every non-mask transformation is represented in the log. Comparative rows
# were already classified by the parse stage, axis identifiers were recovered
# before coalescing, and custom values/attributes are applied here.
pre_axis = h.loc[h.get(
    "identifier_source", pd.Series(index=h.index, dtype=object)).ne(
        "fallback axis")].copy()
axis_mask = h.get(
    "identifier_source", pd.Series(index=h.index, dtype=object)
).eq("fallback axis")
log_rows = [
    clean.transformation_entry(
        "transform_current_period",
        "comparative and other-date rows excluded from the current panel",
        "The row date differs from the filing period in SUB.",
        h_all, ~h_all["is_current"], base_cov, base_cov),
    clean.transformation_entry(
        "transform_axis_identifiers",
        "identifier recovered from a fallback axis for an ID-less filing",
        "Every current row in that filing lacks the standard identifier axis; "
        "the Legal Entity member itself names the investee.",
        h, axis_mask,
        clean.coverage_value(pre_axis, filed, sub, tol, attempted), base_cov),
]

h = clean.recover_custom_fair_values(h, num, sub)
custom_mask = h["fair_value_source"].fillna("").str.startswith("NUM ")
log_rows.append(clean.transformation_entry(
    "transform_custom_fair_values",
    "fair value recovered from a custom NUM tag keyed by identifier",
    "The SOI money-market row has an identifier but no standard fair-value "
    "fact; NUM supplies the omitted value on that same identifier member.",
    h, custom_mask, base_cov,
    clean.coverage_value(h, filed, sub, tol, attempted)))

h = clean.add_cleaning_attributes(h)
log_rows.append(clean.transformation_entry(
    "transform_cleaning_attributes",
    "equity/warrant security class, affiliate category, and unfunded flag",
    "Security and affiliate terms are filed in the identifier or standard "
    "security axes; commitment columns carry unfunded amounts.",
    h, pd.Series(True, index=h.index),
    clean.coverage_value(h, filed, sub, tol, attempted),
    clean.coverage_value(h, filed, sub, tol, attempted)))

kept, rule_log = clean.apply_rules(h, RULES, filed=filed, sub=sub,
                                   tolerance=tol, soi_adsh=attempted)
log = pd.concat([pd.DataFrame(log_rows), rule_log], ignore_index=True)

# 2. Reconcile and admit
rec = reconcile.reconcile(kept, filed, sub, tol, soi_adsh=set(soi["adsh"]))
no_soi = sub.loc[~sub["adsh"].isin(soi["adsh"]), ["adsh", "cik", "name", "form", "period"]]

# 3. Triage and write the outputs
diag = reconcile.diagnose(rec, kept, num, canon)
triage = pd.read_csv(ROOT / "docs" / "triage_notes.csv", dtype=str)
bad = sorted(set(triage["triage_category"]) - set(reconcile.TRIAGE))
if bad:
    sys.exit(f"docs/triage_notes.csv has categories outside Section 7: {bad}")
out = report.write_outputs(kept, rec, diag, log, ROOT, P, triage=triage, no_soi=no_soi)

# Summary
cov = reconcile.coverage(rec)
excluded = set(rec.loc[~rec["admitted"], "adsh"])
untriaged = sorted(excluded - set(triage["adsh"]))
stale = sorted(set(triage["adsh"]) - excluded)
print(f"Release {rdir.name}: {len(sub)} filings in SUB; {cov['filings_attempted']} attempted "
      f"(SOI rows), {len(no_soi)} with no SOI rows (reported separately)")
print(f"Admitted {cov['filings_admitted']} of {cov['filings_attempted']} filings "
      f"({cov['share_of_filings']:.1%}), ${cov['filed_fv_admitted']:,.0f} of "
      f"${cov['filed_fv_attempted']:,.0f} filed fair value ({cov['share_of_dollars']:.1%}), tolerance {tol:.2%}")
print("Excluded filings by triage category:",
      rec.loc[~rec["admitted"], "adsh"].map(triage.set_index("adsh")["triage_category"])
      .fillna("to_triage").value_counts().to_dict())
if untriaged:
    print(f"WARNING: {len(untriaged)} excluded filings have no note in docs/triage_notes.csv, "
          f"e.g. {untriaged[:3]}; they are marked to_triage")
if stale:
    print(f"Note: {len(stale)} notes in docs/triage_notes.csv are for filings now admitted, e.g. {stale[:3]}")
for k, v in out.items():
    print(f"Wrote {Path(v).relative_to(ROOT)}")
