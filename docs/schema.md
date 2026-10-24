# Canonical holdings schema (Team 3, release 2026q3)

**Release:** 2026q3, combined from the SEC's monthly releases 2026_07, 2026_08 and 2026_09
(182 filings: 6, 174 and 2). The months are combined into `data/raw/2026q3_bdc/` by
`src/lookthrough/quarter.py`, called from `scripts/acquire.py`. Every combined SOI row keeps
`source_release` and `source_soi_row`, so it traces back to its row in the monthly file.

**How columns are mapped.** Every SOI column header is the label of an XBRL tag. We find the
tag through the TAG table (`tag`, `tlabel`) and map the column to a canonical field by its tag,
never by its header text or position (`mapping.map_soi_columns`). The full evidence, one row per
SOI column with its tag, taxonomy version and usage, is in `reports/soi_columns.csv`
(written by `scripts/soi_columns.py`). Row and filing counts below are current-period rows.

## Canonical fields

| Field | Source tag or axis | SOI column(s) in our release | Type | Notes |
|---|---|---|---|---|
| fair_value | InvestmentOwnedAtFairValue | **Initial fair value of Investment** (81,930 rows, 176 filings); Investment Owned, Fair Value (0 rows) | float, USD | The us-gaap/2026 label for this tag is "Initial fair value of Investment". The us-gaap/2025 label column exists but is empty in all three months. Matching on the text "Fair Value" would find no fair values at all. |
| cost | InvestmentOwnedAtCost | **Adjusted cost basis** (73,547 rows, 172 filings); Investment Owned, Cost (0 rows) | float, USD | Same 2026 label change as fair_value. |
| principal | InvestmentOwnedBalancePrincipalAmount | Investment Owned, Balance, Principal Amount (54,100 rows, 172 filings) | float, USD | Debt holdings only. |
| interest_rate | InvestmentInterestRate | Investment Interest Rate (39,876 rows, 151 filings) | float, decimal (0.0866 = 8.66%) | Median 0.0866. 4 values above 1 (max 9.91) look like percents entered as numbers: flagged for cleaning. |
| spread | InvestmentBasisSpreadVariableRate | Investment, Basis Spread, Variable Rate (45,778 rows, 154 filings) | float, decimal | Median 0.05, max 0.20. |
| maturity | InvestmentMaturityDate | Investment Maturity Date (25,762 rows, 104 filings) | date | Already YYYY-MM-DD in all three months. The kit does not run norm_date on this column; not needed for our release. |
| pik_rate | InvestmentInterestRatePaidInKind | Investment, Interest Rate, Paid in Kind (6,380 rows, 150 filings) | float, decimal | 8 values above 1 (max 8.0): flagged for cleaning. |
| pct_net_assets | InvestmentOwnedPercentOfNetAssets | Investment Owned, Net Assets, Percentage (41,782 rows, 159 filings) | float, decimal (0.002 = 0.2%) | Median 0.002, but 389 values above 1 (max 865.3): subtotal rows or percents entered as numbers. Not used for reconciliation. |
| identifier | Investment, Identifier Axis | Investment, Identifier Axis (77,960 rows, 175 filings) | text | The holding's name, the key for coalescing rows (with adsh and ddate). |
| investment_type | Investment Type Axis | Investment Type Axis (8,764 rows, 167 filings) | text | |
| industry | Industry Sector Axis | Industry Sector Axis (10,096 rows, 157 filings) | text | |
| affiliation | Investment, Issuer Affiliation Axis | Investment, Issuer Affiliation Axis (5,160 rows, 147 filings) | text | Control and affiliate categories (Part 2). |

## Dates

| Table | Columns | Format in our release |
|---|---|---|
| SOI | ddate, period, filed, maturity, acquisition date | YYYY-MM-DD |
| SUB | period, filed | YYYYMMDD |
| NUM | ddate | YYYYMMDD |

`load.norm_date` converts all three tables to YYYY-MM-DD on load. After normalizing, every SOI
row's period equals its filing's period in SUB, and all 177 filings with SOI rows have
current-period rows.

## Columns the starter kit does not map

The release has 256 SOI columns: 12 metadata, 82 axes, 10 mapped value columns and 152
unmapped value columns. The SOI file has a column for every tag any filer used in its schedule
of investments, so most unmapped columns are rare: 59 are used by a single filing.

| Group | Columns | Example (filings) | Decision |
|---|---|---|---|
| Needed for cleaning | 7 | Investment shares (133); unfunded commitments, "Investment Company, Financial Support to Investee Contractually Required, Not Provided, Amount" (30); cash and money-market columns: Cash equivalents (29), Cash and Cash Equivalents, Fair Value Disclosure (21), Cash and cash equivalents (13), "Security deposit remaining" = MoneyMarketFundsAtCarryingValue (36) | **Needed.** Shares identify equity and warrant holdings; the unfunded-commitment and cash columns identify rows the filed total may exclude (Part 2). |
| Descriptive holding details | 6 | Variable rate type (91), acquisition date (74), interest rate floor (65), paid-in-cash rate (25) | Not needed for reconciliation. Kept in the raw data, not in the panel. |
| Derivatives | 37 | Derivative notional amounts (40), contract end dates (29) | Not needed: derivatives are not investments in the filed total. |
| Roll-forward and income | 23 | Affiliate gross additions (23) and reductions (19), dividend income (10), realized and unrealized gains | Not needed: movements and income during the period, not holdings. |
| No tag in TAG (filers' custom elements) | 26 | InvestmentsIdentifier (1 filing, 457 rows), Investee (2 filings, 383 rows) | Not mapped. A filer whose holdings are named only on a custom element has no standard identifier: a Part 2 artifact. |
| Other rare columns | 46 | Concentration percentage (13), short-term investments (4), cash deposits (3) | Not needed; short-term investments and cash deposits are reviewed with the cash rule. |
| No current-period rows | 7 | | Not needed: used only in comparative schedules. |

## Current and comparative schedules

`scripts/parse.py` labels every SOI row by comparing its `ddate` with the filing's period end
(taken from SUB). Rows per filing are in `reports/periods.csv`.

| Schedule | Rule | SOI rows |
|---|---|---|
| current | ddate = the filing's period end | 101,220 |
| comparative | the filing's most common other ddate | 92,709 |
| other | any remaining ddate | 3,231 |

The comparative date is the prior fiscal year end, so it is not always 31 December: 153
filings compare to 2025-12-31, 13 to 2025-09-30, and 3 to 2026-03-31 (for example Capital
Southwest, whose fiscal year ends in March). 3 filings have no comparative schedule. The
"other" rows come mostly from Main Street Capital (678), MSC Income Fund (308), FS KKR (150),
Prospect Capital (126) and Monroe Capital Income Plus (113). Only current rows enter the panel.

## Coalescing and conflicts

Rows are grouped into one holding by (adsh, ddate, identifier), and `source_rows` lists the SOI
row numbers (`soi_row` in the combined `soi.tsv`) of every row that went into it.

- 23,260 of 101,220 current rows have no identifier and are not coalesced: totals,
  subtotals and holdings named only on a custom axis (Part 2).
- 68,136 current holdings in 175 filings; 9,581 were built from more than one SOI row.
- **603 holdings in 16 filings have conflicting values** across their rows
  (`reports/conflicts.csv`). By field: fair_value 336, principal 312, cost 303, pik_rate 250,
  pct_net_assets 41, interest_rate 27, spread 5.

| Cause | Holdings | Resolution |
|---|---|---|
| One loan reported in pieces, one row per subsidiary that holds a piece (Investment Company, Nonconsolidated Subsidiary Axis; 26 filers, mostly Oaktree, Bain, New Mountain, AGL, Carlyle, Lord Abbett, Barings) and **no** row without a subsidiary | 256 | Add up fair value, cost and principal across the pieces |
| Pieces **plus** a row without a subsidiary member. Example: Capital Southwest, ATS Operating LLC First Lien Term Loan A: $4,000,000 tagged CapTrin Partners LLC, $5,250,000 untagged (SOI rows 40608, 49389) | 89 | Keep the untagged row: in XBRL a fact without an axis member is the total across the axis |
| PIK rate: a second row on the Range Axis (Maximum) gives the highest PIK rate the borrower may elect. Example: FS KKR, A-Lign Assurance LLC: 0.0000 on the main row, 0.0300 on the Maximum row (SOI rows 45552, 195153). FS KKR Capital, KKR FS Income Trust and its Select fund, OFS Capital | 250 | Keep the first value, the main row's rate (the kit's rule) |
| Interest rate on two rows (Steele Creek Capital) | 5 | Keep the first value |
| Blue Owl Cross-Strategy Opportunities LLC held by three Blue Owl funds | 3 | Keep the first value; flagged for the agreement check |

**Evidence for the subsidiary rule.** With the kit's two cleaning rules and a 1% tolerance, the
kit's first-value rule admits 79 filings (29.4% of filed dollars); the subsidiary rule admits
80 (30.6%). Oaktree Strategic Credit Fund moves from a gap of -10.76% to +0.27%, and no
admitted filing drops out. The rule is in `src/lookthrough/coalesce.py`.
