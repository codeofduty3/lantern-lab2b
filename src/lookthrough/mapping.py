"""Map SOI columns to canonical fields by XBRL tag, not by label."""
import re

import pandas as pd

# canonical field -> standard us-gaap tag
CANONICAL = {
    "fair_value": "InvestmentOwnedAtFairValue",
    "cost": "InvestmentOwnedAtCost",
    "principal": "InvestmentOwnedBalancePrincipalAmount",
    "interest_rate": "InvestmentInterestRate",
    "spread": "InvestmentBasisSpreadVariableRate",
    "maturity": "InvestmentMaturityDate",
    "pik_rate": "InvestmentInterestRatePaidInKind",
    "pct_net_assets": "InvestmentOwnedPercentOfNetAssets",
}
# labels the SEC readme presets (fallback if TAG lacks a label)
PRESET = {
    "fair_value": "Investment Owned, Fair Value",
    "cost": "Investment Owned, Cost",
    "principal": "Investment Owned, Balance, Principal Amount",
    "interest_rate": "Investment Interest Rate",
    "spread": "Investment, Basis Spread, Variable Rate",
    "maturity": "Investment Maturity Date",
    "pik_rate": "Investment, Interest Rate, Paid in Kind",
    "pct_net_assets": "Investment Owned, Net Assets, Percentage",
}
AXES = {"identifier": "Investment, Identifier Axis",
        "investment_type": "Investment Type Axis",
        "industry": "Industry Sector Axis",
        "affiliation": "Investment, Issuer Affiliation Axis"}
# Used only when a filing has no standard identifier-axis rows at all.
# These are dimension labels that directly name the investee.
FALLBACK_IDENTIFIER_AXES = [
    "Legal Entity Axis",
    "Investment, Issuer Name Axis",
    "Investment, Name Axis",
    "Investee",
]
# Additional columns needed for Part 2 transformations and tests.
CLEANING = {
    "shares": "InvestmentOwnedBalanceShares",
    "unfunded_commitment":
        "InvestmentCompanyFinancialCommitmentToInvesteeFutureAmount",
}
CLEANING_PRESET = {
    "shares": "Investment shares",
    "unfunded_commitment":
        "Investment Company, Financial Support to Investee Contractually "
        "Required, Not Provided, Amount",
}
META = ["soi_row", "adsh", "cik", "name", "form", "period",
        "ddate", "cstm", "inlineurl"]
NUMERIC = ["fair_value", "cost", "principal", "interest_rate",
           "spread", "pik_rate", "pct_net_assets", "shares",
           "unfunded_commitment"]


def map_soi_columns(soi_columns, tag: pd.DataFrame) -> dict:
    """canonical field -> SOI columns labelling that field's tag."""
    std = tag[(tag["custom"] == "0")
              & tag["tag"].isin(CANONICAL.values())]
    labels = {}
    for r in std.itertuples():
        if isinstance(r.tlabel, str):
            labels.setdefault(r.tag, set()).add(r.tlabel)
    colmap = {}
    for field, t in CANONICAL.items():
        wanted = labels.get(t, set()) | {PRESET[field]}
        cols = [c for c in soi_columns if c in wanted]
        if cols:
            colmap[field] = cols
    return colmap


def map_cleaning_columns(soi_columns, tag: pd.DataFrame) -> dict:
    """canonical cleaning field -> SOI columns, mapped by standard XBRL tag."""
    std = tag[(tag["custom"] == "0")
              & tag["tag"].isin(CLEANING.values())]
    labels = {}
    for r in std.itertuples():
        if isinstance(r.tlabel, str):
            labels.setdefault(r.tag, set()).add(r.tlabel)
    out = {}
    for field, t in CLEANING.items():
        wanted = labels.get(t, set()) | {CLEANING_PRESET[field]}
        cols = [c for c in soi_columns if c in wanted]
        if cols:
            out[field] = cols
    return out


def soi_usecols(header, colmap: dict) -> list:
    """Metadata, axes and mapped value columns present in SOI."""
    want = set(META) | set(AXES.values())
    want |= {c for cols in colmap.values() for c in cols}
    want |= set(FALLBACK_IDENTIFIER_AXES)
    want |= set(CLEANING_PRESET.values())
    return [c for c in header if c in want]


def to_canonical(soi: pd.DataFrame, colmap: dict) -> pd.DataFrame:
    """Metadata, axes and fields; coalesce columns sharing a tag."""
    out = soi[[c for c in META if c in soi.columns]].copy()
    for field, col in AXES.items():
        out[field] = soi[col] if col in soi.columns else pd.NA
    out["identifier_fallback"] = pd.Series(pd.NA, index=soi.index,
                                           dtype="object")
    for col in FALLBACK_IDENTIFIER_AXES:
        if col in soi:
            out["identifier_fallback"] = out["identifier_fallback"].where(
                out["identifier_fallback"].notna(), soi[col])
    out["identifier_source"] = pd.Series(pd.NA, index=soi.index,
                                         dtype="object")
    out.loc[out["identifier"].notna(), "identifier_source"] = AXES["identifier"]
    # The tag table is not passed here; use the release-preset labels and
    # retain any other label supplied by a caller.
    for field, label in CLEANING_PRESET.items():
        cols = [c for c in soi.columns if c == label]
        cols += [c for c in colmap.get(field, []) if c in soi.columns]
        s = pd.Series(pd.NA, index=soi.index, dtype="object")
        for c in dict.fromkeys(cols):
            s = s.where(s.notna(), soi[c])
        out[field] = s
    for field in CANONICAL:
        s = pd.Series(pd.NA, index=soi.index, dtype="object")
        for c in colmap.get(field, []):
            s = s.where(s.notna(), soi[c])
        out[field] = s
    for field in NUMERIC:
        out[field] = pd.to_numeric(out[field], errors="coerce")
    return out


SEG_SPLIT = re.compile(r";(?=[A-Za-z][A-Za-z0-9_]*\([^)]*\)=)")
SEG_PART = re.compile(r"([A-Za-z][A-Za-z0-9_]*)\(([^)]*)\)=(.*)$")
MEMBER = re.compile(r"^(.*)\(([^()]*)\)$")


def parse_segments(s) -> dict:
    """'A(v)=M(v);B(v)=text()' -> {'A': 'M', 'B': 'text'}"""
    if not isinstance(s, str) or not s.strip():
        return {}
    out = {}
    for part in SEG_SPLIT.split(s.strip().rstrip(";")):
        m = SEG_PART.match(part)
        if not m:
            continue
        axis, _version, rest = m.groups()
        mm = MEMBER.match(rest)
        out[axis] = (mm.group(1) if mm else rest).strip()
    return out
