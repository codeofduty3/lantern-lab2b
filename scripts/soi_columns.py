"""Part 1, requirement 2: map every SOI column of the release to its XBRL tag.

Writes reports/soi_columns.csv: one row per SOI column with
  kind      metadata | axis | mapped (a canonical field) | unmapped
  field     the canonical field it feeds (mapped columns only)
  tags      the XBRL tag(s) whose label is this column header (from TAG)
  versions  the taxonomy version(s) of those tags (us-gaap/2025, us-gaap/2026, ...)
  custom    1 if a tag is a filer's custom tag, 0 if standard, empty if no tag found
  rows      current-period SOI rows with a value in this column
  filings   current-period filings with a value in this column

This is the evidence behind docs/schema.md.
Run from the repo root:  python scripts/soi_columns.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import load, mapping, paths  # noqa: E402

P = paths.load_params(ROOT)
rdir = paths.release_dir(P, ROOT)
tag = load.load_tag(rdir)
header = load.soi_header(rdir)
soi = load.load_soi(rdir)
soi = soi[soi["ddate"] == soi["period"]]          # current-period rows only

colmap = mapping.map_soi_columns(header, tag)
field_of = {c: f for f, cols in colmap.items() for c in cols}
by_label = (tag.dropna(subset=["tlabel"])
            .groupby("tlabel")
            .agg(tags=("tag", lambda s: ";".join(sorted(set(s)))),
                 versions=("version", lambda s: ";".join(sorted(set(s)))),
                 custom=("custom", lambda s: ";".join(sorted(set(s))))))

meta = set(mapping.META) | {"qtrs", "filed", "source_release", "source_soi_row"}
rows = []
for col in header:
    if col in meta:
        kind = "metadata"
    elif col.endswith("Axis"):
        kind = "axis"
    else:
        kind = "mapped" if col in field_of else "unmapped"
    has = soi[col].notna() if col in soi else pd.Series(False, index=soi.index)
    t = by_label.loc[col] if col in by_label.index else None
    rows.append({"column": col, "kind": kind, "field": field_of.get(col, ""),
                 "tags": "" if t is None else t["tags"],
                 "versions": "" if t is None else t["versions"],
                 "custom": "" if t is None else t["custom"],
                 "rows": int(has.sum()),
                 "filings": int(soi.loc[has, "adsh"].nunique())})

out = pd.DataFrame(rows)
path = ROOT / P["outputs"]["reports"] / "soi_columns.csv"
path.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(path, index=False)

print(f"{len(out)} SOI columns in {rdir.name}: {out['kind'].value_counts().to_dict()}")
print("\nMapped columns (canonical field <- SOI column):")
print(out[out["kind"] == "mapped"][["field", "column", "tags", "versions", "rows", "filings"]]
      .sort_values("field").to_string(index=False))
u = out[out["kind"] == "unmapped"].sort_values("filings", ascending=False)
print(f"\nUnmapped value columns: {len(u)}, used by 5+ filings: {(u['filings'] >= 5).sum()}")
print(u.head(15)[["column", "tags", "filings"]].to_string(index=False))
print(f"\nWrote {path.relative_to(ROOT)}")
