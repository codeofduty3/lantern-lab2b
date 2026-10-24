"""Stage 1 (acquire): download the team's monthly ZIPs, unpack them, write data/manifest.json.

Team 3's release is the quarter 2026q3, published by the SEC as three monthly ZIPs
(params.yaml: release_months). Each one is downloaded once, unpacked into
data/raw/<month>_bdc/, and recorded in the manifest with its URL, size, SHA-256 and date.

Run from the repo root:  python scripts/acquire.py
"""
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import paths, acquire  # noqa: E402

P = paths.load_params(ROOT)
if P["data"]["use_fixture"]:
    sys.exit("params.yaml has use_fixture: true. Set it to false to acquire the real release.")

months = P.get("release_months") or [P["release"]]
raw = ROOT / P["data"]["raw_dir"]
today = dt.date.today().isoformat()
rows = []

for month in months:
    zip_path = raw / f"{month}_bdc.zip"
    url = acquire.release_url(month, P["sec"]["base_url"])
    if zip_path.exists():
        print(f"{month}: already downloaded")
    else:
        print(f"{month}: downloading {url}")
        zip_path = acquire.download_release(month, raw, P["sec"]["user_agent"], P["sec"]["base_url"])
    print(f"{month}: unpacking (large files take a few minutes)")
    out = acquire.unzip_release(zip_path, raw, month)
    rows.append({
        "release": month,
        "path": str(zip_path.relative_to(ROOT)),
        "url": url,
        "bytes": zip_path.stat().st_size,
        "sha256": acquire.sha256_file(zip_path),
        "recorded": today,
    })
    print(f"{month}: unpacked into {out.relative_to(ROOT)}")

manifest = ROOT / "data" / "manifest.json"
manifest.write_text(json.dumps(rows, indent=2))
bad = acquire.verify_manifest(manifest, root=ROOT)

print()
for r in rows:
    print(f"{r['release']}  {r['bytes']:>12,} bytes  sha256 {r['sha256'][:16]}...")
print("Manifest verifies:", bad == [])
