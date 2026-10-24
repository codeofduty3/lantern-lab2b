"""Coalesce holdings, resolving pieces held through subsidiaries (Team 3).

The kit's holdings.coalesce_holdings keeps the FIRST non-null value of each field
when a holding's rows disagree. In 2026q3, most disagreements in fair value, cost
and principal come from the "Investment Company, Nonconsolidated Subsidiary Axis":
one loan is reported in pieces, one row per subsidiary that holds a piece, sometimes
with an extra row without the axis. In XBRL, a fact without an axis member is the
total across that axis. So for those holdings:

  1. if a row WITHOUT a subsidiary member has a value, use it (it is the total);
  2. otherwise add up the pieces (one per subsidiary).

Every other conflict keeps the kit's rule (first non-null value in SOI order).
"""
import pandas as pd

from . import holdings

SUBSIDIARY_AXIS = "Investment Company, Nonconsolidated Subsidiary Axis"
MONEY = ["fair_value", "cost", "principal"]


def _resolve(rows: pd.DataFrame):
    """Return (values for MONEY fields, resolution label) for one holding's rows."""
    total = rows[rows["subsidiary"].isna()]
    if total[MONEY].notna().any().any():
        return total[MONEY].sum(min_count=1), "subsidiary: kept the row without a subsidiary (total)"
    pieces = rows.drop_duplicates(["subsidiary"] + MONEY)
    return pieces[MONEY].sum(min_count=1), "subsidiary: added the pieces held by each subsidiary"


def coalesce(canon: pd.DataFrame) -> pd.DataFrame:
    """One row per (adsh, ddate, identifier), with n_conflicts, conflict_fields
    and resolution columns. canon needs a 'subsidiary' column (may be all empty)."""
    h = holdings.coalesce_holdings(canon).set_index(holdings.KEY)
    rows = canon[canon["identifier"].notna()]

    fields = [f for f in ["fair_value", "cost", "principal", "interest_rate", "spread",
                          "maturity", "pik_rate", "pct_net_assets",
                          "investment_type", "industry", "affiliation"] if f in rows]
    differs = rows.groupby(holdings.KEY, sort=False)[fields].nunique().gt(1)
    h["conflict_fields"] = differs.apply(lambda r: ";".join(r.index[r]), axis=1).reindex(h.index)
    h["resolution"] = ""
    h.loc[h["n_conflicts"] > 0, "resolution"] = "first value in SOI order (kit rule)"

    split = rows.groupby(holdings.KEY, sort=False).filter(
        lambda g: len(g) > 1 and g["subsidiary"].notna().any())
    fixes = []
    for key, g in split.groupby(holdings.KEY, sort=False):
        values, how = _resolve(g)
        fixes.append({**dict(zip(holdings.KEY, key)), **values.to_dict(), "resolution": how})
    if fixes:
        fx = pd.DataFrame(fixes).set_index(holdings.KEY)
        h = h.sort_index()
        fx = fx.sort_index()
        h.loc[fx.index, MONEY + ["resolution"]] = fx[MONEY + ["resolution"]]
    return h.reset_index()
