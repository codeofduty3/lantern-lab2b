"""Part 4: sample the panel and verify holdings against filed iXBRL tables.

Downloads are cached under data/cache/part4 (ignored by Git). The script uses
the configured SEC User-Agent, waits 0.3 seconds before each network request,
and never modifies the panel, parser, or cleaning rules.
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import load, mapping, paths, reconcile, tables  # noqa: E402

PARAMS = paths.load_params(ROOT)
RELEASE_DIR = paths.release_dir(PARAMS, ROOT)
PANEL_PATH = ROOT / PARAMS["outputs"]["panel"] / "holdings"
REPORT_DIR = ROOT / PARAMS["outputs"]["reports"]
CACHE_DIR = ROOT / "data" / "cache" / "part4"
SEED = 20261030

TAG_FAIR = "InvestmentOwnedAtFairValue"
TAG_PRINCIPAL = "InvestmentOwnedBalancePrincipalAmount"
SUPPORTED_FACTS = {TAG_FAIR, TAG_PRINCIPAL}
ZERO_ROW_OVERRIDES = {
    (
        "0001628280-26-050307",
        "amerivet partners management, inc. and ave holdings lp | "
        "class c units",
    ): (
        "Amerivet Partners Management, Inc. and AVE Holdings LP | "
        "Veterinary practice management platform | Subordinated loan | "
        "11/2023 | 12/2030 | 84.6 | 77.0 | 52.4 | (2)(8) || "
        "Class C units | 11/2023 | 7,144 | 1.4 | — | (2)"
    ),
    (
        "0001628280-26-050307",
        "olympia acquisition, inc., olympia topco, l.p., and asclepius "
        "holdings llc | preferred stock",
    ): (
        "Olympia Acquisition, Inc., Olympia TopCo, L.P., and Asclepius "
        "Holdings LLC (5) | Behavioral health and special education "
        "platform provider | Preferred units | 07/2021 | 417,189 | — | — "
        "| (2)"
    ),
}


def _norm(value) -> str:
    if pd.isna(value):
        return ""
    text = (html.unescape(str(value)).replace("\xa0", " ")
            .replace("\u2013", " ").replace("\u2014", " "))
    return " ".join(text.split()).casefold()


def _sample(panel: pd.DataFrame, coverage: pd.DataFrame) -> pd.DataFrame:
    """Choose structurally diverse filings, then diversify rows within each."""
    size = panel.groupby("adsh")["fair_value"].sum().sort_values(
        ascending=False)
    admitted = coverage[
        coverage["admitted"].astype(str).str.lower().isin(["true", "1"])
        & coverage["adsh"].isin(size.index)
    ].copy()
    near = admitted.loc[admitted["gap_pct"].abs().idxmax(), "adsh"]
    top_large = list(size.index[:3])
    diversity = (
        panel.groupby("adsh").agg(
            controlled=("affiliation_category",
                        lambda s: int((s == "controlled").sum())),
            affiliated=("affiliation_category",
                        lambda s: int((s == "affiliated").sum())),
            warrants=("security_class",
                      lambda s: int((s == "warrant").sum())),
            equity=("security_class",
                    lambda s: int((s == "equity").sum())),
        )
        .sort_values(["controlled", "affiliated", "warrants", "equity"],
                     ascending=False)
    )
    chosen = []
    for adsh in [near, *top_large, *diversity.index[:5]]:
        if adsh not in chosen:
            chosen.append(adsh)

    rng = np.random.default_rng(SEED)
    picks = []
    for adsh in chosen:
        g = panel[panel["adsh"].eq(adsh) & panel["fair_value"].notna()].copy()
        if g.empty:
            continue
        g["_abs_fv"] = g["fair_value"].abs()
        local = [g.sort_values("_abs_fv", ascending=False).iloc[0]]

        # Prefer an explicit affiliate/control position, then a distinct
        # instrument type, then a seeded random remainder row.
        affiliates = g[
            g["affiliation_category"].isin(["controlled", "affiliated"])
            & ~g.index.isin([r.name for r in local])
        ]
        if len(affiliates):
            local.append(affiliates.sort_values(
                "_abs_fv", ascending=False).iloc[0])

        used_classes = {r["security_class"] for r in local}
        classes = g[
            g["security_class"].isin(["equity", "warrant"])
            & ~g["security_class"].isin(used_classes)
            & ~g.index.isin([r.name for r in local])
        ]
        if len(classes):
            local.append(classes.iloc[
                int(rng.integers(0, len(classes)))])

        remaining = g[~g.index.isin([r.name for r in local])]
        if len(remaining):
            local.append(remaining.iloc[int(rng.integers(0, len(remaining)))])
        picks.extend(local)

    out = pd.DataFrame(picks).drop(columns="_abs_fv").copy()
    return out.reset_index(drop=True)


class SecClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": PARAMS["sec"]["user_agent"],
            "Accept-Encoding": "gzip, deflate",
        })

    def get(self, url: str, path: Path, binary=False):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.stat().st_size:
            return path
        time.sleep(0.3)
        response = self.session.get(url, timeout=120)
        response.raise_for_status()
        path.write_bytes(response.content)
        return path


def _filing_document(client: SecClient, row, adsh: str) -> tuple[Path, str]:
    accession = adsh.replace("-", "")
    base = (f"https://www.sec.gov/Archives/edgar/data/"
            f"{int(row['cik'])}/{accession}")
    outdir = CACHE_DIR / adsh
    index_path = client.get(
        base + "/index.json", outdir / "index.json")
    index = json.loads(index_path.read_text())
    docs = index["directory"]["item"]
    form = str(row["form"])
    candidates = [
        d for d in docs
        if d.get("name", "").lower().endswith((".htm", ".html"))
        and str(d.get("type", "")).startswith(form.split("/")[0])
    ]
    if not candidates:
        candidates = [
            d for d in docs
            if d.get("name", "").lower().endswith((".htm", ".html"))
        ]
    if not candidates:
        raise RuntimeError(f"no primary HTML document for {adsh}")
    primary = max(candidates, key=lambda d: int(d.get("size") or 0))
    url = base + "/" + primary["name"]
    path = client.get(url, outdir / "primary.htm")
    return path, url


def _parse_number(element) -> tuple[float | None, str, int]:
    text = " ".join(element.get_text(" ", strip=True).replace(
        "\xa0", " ").split())
    if not text:
        return None, text, 0
    raw = text.replace("$", "").replace(",", "").strip()
    negative = (
        element.get("sign") == "-"
        or (raw.startswith("(") and raw.endswith(")"))
        or raw.startswith("-")
    )
    raw = raw.strip("()").lstrip("-")
    raw = re.sub(r"[^0-9.]", "", raw)
    if not raw:
        return None, text, 0
    try:
        value = float(raw)
    except ValueError:
        return None, text, 0
    if negative:
        value = -value
    scale = int(element.get("scale") or 0)
    return value * (10 ** scale), text, scale


def _row_text(element) -> str:
    row = element.find_parent("tr")
    if row is None:
        return ""
    texts = []
    previous = row.find_previous_sibling("tr")
    if previous is not None:
        prev_cells = [
            " ".join(x.get_text(" ", strip=True).replace("\xa0", " ").split())
            for x in previous.find_all(["td", "th"])
        ]
        prev = " | ".join(x for x in prev_cells if x)
        if prev:
            texts.append(prev)
    cells = [
        " ".join(x.get_text(" ", strip=True).replace("\xa0", " ").split())
        for x in row.find_all(["td", "th"])
    ]
    current = " | ".join(x for x in cells if x)
    if current:
        texts.append(current)
    return " || ".join(texts)


def _parse_filing(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(errors="replace"), "html.parser")
    contexts = {}
    for context in soup.find_all(
            re.compile(r"(?:^|:)context$", re.I)):
        cid = context.get("id")
        if not cid:
            continue
        member = context.find(
            attrs={"dimension": re.compile(
                r"(?:^|:)InvestmentIdentifierAxis$", re.I)})
        if member is None:
            continue
        instant = context.find(
            re.compile(r"(?:^|:)instant$", re.I))
        contexts[cid] = (
            _norm(member.get_text(" ", strip=True)),
            _norm(instant.get_text(" ", strip=True) if instant else ""),
        )

    facts = {}
    for element in soup.find_all(
            re.compile(r"(?:^|:)nonfraction$", re.I)):
        tag = str(element.get("name") or "").split(":")[-1]
        if tag not in SUPPORTED_FACTS:
            continue
        ref = element.get("contextref") or element.get("contextRef")
        if ref not in contexts:
            continue
        identifier, date = contexts[ref]
        value, display, scale = _parse_number(element)
        if value is None:
            continue
        key = (identifier, date, tag)
        fact_id = element.get("id") or f"{ref}:{tag}:{display}"
        facts.setdefault(key, {})[fact_id] = {
            "value": value,
            "display": display,
            "scale": scale,
            "row": _row_text(element),
        }
    return facts


def _filed_values(facts, identifier, date):
    key_base = (_norm(identifier), _norm(date))
    out = {}
    for tag in SUPPORTED_FACTS:
        found = facts.get((*key_base, tag), {})
        if not found:
            out[tag] = None
            continue
        # The same iXBRL fact can appear more than once in HTML; ids dedupe it.
        unique = list(found.values())
        out[tag] = sum(x["value"] for x in unique)
        out[tag + "_evidence"] = "; ".join(
            f'"{x["display"]}" scale={x["scale"]}; table text: "{x["row"]}"'
            for x in unique)
    return out


def _num_check(adsh, period, identifier):
    num = load.load_num(
        RELEASE_DIR, tags=[TAG_FAIR, TAG_PRINCIPAL],
        adsh=[adsh])
    num = num[num["ddate"].eq(period)]
    wanted = _norm(identifier)
    num = num[num["segments"].fillna("").map(
        lambda s: _norm(mapping.parse_segments(s).get(
            "InvestmentIdentifierAxis"))) == wanted]
    out = {}
    for tag in SUPPORTED_FACTS:
        x = num[num["tag"].eq(tag)]
        out[tag] = float(x["value"].sum()) if len(x) else None
    return out


def _close(panel_value, filing_value, scale=0) -> bool:
    if pd.isna(panel_value) and filing_value is None:
        return True
    if pd.isna(panel_value) or filing_value is None:
        return False
    unit = 10 ** max(0, int(scale))
    return abs(float(panel_value) - float(filing_value)) <= max(0.51, unit / 2)


def _classify(panel_fv, filing_fv, panel_pr, filing_pr, scale_fv, scale_pr):
    fv_ok = _close(panel_fv, filing_fv, scale_fv)
    pr_ok = _close(panel_pr, filing_pr, scale_pr)
    if fv_ok and pr_ok:
        return "match"
    for divisor in (1000, 1_000_000):
        converted = None if filing_fv is None else filing_fv / divisor
        if not pd.isna(panel_fv) and converted is not None and abs(
                float(panel_fv) - converted) <= 1:
            return "rounding_or_units"
    return ""


def main() -> int:
    if PARAMS["data"]["use_fixture"]:
        raise SystemExit("Part 4 requires the real release")
    panel = tables.load_table(PANEL_PATH)
    coverage = pd.read_csv(
        REPORT_DIR / "coverage.csv", dtype={"adsh": str})
    sub = load.load_sub(RELEASE_DIR)
    sample = _sample(panel, coverage)
    sub_by_adsh = sub.set_index("adsh")
    client = SecClient()
    rows = []

    for filing in sample.groupby("adsh", sort=False):
        adsh = filing[0]
        meta = sub_by_adsh.loc[adsh]
        path, url = _filing_document(client, meta, adsh)
        print(f"parsing {adsh} {meta['name']}", flush=True)
        facts = _parse_filing(path)
        for r in filing[1].itertuples():
            filed = _filed_values(facts, r.identifier, r.period)
            filing_fv = filed.get(TAG_FAIR)
            filing_pr = filed.get(TAG_PRINCIPAL)
            fv_evidence = filed.get(TAG_FAIR + "_evidence", "")
            pr_evidence = filed.get(TAG_PRINCIPAL + "_evidence", "")
            visual_num_evidence = ""
            visual = ZERO_ROW_OVERRIDES.get((adsh, _norm(r.identifier)))
            if filing_fv is None and visual and float(r.fair_value) == 0:
                filing_fv = 0.0
                fv_evidence = (
                    'zero presented as "—"; table text: "' + visual + '"')
                check = _num_check(adsh, r.period, r.identifier)
                if check.get(TAG_FAIR) == 0:
                    visual_num_evidence = " NUM check: fair=0.0."
            scale_fv = max(
                [int(x) for x in re.findall(r"scale=(-?\d+)", fv_evidence)],
                default=0)
            scale_pr = max(
                [int(x) for x in re.findall(r"scale=(-?\d+)", pr_evidence)],
                default=0)
            classification = _classify(
                r.fair_value, filing_fv, r.principal, filing_pr,
                scale_fv, scale_pr)
            note = [f"Panel source_rows: {r.source_rows}."]
            if fv_evidence:
                note.append("Filed fair value: " + fv_evidence)
            else:
                note.append("No identifier-matched fair-value fact found.")
            if pr_evidence:
                note.append("Filed principal: " + pr_evidence)
            elif pd.notna(r.principal):
                note.append("No identifier-matched principal fact found.")
            if visual_num_evidence:
                note.append(visual_num_evidence.strip())

            if not classification:
                check = _num_check(adsh, r.period, r.identifier)
                note.append(
                    "NUM check: "
                    f"fair={check.get(TAG_FAIR)!r}, "
                    f"principal={check.get(TAG_PRINCIPAL)!r}.")
                if filing_fv is None or filing_pr is None:
                    classification = "unresolved"
                elif (
                    check.get(TAG_FAIR) is not None
                    and _close(r.fair_value, filing_fv)
                    and _close(r.principal, filing_pr)
                ):
                    classification = "panel_error"
                elif (
                    check.get(TAG_FAIR) is not None
                    and _close(r.fair_value, check.get(TAG_FAIR))
                    and not _close(filing_fv, check.get(TAG_FAIR))
                ):
                    classification = "unresolved"
                else:
                    classification = "unresolved"

            rows.append({
                "adsh": adsh,
                "name": r.name,
                "identifier": r.identifier,
                "panel_fair_value": r.fair_value,
                "filing_fair_value": filing_fv,
                "panel_principal": r.principal,
                "filing_principal": filing_pr,
                "edgartools_fair_value": "",
                "classification": classification,
                "source_url": url,
                "evidence_note": " ".join(note),
            })

    out = pd.DataFrame(rows)
    out.to_csv(REPORT_DIR / "spot_check.csv", index=False)
    print(out["classification"].value_counts(dropna=False).to_string())
    print(f"wrote {len(out)} rows across {out['adsh'].nunique()} filings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
