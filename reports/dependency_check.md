# Part 4 dependency verification

## Demonstration scope

The panel is an investment-holdings panel **excluding cash and money-market
lines**. That is a deliberate product definition for the borrower-to-BDC view:
a money-market fund line is not a loan to a borrower. Some filers include cash
in their filed investment total while others do not, so the exclusion cannot
reconcile every filing to that total. It raises aggregate filed-dollar
coverage from 40.0% to 42.1%; remaining cash-related differences are retained
as evidence in the triage report.

## Result

No disagreements found. Thirty sampled holdings across nine filings match the
human-readable Schedule of Investments on both fair value and principal,
including zero-valued lines and holdings assembled from multiple source rows.
No unresolved rows remain.

A separate fixed-seed audit of 20 holdings removed by
`rule_issuer_aggregates` found 20/20 correct removals and no false positives;
the evidence is in [aggregate_audit.md](aggregate_audit.md).

| Classification | Holdings |
|---|---:|
| match | 30 |
| rounding_or_units | 0 |
| panel_error | 0 |
| source_error | 0 |
| unresolved | 0 |

The fixed random seed is `20261030`. It is used inside
`scripts/verify_dependency.py` for selecting additional holdings within each
chosen filing.

## Sampling method

The sample is stratified rather than a uniform random sample. The filing strata
were: (1) the admitted filing with the largest absolute reconciliation gap,
(2) the three filings with the largest total panel fair value, and (3) the five
filings with the highest combined counts of controlled, affiliated, warrant,
and equity holdings. This produced nine distinct filings. Within each filing,
the sample includes the largest holding by absolute fair value, the largest
explicit affiliate/control holding when present, a seeded selection from a
different equity/warrant class when present, and a seeded selection from the
remaining rows. The result has 30 holdings, satisfying the minimum of 20 across
five filings.

The stratification produced:

| Dimension | Count |
|---|---:|
| Debt holdings | 16 |
| Equity holdings | 9 |
| Warrant holdings | 3 |
| Other holdings | 2 |
| Explicit affiliated positions | 6 |
| Explicit controlled positions | 1 |
| Non-affiliated positions | 9 |
| Holdings spanning multiple source rows | 12 |

Fair values range from zero to $1,896,800,000 with a median of $15,981,767.
SOUND POINT DIRECT LENDING BDC was the near-tolerance stratum, admitted with a
gap of -0.9539%.

## Filing access and evidence extraction

For every sampled filing, the verifier first fetched the filing `index.json`
using its accession number (hyphens removed), selected the form-tagged primary
HTML document, and fetched that document through the SEC Archives URL. All
requests sent the User-Agent from `params.yaml`; the client waits 0.3 seconds
before each request, keeping the request rate below five per second. Primary
documents and filing indexes are cached under the Git-ignored
`data/cache/part4/`.

The primary documents are inline-XBRL filings. The verifier reads
`InvestmentOwnedAtFairValue` and `InvestmentOwnedBalancePrincipalAmount`
facts, resolves each fact's `InvestmentIdentifierAxis` context and period, and
applies the displayed iXBRL scale. It does not use the filed reconciliation
total. Parentheses and XBRL sign attributes are treated as negative, and facts
sharing an identifier are combined when a holding spans multiple rows. The
exact visible table text, including the preceding row label when the filing
splits a holding, is stored in `reports/spot_check.csv`.
Within those quoted strings, `|` marks an HTML cell boundary and `||` marks
the boundary between adjacent HTML rows; the cell text itself is not otherwise
rewritten.

EdgarTools was not used because no pinned version is installed or specified in
the repository. The `edgartools_fair_value` column is therefore blank.

## Disagreements

None. Filing fair value and principal both equal the panel values for all 30
holdings; the maximum absolute difference is zero for both fields.

Two zero-valued equity rows required explicit interpretation of the table's em
dash convention: ARES CAPITAL CORP accession `0001628280-26-050307`,
`Amerivet Partners Management, Inc. and AVE Holdings LP | Class C units`, and
`Olympia Acquisition, Inc., Olympia TopCo, L.P., and Asclepius Holdings LLC |
Preferred stock`. Their exact table rows and matching NUM facts of zero are
recorded in `spot_check.csv`.

## Unresolved items

None.

No `reports/issue_draft.md` was created because no library or data-set error
was supported by the filing evidence.
