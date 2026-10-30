# Part 5 economics

## Cost per completed task

The measured task is one filing processed through the complete pipeline.
Forced full-rebuild run 1 took 132.26 seconds, or 0.747232 seconds per
attempted filing; at an assumed compute rate of **$0.10 per compute-hour**, the
cost is **$0.000020756 per filing**. Forced run 2 took 145.16 seconds, or
0.820113 seconds per attempted filing, costing **$0.000022781 per filing**.
The two-run average is **$0.000021769 per filing**. The $0.10/hour rate is an
assumption inherited from the notebook 08 example, not a quoted cloud price.
Model cost is **$0** because this pipeline calls no model or generative API.

## Latency

Measured wall-clock time for `dvc repro --force` from the existing raw release,
including re-unpacking/combining raw inputs and rebuilding every stage, was
**132.26 seconds** on run 1 and **145.16 seconds** on run 2. Average latency per
attempted filing was **0.747232 seconds** and **0.820113 seconds** respectively.
The two-run average was 138.71 seconds total and 0.783672 seconds per filing.
Measurements were taken on an Intel Core i9-9880H at 2.30 GHz with 64 GB RAM,
macOS 26.5.2 x86_64, Python 3.11.17.

## Human time replaced

The assumed analyst effort is **2.0 hours per BDC by hand**, based on the
notebook 08 example, with an assumed loaded analyst rate of **$120/hour**.
Across 177 attempted filings, the gross manual effort is 354 hours. After
subtracting the two-run average pipeline time of 0.0385 hours, the net saving is
**176.96 hours ($21,235.38)** at x0.5 of the assumption, **353.96 hours
($42,475.38)** at x1, and **707.96 hours ($84,955.38)** at x2.

## Quality

`reports/coverage.json` reports **88 of 177 attempted filings admitted
(49.7%)** and **$234,366,032,543 of $556,908,483,659 attempted filed fair value
admitted (42.1%)**. Five SUB filings had no SOI rows and are reported
separately. Part 4 verified **30 holdings across 9 admitted filings** against
human-readable filing tables; all 30 matched and no item was unresolved. That
sample covers admitted filings only. EdgarTools was not used because no pinned
version was installed or specified.

## Scale

There are **16 quarterly releases** from Q4 2022 through Q3 2026 inclusive.
Assuming every release has the same 177 filings and the same average runtime,
that is 2,832 filing tasks, requiring **0.6165 compute-hours** and costing
**$0.06165**. Using the measured run range gives 0.5878 to 0.6452 hours and
$0.05878 to $0.06452. This is a stated linear extrapolation from 2026q3; older
releases may differ in filing count, taxonomy, table structure, and file size.

## Build versus buy

The starter kit provided the SEC download/unpack helpers, DVC scaffolding, flat
SUB/TAG/NUM/SOI readers, tag-based column mapping, a first-pass reconciliation,
and the general rule/test harness, which saved substantial acquisition and
plumbing work. Open-source pandas, PyArrow, DVC, BeautifulSoup, and pytest
provided table processing, artifact versioning, HTML parsing, and mutation
testing. We still had to build the quarter-specific tag remapping, subsidiary
coalescing, structural cleaning rules, identifier recovery, custom-value
recovery, filing-table verification, triage evidence, and the clean/reconcile/
report stage boundaries needed for reproducible rebuilds.
