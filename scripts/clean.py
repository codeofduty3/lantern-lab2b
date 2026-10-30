"""Stage 3 (clean): apply Part 2 transformations and structural rules.

Reads the canonical holdings from the parse stage and writes one cleaned current
holding per panel row plus the auditable cleaning log.

Writes:
  outputs/cleaned/holdings.parquet
  reports/cleaning_log.csv
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import clean, load, mapping, paths, reconcile, tables  # noqa: E402

P = paths.load_params(ROOT)
rdir = paths.release_dir(P, ROOT)
tol = float(P["reconcile"]["tolerance"])

sub, tag = load.load_sub(rdir), load.load_tag(rdir)
header = load.soi_header(rdir)
colmap = mapping.map_soi_columns(header, tag)
soi = load.load_soi(rdir, mapping.soi_usecols(header, colmap))
soi = soi[soi["adsh"].isin(sub["adsh"])]
attempted = set(soi["adsh"])
num = load.load_num(rdir, tags=[reconcile.FV_TAG], custom_fv=True)
h_all = tables.load_table(ROOT / "outputs" / "canonical" / "holdings")
filed = reconcile.filed_totals(num, sub)

h = h_all[h_all["is_current"]].copy()
base_cov = clean.coverage_value(h, filed, sub, tol, attempted)

# Comparative-period classification happens in parse; axis recovery happens
# before coalescing. The remaining transformations are logged here.
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

kept, rule_log = clean.apply_rules(
    h, clean.CLEANING_RULES, filed=filed, sub=sub, tolerance=tol,
    soi_adsh=attempted)
log = pd.concat([pd.DataFrame(log_rows), rule_log], ignore_index=True)
log.loc[log["rule"].eq("rule_cash"), "motivation"] = (
    "Panel scope for Quanta borrower-to-BDC relationships: investment "
    "holdings exclude cash and money-market funds, which are not loans to a "
    "borrower; filers differ on including cash in filed totals, so residual "
    "gaps are triaged."
)

out = tables.save_table(kept, ROOT / "outputs" / "cleaned" / "holdings")
log_path = ROOT / P["outputs"]["reports"] / "cleaning_log.csv"
log_path.parent.mkdir(parents=True, exist_ok=True)
log.to_csv(log_path, index=False)

print(f"Cleaned {len(kept):,} current holdings from {len(h):,} candidates")
for r in log.itertuples():
    print(f"  {r.rule}: {r.rows_affected:,} rows; "
          f"coverage {r.coverage_before} -> {r.coverage_after}")
print(f"Wrote {out.relative_to(ROOT)}, {log_path.relative_to(ROOT)}")
