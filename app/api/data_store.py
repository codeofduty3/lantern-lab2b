"""Load generated LANTERN JSON files without analytical data libraries."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _read(name: str):
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run `python scripts/export_app_data.py` first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


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
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def filing(adsh: str) -> dict | None:
    return next(
        (
            item
            for item in filings_document()["filings"]
            if item["adsh"] == adsh
        ),
        None,
    )
