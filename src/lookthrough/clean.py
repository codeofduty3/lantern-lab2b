"""Structural cleaning rules and transformations for the BDC schedule.

Each rule returns ``(drop_mask, one_line_artifact)``. Coverage values in the
log are calculated only after the rule has been chosen; they never influence a
pattern or the rule order.
"""
import re

import numpy as np
import pandas as pd

from .mapping import parse_segments

# Generic labels are consumed by a following investment noun. This deliberately
# does not match real borrowers such as "Total Access Elevator, LLC" or
# "Total Expert Inc.".
TOTAL = (
    r"^\s*subtotal\b|^\s*sub\s+total\b"
    r"|^\s*total(?:\s+(?:of\b|investments?\b|cash\b|controlled\b"
    r"|non[- ]control\b|portfolio\b|debt\b|equity\b|preferred\b|unfunded\b)"
    r"|(?=\s*[|:])|$)|\btotal\s+investments\b|,\s+total\s+"
)
CATEGORY_TOTAL = (
    r"^(?:net assets|affiliated investments|control investments"
    r"|controlled investments|co-investment"
    r"|investments at fair value(?:\s+\[member\])?)$"
)
CASH = r"cash and cash equivalents|money market"
DEBT = (r"loan|lien|unitranche|note|bond|revolv|delayed draw"
        r"|subordinat|debt")
EQUITY = (
    r"common (?:stock|equity|units|shares)|preferred|membership"
    r"|equity interest|partnership interest|class [a-z0-9-]+ (?:units|stock)"
    r"|warrant"
)
MONEY_MARKET_FV_TAGS = {
    "MoneyMarketFundsFairValueDisclosure",
    "MoneyMarketFundsAtFairValue",
}


def _matches(h: pd.DataFrame, pattern: str) -> pd.Series:
    return h["identifier"].fillna("").str.contains(
        pattern, case=False, regex=True, na=False)


def rule_totals(h: pd.DataFrame):
    """Drop total/subtotal labels and category-only non-holding labels."""
    labels = h["identifier"].fillna("").str.strip()
    drop = (_matches(h, TOTAL)
            | labels.str.contains(CATEGORY_TOTAL, case=False,
                                  regex=True, na=False))
    return drop, "identifier is a total/subtotal or category-only label"


def _name_key(value) -> str:
    """Normalize an issuer label for within-filing duplicate detection."""
    text = str(value).lower().replace("[member]", " ")
    text = re.sub(
        r"^(?:affiliated investments?|controlled investments?"
        r"|non[ -]controlled(?:/non[ -]affiliated)? investments?"
        r"|investments?[ -]non[ -]controlled/non[ -]affiliated)"
        r"\s*[-:|]?\s*",
        "", text,
    )
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def rule_issuer_aggregates(h: pd.DataFrame):
    """Drop short issuer/control summaries that coexist with details.

    Candidates have no cost or principal and no instrument delimiter.
    A second identifier in the same filing must contain the complete candidate
    issuer and add instrument detail. This captures issuer totals and
    affiliated/control-table restatements without relying on the filed total.
    """
    drop = pd.Series(False, index=h.index)
    text = h["identifier"].fillna("")
    candidates = (
        h["cost"].isna()
        & h["principal"].isna()
        & h["fair_value"].notna()
        & ~text.str.contains("|", regex=False)
    )
    if not candidates.any():
        return drop, "short issuer summary duplicates a detailed row"

    work = h.loc[candidates, ["adsh", "identifier"]].copy()
    work["_key"] = work["identifier"].map(_name_key)
    for adsh, rows in work.groupby("adsh", sort=False):
        filing = h[h["adsh"] == adsh]
        names = filing["identifier"].fillna("").map(_name_key)
        detail = (
            filing["identifier"].fillna("").str.contains("|", regex=False)
            | filing["identifier"].fillna("").str.contains(r"\(", regex=True)
            | filing["cost"].notna()
            | filing["principal"].notna()
        )
        for idx, r in rows.iterrows():
            key = r["_key"]
            if len(key) < 8:
                continue
            pattern = rf"(?:^| ){re.escape(key)}(?: |$)"
            matches = names.str.contains(pattern, regex=True, na=False)
            more_detail = names.str.len().gt(len(key)) & detail
            if bool((matches & more_detail).any()):
                drop.at[idx] = True
    return drop, "short issuer summary duplicates a detailed row"


def rule_cash(h: pd.DataFrame):
    """Drop cash and money-market identifiers from the holdings panel."""
    return _matches(h, CASH), "cash or money-market line in schedule"


def recover_axis_identifiers(canon: pd.DataFrame) -> pd.DataFrame:
    """Recover an identifier from a fallback axis for otherwise ID-less filings.

    Recovery is deliberately limited to filings with no current-period standard
    identifier. Filings that already use the standard axis can contain
    supplementary issuer-name aggregates; applying a fallback there would
    duplicate holdings.
    """
    out = canon.copy()
    if "identifier_fallback" not in out:
        return out
    cur = out["is_current"].fillna(False) if "is_current" in out else pd.Series(
        True, index=out.index)
    missing_filings = set(
        out.loc[cur].groupby("adsh")["identifier"]
        .apply(lambda s: s.isna().all()).loc[lambda s: s].index
    )
    mask = (
        cur
        & out["adsh"].isin(missing_filings)
        & out["identifier"].isna()
        & out["identifier_fallback"].notna()
    )
    if mask.any():
        fallback = (
            out.loc[mask, "identifier_fallback"]
            .astype("string")
            .str.replace(r"\s*\[Member\]\s*$", "", regex=True)
            .str.strip()
        )
        out.loc[mask, "identifier"] = fallback
        out.loc[mask, "identifier_source"] = "fallback axis"
    return out


def recover_custom_fair_values(h: pd.DataFrame, num: pd.DataFrame,
                               sub: pd.DataFrame) -> pd.DataFrame:
    """Fill fair value omitted from SOI when an identifier-dimensioned NUM
    money-market fact supplies it.

    This is a transformation: it changes fair value and labels each filled row
    through ``fair_value_source``.
    """
    out = h.copy()
    if "fair_value_source" not in out:
        out["fair_value_source"] = pd.NA
    has_soi = out["fair_value"].notna()
    out.loc[has_soi, "fair_value_source"] = "SOI InvestmentOwnedAtFairValue"

    periods = sub.set_index("adsh")["period"]
    facts = num[
        num["tag"].isin(MONEY_MARKET_FV_TAGS)
        & num["ddate"].eq(num["adsh"].map(periods))
    ].copy()
    if facts.empty:
        return out
    facts["identifier"] = facts["segments"].map(
        lambda s: parse_segments(s).get("InvestmentIdentifierAxis"))
    facts = facts[facts["identifier"].notna()]
    if facts.empty:
        return out
    facts = (facts.groupby(["adsh", "ddate", "identifier", "tag"],
                           as_index=False)["value"].max())
    facts["fact_identifier"] = (
        facts["identifier"].str.strip().str.casefold())
    out["fact_identifier"] = (
        out["identifier"].fillna("").str.strip().str.casefold())
    targets = out["fair_value"].isna()
    for r in facts.itertuples():
        m = (targets
             & out["adsh"].eq(r.adsh)
             & out["ddate"].eq(r.ddate)
             & out["fact_identifier"].eq(r.fact_identifier))
        if m.sum() == 1 and pd.notna(r.value):
            out.loc[m, "fair_value"] = float(r.value)
            out.loc[m, "fair_value_source"] = f"NUM {r.tag}"
            targets &= ~m
    return out.drop(columns="fact_identifier")


def add_cleaning_attributes(h: pd.DataFrame) -> pd.DataFrame:
    """Classify security/affiliation and flag unfunded commitments in place."""
    out = h.copy()
    text = out["identifier"].fillna("")
    lower = text.str.lower()
    principal = (out["principal"].notna() if "principal" in out
                 else pd.Series(False, index=out.index))
    shares = (out["shares"].notna() if "shares" in out
              else pd.Series(False, index=out.index))
    warrant = lower.str.contains(r"warrants?", regex=True, na=False)
    cash = lower.str.contains(CASH, regex=True, na=False)
    debt = principal | lower.str.contains(DEBT, regex=True, na=False)
    equity = (shares
              | lower.str.contains(EQUITY, regex=True, na=False))
    out["security_class"] = np.select(
        [warrant, cash, debt, equity],
        ["warrant", "cash", "debt", "equity"], default="other")

    controlled_text = lower.str.replace(
        r"non[- ]controlled", " ", regex=True)
    controlled = controlled_text.str.contains(
        r"\bcontrolled\b|\bcontrol investments\b", regex=True, na=False)
    nonaffiliate = lower.str.contains(
        r"non[- ]affiliated|non[- ]affiliate", regex=True, na=False)
    affiliated = lower.str.contains(r"\baffiliated\b|\baffiliate\b",
                                    regex=True, na=False)
    out["affiliation_category"] = np.select(
        [nonaffiliate, controlled, affiliated],
        ["non-affiliated", "controlled", "affiliated"], default="unspecified")

    amount = (out["unfunded_commitment"] if "unfunded_commitment" in out
              else pd.Series(pd.NA, index=out.index))
    as_text = amount.astype("string").str.lower()
    amount_flag = amount.notna() & ~as_text.isin(["0", "0.0", "0.00"])
    out["has_unfunded_commitment"] = (
        amount_flag
        | lower.str.contains(r"unfunded", regex=True, na=False)
    )
    return out


RULE_META = {
    "rule_totals": {
        "motivation": (
            "The filed identifier is a total/subtotal or a category-only "
            "label rather than an individual investment."),
    },
    "rule_issuer_aggregates": {
        "motivation": (
            "Within one filing, a short identifier with neither cost nor "
            "principal contains the same issuer key as a separately filed "
            "instrument-detail row."),
    },
    "rule_cash": {
        "motivation": (
            "The identifier explicitly names cash or a money-market fund, "
            "so it is a liquidity line rather than an investment holding."),
    },
}

BASELINE_RULES = [rule_totals, rule_cash]
CLEANING_RULES = [rule_totals, rule_issuer_aggregates, rule_cash]


def coverage_value(current, filed, sub, tolerance, soi_adsh):
    """Report dollar coverage for transparency; never used by a rule."""
    if filed is None or sub is None or tolerance is None:
        return pd.NA
    # Imported lazily to keep clean.py free of an import cycle.
    from . import reconcile
    rec = reconcile.reconcile(
        current, filed, sub, float(tolerance), soi_adsh=soi_adsh)
    return reconcile.coverage(rec)["share_of_dollars"]


def _example(frame: pd.DataFrame, drop: pd.Series) -> tuple:
    selected = frame.loc[drop]
    if selected.empty:
        return "", ""
    row = selected.iloc[0]
    source = str(row["source_rows"]).split(";")[0]
    return str(row["adsh"]), source


def transformation_entry(rule, artifact, motivation, current, affected,
                         coverage_before=pd.NA, coverage_after=pd.NA):
    """Create a cleaning-log row for a documented non-mask transformation."""
    affected = affected.reindex(current.index, fill_value=False).astype(bool)
    adsh, soi_row = _example(current, affected)
    return {
        "rule": rule,
        "artifact": artifact,
        "motivation": motivation,
        "example_adsh": adsh,
        "example_soi_row": soi_row,
        "rows_affected": int(affected.sum()),
        "coverage_before": coverage_before,
        "coverage_after": coverage_after,
    }


def apply_rules(h: pd.DataFrame, rules, filed=None, sub=None,
                tolerance=None, soi_adsh=None) -> tuple:
    """Apply rules in documented semantic order and return kept rows + log."""
    log, keep = [], pd.Series(True, index=h.index)
    for rule in rules:
        drop, why = rule(h)
        drop = drop.reindex(h.index, fill_value=False).astype(bool) & keep
        before = coverage_value(h[keep], filed, sub, tolerance, soi_adsh)
        after = coverage_value(h[keep & ~drop], filed, sub, tolerance,
                               soi_adsh)
        adsh, soi_row = _example(h, drop)
        meta = RULE_META.get(rule.__name__, {})
        log.append({
            "rule": rule.__name__,
            "artifact": why,
            "motivation": meta.get("motivation", why),
            "example_adsh": adsh,
            "example_soi_row": soi_row,
            "rows_affected": int(drop.sum()),
            "coverage_before": before,
            "coverage_after": after,
        })
        keep &= ~drop
    return h[keep].copy(), pd.DataFrame(log)


def is_debt(h: pd.DataFrame) -> pd.Series:
    text = (h["identifier"].fillna("") + " "
            + h["investment_type"].fillna(""))
    return (h["principal"].notna() | h["spread"].notna()
            | text.str.contains(DEBT, case=False))
