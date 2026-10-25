"""Stage 2 (parse): Part 1, requirement 3.

1. Load SUB, TAG and SOI for the release and map SOI columns by XBRL tag.
2. Normalize dates and label each SOI row current, comparative or other.
3. Coalesce each holding's rows into one row, keeping source_rows (SOI row numbers).
4. Count holdings with conflicting values and record how each was resolved.

Writes:
  outputs/canonical/holdings.parquet   one row per holding and date (all dates; is_current flags
                                     the current period), input to cleaning and reconciliation
  reports/periods.csv                SOI rows per filing: current, comparative, other dates
  reports/conflicts.csv              every current-period holding with conflicting values

Run from the repo root:  python scripts/parse.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import coalesce, holdings, load, mapping, paths, tables  # noqa: E402

P = paths.load_params(ROOT)
rdir = paths.release_dir(P, ROOT)
reports = ROOT / P["outputs"]["reports"]
reports.mkdir(parents=True, exist_ok=True)

# 1. Load and map by tag
sub, tag = load.load_sub(rdir), load.load_tag(rdir)
header = load.soi_header(rdir)
colmap = mapping.map_soi_columns(header, tag)
extra = [c for c in [coalesce.SUBSIDIARY_AXIS] if c in header]
soi = load.load_soi(rdir, mapping.soi_usecols(header, colmap) + extra)
soi = soi[soi["adsh"].isin(sub["adsh"])]
canon = holdings.split_periods(mapping.to_canonical(soi, colmap), sub)
canon["subsidiary"] = soi[coalesce.SUBSIDIARY_AXIS] if extra else pd.NA

# 2. Current, comparative (the filing's most common other date), other
other = canon.loc[~canon["is_current"]]
comp_date = other.groupby("adsh")["ddate"].agg(lambda s: s.value_counts().index[0])
canon["schedule"] = "other"
canon.loc[canon["is_current"], "schedule"] = "current"
canon.loc[~canon["is_current"] & canon["ddate"].eq(canon["adsh"].map(comp_date)),
          "schedule"] = "comparative"
periods = (canon.groupby(["adsh", "name", "form", "period", "schedule"]).size()
           .unstack(fill_value=0).reset_index())
periods["comparative_date"] = periods["adsh"].map(comp_date)
periods.to_csv(reports / "periods.csv", index=False)

# 3 and 4. Coalesce, count and resolve conflicts
h = coalesce.coalesce(canon)
out = tables.save_table(h, ROOT / "outputs" / "canonical" / "holdings")
cur = h[h["is_current"]]
conf = cur[cur["n_conflicts"] > 0]
conf[["adsh", "name", "identifier", "n_rows", "n_conflicts", "conflict_fields",
      "resolution", "fair_value", "source_rows"]].to_csv(reports / "conflicts.csv", index=False)

# Summary
print(f"Release {rdir.name}: {sub['adsh'].nunique()} filings, {len(soi):,} SOI rows")
print("SOI rows by schedule:", canon["schedule"].value_counts().to_dict())
cur_rows = canon[canon["is_current"]]
print(f"Current rows without an identifier: {cur_rows['identifier'].isna().sum():,} "
      f"of {len(cur_rows):,} (not coalesced; see Part 2)")
print(f"Current holdings: {len(cur):,} in {cur['adsh'].nunique()} filings; "
      f"{(cur['n_rows'] > 1).sum():,} were built from more than one SOI row")
print(f"Holdings with conflicting values: {len(conf):,} in {conf['adsh'].nunique()} filings")
print("  by field:", {f: int(conf['conflict_fields'].str.contains(rf'(?:^|;){f}(?:;|$)').sum())
                      for f in ["fair_value", "cost", "principal", "interest_rate", "spread",
                                "pik_rate", "pct_net_assets"]})
print("  resolved by:", conf["resolution"].value_counts().to_dict())
print(f"\nWrote {out.relative_to(ROOT)}, reports/periods.csv, reports/conflicts.csv")
