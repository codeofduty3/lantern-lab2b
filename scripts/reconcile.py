"""Stage 4 (reconcile): compare cleaned holdings with each filed total.

The admission threshold comes from `reconcile.tolerance` in params.yaml.
Every current filing with SOI rows is retained in the reconciliation table,
including filings with no identifiable holdings.

Writes intermediate admission evidence consumed by the report stage.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lookthrough import clean, holdings, load, mapping, paths, reconcile, tables  # noqa: E402

P = paths.load_params(ROOT)
rdir = paths.release_dir(P, ROOT)
tol = float(P["reconcile"]["tolerance"])

sub, tag = load.load_sub(rdir), load.load_tag(rdir)
header = load.soi_header(rdir)
colmap = mapping.map_soi_columns(header, tag)
soi = load.load_soi(rdir, mapping.soi_usecols(header, colmap))
soi = soi[soi["adsh"].isin(sub["adsh"])]
attempted = set(soi["adsh"])
num = load.load_num(rdir, tags=[reconcile.FV_TAG], custom_fv=True)
canon = holdings.split_periods(mapping.to_canonical(soi, colmap), sub)
canon = clean.recover_axis_identifiers(canon)
kept = tables.load_table(ROOT / "outputs" / "cleaned" / "holdings")

filed = reconcile.filed_totals(num, sub)
rec = reconcile.reconcile(kept, filed, sub, tol, soi_adsh=attempted)
no_soi = sub.loc[
    ~sub["adsh"].isin(soi["adsh"]),
    ["adsh", "cik", "name", "form", "period"],
].copy()
diag = reconcile.diagnose(rec, kept, num, canon)

outdir = ROOT / "outputs" / "reconciled"
paths_written = [
    tables.save_table(kept, outdir / "holdings"),
    tables.save_table(rec, outdir / "rec"),
    tables.save_table(diag, outdir / "diag"),
    tables.save_table(no_soi, outdir / "no_soi"),
]
cov = reconcile.coverage(rec)
print(f"Release {rdir.name}: {len(sub)} SUB filings; "
      f"{cov['filings_attempted']} attempted; {len(no_soi)} without SOI rows")
print(f"Admitted {cov['filings_admitted']} filings "
      f"({cov['share_of_filings']:.1%}); "
      f"${cov['filed_fv_admitted']:,.0f} filed fair value admitted "
      f"({cov['share_of_dollars']:.1%}); tolerance {tol:.2%}")
for path in paths_written:
    print(f"Wrote {path.relative_to(ROOT)}")
