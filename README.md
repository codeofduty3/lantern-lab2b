# Lab 2B starter kit: Look-Through (SEC BDC data sets)

DAMG 7245, Fall 2026. Companion to the Tool Tutorial Part 2B deck, the BDC Primer and Case Study 2B.

## Setup (10 minutes)
Copy this folder into your team's Case Study 1 repository as `cs2b/`, and run everything from inside it.
```
cd cs2b
python -m venv .venv && source .venv/bin/activate      # Python 3.10 or later
pip install -r requirements.txt
jupyter lab                                             # open notebooks/00_setup.ipynb
```
Then set `sec.user_agent` (your name and email) and your team's `release` in `params.yaml`.

## Work through, in order
| Notebook | Step |
|---|---|
| 00_setup | Environment, parameters, tests |
| 01_primer_exercise | One holding, from flat file to filing |
| 02_acquire | Download your release, manifest, DVC (switches you to real data) |
| 03_raw_parse | SUB, TAG, NUM and SOI; map columns by tag |
| 04_periods_and_dimensions | Dates, current vs comparative schedules, segments, coalescing |
| 05_clean | Find artifacts, write rules, keep a cleaning log |
| 06_reconcile | Reconcile to filed totals, coverage, triage, outputs, self-check |
| 07_verify_dependency | Spot-check against the filings; optional EdgarTools comparison |
| 08_pipeline_and_economics | Tests that fail, timing, unit economics, DVC pipeline |

You start in **fixture mode** (`data.use_fixture: true`): a synthetic release in the SEC's layout, with fictional BDCs, so everything runs offline. Notebook 02 switches you to your real release.

## Checks
```
python tests/run_tests.py                 # or: pytest -q
python tools/run_notebooks.py             # runs every notebook's code in order
PYTHONPATH=src python -m lookthrough.check   # Case Study 2B self-check on your outputs
python tools/smoke_real.py <release> "Name email"   # baseline on any real release (needs network)
```

## Layout
`src/lookthrough/` helpers (paths, acquire, load, mapping, holdings, clean, reconcile, pipeline, report, tables, check);
`data/fixture/` the synthetic release (rebuild with `python tools/make_fixture.py`); `data/raw/` your release (DVC, never Git);
`outputs/panel/` the reconciled panel; `reports/` coverage, triage, cleaning log, spot checks; `docs/` schema and pipeline notes.

## Analytical scope

The output panel represents investment holdings used for a borrower-to-BDC
relationship view and deliberately excludes cash and money-market lines. A
money-market fund is not a company borrower. Because filers differ on whether
cash is included in their filed investment total, the exclusion is applied
uniformly at the panel-scope level and cash-related filing differences remain
visible in the triage report.

## Data
Public data only: the SEC BDC data sets (https://www.sec.gov/data-research/sec-markets-data/bdc-data-sets) and the SEC BDC readme (https://www.sec.gov/files/bdc_readme.pdf). Fixture data is synthetic.

## Read-only app and code lab

The 2026 Q3 application is an additive read-only view of the completed panel.
It does not change the DVC pipeline or any existing report.

Install the two web runtime packages in the existing environment, then generate
the compact app data and start the API and static site in separate terminals:

```bash
pip install -r app/api/requirements.txt
pip install "uvicorn>=0.30,<1"
python scripts/export_app_data.py
PYTHONPATH=. .venv/bin/uvicorn app.api.main:app --reload --port 8000
.venv/bin/python -m http.server 8001 --directory app/web
```

Open `http://127.0.0.1:8001` for the five-page site and
`http://127.0.0.1:8000/docs` for Swagger. The generated `app/data/` directory is
ignored by Git because the 88 per-filing JSON exports are about 20 MiB.

The end-to-end code lab is in
[`docs/codelab/README.md`](docs/codelab/README.md), with its executed notebook at
[`notebooks/codelab.ipynb`](notebooks/codelab.ipynb). It is not a dependency of
`dvc.yaml`.

### Deployment

Vercel is used because it can route the static five-page site and the FastAPI
function without Replit-specific setup. The production app is
<https://lantern-lab2b.vercel.app>, Swagger is
<https://lantern-lab2b.vercel.app/docs>. Vercel creates authenticated preview
deployments for pull requests; use the current preview from Vercel rather than
treating a fixed, account-protected preview URL as a public API test target.

The `buildCommand` regenerates the compact app data before deployment.
`vercel.json` excludes the local DVC data, virtual environment and reports from
the API bundle, and routes `/api` plus `/docs` to FastAPI while every other path
serves `app/web`.
