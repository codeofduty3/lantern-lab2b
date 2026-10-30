"""Load generated LANTERN JSON files without analytical data libraries."""

from __future__ import annotations

import gzip
import json
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
BUNDLE_PATH = Path(__file__).resolve().parent / "serve_data.json.gz"


@lru_cache(maxsize=1)
def _bundle() -> dict | None:
    if not BUNDLE_PATH.exists():
        return None
    return json.loads(gzip.decompress(BUNDLE_PATH.read_bytes()).decode("utf-8"))


def _read(name: str):
    path = DATA_DIR / name
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    key = name.removesuffix(".json")
    bundle = _bundle()
    if bundle is not None and key in bundle:
        return bundle[key]
    raise FileNotFoundError(
        f"Missing {path}. Run `python scripts/export_app_data.py` first."
    )


@lru_cache(maxsize=1)
def coverage() -> dict:
    return _read("coverage.json")


@lru_cache(maxsize=1)
def filings_document() -> dict:
    return _read("filings.json")


@lru_cache(maxsize=1)
def triage_document() -> dict:
    return _read("triage.json")


@lru_cache(maxsize=1)
def cleaning_rules_document() -> dict:
    return _read("cleaning_rules.json")


@lru_cache(maxsize=256)
def holdings_document(adsh: str) -> dict | None:
    path = DATA_DIR / "holdings" / f"{adsh}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    bundle = _bundle()
    if bundle is None:
        return None
    return bundle.get("holdings", {}).get(adsh)


def filing(adsh: str) -> dict | None:
    return next(
        (
            item
            for item in filings_document()["filings"]
            if item["adsh"] == adsh
        ),
        None,
    )
