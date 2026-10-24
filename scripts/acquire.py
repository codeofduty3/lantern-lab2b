"""Stage 1 (acquire): download the release, unpack it, write data/manifest.json.

Run from the repo root:  python scripts/acquire.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import paths, acquire  # noqa: E402

P = paths.load_params(ROOT)
if P["data"]["use_fixture"]:
    sys.exit("params.yaml has use_fixture: true. Set it to false to acquire the real release.")

release = P["release"]
raw = ROOT / P["data"]["raw_dir"]
zip_path = raw / f"{release}_bdc.zip"
url = acquire.release_url(release, P["sec"]["base_url"])

if zip_path.exists():
    print(f"Already downloaded: {zip_path.relative_to(ROOT)}")
else:
    print(f"Downloading {url} ...")
    zip_path = acquire.download_release(release, raw, P["sec"]["user_agent"], P["sec"]["base_url"])