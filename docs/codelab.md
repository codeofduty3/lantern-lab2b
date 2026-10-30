author: Project LANTERN
summary: Build a traceable BDC holdings panel from SEC data, test every cleaning rule, verify the result against EDGAR, and serve it through a separate static UI and API.
id: lantern-case-study-2b
categories: data-engineering,dvc,sec,fastapi
environments: Web
status: Published
feedback link: https://github.com/codeofduty3/lantern-lab2b/issues

# Project LANTERN: From SEC BDC Data to a Traceable Look-Through Panel

## Overview
Duration: 0:03:00

This codelab follows one quarterly SEC Business Development Company (BDC)
release from its monthly ZIP files to a reproducible holdings panel, an
evidence-based reconciliation report, a read-only API, and a browser UI.

By the end you will be able to:

* Explain how `SUB`, `TAG`, `NUM`, and `SOI` describe the same filing.
* Collapse multiple SOI facts into one investment while preserving source rows.
* Apply structural cleaning rules without tuning them to the filed total.
* Reconcile holdings to each fund's disclosed fair value.
* Test a sample against the human-readable filing on SEC EDGAR.
* Rebuild every output with DVC and consume it through a separate UI and API.

The release used here is `2026q3`, assembled from the SEC monthly files
`2026_07`, `2026_08`, and `2026_09`. The panel deliberately excludes cash and
money-market lines because they are not borrower investments.

## Part 0 — Acquire and verify the SEC release
Duration: 0:05:00

**Goal:** restore the three raw SEC files and prove that their hashes match the
committed manifest.

Install the project once:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Restore the DVC-tracked raw release:

```bash
dvc pull
```

Inspect the release configuration and manifest:

```bash
cat params.yaml
cat data/manifest.json
```

Expected configuration:

```text
release: 2026q3
release_months: 2026_07, 2026_08, 2026_09
use_fixture: false
```

The manifest records one SHA-256 per monthly ZIP. `scripts/acquire.py` downloads,
unpacks, verifies, and combines those files into `data/raw/2026q3_bdc/`.
Raw data belongs in DVC, not Git.

**What could go wrong:** a stale manifest or an interrupted download will fail
the hash check. Do not bypass that check; remove the bad DVC checkout and run
`dvc pull` again.

Positive
: A valid release has 182 SUB rows and 197,160 SOI rows before period filtering.

## Part 1 — Parse, map, and coalesce holdings
Duration: 0:07:00

**Goal:** turn long-form XBRL facts into one current-period holding per filing
and investment identifier.

Run the parse stage:

```bash
dvc repro parse
```

Inspect what the stage printed. The verified release has:

* 182 filings in `SUB`;
* 101,220 current SOI rows;
* 68,175 candidate holdings after coalescing;
* 9,599 candidates assembled from more than one SOI row.

Inspect one source row:

```bash
python - <<'PY'
import yaml
from src.lookthrough import load, mapping, paths

params = paths.load_params(".")
release_dir = paths.release_dir(params, ".")
header = load.soi_header(release_dir)
tags = load.load_tag(release_dir)
columns = mapping.map_soi_columns(header, tags)
soi = load.load_soi(release_dir, mapping.soi_usecols(header, columns))
print(soi[["adsh", "soi_row", "Investment, Identifier Axis",
           "Investment Owned, Fair Value"]].head().to_string())
PY
```

The important provenance rule is that `source_rows` retains every original SOI
row. A coalesced holding is still traceable to the machine evidence that created
it.

**What could go wrong:** summing every SOI date mixes comparative schedules into
the current period. `holdings.split_periods` compares each row date with the
filing period from `SUB`.

## Part 2 — Clean with structural rules
Duration: 0:08:00

**Goal:** remove totals, duplicated issuer summaries, and liquidity lines using
signals visible in the row itself.

Run:

```bash
dvc repro clean
```

Open `reports/cleaning_log.csv` and `docs/cleaning_log.md`.

The rules run in this order:

1. `rule_totals` removes explicit total, subtotal, and category-only labels.
2. `rule_issuer_aggregates` removes a short issuer row when a detailed
   instrument row for the same issuer also exists in that filing.
3. `rule_cash` removes explicit cash and money-market lines.

Coverage is calculated after each rule for reporting, but it never selects a
pattern or changes the rule order. In the verified release the reported dollar
coverage moves from 27.1% before the three structural rules to 28.8%, 40.0%,
and then 42.1% after cash exclusion.

Inspect the logged examples:

```bash
python - <<'PY'
import pandas as pd

log = pd.read_csv("reports/cleaning_log.csv")
print(log[["rule", "example_adsh", "example_soi_row",
           "rows_affected", "coverage_before", "coverage_after"]]
      .to_string(index=False))
PY
```

**What could go wrong:** a rule tuned to one fund's reconciliation gap will
break another filing. Each rule's motivation must make sense from the
identifier structure alone.

Negative
: Cash is excluded uniformly. A filer that includes cash in its filed total
will remain outside tolerance and must be triaged with evidence.

## Part 3 — Reconcile and report coverage
Duration: 0:07:00

**Goal:** compare every attempted filing with its own undimensioned
`InvestmentOwnedAtFairValue` fact and retain every exclusion.

Run the remaining stages:

```bash
dvc repro reconcile report
PYTHONPATH=src python -m lookthrough.check
```

Expected verified summary:

```text
88 of 177 attempted filings admitted (49.7%)
$234,366,032,543 of $556,908,483,659 filed fair value admitted (42.1%)
5 filings with no SOI rows reported separately
10/10 self-checks pass
```

Inspect the outputs:

* `outputs/panel/holdings.parquet` contains 33,222 investment holdings.
* `reports/coverage.csv` contains one row for every attempted filing.
* `reports/coverage.json` is the DVC metric used by the API.
* `reports/triage.md` explains every exclusion.

Every summary number must include both filing coverage and dollar coverage.
Filing counts alone make a small admitted filing look equivalent to a large one.

**What could go wrong:** building the reconciliation universe from the panel
drops filings with zero identifiable holdings. The implementation starts from
all filings with SOI rows and explicitly reports the five filings with no SOI
rows.

## Part 4 — Verify against the human-readable filing
Duration: 0:08:00

**Goal:** test whether panel values match the filing narrative rather than
merely matching another copy of the same SOI data.

Run the dependency verifier:

```bash
python scripts/verify_dependency.py
```

The verifier:

1. samples nine admitted filings with diverse structure and size;
2. fetches each primary HTML filing from SEC EDGAR;
3. reads identifier-matched fair value and principal facts from the document;
4. compares those values with the committed panel; and
5. checks the data release's `NUM` facts only when diagnosing disagreement.

Expected result:

```text
match: 30
rounding_or_units: 0
panel_error: 0
source_error: 0
unresolved: 0
```

Open `reports/spot_check.csv` and choose one `source_url`. Confirm the displayed
holding and value occur in the filing. The sample covers admitted filings only;
it is not evidence that every excluded filing should be forced into the panel.

**What could go wrong:** using the panel's own `SOI` values for the “filing”
side makes the test circular. The human-readable SEC document is the independent
source in this step.

## Part 5 — Reproduce, measure, and serve
Duration: 0:08:00

**Goal:** rebuild the complete pipeline, run the test suite, and consume the
result through separate serving layers.

Run the complete contract:

```bash
dvc repro
dvc status
dvc metrics show
PYTHONPATH=src python -m lookthrough.check
pytest -q
```

Generate the compact API bundle:

```bash
python scripts/export_app_data.py
```

Run the local backend and static UI:

```bash
PYTHONPATH=. uvicorn app.api.main:app --port 8000
python serve_web.py
```

Open:

* UI: `http://127.0.0.1:3000`
* API documentation: `http://127.0.0.1:8000/docs`
* Codelab: `http://127.0.0.1:3000/codelab/`

The public deployment uses the same separation:

* Replit serves `app/web/` and the generated static codelab.
* Vercel serves the read-only FastAPI backend and compact JSON data.
* `app/web/config.js` or the Replit `LANTERN_API_BASE` environment variable
  points the static UI at the backend.

The economic report in `reports/economics.md` states measured wall-clock values,
its compute-rate assumption, and the linear scale extrapolation. Re-run the
measurement on your own hardware before quoting speed as a universal result.

**What could go wrong:** the UI and API are intentionally deployable
separately. If the UI loads but shows a network error, check the API base URL
and backend CORS configuration before changing the data.

Positive
: A correct full run leaves `dvc status` clean, the self-check at 10/10, and all
tests passing.
