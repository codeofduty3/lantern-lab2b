"""Combine the SEC's monthly BDC releases into one quarterly release folder.

Team 3's release is 2026q3, which the SEC publishes as three monthly ZIPs
(2026_07, 2026_08, 2026_09). Every other helper in lookthrough, and the
self-check, reads ONE release folder. build_quarter writes that folder,
data/raw/<release>_bdc/, in the same layout as a monthly release:

    soi.tsv                 rows of all months; columns = union of the months' columns,
                            plus source_release and source_soi_row (provenance back
                            to the row in the monthly file)
    datasets/sub.tsv        filings of all months, plus source_release
    datasets/tag.tsv        tags of all months, duplicates removed
    datasets/num.tsv        facts of all months (streamed: num.tsv is over 1 GB)
"""
from pathlib import Path

import pandas as pd

READ = dict(sep="\t", dtype=str, keep_default_na=False, na_values=[""], low_memory=False)
WRITE = dict(sep="\t", index=False, na_rep="")


def _month_dir(raw_dir, month) -> Path:
    return Path(raw_dir) / f"{month}_bdc"


def _concat_text(paths, out_path):
    """Stack TSV files that share one header, without loading them into memory."""
    header = None
    with open(out_path, "w", encoding="utf-8", newline="") as out:
        for p in paths:
            with open(p, encoding="utf-8", newline="") as fh:
                h = fh.readline()
                if header is None:
                    header = h
                    out.write(h)
                elif h != header:
                    raise ValueError(f"{p} has a different header from {paths[0]}")
                for line in fh:
                    out.write(line)


def build_quarter(raw_dir, months, release) -> dict:
    """Write raw_dir/<release>_bdc from the monthly folders; return a summary."""
    raw_dir = Path(raw_dir)
    target = raw_dir / f"{release}_bdc"
    (target / "datasets").mkdir(parents=True, exist_ok=True)
    dirs = [_month_dir(raw_dir, m) for m in months]

    # SUB: one row per filing; no filing appears in two months (checked below)
    sub = pd.concat([pd.read_csv(d / "datasets" / "sub.tsv", **READ).assign(source_release=m)
                     for m, d in zip(months, dirs)], ignore_index=True)
    dup = sub["adsh"].duplicated(keep=False)
    if dup.any():
        raise ValueError(f"filings in more than one month: {sorted(sub.loc[dup, 'adsh'].unique())[:5]}")
    sub.to_csv(target / "datasets" / "sub.tsv", **WRITE)

    # TAG: the same tag can be defined in several months
    tag = pd.concat([pd.read_csv(d / "datasets" / "tag.tsv", **READ) for d in dirs],
                    ignore_index=True).drop_duplicates(["tag", "version"])
    tag.to_csv(target / "datasets" / "tag.tsv", **WRITE)

    # NUM: same columns every month; stream it
    _concat_text([d / "datasets" / "num.tsv" for d in dirs], target / "datasets" / "num.tsv")

    # SOI: each month has its own column set, so align on the union of columns
    sois, order = [], []
    for m, d in zip(months, dirs):
        s = pd.read_csv(d / "soi.tsv", **READ)
        s["source_release"] = m
        s["source_soi_row"] = range(len(s))
        order += [c for c in s.columns if c not in order]
        sois.append(s)
    soi = pd.concat([s.reindex(columns=order) for s in sois], ignore_index=True)
    soi.to_csv(target / "soi.tsv", **WRITE)

    for extra in ("readme.htm", "bdc_metadata.json"):
        src = dirs[-1] / extra
        if src.exists():
            (target / extra).write_bytes(src.read_bytes())

    return {"release": release, "months": list(months), "filings": len(sub),
            "soi_rows": len(soi), "soi_columns": len(order) - 2,
            "filings_by_month": sub["source_release"].value_counts().reindex(months).tolist()}
