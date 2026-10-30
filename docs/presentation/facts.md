# Project LANTERN: presentation facts

Prepared from `integration/cs2b-final` at commit
`ba4f130b55a449d406e78a2ff8de2b707944ff8c` on 2026-10-30.

This file contains factual material only. It is not a slide deck.

## 1. Release and scope

| Item | Fact | Source |
|---|---|---|
| Release | `2026q3` | `params.yaml`, `release` |
| Monthly inputs | `2026_07`, `2026_08`, `2026_09` | `params.yaml`, `release_months` |
| Manifest entries | The same three monthly releases | `data/manifest.json` |
| Release mismatch | None found between `params.yaml`, `release_months`, and the manifest; the values represent months within the assigned quarterly release | `params.yaml`, `data/manifest.json` |
| Reconciliation tolerance | `0.01` (1 percentage point) | `params.yaml`, `reconcile.tolerance`; `dvc.lock` |
| Filings in SUB | 182 | `dvc repro --force` parse/reconcile output, reading the DVC-restored release |
| Filings attempted | 177 | `reports/coverage.json`; `dvc repro --force` |
| Filings without SOI rows | 5 | `reports/coverage.json`; `dvc repro --force` |

The monthly ZIP sizes and SHA-256 values are recorded in
`data/manifest.json`; the acquisition run reported `Manifest verifies: True`.

**NOT AVAILABLE:** independent confirmation that the course assigned
`2026q3` to Team 3. `params.yaml` says “Team 3's assigned quarter (Canvas)”, but
the external Canvas assignment is not in the repository.

## 2. Coverage

Source: `reports/coverage.json`, produced by `dvc repro --force`.

| Metric | Value |
|---|---:|
| Filings attempted | 177 |
| Filings admitted | 88 |
| Filing coverage | 49.7% (`0.497`) |
| Filed fair value attempted | $556,908,483,659 |
| Filed fair value admitted | $234,366,032,543 |
| Dollar coverage | 42.1% (`0.421`) |
| Filings with no SOI rows | 5 |

### Excluded filings by category

Source: `reports/coverage.csv`; calculation summed rows where
`admitted == False`, grouped by `triage_category`.

| Category | Filings | Filed fair value |
|---|---:|---:|
| `comparative_leakage` | 0 | $0 |
| `totals_counted` | 19 | $53,299,246,575 |
| `cash_lines` | 4 | $6,174,218,560 |
| `restated_copies` | 28 | $118,496,853,330 |
| `unfunded_commitments` | 2 | $4,202,711,000 |
| `custom_tags` | 3 | $1,039,679,000 |
| `no_identified_holdings` | 2 | $926,422,701 |
| `affiliate_split` | 0 | $0 |
| `no_filed_total` | 7 | $0 |
| `other` | 24 | $138,403,319,950 |
| **Total** | **89** | **$322,542,451,116** |

### Five largest excluded filings

Source: `reports/coverage.csv`; selected by largest `filed_fv` where
`admitted == False`.

| Filing | Accession | Category | Filed fair value | Gap |
|---|---|---|---:|---:|
| BLACKSTONE PRIVATE CREDIT FUND | `0001803498-26-000048` | `other` | $77,649,107,000 | +9.02% |
| BLUE OWL CREDIT INCOME CORP. | `0001812554-26-000047` | `restated_copies` | $35,690,147,000 | +9.19% |
| HPS CORPORATE LENDING FUND | `0001628280-26-056772` | `other` | $24,178,038,000 | +6.51% |
| BLUE OWL CAPITAL CORP | `0001655888-26-000056` | `totals_counted` | $14,955,049,000 | +16.11% |
| BLUE OWL TECHNOLOGY FINANCE CORP. | `0001747777-26-000028` | `restated_copies` | $14,680,538,000 | +6.94% |

### Gap distribution among admitted filings

Source: `reports/coverage.csv`, `gap_pct` where `admitted == True`.

| Statistic | Gap |
|---|---:|
| Minimum | -0.9539% |
| Median | 0.0000% |
| Maximum | +0.9466% |

All three values lie within the configured ±1% tolerance.

## 3. Cleaning transformations and rules

Source: `reports/cleaning_log.csv`. Coverage values are shares of attempted
filed dollars at that step, not shares of rows.

| Step | Artifact handled | Rows affected | Coverage before | Coverage after |
|---|---|---:|---:|---:|
| `transform_current_period` | Excludes comparative and other-date rows | 64,835 | 28.5% | 28.5% |
| `transform_axis_identifiers` | Recovers a holding name from a fallback legal-entity axis only when a filing has no standard current identifier | 39 | 28.5% | 28.5% |
| `transform_custom_fair_values` | Fills an omitted SOI fair value from an identifier-keyed custom NUM fact | 28 | 28.5% | 27.1% |
| `transform_cleaning_attributes` | Adds security class, affiliation category, and unfunded-commitment flag | 68,175 | 27.1% | 27.1% |
| `rule_totals` | Explicit total/subtotal and category-only labels | 59 | 27.1% | 28.8% |
| `rule_issuer_aggregates` | Short issuer summary with no cost/principal when a detailed row for the same issuer exists in the filing | 311 | 28.8% | 40.0% |
| `rule_cash` | Explicit cash and money-market lines | 40 | 40.0% | 42.1% |

### Verified examples

Source: labels and canonical pre-rule values from
`outputs/canonical/holdings.parquet`; existence was checked against the raw SOI
rows loaded by `src/lookthrough/load.py`.

| Rule | Accession | SOI row | Label | Pre-rule fair value | Structural signal |
|---|---|---|---:|---:|---|
| `rule_totals` | `0000930413-26-002499` | 106,977 | `Investments at Fair Value [Member]` | $1,563,657,000 | Exact category-only label, not an investee |
| `rule_issuer_aggregates` | `0000017313-26-000095` | 40,610 | `CapTrin Partners, LLC` | $97,800,000 | No cost or principal; a detailed row contains the same normalized issuer key |
| `rule_cash` | `0001193125-26-335023` | 129,396 | `MFB Northern Inst Funds Treas Portfolio Premier CL Short-Term Investments Money Market Interest Rate 4.16%%` | $3,966,000 | Label explicitly names a money-market line |

All three accession/SOI-row pairs were found exactly once in the raw SOI data.

## 4. Traced admitted filing

Filing: **STELLUS CAPITAL INVESTMENT CORP**, accession
`0001104659-26-093435`, period 2026-06-30.

Source: raw SOI loaded with `src/lookthrough/load.py`; current holdings from
`outputs/canonical/holdings.parquet`; final values from
`outputs/panel/holdings.parquet` and `reports/coverage.csv`.

| Stage | Row count |
|---|---:|
| Raw SOI rows, including all schedules | 2,168 |
| Current-period raw SOI rows | 1,085 |
| Current holdings after source-row filtering and coalescing | 403 |
| After `rule_totals` | 403 |
| After `rule_issuer_aggregates` | 402 |
| After `rule_cash` | 402 |
| Final panel | 402 |

| Metric | Value |
|---|---:|
| Panel fair value | $971,696,643 |
| Filed fair value | $968,246,417 |
| Gap | +0.3563% |
| Admitted | Yes |
| Panel holdings spanning multiple SOI rows | 401 of 402 |

One example multi-row holding is `2X LLC Investors LP Class A Units`, built from
current SOI rows `42670;42671`.

**Limited availability:** no admitted filing simultaneously has more than one
of the three structural drop rules firing and a current holding spanning
multiple SOI rows. A full scan of the reconstructed rule masks found two
admitted filings with two rule types, but neither contains a multi-row holding.
The requested exact combination is therefore **NOT AVAILABLE**. Stellus is the
nearest trace: multiple cleaning-log transformations run, one structural rule
fires, and 401 holdings are multi-row.

## 5. Excluded filing stories

### PARTNERS GROUP LENDING FUND, LLC

Source: `docs/triage_notes.csv`, `reports/coverage.csv`, and the raw SOI.

| Item | Fact |
|---|---|
| Accession | `0001398344-26-014697` |
| Filed fair value | $520,571,000 |
| Holdings fair value | N/A — no holding could be identified |
| Gap | N/A — not defined without a holdings total |
| Category | `no_identified_holdings` |
| Evidence | 457 current-period SOI rows; none has `Investment, Identifier Axis` |
| Example | SOI row 14,549 |
| Why not forced | The available custom identifier column mixes affiliation, asset class, industry, and issuer members. It does not identify one individual investee, so forcing those rows into holdings would require unsupported interpretation. |

### GREAT ELM CAPITAL CORP.

Source: `reports/coverage.csv`, `docs/triage_notes.csv`, and
`outputs/panel/holdings.parquet`.

| Item | Fact |
|---|---|
| Accession | `0001193125-26-335023` |
| Category | `cash_lines` |
| Filed fair value | $272,252,000 |
| Holdings fair value | $268,286,000 |
| Gap | -1.4567% |
| Example | SOI row 129,396; money-market holding valued at $3,966,000 |
| Why not forced | The panel excludes cash and money-market lines uniformly, even when a filer includes them in its reported total. The resulting difference remains visible rather than creating a filer-specific exception. |

## 6. Why the panel changed

| Version | Panel rows | Total panel fair value | Filed-dollar coverage | DVC stages |
|---|---:|---:|---:|---|
| Baseline committed main `c008f6b` | 27,669 | $170,490,964,061 | 30.6% | `acquire`, `parse`, `reconcile` |
| Merged integration branch | 33,222 | $234,404,394,079 | 42.1% | `acquire`, `parse`, `clean`, `reconcile`, `report` |

Sources:

- The pre-merge panel was reproduced from `c008f6b` before the merges; the
  observed values were 27,669 rows and $170,490,964,061.
- Current values are from `reports/panel_fingerprint.json` and
  `outputs/panel/holdings.parquet`.
- `git show c008f6b:dvc.lock` lists only `acquire`, `parse`, and `reconcile`.
  The integration `dvc.lock` adds `clean` and `report`.
- `git diff c008f6b..integration/cs2b-final --stat -- dvc.lock` reports
  171 insertions and 36 deletions.

The large change is explained by changed filing admission, not just row
removals:

- `git show c008f6b:reports/coverage.csv` had 80 admitted filings.
- The merged `reports/coverage.csv` has 88 admitted filings.
- Comparing admitted accession sets shows 12 newly admitted filings and 4
  filings no longer admitted.
- The 12 newly admitted filings contribute 7,375 panel holdings and
  $74,717,221,256 fair value.
- Net growth is 5,553 rows and $63,913,430,018.
- The 12 additions are offset by four lost admitted filings, rule removals, and
  changed holdings in retained filings.

Relevant commits from `git log c008f6b..integration/cs2b-final`:

- `4cfac43` — Complete Part 2 cleaning rules and validation
- `bfc16e8` — Merge `codex/part-2-cleaning`
- `b2e86f3` — Complete dependency verification and modular DVC pipeline
- `01ab2eb` — Merge `codex/part-4-dependency-check`
- `d6fa88a` — Merge the app/code-lab branch

The four filings admitted in the baseline but not in the merged panel are
OakTree Strategic Credit Fund, Golub Capital BDC 4 Inc., OakTree Gardens OLP,
and TriplePoint Private Venture Credit Inc., according to the accession-set
comparison of the two `coverage.csv` files.

## 7. Part 4 verification

Sources: `reports/dependency_check.md`, `reports/spot_check.csv`,
`scripts/verify_dependency.py`.

| Metric | Value |
|---|---:|
| Sampled holdings | 30 |
| Sampled filings | 9 |
| `match` | 30 |
| `rounding_or_units` | 0 |
| `panel_error` | 0 |
| `source_error` | 0 |
| `unresolved` | 0 |
| Holdings spanning multiple source rows | 12 |
| EdgarTools result values | 0 / not used |

The “filing” values come from the primary human-readable filing HTML fetched
from SEC EDGAR and parsed from identifier-matched iXBRL facts
(`scripts/verify_dependency.py:153 _filing_document()`,
`scripts/verify_dependency.py:230 _parse_filing()`, and
`scripts/verify_dependency.py:274 _filed_values()`). NUM/SOI is consulted only
to diagnose disagreement. The check is **not circular**.

The 30 holdings cover admitted filings only. The sample is stratified rather
than a uniform random sample. EdgarTools was not used because no pinned version
was installed or specified.

## 8. Pipeline and tests

### DVC stages

Source: `dvc.yaml`.

1. `acquire` — `python scripts/acquire.py`
2. `parse` — `python scripts/parse.py`
3. `clean` — `python scripts/clean.py`
4. `reconcile` — `python scripts/reconcile.py`
5. `report` — `python scripts/report.py`

### Commands run

| Check | Observed result |
|---|---|
| `dvc status` | `Data and pipelines are up to date.` |
| `dvc metrics show` | 88 admitted / 177 attempted; 49.7%; $234,366,032,543 admitted of $556,908,483,659; 42.1%; 5 without SOI rows |
| `PYTHONPATH=src python -m lookthrough.check` | 10/10 checks passed |
| `pytest -q` | 36 passed, 1 Starlette deprecation warning |

### Mutation evidence

Source: `reports/tests_that_fail.md`.

The report lists ten mutations, and each was restored. Example:

- Before: replace the `rule_totals` drop mask with an all-false mask.
- Mutated result: the real-release test fails with
  `assert drop[_row(... "Total Annex Cloud")]` evaluating to
  `assert np.False_`.
- After restore: `pytest -q
  tests/test_cleaning_real_release.py::test_rule_totals_real_release_and_spares_borrower_names`
  reported `1 passed`.

The other reported mutations cover current-period filtering, axis recovery,
custom fair values, cleaning attributes, issuer aggregates, cash removal,
pipeline parameter declaration, admission tolerance, and no-filing-dropped
behavior.

## 9. Economics

### Current measurement

Command run twice:

```bash
PATH="$PWD/.venv/bin:$PATH" /usr/bin/time -p .venv/bin/dvc repro --force
```

Machine: Intel Core i9-9880H, 2.30 GHz, 64 GB RAM, macOS 26.5.2 x86_64,
Python 3.11.17.

Sources: `/usr/bin/time` output from the two runs.

| Run | Wall clock | Seconds per attempted filing |
|---|---:|---:|
| 1 | 132.94 s | 0.7511 s |
| 2 | 135.00 s | 0.7627 s |
| Average | 133.97 s | 0.7569 s |

At the report’s stated $0.10 per compute-hour assumption, the current average
is $0.000021025 per attempted filing.

### Five economics lines from `reports/economics.md`

1. **Cost per completed task:** run 1 was 132.26 s / $0.000020756 per filing;
   run 2 was 145.16 s / $0.000022781; two-run average $0.000021769.
2. **Latency:** measured with `dvc repro --force`; report averages 138.71 s or
   0.783672 s per attempted filing.
3. **Human time replaced:** 2.0 analyst hours per BDC; 354 gross hours across
   177 filings; net 176.96 hours ($21,235.38) at ×0.5, 353.96 hours
   ($42,475.38) at ×1, and 707.96 hours ($84,955.38) at ×2.
4. **Quality:** 88/177 filings and 42.1% of filed dollars; 30/30 sampled
   holdings matched; no unresolved sample rows.
5. **Scale:** 16 quarterly releases from Q4 2022 through Q3 2026, 2,832 filing
   tasks, 0.6165 compute-hours and $0.06165 total at average measured latency.

### Assumptions stated in `reports/economics.md`

- One filing processed through the complete pipeline is one task.
- Compute costs $0.10 per compute-hour; this is inherited from the course
  notebook and is not a quoted cloud price.
- Model cost is $0 because the pipeline calls no generative model.
- Manual review takes 2.0 hours per BDC.
- Loaded analyst time costs $120/hour.
- Scale assumes 16 releases, 177 filings in each release, and the same average
  runtime as 2026q3.

The current two-run timings (132.94 s and 135.00 s) differ from the stored
report timings (132.26 s and 145.16 s), but the machine and command are the
same. Timing variation is expected; both sets should be presented as
machine-specific measurements, not universal benchmarks.

## 10. App and code lab

Sources: live URL checks and browser rendering on 2026-10-30.

| Surface | URL | Status |
|---|---|---|
| Streamlit UI | <https://lantern-lab2b.streamlit.app> | Browser-rendered successfully; displayed 88/177 and 42.1% |
| API documentation | <https://lantern-lab2b.vercel.app/docs> | HTTP 200 |
| Public codelab | <https://lantern-cs2b-codelab.vercel.app> | HTTP 200 |

Tested API endpoints and responses:

| Endpoint | Status |
|---|---|
| `/api/health` | 200 |
| `/api/coverage` | 200 |
| `/api/filings` | 200 |
| `/api/filings/0001628280-26-050307` | 200 |
| `/api/filings/0001628280-26-050307/holdings` | 200 |
| `/api/triage` | 200 |
| `/api/cleaning-rules` | 200 |

### Screenshots

- Coverage page: [`assets/coverage.jpg`](assets/coverage.jpg)
- Filing detail page: [`assets/filing-detail.jpg`](assets/filing-detail.jpg)
- Excluded filings page: [`assets/excluded-filings.jpg`](assets/excluded-filings.jpg)
- Swagger `/docs`: [`assets/swagger-docs.jpg`](assets/swagger-docs.jpg)

Screenshots were captured from the live pages with the interface and data fully
loaded. No screenshots were fabricated.

## 11. Code references

| Stage | File and function/entry point |
|---|---|
| Acquire | `scripts/acquire.py:29` acquisition loop; `src/lookthrough/acquire.py:20 download_release()`, `src/lookthrough/acquire.py:78 verify_manifest()` |
| Parse mapping | `src/lookthrough/mapping.py:59 map_soi_columns()`, `src/lookthrough/mapping.py:102 to_canonical()` |
| Parse periods | `src/lookthrough/holdings.py:13 split_periods()` |
| Parse coalescing | `src/lookthrough/coalesce.py:32 coalesce()` |
| Clean transformations | `src/lookthrough/clean.py:116 recover_axis_identifiers()`, `src/lookthrough/clean.py:151 recover_custom_fair_values()`, `src/lookthrough/clean.py:196 add_cleaning_attributes()` |
| Clean rules | `src/lookthrough/clean.py:47 rule_totals()`, `src/lookthrough/clean.py:69 rule_issuer_aggregates()`, `src/lookthrough/clean.py:111 rule_cash()` |
| Reconcile | `src/lookthrough/reconcile.py:14 filed_totals()`, `src/lookthrough/reconcile.py:23 reconcile()`, `src/lookthrough/reconcile.py:45 coverage()`, `src/lookthrough/reconcile.py:63 diagnose()` |
| Report | `src/lookthrough/report.py:16 write_outputs()` |
| API | `app/api/main.py:73 health()`, `app/api/main.py:86 get_coverage()`, `app/api/main.py:102 get_filings()`, `app/api/main.py:124 get_filing()`, `app/api/main.py:139 get_holdings()`, `app/api/main.py:164 get_triage()`, `app/api/main.py:178 get_cleaning_rules()` |
| Streamlit | `streamlit_app.py:88 coverage_page()`, `streamlit_app.py:159 filing_detail()`, `streamlit_app.py:232 filings_page()`, `streamlit_app.py:281 excluded_page()`, `streamlit_app.py:324 method_page()`, `streamlit_app.py:350 codelab_page()` |
| Part 4 verifier | `scripts/verify_dependency.py:153 _filing_document()`, `scripts/verify_dependency.py:230 _parse_filing()`, `scripts/verify_dependency.py:274 _filed_values()` |

## 12. Limitations

- Coverage is not complete: 89 of 177 filings remain excluded and filed-dollar
  coverage is 42.1%.
- Five additional SUB filings have no SOI rows and are outside the attempted
  reconciliation set.
- Cash and money-market lines are excluded by product definition. Filers that
  include those lines in their filed total can remain outside tolerance.
- PARTNERS GROUP LENDING FUND cannot be reconstructed from the standard
  identifier axis; its custom identifier column is mixed and was not forced.
- Part 4 checks 30 holdings in 9 admitted filings. It does not prove every
  holding or any excluded filing.
- The Part 4 sample is stratified, not randomly representative.
- ``rule_issuer_aggregates`` has a 20-row audit, not an exhaustive audit of all
  311 removed rows.
- The panel does not support cross-BDC borrower matching, cross-period identity,
  or credit-signal claims.
- Exact combination unavailable: no admitted filing has more than one
  structural drop rule plus a multi-row holding. Stellus is the nearest traced
  example.
- Economics depend on measured hardware and explicitly stated labor, compute,
  release-count, and filing-count assumptions.
- The demo-video URL is not present in the repository.
- The instructor’s assignment of `2026q3` is not independently verifiable from
  repository files.
- The repository does not contain the exact `data/raw.dvc` path expected by one
  review checklist; it tracks `data/raw` inline through `dvc.yaml` and
  `dvc.lock`.

## 13. Likely grader questions

| Question | Short answer | Backing file |
|---|---|---|
| How much of the release is represented? | 88 of 177 filings (49.7%) and 42.1% of filed dollars. | `reports/coverage.json` |
| Why are 89 filings excluded? | Structural ambiguity, duplicate/total rows, cash scope, missing identifiers/totals, or unresolved gaps; each has a category and evidence. | `reports/coverage.csv`, `docs/triage_notes.csv` |
| How are filed totals determined? | The current-period, undimensioned `InvestmentOwnedAtFairValue` NUM fact for each filing. | `src/lookthrough/reconcile.py:14 filed_totals()` |
| Are rules tuned to the coverage gap? | No; rules use dates, identifiers, totals, duplicate issuer keys, and explicit liquidity labels. Coverage is reported after rule selection. | `src/lookthrough/clean.py`, `docs/cleaning_log.md` |
| Is Part 4 circular? | No; filing-side values come from human-readable SEC HTML, while NUM/SOI is used only for diagnosis. | `scripts/verify_dependency.py` |
| Does Part 4 prove the whole panel? | No; it samples 30 holdings across 9 admitted filings. | `reports/dependency_check.md` |
| Why is Partners Group excluded? | Its 457 current SOI rows lack the standard identifier axis; the custom column mixes incompatible member types. | `docs/triage_notes.csv`, `docs/cleaning_log.md` |
| Why did the panel grow when rules remove rows? | Twelve newly admitted filings contribute 7,375 rows and $74.7B, outweighing removals and four lost filings. | Baseline/merged `coverage.csv`; current panel Parquet |
| How is the pipeline tied together? | Five DVC stages run acquire → parse → clean → reconcile → report. | `dvc.yaml`, `dvc.lock` |
| What would break if behavior changed? | Real-release and pipeline tests cover transformations, all rules, tolerance, admission, no-filing-dropped, API contracts, and the app. | `tests/`, `reports/tests_that_fail.md` |
