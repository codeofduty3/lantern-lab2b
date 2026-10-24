"""Part 1, requirement 4: our side of the agreement check.

Without EdgarTools, we compare our parsed holdings with the human-readable schedule of
investments of three filings, one from each monthly ZIP. For each filing this writes our
holding count, fair-value total, the filing's own total (NUM), the link to the document,
and the largest holdings to look up, to reports/agreement_ours.csv.
The comparison itself is written up in reports/agreement.md.

Run from the repo root after scripts/parse.py:  python scripts/agreement.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import load, paths, reconcile, tables  # noqa: E402

FILINGS = {
    "0001487918-26-000078": "OFS Capital Corp (2026_07)",
    "0001193125-26-346670": "TCW Steel City Senior Lending BDC (2026_08)",
    "0002131040-26-000008": "Robinhood Ventures Fund II (2026_09)",
}

P = paths.load_params(ROOT)
rdir = paths.release_dir(P, ROOT)
sub = load.load_sub(rdir)
num = load.load_num(rdir, tags=[reconcile.FV_TAG], adsh=list(FILINGS))
filed = reconcile.filed_totals(num, sub).set_index("adsh")["filed_fv"]
h = tables.load_table(ROOT / "outputs" / "interim" / "holdings")
h = h[h["is_current"] & h["adsh"].isin(list(FILINGS))]

rows = []
for adsh, label in FILINGS.items():
    x = h[h["adsh"] == adsh].sort_values("fair_value", ascending=False)
    total = x["fair_value"].sum()
    rows.append({"adsh": adsh, "filing": label,
                 "our_holdings": len(x),
                 "our_fair_value": total,
                 "filed_total_num": filed.get(adsh),
                 "gap_pct": (total - filed.get(adsh)) / filed.get(adsh) if adsh in filed else None,
                 "document": x["inlineurl"].iloc[0] if len(x) else "",
                 "largest_holdings": " | ".join(f"{i} = {v:,.0f}"
                                                for i, v in zip(x["identifier"].head(3), x["fair_value"].head(3)))})
    print(f"\n{label}  ({adsh})")
    print(f"  ours: {len(x)} holdings, fair value {total:,.0f}")
    print(f"  filing's own total (NUM): {filed.get(adsh, float('nan')):,.0f}")
    print(f"  document: {rows[-1]['document']}")
    for i, v in zip(x["identifier"].head(3), x["fair_value"].head(3)):
        print(f"    {v:>14,.0f}  {i[:110]}")

out = ROOT / P["outputs"]["reports"] / "agreement_ours.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"\nWrote {out.relative_to(ROOT)}")
