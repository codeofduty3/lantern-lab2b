"""Stage 5 (report): write the final panel and human-readable reports."""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import paths, reconcile, report, tables  # noqa: E402

P = paths.load_params(ROOT)
kept = tables.load_table(ROOT / "outputs" / "cleaned" / "holdings")
rec = tables.load_table(ROOT / "outputs" / "reconciled" / "rec")
diag = tables.load_table(ROOT / "outputs" / "reconciled" / "diag")
no_soi = tables.load_table(ROOT / "outputs" / "reconciled" / "no_soi")
log = pd.read_csv(
    ROOT / P["outputs"]["reports"] / "cleaning_log.csv", dtype=str)
triage = pd.read_csv(ROOT / "docs" / "triage_notes.csv", dtype=str)

bad = sorted(set(triage["triage_category"]) - set(reconcile.TRIAGE))
if bad:
    sys.exit(f"docs/triage_notes.csv has categories outside Section 7: {bad}")

out = report.write_outputs(
    kept, rec, diag, log, ROOT, P, triage=triage, no_soi=no_soi,
    write_cleaning_log=False)
cov = reconcile.coverage(rec)
excluded = set(rec.loc[~rec["admitted"], "adsh"])
untriaged = sorted(excluded - set(triage["adsh"]))
stale = sorted(set(triage["adsh"]) - excluded)

print(f"Admitted {cov['filings_admitted']} of {cov['filings_attempted']} "
      f"filings ({cov['share_of_filings']:.1%}), "
      f"${cov['filed_fv_admitted']:,.0f} of "
      f"${cov['filed_fv_attempted']:,.0f} filed fair value "
      f"({cov['share_of_dollars']:.1%})")
if untriaged:
    print(f"WARNING: {len(untriaged)} excluded filings have no triage note; "
          f"e.g. {untriaged[:3]}")
if stale:
    print(f"Note: {len(stale)} triage notes refer to admitted filings; "
          f"e.g. {stale[:3]}")
for key, value in out.items():
    print(f"Wrote {Path(value).relative_to(ROOT)}")
print("Wrote reports/coverage.json")
