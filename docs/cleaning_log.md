# Cleaning log: Project LANTERN, 2026q3

## Scope and evidence rule

This log covers the verified real release in `data/raw/2026q3_bdc`, which was
parsed after the manifest check. Rules were selected from row structure:
identifier labels, row dates, duplicate issuer keys, missing standard
identifiers, and standard or custom dimension columns. Filed totals were used
only after rule selection to calculate the `coverage_before` and
`coverage_after` fields in `reports/cleaning_log.csv`; those fields are shares
of attempted filed dollars and did not determine any pattern or rule order.

## transform_current_period

`holdings.split_periods` matches each row's `ddate` to the filing period from
SUB and excludes non-current dates from the current panel. The release has
92,709 comparative rows and 3,231 other-date rows; after coalescing, 64,835
non-current holdings are excluded. For example, accession
`0000017313-26-000095`, SOI row 42732, has `ddate` 2026-03-31 rather than the
filing period 2026-06-30. This is a filtering transformation; dollar coverage
was unchanged at 0.285 before and after because both measurements operate on
the current schedule.

## transform_axis_identifiers

`clean.recover_axis_identifiers` recovers a holding name from a filed fallback
axis only when every current-period row for that accession lacks the standard
`Investment, Identifier Axis`. That condition avoids importing supplementary
issuer-name totals into filings that already have instrument-level identifiers.
For NEOSTELLAR CAPITAL CORP (`0001493152-26-036285`), 86 current SOI rows use
`Legal Entity Axis` without a standard identifier; coalescing the recovered
names produces 39 holdings, including SOI row 10586 for ARK Type One Deep
Ventures Fund LLC. Filed-dollar coverage remained 0.285 before and after
this recovery.

PARTNERS GROUP LENDING FUND, LLC (`0001398344-26-014697`) also has no standard
identifier, but its custom `InvestmentsIdentifier` column contains a mixture
of affiliation, asset-class, industry, and issuer members. Those rows were not
promoted to holdings because the custom column alone does not identify an
individual investee; this conservative gap is flagged for review.

## transform_custom_fair_values

`clean.recover_custom_fair_values` fills omitted fair values from NUM only when
the custom money-market tag is keyed by the same `InvestmentIdentifierAxis`
member and filing date as an existing SOI holding. This is a fair-value
transformation, and affected rows are labeled with a `NUM <tag>` value in
`fair_value_source`. It filled 28 real holdings in 17 filings. For example,
GOLUB CAPITAL PRIVATE INCOME FUND I (`0002082559-26-000086`), SOI row 130821,
has no standard fair value; NUM's `MoneyMarketFundsFairValueDisclosure`
supplies 9,637,000. Filed-dollar coverage moved from 0.285 to 0.271 after this
recovery, before the cash rule removed those liquidity lines.

## transform_cleaning_attributes

`clean.add_cleaning_attributes` preserves equity and warrant holdings while
adding `security_class`, classifies explicit controlled/affiliated/non-affiliated
language into `affiliation_category`, and carries the standard unfunded
commitment amount into `unfunded_commitment` with a
`has_unfunded_commitment` flag. These are descriptive transformations, not drop
rules. They cover all 68,175 current holdings and identify 5,949 equity rows,
1,588 warrants, 220 controlled rows, and 4,459 rows with an unfunded flag.
An equity example is CAPITAL SOUTHWEST CORP (`0000017313-26-000095`), SOI row
42985; a warrant example is the same accession, SOI row 43014. The later issuer
and cash rules may remove rows after classification, so these are pre-rule
counts.

The affiliation axis itself appears only on category rows in this long-format
SOI. It cannot be joined row-for-row to every instrument without the original
XBRL context. The transformation therefore classifies explicit affiliation
text in identifiers and leaves `unspecified` where the evidence is absent.
Unfunded commitment facts that are separate NUM dimensions, such as the KKR FS
funds, remain outside the holdings panel instead of being converted into
fabricated investment rows.

## rule_totals

`clean.rule_totals` drops identifiers that are explicit total/subtotal labels
or exact category-only labels such as `Net Assets`,
`Investments at Fair Value [Member]`, and `Control Investments`. The total
pattern requires a generic total phrase such as `Total Investments`,
`Sub Total investments`, `Total cash`, or `, Total <issuer>`; this protects
real borrowers whose names begin with `Total`. The rule removes 59 current
holdings in 22 filings, including HERCULES CAPITAL, INC.
(`0001280784-26-000042`), SOI row 2765, and STEPSTONE PRIVATE CREDIT FUND LLC
(`0001193125-26-351731`), SOI row 136461. Filed-dollar coverage changed from
0.271 to 0.288 only as a reported consequence.

## rule_issuer_aggregates

`clean.rule_issuer_aggregates` detects a short identifier with neither cost nor
principal when the same filing also has one or more detailed identifiers that
contain that complete issuer name. This structural duplicate-key signal
identifies issuer summaries and affiliated/control-table restatements without
using the filed total. The rule removes 311 current rows in 36 filings, for
example CAPITAL SOUTHWEST CORP, SOI row 40610 (`CapTrin Partners, LLC`) beside
its instrument-detail rows, and SIXTH STREET SPECIALTY LENDING, INC.
(`0001193125-26-332725`), SOI row 121637 (`IRGSE Holding Corp`) beside four
loan/equity instruments. The minimal eight-character issuer key protects
short generic fragments and was chosen from the structural evidence. Reported
filed-dollar coverage changed from 0.288 to 0.400.

## rule_cash

`clean.rule_cash` drops identifiers that explicitly name cash or a
money-market fund. This is a product-scope rule: the panel is an investment
holdings extract, so liquidity lines are excluded whether or not a filing
includes them in its filed investments total. After earlier rules, it removes
40 current rows in 26 filings. A verified example is BRIGHTWOOD CAPITAL CORP I
(`0001104659-26-094146`), SOI row 81264, a money-market fund; GREAT ELM CAPITAL
CORP. (`0001193125-26-335023`), SOI row 129396, is another explicit
money-market holding. Reported filed-dollar coverage changed from 0.400 to
0.421.

The panel definition is **investment holdings excluding cash and money-market
lines**. This is a deliberate scope decision for Quanta's borrower-to-BDC
relationship view: a money-market fund line does not identify a company that
borrows from the BDC. Some filers include cash in their filed investment total
and some do not, so this single scope rule cannot reconcile every filing to
its filed total. The resulting difference for filers whose totals include cash
is left visible and categorized in the triage report rather than hidden by a
filer-specific exception.

## Investigated, not observed

Superseded or amended filing copies were investigated and not observed: the
raw SUB table has 182 rows, every `prevrpt` value is `0`, and no
`(cik, period, form)` group has more than one accession. The restated copies
that were observed are repeated affiliate/control-table entries inside the
same filing, handled by `rule_issuer_aggregates`, rather than older accession
versions. No rule was added for superseded accession copies.
