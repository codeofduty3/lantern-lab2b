"""Write or verify the deterministic content fingerprint of the final panel.

Usage:
  python scripts/check_panel_fingerprint.py --write
  python scripts/check_panel_fingerprint.py --check
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import paths, tables  # noqa: E402


def fingerprint(path: Path) -> dict:
    panel = tables.load_table(path)
    keys = "\n".join(sorted(
        f"{adsh}|{source_rows}"
        for adsh, source_rows in zip(panel["adsh"], panel["source_rows"])
    ))
    return {
        "rows": int(len(panel)),
        "filings": int(panel["adsh"].nunique()),
        "total_fair_value": float(panel["fair_value"].sum()),
        "adsh_source_rows_sha256": hashlib.sha256(
            keys.encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    P = paths.load_params(ROOT)
    panel_path = ROOT / P["outputs"]["panel"] / "holdings"
    expected_path = ROOT / P["outputs"]["reports"] / "panel_fingerprint.json"
    actual = fingerprint(panel_path)
    if args.write:
        expected_path.write_text(json.dumps(actual, indent=2) + "\n")
        print(json.dumps(actual, indent=2))
        return 0

    expected = json.loads(expected_path.read_text())
    if actual != expected:
        print("Panel fingerprint mismatch")
        print("expected:", json.dumps(expected, sort_keys=True))
        print("actual:  ", json.dumps(actual, sort_keys=True))
        return 1
    print("Panel fingerprint matches:", json.dumps(actual, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
