# Project LANTERN code lab

Public codelab: <https://lantern-cs2b-codelab.vercel.app>

The public tutorial is generated with `claat` from
[`docs/codelab.md`](../codelab.md). The generated files are committed in
`docs/lantern-case-study-2b/`, so the tutorial can be opened without running a
notebook or local server. This README and the executed notebook provide the
deeper implementation walkthrough used to author the public codelab.

This is the reproducible path from SEC business-development-company (BDC)
schedule-of-investments rows to Project LANTERN's panel, reconciliation and
read-only app. It uses the real release named in `params.yaml`, not the
synthetic fixture.

Open `notebooks/codelab.ipynb` from the repository root after `dvc pull`.
The notebook is already executed with small outputs. To execute a clean copy:

```bash
dvc pull
jupyter nbconvert --to notebook --execute notebooks/codelab.ipynb \
  --output /tmp/codelab-executed.ipynb
```

The notebook is not a `dvc.yaml` dependency. Nothing under `app/` or this
directory participates in `dvc repro`.

## Before you start

You need Python and the packages in `requirements.txt`. The notebook can
download the human-readable SEC filing with `requests` and parse it with
BeautifulSoup. If `sec.gov` is unavailable, that comparison is skipped; all
other steps use the DVC-restored release.

The lab starts with two SEC vocabulary facts:

- A **BDC** is a company that raises public capital and lends to or invests in
  smaller businesses. Its schedule of investments (SOI) lists those positions.
- XBRL files report the same table twice: **SUB** identifies filings, **TAG**
  explains standard tags, **NUM** holds numeric facts including the BDC's filed
  total, and **SOI** presents schedule rows.

The terms `InvestmentOwnedAtFairValue`,
`InvestmentOwnedBalancePrincipalAmount`, and XBRL "axis" appear in the files.
They are labels for money and dimensions, not new analytical scores.

## Traced filing

The notebook traces **STELLUS CAPITAL INVESTMENT CORP**, accession
`0001104659-26-093435`, period 2026-06-30.

This filing was selected because:

- 805 current SOI rows coalesce to 403 candidate holdings;
- 402 candidates span multiple SOI rows, showing how XBRL stores values and
  dimensions separately;
- the issuer-summary rule removes one row;
- period filtering and cleaning-attribute transformations also apply; and
- the live filing table can be compared with the released data.

The worked example is `2X LLC Investors LP Class A Units`: current SOI rows
42670 and 42671 become one holding with `source_rows="42670;42671"`.

## Step 1: See the schedule and the machine rows

**Goal.** Connect a human-readable fund table to the SEC's flat SOI fields.

**Why.** A number is only useful if a reader can locate the represented
investment. The filing is the source narrative; the release is the machine
representation.

**Code outline.**

```python
url = inline_url.replace("https://www.sec.gov/ix?doc=/", "https://www.sec.gov/")
raw = load.load_soi(release_dir, mapping.soi_usecols(header, colmap))
example = raw.query("adsh == @ADSH and ddate == '2026-06-30'")
```

The notebook fetches only the filing page and prints a compact view of the
security table around `2X Investors LP Class A Units`, followed by its raw SOI
rows.

**Expected output.** Fair value 1,220,895, amortized cost 176,915, shares
43,875, and source rows 42668–42671. Rows 42668–42669 are comparative; rows
42670–42671 are current and contain the value and dimension facts separately.

**What could go wrong.** SEC access may fail or the visual label may omit a
word present in the XBRL identifier. Do not infer a value from the displayed
text if retrieval fails; keep the release row as the evidence.

## Step 2: Understand SUB, TAG, NUM and SOI

**Goal.** Learn what each release file contributes and how large it is.

**Why.** Mapping by human column label alone is fragile. The project maps the
SOI columns through standard XBRL tags in **TAG**, while **NUM** supplies facts
such as the BDC's undimensioned filed fair value.

**Code outline.**

```python
sub = load.load_sub(release_dir)
tag = load.load_tag(release_dir)
row_counts = {"SUB": len(sub), "TAG": len(tag), "NUM": count_lines(num_path),
              "SOI": count_lines(soi_path)}
```

**Expected output.** The notebook prints the release name and four row counts,
then a four-row explanation table.

**What could go wrong.** SUB keeps current reports by excluding
`prevrpt == "1"`; SUB's row count can therefore differ from the raw line count.
`NUM` is much larger than SOI and should be filtered while reading.

## Step 3: Sum the naive schedule

**Goal.** Compare a direct current-period SOI sum with the BDC's own filed
`InvestmentOwnedAtFairValue` fact.

**Why.** The SOI is a long, dimensioned fact table. A simple sum can count
category lines, duplicate issuer tables or facts outside the investment total.
That difference motivates parsing and cleaning before admission.

**Code outline.**

```python
raw_total = current_rows["fair_value"].sum()
filed_total = reconcile.filed_totals(num, sub)
gap = raw_total / filed_total - 1
```

**Expected output.** The notebook labels the raw, coalesced, cleaned and filed
totals separately. Stellus is admitted because its final absolute gap is within
the tolerance in `params.yaml`.

**What could go wrong.** Do not sum every date in SOI; comparative schedules
would add old valuations. Do not treat the long-format missing cells as zero.

## Step 4: Map and coalesce holdings

**Goal.** Turn many XBRL facts into one row per filing, date and investment
identifier.

**Why.** XBRL often places an amount and a dimension on different rows. The
canonical mapping assigns standard fields by tag; coalescing keeps every SOI
row number in `source_rows`.

**Code outline.**

```python
canonical = holdings.split_periods(mapping.to_canonical(soi, colmap), sub)
coalesced = coalesce.coalesce(canonical)
```

**Expected output.** The traced filing has one record for
`2X LLC Investors LP Class A Units` with source rows `42670;42671`, fair value
1,220,895 and cost 176,915.

**What could go wrong.** Treating `source_release` as the source row is wrong;
the parsed `soi_row` is the zero-based data-row provenance. Visual filing labels
and XBRL identifiers need not be character-for-character identical.

## Step 5: Apply each cleaning transformation and rule

**Goal.** Audit every change in the declared semantic order.

**Why.** Rules are structural, not fitted to a desired coverage number. Each
one should name its artifact, show a real example, report affected rows and
make its effect on the traced filing visible.

The notebook applies:

1. `transform_current_period`
2. `transform_axis_identifiers`
3. `transform_custom_fair_values`
4. `transform_cleaning_attributes`
5. `rule_totals`
6. `rule_issuer_aggregates`
7. `rule_cash`

For each step it prints the goal, artifact, example filed in
`reports/cleaning_log.csv`, rows affected in the release, and the traced
filing's holding count and fair-value sum before and after.

**Expected output.** For Stellus, the issuer-aggregate rule removes
`J.R. Watkins, LLC Term Loan` from source rows 122368–122369. Total and cash
rules remove no Stellus rows. The release-wide row counts and coverage values
match the cleaning log.

**What could go wrong.** Applying a cash rule before issuer aggregates can
change which examples and counts a later rule sees. Keep the published order.
Descriptive transformations such as security classification do not drop rows.

## Step 6: Reconcile admission and coverage

**Goal.** Compare cleaned holdings with the filed total and understand who is
included.

**Why.** Coverage must be stated beside the panel value, and each filing
detail must show the filer's own total. Admission uses:

```text
abs(holdings_fv - filed_fv) / filed_fv <= 0.01
```

The notebook prints the tolerance and the copied release coverage object.
Coverage has two denominators: filings and filed dollars. They are not
interchangeable.

**Expected output.** 177 filings attempted, 88 admitted, 49.7% filing coverage
and 42.1% filed-dollar coverage. Five additional SUB filings have no SOI rows
and are reported separately.

**What could go wrong.** A filing count cannot stand in for dollar coverage.
Do not call the admitted subset “the market” or silently drop excluded funds.

## Step 7: Inspect an exclusion without forcing it

**Goal.** Understand why a real filing remains outside the panel.

**Why.** Forcing a filing inside by tuning a rule to its filed total would
destroy the structural evidence and leak the target into the method.

The notebook selects `PARTNERS GROUP LENDING FUND, LLC` and displays its copied
triage category, gap, evidence, example and fix. Its omitted standard
identifier and custom mixture of affiliation, asset-class, industry and issuer
members do not safely establish individual holdings.

**What could go wrong.** A custom column is not automatically an investment
identifier. A repeated value is not automatically a duplicate holding.

## Step 8: Verify against the filing

**Goal.** Compare the stored holding with the human-readable schedule and state
where each total came from.

**Why.** The app needs provenance at both holding and filing levels.

The notebook compares the 2X security's filed shares, cost, fair value and
percentage with the panel. It also prints the undimensioned NUM fact used as the
filing total.

**Expected output.** The 2X fair value/cost/shares match the displayed schedule.
The **filed** total is the undimensioned `InvestmentOwnedAtFairValue` NUM fact,
not a sum of the human-readable page.

**What could go wrong.** The visual table rounds or abbreviates, and renderings
may omit words. “Matches the page” is evidence for sampled values, not proof
that every fact has been interpreted correctly.

## Step 9: Reproduce

**Goal.** Rebuild the release and verify the same analytical contract.

**Why.** Saved outputs are not reproducibility.

```bash
dvc pull
dvc repro
PYTHONPATH=src python -m lookthrough.check
pytest -q
```

The app is separate:

```bash
python scripts/export_app_data.py
pytest -q tests/test_app.py
PYTHONPATH=. .venv/bin/uvicorn app.api.main:app --reload --port 8000
.venv/bin/python -m http.server 8001 --directory app/web
```

**Expected output.** DVC reports a clean pipeline, the self-check passes 10/10,
and pytest passes. The app test suite compares exported values with
`coverage.json`, `coverage.csv` and the panel.

**What could go wrong.** A fresh clone lacks DVC-tracked inputs until
`dvc pull`, and generated app JSON until `export_app_data.py`. Neither missing
state changes the analytical pipeline.

## Step 10: Respect the limits

This case study creates a traceable BDC investment-holdings panel. It does not:

- match a borrower across BDCs or periods;
- infer a common issuer identity;
- produce credit risk, default or return signals;
- treat an excluded filing as empty; or
- claim that admitted schedules cover all filings or all filed dollars.

The app is read-only. Its five pages are coverage, attempted filings, filing
detail, excluded filings and method.

## Natural-language prompt for a classmate

> Using the DVC-restored 2026 Q3 SEC BDC release, trace accession
> `0001104659-26-093435` from current SOI rows through coalescing and each
> structural cleaning rule. Reconcile the result to its undimensioned filed
> fair value, explain why it is admitted despite a nonzero gap, and compare one
> multi-row equity holding with the human-readable filing. State release-wide
> filing and dollar coverage, and explain one excluded filing without trying to
> force it into the panel.
