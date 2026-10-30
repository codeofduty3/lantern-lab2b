# Triage of non-admitted filings

For each filing: the evidence, the root-cause category, an example (accession number and SOI row), and the fix you applied or why none is possible.

## BLACKSTONE PRIVATE CREDIT FUND (0001803498-26-000048)

- Gap: +9.02%
- Holdings identified: 1921; current SOI rows without an identifier: 402
- Holdings with missing fair value: 24
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 499
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +9.02% ($7,006.9M): holdings $84,656.0M vs filed $77,649.1M. Joint-venture look-through: holdings of Emerald JV LP and Verdelite JV LP (the JVs' own portfolios) are listed beside BCRED's LP interests in those JVs, which the filed total counts. These 659 rows sum to $6,991.9M; without them the gap would be +0.02% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001803498-26-000048 / soi_row 150423 (Port Arthur LNG Phase II Intermediate Company, LLC - Class B Units | Emerald JV LP: $1,085.7M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## BLUE OWL CREDIT INCOME CORP. (0001812554-26-000047)

- Gap: +9.19%
- Holdings identified: 533; current SOI rows without an identifier: 185
- Holdings with missing fair value: 4
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 357
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +9.19% ($3,278.9M): holdings $38,969.1M vs filed $35,690.1M. Rows with neither cost nor principal (e.g. 'LSI Financing LLC | Controlled Affiliates' repeating the schedule holding) plus 'Blue Owl Cross-Strategy Opportunities LLC (BOCSO)' at $1,240.0M, the same value reported by Blue Owl Capital Corp and Blue Owl Technology Income Corp, i.e. the JV's whole value, not this BDC's share. 51% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 14 rows sum to $3,255.6M; without them the gap would be +0.07% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001812554-26-000047 / soi_row 53231 (Blue Owl Cross-Strategy Opportunities LLC (BOCSO): $1,240.0M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## HPS CORPORATE LENDING FUND (0001628280-26-056772)

- Gap: +6.51%
- Holdings identified: 1030; current SOI rows without an identifier: 396
- Holdings with missing fair value: 216
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 249
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +6.50% ($1,571.0M): holdings $25,749.0M vs filed $24,178.0M. The rows without the ' | <issuer affiliation>' suffix carry cost and principal and add up to the gap. Which table they come from is not identified from the data sets. These 22 rows sum to $1,573.3M; without them the gap would be -0.01% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001628280-26-056772 / soi_row 77231 (Emerus Holdings, Inc. 1: $243.0M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## BLUE OWL CAPITAL CORP (0001655888-26-000056)

- Gap: +16.11%
- Holdings identified: 598; current SOI rows without an identifier: 218
- Holdings with missing fair value: 6
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 48
- Negative fair value tagged by investment type in NUM: -8,744,000
- **Evidence:** Gap +26.04% ($3,893.9M): holdings $18,848.9M vs filed $14,955.0M. Rows without the ' | <affiliation>' suffix: affiliated-table issuer rows (e.g. 'Wingspire Capital Holdings LLC') and BOCSO at $1,240.0M (the JV's whole value). 44% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 23 rows sum to $3,893.9M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001655888-26-000056 / soi_row 53229 (Blue Owl Cross-Strategy Opportunities LLC (BOCSO): $1,240.0M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the rows that lack the filer's issuer-affiliation suffix (' | ...'), which repeat or total schedule holdings.

## BLUE OWL TECHNOLOGY FINANCE CORP. (0001747777-26-000028)

- Gap: +6.94%
- Holdings identified: 501; current SOI rows without an identifier: 210
- Holdings with missing fair value: 8
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 44
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +9.67% ($1,419.9M): holdings $16,100.4M vs filed $14,680.5M. Rows with neither cost nor principal (affiliated-table repeats, e.g. 'LSI Financing LLC'). 65% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 111 rows sum to $1,402.0M; without them the gap would be +0.12% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001747777-26-000028 / soi_row 126818 (LSI Financing LLC: $238.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## FS KKR CAPITAL CORP (0001628280-26-053783)

- Gap: +20.37%
- Holdings identified: 670; current SOI rows without an identifier: 102
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 17
- Negative fair value tagged by investment type in NUM: -1,111,000,000
- **Evidence:** Gap +49.61% ($5,664.5M): holdings $17,082.6M vs filed $11,418.1M. Issuer rows with neither cost nor principal repeat the schedule (e.g. 'Credit Opportunities Partners JV, LLC'). The remainder equals the $1,111.0M negative unfunded-commitment fact (InvestmentTypeAxis) the filer nets out of its total. 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 94 rows sum to $4,553.5M; without them the gap would be +9.73%, which equals the $1,111.0M unfunded-commitment fact.
- **Root-cause category:** restated_copies
- **Example:** 0001628280-26-053783 / soi_row 62867 (Credit Opportunities Partners JV, LLC: $1,648.7M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## ARES CORE INFRASTRUCTURE FUND (0002031750-26-000064)

- Gap: +12.63%
- Holdings identified: 79; current SOI rows without an identifier: 125
- Holdings with missing fair value: 11
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 2
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +104.72% ($7,676.4M): holdings $15,006.5M vs filed $7,330.1M. 'Denali Equity Holdings LLC' ($6,118.9M, no cost) equals the sum of the 11 equity rows and 'First lien senior secured loans' ($925.8M) is the loan subtotal; affiliated-table repeats (AEJV, Meade, Redwood) add the rest. These 5 rows sum to $7,676.1M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0002031750-26-000064 / soi_row 73831 (Denali Equity Holdings LLC: $6,118.9M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## OAKTREE STRATEGIC CREDIT FUND (0001872371-26-000013)

- Gap: +3.31%
- Holdings identified: 368; current SOI rows without an identifier: 152
- Holdings with missing fair value: 3
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 36
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** The identifier duplicates the $13.148M OSCF EDL JV fair value in SOI row 146930 and omits cost and principal. The remaining gap after current structural cleaning is not attributed to this rule.
- **Root-cause category:** restated_copies
- **Example:** 0001872371-26-000013 / soi_row 146929 (OSCF EDL JV LLC membership interest)
- **Fix or reason:** No additional rule: the remaining difference is not established from row structure.

## MAIN STREET CAPITAL CORP (0001396440-26-000094)

- Gap: +14.94%
- Holdings identified: 740; current SOI rows without an identifier: 226
- Holdings with missing fair value: 3
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 4
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +14.94% ($858.2M): holdings $6,604.3M vs filed $5,746.0M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 78 rows sum to $858.2M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001396440-26-000094 / soi_row 53647 (Bolder Panther Group, LLC | Secured Debt 1: $101.0M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## PROSPECT CAPITAL CORP (0001287032-26-000269)

- Gap: +2.93%
- Holdings identified: 277; current SOI rows without an identifier: 454
- Holdings with missing fair value: 52
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 89
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +60.82% ($3,857.4M): holdings $10,199.9M vs filed $6,342.6M. Issuer-level rows with neither cost nor principal (e.g. 'National Property REIT Corp.', 'First Tower Finance Company LLC') beside the instrument rows. 9% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 29 rows sum to $3,857.4M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001287032-26-000269 / soi_row 131747 (National Property REIT Corp.: $1,081.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## NORTH HAVEN PRIVATE INCOME FUND LLC (0001193125-26-342549)

- Gap: +8.99%
- Holdings identified: 1109; current SOI rows without an identifier: 219
- Holdings with missing fair value: 286
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 328
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +8.99% ($537.4M): holdings $6,518.1M vs filed $5,980.6M. Rows with neither cost nor principal (e.g. 'Investments - non-controlled/affiliated North Haven Keystone, LLC' repeating the JV interest). 54% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 5 rows sum to $200.1M; without them the gap would be +5.64%; the remainder is not identified from the data sets.
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-342549 / soi_row 99829 (Investments - non-controlled/affiliated North Haven Keystone, LLC: $108.4M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## BLUE OWL TECHNOLOGY INCOME CORP. (0001869453-26-000053)

- Gap: +25.69%
- Holdings identified: 414; current SOI rows without an identifier: 119
- Holdings with missing fair value: 5
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 28
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +28.05% ($1,418.3M): holdings $6,475.2M vs filed $5,056.9M. Rows without the ' | <affiliation>' suffix, mostly BOCSO at $1,240.0M (the JV's whole value, also in two other Blue Owl BDCs) and affiliated-table repeats. 9% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 11 rows sum to $1,468.6M; without them the gap would be -0.99% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001869453-26-000053 / soi_row 53233 (Blue Owl Cross-Strategy Opportunities LLC (BOCSO): $1,240.0M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the rows that lack the filer's issuer-affiliation suffix (' | ...'), which repeat or total schedule holdings.

## MONROE CAPITAL INCOME PLUS CORP (0001742313-26-000046)

- Gap: +1.26%
- Holdings identified: 944; current SOI rows without an identifier: 336
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 240
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +7.47% ($444.8M): holdings $6,401.2M vs filed $5,956.4M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 65 rows sum to $444.8M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001742313-26-000046 / soi_row 137077 (NFS Intermediate HoldCo, LLC (Series B preferred units): $63.8M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## FRANKLIN BSP CAPITAL CORP (0001825248-26-000024)

- Gap: +37.03%
- Holdings identified: 581; current SOI rows without an identifier: 153
- Holdings with missing fair value: 2
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 142
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +37.03% ($1,510.6M): holdings $5,590.0M vs filed $4,079.4M. Rows without the ' | ...' suffix: JV and affiliate rows without cost (e.g. 'FBLC Senior Loan Fund, LLC, Joint Venture') and note-table aggregates ('Top Five Largest Portfolio Company Investments'). 50% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 195 rows sum to $1,510.7M; without them the gap would be -0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001825248-26-000024 / soi_row 80583 (FBLC Senior Loan Fund, LLC, Joint Venture: $218.2M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the rows that lack the filer's issuer-affiliation suffix (' | ...'), which repeat or total schedule holdings.

## BARINGS PRIVATE CREDIT CORP (0001859919-26-000068)

- Gap: +1.34%
- Holdings identified: 878; current SOI rows without an identifier: 254
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 21
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +3.47% ($187.7M): holdings $5,599.8M vs filed $5,412.1M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 6% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 6 rows sum to $198.7M; without them the gap would be -0.20% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001859919-26-000068 / soi_row 162513 (Rocade Holdings LLC: $115.0M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## TPG TWIN BROOK CAPITAL INCOME FUND (0001913724-26-000024)

- Gap: +2.04%
- Holdings identified: 843; current SOI rows without an identifier: 147
- Holdings with missing fair value: 2
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 13
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +4.85% ($233.9M): holdings $5,055.2M vs filed $4,821.3M. Rows with neither cost nor principal (e.g. 'Twin Brook Equity Holdings, LLC' repeating its equity interest). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 3 rows sum to $135.7M; without them the gap would be +2.04%; the remainder is not identified from the data sets.
- **Root-cause category:** restated_copies
- **Example:** 0001913724-26-000024 / soi_row 174563 (Twin Brook Equity Holdings, LLC: $103.1M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## LORD ABBETT PRIVATE CREDIT FUND (0000930413-26-002499)

- Gap: +209.24%
- Holdings identified: 213; current SOI rows without an identifier: 235
- Holdings with missing fair value: 3
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 0
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +309.45% ($4,838.8M): holdings $6,402.4M vs filed $1,563.7M. Every identifier is an XBRL member; category and industry members ('Investments at Fair Value [Member]' equals the filed total itself, 'First Lien Secured Debt [Member]', industry members) are totals counted as holdings. These 35 rows sum to $4,642.6M; without them the gap would be +12.55%; the remainder is not identified from the data sets.
- **Root-cause category:** totals_counted
- **Example:** 0000930413-26-002499 / soi_row 106977 (Investments at Fair Value [Member]: $1,563.7M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## BAIN CAPITAL SPECIALTY FINANCE, INC. (0001193125-26-342491)

- Gap: +97.05%
- Holdings identified: 874; current SOI rows without an identifier: 358
- Holdings with missing fair value: 179
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 95
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +97.05% ($2,293.9M): holdings $4,657.5M vs filed $2,363.6M. Joint-venture look-through: rows without the filer's 'Non-controlled/... Investments' / 'Controlled Affiliate Investments' prefix (e.g. 'Aerospace & Defense ATS First Lien ...') are the portfolios of its loan programs (International Senior Loan Program, Bain Capital Senior Loan Program); the prefixed rows alone sum to the filed total. These 191 rows sum to $2,293.5M; without them the gap would be +0.02% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001193125-26-342491 / soi_row 40494 (Services: Business Easy Ice First Lien Senior Secured Loan SOFR Floor 1.00% Spread 5.40% I: $39.4M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## NEW MOUNTAIN FINANCE CORP (0001496099-26-000029)

- Gap: +77.36%
- Holdings identified: 497; current SOI rows without an identifier: 181
- Holdings with missing fair value: 11
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 13
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +98.17% ($2,247.8M): holdings $4,537.6M vs filed $2,289.8M. Joint-venture look-through: 'Funded Investments - ...' rows are the portfolios of NMFC's senior loan programs; issuer rows without cost or principal repeat the schedule. These 130 rows sum to $2,245.2M; without them the gap would be +0.11% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001496099-26-000029 / soi_row 137183 (NMFC Senior Loan Program III LLC: $157.9M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## PENNANTPARK FLOATING RATE CAPITAL LTD. (0001193125-26-342352)

- Gap: +58.29%
- Holdings identified: 725; current SOI rows without an identifier: 93
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 67
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +58.29% ($1,460.0M): holdings $3,964.7M vs filed $2,504.7M. Joint-venture look-through: the 'First Lien Secured ...' rows are the portfolio of PennantPark Senior Secured Loan Fund (PSSL), listed beside PFLT's own schedule ('Inv in NCNA Prtfl Comp ...'). These 174 rows sum to $1,436.1M; without them the gap would be +0.95% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001193125-26-342352 / soi_row 82635 (First Lien Secured Debt Issuer Name Beacon Behavioral Support Services, LLC Acquisition 10: $24.8M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## MORGAN STANLEY DIRECT LENDING FUND (0001193125-26-337915)

- Gap: +9.21%
- Holdings identified: 1036; current SOI rows without an identifier: 159
- Holdings with missing fair value: 283
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 386
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +12.93% ($459.7M): holdings $4,014.0M vs filed $3,554.3M. Rows with neither cost nor principal (e.g. 'Capstone Lending LLC' repeating the JV equity interest). 76% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 5 rows sum to $135.3M; without them the gap would be +9.13%; the remainder is not identified from the data sets.
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-337915 / soi_row 55783 (Capstone Lending LLC: $102.5M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## CARLYLE SECURED LENDING, INC. (0001544206-26-000055)

- Gap: +62.16%
- Holdings identified: 351; current SOI rows without an identifier: 264
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 223
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +62.16% ($1,466.9M): holdings $3,826.9M vs filed $2,360.0M. Joint-venture look-through: 'Credit Fund | ...' rows are the portfolio of Middle Market Credit Fund; issuer rows without cost or principal repeat the JV interests. These 86 rows sum to $1,466.9M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001544206-26-000055 / soi_row 129590 (Middle Market Credit Fund, LLC, Subordinated Loan and Members Interest: $123.8M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## KKR FS INCOME TRUST (0001628280-26-056131)

- Gap: +23.75%
- Holdings identified: 502; current SOI rows without an identifier: 53
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 18
- Negative fair value tagged by investment type in NUM: -511,012,000
- **Evidence:** Gap +23.75% ($629.1M): holdings $3,278.2M vs filed $2,649.2M. The filer nets $511.0M of unfunded commitments (negative InvestmentTypeAxis fact in NUM) out of its filed total; affiliated-issuer rows with neither cost nor principal add the rest of the gap. Rows without cost or principal: 26 rows, $118.0M; with the netted $511.0M the gap would be +0.00%.
- **Root-cause category:** unfunded_commitments
- **Example:** 0001628280-26-056131 / soi_row 44847 (Affiliated Issuer | KSC I Aircraft LP, ABF Equity: $59.2M)
- **Fix or reason:** None by dropping rows: the filer nets unfunded commitments out of its filed total (negative InvestmentTypeAxis fact in NUM). Reconciling needs a documented adjustment for that NUM fact (Part 2), not a row filter.

## OAKTREE SPECIALTY LENDING CORP (0001414932-26-000017)

- Gap: +18.88%
- Holdings identified: 539; current SOI rows without an identifier: 146
- Holdings with missing fair value: 7
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 34
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +18.88% ($517.7M): holdings $3,259.5M vs filed $2,741.8M. The excess is not attributable to an identifiable group of rows (no issuer totals, repeats or JV suffix group matches the gap); OCSL's JVs (Senior Loan Fund, OCSI Glick JV) may be partly listed.
- **Root-cause category:** other
- **Example:** 0001414932-26-000017 / soi_row 164805 (Senior Loan Fund JV I, LLC, Multi-Sector Holdings, Subordinated Debt: $84.5M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## MIDCAP FINANCIAL INVESTMENT CORP (0001193125-26-335848)

- Gap: +8.94%
- Holdings identified: 638; current SOI rows without an identifier: 656
- Holdings with missing fair value: 60
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 95
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +10.97% ($304.0M): holdings $3,074.4M vs filed $2,770.3M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 83% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 26 rows sum to $304.2M; without them the gap would be -0.01% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-335848 / soi_row 61719 (Controlled Investments Merx Aviation Finance, LLC, Membership Interests: $68.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## TRINITY CAPITAL INC. (0001193125-26-333907)

- Gap: +7.84%
- Holdings identified: 554; current SOI rows without an identifier: 258
- Holdings with missing fair value: 66
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 60
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +7.84% ($214.3M): holdings $2,946.6M vs filed $2,732.3M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 30% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 25 rows sum to $226.0M; without them the gap would be -0.43% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001193125-26-333907 / soi_row 61482 (Control Investments Trin H OpCo I LLC: $32.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## GOLDMAN SACHS BDC, INC. (0001193125-26-338331)

- Gap: -9.69%
- Holdings identified: 511; current SOI rows without an identifier: 124
- Holdings with missing fair value: 2
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 45
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -9.69% (-$309.6M): holdings $2,885.6M vs filed $3,195.2M. Holdings fall short of the filed total. NUM's per-holding facts give the same sum as the SOI, so the shortfall is in the filer's tagging (two holdings have no fair value in SOI); no NUM fact matches it.
- **Root-cause category:** other
- **Example:** 0001193125-26-338331 / soi_row 97793 (Investment Debt Investments  232.7% United States  219.9% 1st Lien/Senior Secured Debt  20: $74.2M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## BAIN CAPITAL PRIVATE CREDIT (0001193125-26-349812)

- Gap: +29.89%
- Holdings identified: 516; current SOI rows without an identifier: 206
- Holdings with missing fair value: 39
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 86
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +29.89% ($662.5M): holdings $2,878.9M vs filed $2,216.4M. Joint-venture look-through: rows without the 'Non-controlled/... Investments' / 'Controlled Affiliate' prefix are the loan program's portfolio (as for Bain Capital Specialty Finance). These 87 rows sum to $662.4M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001193125-26-349812 / soi_row 40214 (Consumer Goods: Non-Durable Summer Fridays, LLC First Lien Senior Secured Loan SOFR Floor : $16.1M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## CARLYLE CREDIT SOLUTIONS, INC. (0001702510-26-000084)

- Gap: +1.38%
- Holdings identified: 297; current SOI rows without an identifier: 243
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 198
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.38% ($37.9M): holdings $2,787.5M vs filed $2,749.7M. Rows with neither cost nor principal ('Investments | Affiliated ...' repeats). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 5 rows sum to $37.9M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001702510-26-000084 / soi_row 106956 (Investments | Affiliated Issuer | Align Precision Group, LLC 1: $21.4M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## GOLUB CAPITAL BDC 4, INC. (0001901612-26-000031)

- Gap: +1.17%
- Holdings identified: 922; current SOI rows without an identifier: 145
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** The filing has many repeated zero and small fair values across distinct 'One stop' instruments; no duplicate issuer summary was established from row structure alone.
- **Root-cause category:** other
- **Example:** 0001901612-26-000031 / soi_row 43816 (Action Termite Control LLC common stock)
- **Fix or reason:** No additional rule: the remaining difference is not established from the data set.

## CAPITAL SOUTHWEST CORP (0000017313-26-000095)

- Gap: +22.01%
- Holdings identified: 578; current SOI rows without an identifier: 290
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 260
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +26.45% ($582.6M): holdings $2,784.9M vs filed $2,202.3M. Holdings appear twice with identifiers that differ only in case (e.g. 'ITA HOLDINGS' and 'ITA Holdings'), and 'CapTrin Partners' appears without cost. These 72 rows sum to $446.0M; without them the gap would be +6.20%; the remainder is not identified from the data sets.
- **Root-cause category:** restated_copies
- **Example:** 0000017313-26-000095 / soi_row 40610 (CapTrin Partners, LLC: $97.8M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: coalesce identifiers that differ only in case/punctuation and drop no-cost repeats.

## SARATOGA INVESTMENT CORP. (0001213900-26-075931)

- Gap: +127.40%
- Holdings identified: 436; current SOI rows without an identifier: 33
- Holdings with missing fair value: 31
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 14
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +227.40% ($2,561.3M): holdings $3,687.6M vs filed $1,126.3M. Rows without principal are subtotals ('Sub Total Non-control/Non-affiliate investments', '... - Total <industry>'), plus about $370.8M of rows from the Saratoga CLO portfolio. These 283 rows sum to $2,561.1M; without them the gap would be +0.02% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001213900-26-075931 / soi_row 7382 (Sub Total Non-control/Non-affiliate investments: $1,034.7M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## CION INVESTMENT CORP (0001534254-26-000010)

- Gap: +40.56%
- Holdings identified: 358; current SOI rows without an identifier: 58
- Holdings with missing fair value: 37
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 13
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +40.56% ($730.2M): holdings $2,530.3M vs filed $1,800.1M. Rows with neither cost nor principal (affiliated-table issuer rows, e.g. 'David's Bridal'). 98% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 56 rows sum to $680.1M; without them the gap would be +2.78%; the remainder is not identified from the data sets.
- **Root-cause category:** restated_copies
- **Example:** 0001534254-26-000010 / soi_row 126529 (Longview Intermediate Holdings C, LLC | Membership Units | Non-Controlled,AffiliatedInvest: $108.8M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## BARINGS BDC, INC. (0001379785-26-000030)

- Gap: +1.34%
- Holdings identified: 705; current SOI rows without an identifier: 240
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 21
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.34% ($33.1M): holdings $2,491.6M vs filed $2,458.6M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 14% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 4 rows sum to $33.1M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001379785-26-000030 / soi_row 76109 (Eclipse Business Capital Holdings LLC | Revolver | Funded: $12.9M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## PENNANTPARK INVESTMENT CORP (0001193125-26-342350)

- Gap: +107.13%
- Holdings identified: 611; current SOI rows without an identifier: 67
- Holdings with missing fair value: 7
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 51
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +137.18% ($1,636.8M): holdings $2,830.0M vs filed $1,193.2M. Joint-venture look-through: 'First Lien ...' rows are the portfolio of PennantPark Senior Secured Loan Fund; issuer rows without cost or principal repeat the JV interests. These 121 rows sum to $1,624.1M; without them the gap would be +1.06%; the remainder is not identified from the data sets.
- **Root-cause category:** other
- **Example:** 0001193125-26-342350 / soi_row 148783 (PennantPark Senior Loan Fund, LLC: $191.9M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## SLR INVESTMENT CORP. (0001193125-26-332726)

- Gap: +8.62%
- Holdings identified: 110; current SOI rows without an identifier: 60
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 13
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +8.62% ($180.9M): holdings $2,280.2M vs filed $2,099.3M. Rows without the filer's asset-class prefix (single-name rows, e.g. 'Western Veterinary ...'); the prefixed rows alone sum to the filed total. These look like a joint venture's portfolio, but this is not confirmed in the filing. These 25 rows sum to $180.9M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001193125-26-332726 / soi_row 180535 (Western Veterinary Partners LLC | Diversified Consumer Services | S+525 | 1.00% | 8.95% | : $15.0M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the joint venture's own portfolio rows and keep only the BDC's interest in the JV, which the filed total counts.

## FIDELITY PRIVATE CREDIT FUND (0001193125-26-346851)

- Gap: -7.95%
- Holdings identified: 384; current SOI rows without an identifier: 271
- Holdings with missing fair value: 32
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 0
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -7.95% (-$196.8M): holdings $2,279.7M vs filed $2,476.5M. NUM has InvestmentOwnedAtFairValue on CashAndCashEquivalentsAxis = $196.8M, exactly the shortfall: the filed total includes cash equivalents that are not schedule holdings.
- **Root-cause category:** cash_lines
- **Example:** 0001193125-26-346851 / NUM InvestmentOwnedAtFairValue on CashAndCashEquivalentsAxis at 2026-06-30: 2 facts, $196.8M; no SOI row
- **Fix or reason:** None from SOI: the filed total includes cash equivalents / short-term investments that are not schedule holdings with an identifier. They exist only as NUM facts; adding them would be a NUM recovery (stretch goal), not applied.

## T SERIES BDC LLC (0001193125-26-344703)

- Gap: +2.01%
- Holdings identified: 833; current SOI rows without an identifier: 163
- Holdings with missing fair value: 272
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 299
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +2.01% ($44.6M): holdings $2,261.4M vs filed $2,216.8M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 0% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 4 rows sum to $44.6M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001193125-26-344703 / soi_row 108445 (Investments in Non-Controlled, Affiliated First Lien Debt DCA Buyer, LLC: $21.3M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## KAYNE ANDERSON BDC, INC. (0001193125-26-342385)

- Gap: -1.69%
- Holdings identified: 335; current SOI rows without an identifier: 57
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 67
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -1.69% (-$38.8M): holdings $2,253.0M vs filed $2,291.8M. Holdings fall short of the filed total; NUM's per-holding facts give the same sum, and its money-market line has no fair value in SOI. No NUM fact matches the shortfall.
- **Root-cause category:** other
- **Example:** 0001193125-26-342385 / soi_row 65127 (Debt Investments - Financial services - SGCP Intermediate, Inc. (SG Credit) - First lien s: $80.0M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## NEW MOUNTAIN PRIVATE CREDIT FUND (0002037804-26-000015)

- Gap: +17.86%
- Holdings identified: 465; current SOI rows without an identifier: 187
- Holdings with missing fair value: 8
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 11
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +17.86% ($326.4M): holdings $2,154.0M vs filed $1,827.6M. The excess is not attributable to an identifiable group of rows; the NEWCRED Senior Loan Program interest is held, but its portfolio rows are not separable by identifier.
- **Root-cause category:** other
- **Example:** 0002037804-26-000015 / soi_row 136856 (NEWCRED Senior Loan Program I LLC | Membership Interest | Non-Affiliated Issuer: $68.0M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## FORTRESS PRIVATE LENDING FUND (0001193125-26-344953)

- Gap: +4.20%
- Holdings identified: 171; current SOI rows without an identifier: 142
- Holdings with missing fair value: 8
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 58
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +4.20% ($80.6M): holdings $1,999.7M vs filed $1,919.1M. The excess is not attributable to an identifiable group of rows.
- **Root-cause category:** other
- **Example:** 0001193125-26-344953 / soi_row 112558 (Investments NCNA Inv. Debt Inv. Capital Goods Blue Raven Solutions, LLC, Triman Industries: $69.4M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## KKR FS INCOME TRUST SELECT (0001628280-26-056136)

- Gap: +21.92%
- Holdings identified: 432; current SOI rows without an identifier: 50
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 17
- Negative fair value tagged by investment type in NUM: -279,581,000
- **Evidence:** Gap +21.92% ($340.5M): holdings $1,894.0M vs filed $1,553.5M. The filer nets $279.6M of unfunded commitments (negative InvestmentTypeAxis fact in NUM) out of its filed total; affiliated-issuer rows with neither cost nor principal add the rest of the gap. Rows without cost or principal: 19 rows, $60.9M; with the netted $279.6M the gap would be +0.00%.
- **Root-cause category:** unfunded_commitments
- **Example:** 0001628280-26-056136 / soi_row 44850 (Affiliated Issuer | KSC I Aircraft LP, ABF Equity: $37.0M)
- **Fix or reason:** None by dropping rows: the filer nets unfunded commitments out of its filed total (negative InvestmentTypeAxis fact in NUM). Reconciling needs a documented adjustment for that NUM fact (Part 2), not a row filter.

## 26NORTH BDC, INC. (0001193125-26-340235)

- Gap: -2.07%
- Holdings identified: 144; current SOI rows without an identifier: 10
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 47
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -2.07% (-$37.4M): holdings $1,768.8M vs filed $1,806.2M. The filer's custom fact InvestmentOwnedAtFairValueExcludingShortTermInvestments ($1,768.8M) equals the holdings sum exactly, so the filed total includes short-term investments that are not schedule holdings.
- **Root-cause category:** cash_lines
- **Example:** 0001193125-26-340235 / NUM InvestmentOwnedAtFairValueExcludingShortTermInvestments (undimensioned, 2026-06-30) = $1,768.8M; no SOI row
- **Fix or reason:** None from SOI: the filed total includes cash equivalents / short-term investments that are not schedule holdings with an identifier. They exist only as NUM facts; adding them would be a NUM recovery (stretch goal), not applied.

## CRESCENT CAPITAL BDC, INC. (0001193125-26-342351)

- Gap: -1.12%
- Holdings identified: 639; current SOI rows without an identifier: 131
- Holdings with missing fair value: 69
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 67
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -1.12% (-$17.5M): holdings $1,553.1M vs filed $1,570.7M. Holdings fall short of the filed total; 69 holdings have no fair value in SOI, and NUM's per-holding facts give the same sum. No NUM fact matches the shortfall.
- **Root-cause category:** other
- **Example:** 0001193125-26-342351 / soi_row 116133 (Investments United States Equity Investments Diversified Financials First Eagle Logan JV, : $27.9M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## AGL PRIVATE CREDIT INCOME FUND (0001193125-26-334994)

- Gap: +21.25%
- Holdings identified: 275; current SOI rows without an identifier: 86
- Holdings with missing fair value: 64
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 41
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +21.25% ($267.1M): holdings $1,523.9M vs filed $1,256.9M. The 99 rows styled 'Investments Industry ...' plus a Goldman Sachs government money-market line add up to the gap; the 'Investments Non-controlled/...' rows alone sum to the filed total. Which table the 'Investments Industry' rows come from is not identified from the data sets. These 82 rows sum to $267.1M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** other
- **Example:** 0001193125-26-334994 / soi_row 108006 (Investments Goldman Sachs Financial Square Government Institutional Fund: $24.4M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## OVERLAND ADVANTAGE (0001193125-26-346556)

- Gap: -6.63%
- Holdings identified: 42; current SOI rows without an identifier: 26
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 41
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -6.63% (-$107.4M): holdings $1,511.9M vs filed $1,619.3M. The filer's custom fact FairValueExcludeInvestmentInUSTreasuryBills ($1,511.9M) equals the holdings sum exactly, so the filed total includes US Treasury bills that are not schedule holdings.
- **Root-cause category:** cash_lines
- **Example:** 0001193125-26-346556 / NUM FairValueExcludeInvestmentInUSTreasuryBills (undimensioned, 2026-06-30) = $1,511.9M; no SOI row
- **Fix or reason:** None from SOI: the filed total includes cash equivalents / short-term investments that are not schedule holdings with an identifier. They exist only as NUM facts; adding them would be a NUM recovery (stretch goal), not applied.

## MSC INCOME FUND, INC. (0001535778-26-000085)

- Gap: +4.42%
- Holdings identified: 504; current SOI rows without an identifier: 171
- Holdings with missing fair value: 3
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 4
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +4.42% ($61.4M): holdings $1,450.8M vs filed $1,389.4M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 98% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 26 rows sum to $62.4M; without them the gap would be -0.07% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001535778-26-000085 / soi_row 160316 (RA Outdoors LLC | Secured Debt 2.1: $12.7M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## BLACKROCK TCP CAPITAL CORP. (0001193125-26-336794)

- Gap: +11.40%
- Holdings identified: 349; current SOI rows without an identifier: 86
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 1
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +11.40% ($147.2M): holdings $1,437.7M vs filed $1,290.5M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 21 rows sum to $147.2M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-336794 / soi_row 61619 (Controlled Affiliates, 36th Street Capital Partners Holdings, LLC, Senior Note, 12%, due 1: $59.8M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## LORD ABBETT PRIVATE CREDIT FUND S (0000930413-26-002500)

- Gap: +217.70%
- Holdings identified: 205; current SOI rows without an identifier: 153
- Holdings with missing fair value: 9
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 0
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +318.49% ($1,368.8M): holdings $1,798.5M vs filed $429.8M. As for the other Lord Abbett fund: category and industry members on the identifier axis are totals counted as holdings. These 33 rows sum to $1,263.4M; without them the gap would be +24.52%; the remainder is not identified from the data sets.
- **Root-cause category:** totals_counted
- **Example:** 0000930413-26-002500 / soi_row 106979 (Investments at Fair Value [Member]: $429.8M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## GLADSTONE INVESTMENT CORPORATIONDE (0001321741-26-000017)

- Gap: +6.24%
- Holdings identified: 75; current SOI rows without an identifier: 79
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 16
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +6.23% ($79.9M): holdings $1,361.9M vs filed $1,282.0M. Rows without cost (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 6 rows sum to $79.9M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001321741-26-000017 / soi_row 175372 (UPB Acquisition, Inc. - Preferred Stock: $29.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## BARINGS CAPITAL INVESTMENT CORP (0001811972-26-000018)

- Gap: +1.35%
- Holdings identified: 653; current SOI rows without an identifier: 177
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 21
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.35% ($18.0M): holdings $1,350.3M vs filed $1,332.3M. Two rows without the ' | ...' suffix. 0% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 2 rows sum to $18.0M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001811972-26-000018 / soi_row 50780 (Banff Partners LP: $14.7M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: drop the rows that lack the filer's issuer-affiliation suffix (' | ...'), which repeat or total schedule holdings.

## SILVER POINT SPECIALTY LENDING FUND (0001193125-26-337440)

- Gap: +4.32%
- Holdings identified: 210; current SOI rows without an identifier: 160
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 62
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +4.41% ($50.6M): holdings $1,199.0M vs filed $1,148.4M. Rows without cost ('Fund's ...' affiliated-table repeats). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 9 rows sum to $52.7M; without them the gap would be -0.18% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-337440 / soi_row 85868 (Fund's affiliated/non-controlled investments Portfolio Company Takko Fashion Sarl Type of : $12.4M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## OXFORD SQUARE CAPITAL CORP. (0001213900-26-087243)

- Gap: +7524.54%
- Holdings identified: 98; current SOI rows without an identifier: 1
- Holdings with missing fair value: 13
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 26
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +7524.54% ($1,159.5M): holdings $1,174.9M vs filed $15.4M. The undimensioned InvestmentOwnedAtFairValue fact is only $15.4M, while the affiliation-axis facts in NUM sum to $252.8M (= 'Investments in Securities and Cash Equivalents' $285.6M minus cash equivalents $32.8M). The schedule also carries hierarchical subtotals ('Senior Secured Notes - United States - ...'). These 67 rows sum to $1,097.8M; without them the gap would be +400.82%; the remainder is not identified from the data sets.
- **Root-cause category:** other
- **Example:** 0001213900-26-087243 / soi_row 112095 (Investments in Securities and Cash Equivalents: $285.6M)
- **Fix or reason:** None possible: the filed total in NUM is not the portfolio total, so no row-level cleaning can reconcile it.

## AUDAX PRIVATE CREDIT FUND, LLC (0001193125-26-351877)

- Gap: +1.63%
- Holdings identified: 620; current SOI rows without an identifier: 249
- Holdings with missing fair value: 184
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 28
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.63% ($18.4M): holdings $1,145.9M vs filed $1,127.5M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 6 rows sum to $18.4M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-351877 / soi_row 152571 (Portfolio Company Heritage Partners Investment Type Bank Loans: $6.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## PHENIXFIN CORP (0001213900-26-085667)

- Gap: n/a
- Holdings identified: 95; current SOI rows without an identifier: 73
- Holdings with missing fair value: 5
- No filed total in NUM: True
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 29
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. It reports InvestmentsFairValueDisclosure = $301.6M instead, which is not the required fact. Holdings identified: 97, $1,206.5M.
- **Root-cause category:** no_filed_total
- **Example:** 0001213900-26-085667 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## OAKTREE GARDENS OLP, LLC (0001974793-26-000013)

- Gap: +1.76%
- Holdings identified: 81; current SOI rows without an identifier: 42
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 23
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** A few distinct instruments share small or zero fair values; no aggregate/category row remains after the structural rules.
- **Root-cause category:** other
- **Example:** 0001974793-26-000013 / soi_row 46981 (Angel Lux Bidco first-lien term loan)
- **Fix or reason:** No additional rule: the remaining difference is not established from the data set.

## JOHN HANCOCK COMVEST PRIVATE INCOME FUND (0001193125-26-349413)

- Gap: +1.79%
- Holdings identified: 217; current SOI rows without an identifier: 33
- Holdings with missing fair value: 18
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 8
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.79% ($16.7M): holdings $950.1M vs filed $933.4M. Rows with neither cost nor principal ('Affiliated investments ...' repeats). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 4 rows sum to $16.7M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-349413 / soi_row 44737 (Affiliated investments Calidris Investment Partners Holdings Ltd - Term Loan First Lien Se: $8.2M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## WHITEHORSE FINANCE, INC. (0001104659-26-093465)

- Gap: +63.71%
- Holdings identified: 250; current SOI rows without an identifier: 174
- Holdings with missing fair value: 20
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 141
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +63.71% ($362.6M): holdings $931.8M vs filed $569.2M. The excess is not attributable to an identifiable group of rows; the 'WHF STRS' JV rows and a few rows without cost explain only part.
- **Root-cause category:** other
- **Example:** 0001104659-26-093465 / soi_row 180660 (WHF STRS Ohio Senior Loan Fund LLC Subordinated Note: $86.3M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## PHILLIP STREET BDC LLC (0001193125-26-344614)

- Gap: n/a
- Holdings identified: 262; current SOI rows without an identifier: 57
- Holdings with missing fair value: 0
- No filed total in NUM: True
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. It reports InvestmentsFairValueDisclosure = $998.2M instead, which is not the required fact. Holdings identified: 262, $920.6M.
- **Root-cause category:** no_filed_total
- **Example:** 0001193125-26-344614 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## TCW SPECIALTY LENDING LLC (0001193125-26-346673)

- Gap: +20.89%
- Holdings identified: 88; current SOI rows without an identifier: 38
- Holdings with missing fair value: 14
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 35
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +20.89% ($149.4M): holdings $864.4M vs filed $715.0M. Rows with neither cost nor principal ('Non-Controlled Affiliated Investments ...' repeats). 50% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 8 rows sum to $149.4M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-346673 / soi_row 138858 (Non-Controlled Affiliated Investments: $74.7M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## TCW DIRECT LENDING VII LLC (0001193125-26-346651)

- Gap: +36.70%
- Holdings identified: 91; current SOI rows without an identifier: 26
- Holdings with missing fair value: 18
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 73
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +36.70% ($222.8M): holdings $829.9M vs filed $607.1M. Rows with neither cost nor principal ('Non-Controlled Affiliated Investments ...' repeats). 50% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 11 rows sum to $222.8M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-346651 / soi_row 138855 (Non-Controlled Affiliated Investments: $111.4M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## VARAGON CAPITAL CORP (0001193125-26-344075)

- Gap: -1.30%
- Holdings identified: 369; current SOI rows without an identifier: 288
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 70
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -1.30% (-$10.8M): holdings $825.8M vs filed $836.6M. Holdings fall short of the filed total; NUM's per-holding facts give the same sum and no NUM fact matches the shortfall.
- **Root-cause category:** other
- **Example:** 0001193125-26-344075 / soi_row 61741 (Controlled Investments, Industry Investment Funds and Vehicles, Company Senior Direct Lend: $171.9M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## BLUE OWL CAPITAL CORP II (0001655887-26-000016)

- Gap: +6.73%
- Holdings identified: 376; current SOI rows without an identifier: 134
- Holdings with missing fair value: 138
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 184
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +10.50% ($72.6M): holdings $763.5M vs filed $691.0M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 0% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 10 rows sum to $72.1M; without them the gap would be +0.07% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001655887-26-000016 / soi_row 136792 (New PLI Holdings, LLC (dba PLI): $25.8M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## TCW DIRECT LENDING VIII LLC (0001193125-26-346657)

- Gap: +11.04%
- Holdings identified: 78; current SOI rows without an identifier: 38
- Holdings with missing fair value: 5
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 45
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +11.04% ($72.7M): holdings $731.7M vs filed $659.0M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 7 rows sum to $72.7M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-346657 / soi_row 75978 (EagleRock Land LLC Class A Units: $40.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## 5C LENDING PARTNERS CORP. (0001193125-26-334649)

- Gap: -1.41%
- Holdings identified: 57; current SOI rows without an identifier: 32
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 60
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -1.41% (-$10.0M): holdings $697.3M vs filed $707.2M. Holdings fall short of the filed total; its money-market line ('Company Total Cash Equivalents BlackRock Liquidity Funds ...') has no fair value in SOI, and no NUM fact matches the shortfall.
- **Root-cause category:** other
- **Example:** 0001193125-26-334649 / soi_row 60406 (Company Non-controlled, non-affiliated investments Debt Investments Professional Services : $62.3M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## MUZINICH BDC, INC. (0001213900-26-089024)

- Gap: n/a
- Holdings identified: 53; current SOI rows without an identifier: 40
- Holdings with missing fair value: 9
- No filed total in NUM: True
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 17
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. Holdings identified: 54, $814.1M.
- **Root-cause category:** no_filed_total
- **Example:** 0001213900-26-089024 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## BCP INVESTMENT CORP (0001193125-26-337959)

- Gap: +46.99%
- Holdings identified: 237; current SOI rows without an identifier: 96
- Holdings with missing fair value: 40
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 111
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +68.93% ($312.1M): holdings $764.8M vs filed $452.7M. Rows without cost (affiliated/controlled-investments table rows). 34% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 41 rows sum to $312.3M; without them the gap would be -0.05% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001193125-26-337959 / soi_row 137254 (Non Controlled Affiliated and Controlled Investments [Member]: $106.4M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## WEST BAY BDC LLC (0001193125-26-344618)

- Gap: -4.19%
- Holdings identified: 145; current SOI rows without an identifier: 25
- Holdings with missing fair value: 7
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -4.19% (-$25.5M): holdings $583.1M vs filed $608.5M. Holdings fall short of the filed total; 7 holdings have no fair value in SOI, and NUM's per-holding facts give the same sum. No NUM fact matches the shortfall.
- **Root-cause category:** other
- **Example:** 0001193125-26-344618 / soi_row 64505 (Debt Investments - 209.2% United States - 209.2% 1st Lien/Senior Secured Debt - 203.7% Spe: $25.0M)
- **Fix or reason:** No fix: the root cause is not identified from the data sets alone; it needs a read of the filing's schedule.

## FIRST EAGLE PRIVATE CREDIT FUND (0001193125-26-349367)

- Gap: n/a
- Holdings identified: 189; current SOI rows without an identifier: 90
- Holdings with missing fair value: 16
- No filed total in NUM: True
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 116
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. It reports InvestmentsFairValueDisclosure = $552.9M instead, which is not the required fact. Holdings identified: 189, $550.9M.
- **Root-cause category:** no_filed_total
- **Example:** 0001193125-26-349367 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## LGAM PRIVATE CREDIT LLC (0001193125-26-344644)

- Gap: +1.40%
- Holdings identified: 576; current SOI rows without an identifier: 145
- Holdings with missing fair value: 201
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 223
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.40% ($7.4M): holdings $534.7M vs filed $527.3M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 0% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 2 rows sum to $7.4M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001193125-26-344644 / soi_row 108442 (Investments in Non-Controlled, Affiliated First Lien Debt DCA Buyer, LLC: $6.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## ADVANCED FLOWER CAPITAL INC. (0001628280-26-056471)

- Gap: +70.19%
- Holdings identified: 19; current SOI rows without an identifier: 16
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 17
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +70.19% ($203.4M): holdings $493.1M vs filed $289.8M. Two industry subtotal rows ('Cannabis', 'Leisure Products') equal the sum of the '<industry> | <company>' rows beneath them. These 2 rows sum to $203.4M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001628280-26-056471 / soi_row 55618 (Cannabis: $198.4M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## MUZINICH CORPORATE LENDING INCOME FUND, INC. (0001213900-26-089203)

- Gap: n/a
- Holdings identified: 114; current SOI rows without an identifier: 38
- Holdings with missing fair value: 2
- No filed total in NUM: True
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 0
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. It reports InvestmentsFairValueDisclosure = $102.4M instead, which is not the required fact. Holdings identified: 117, $591.1M.
- **Root-cause category:** no_filed_total
- **Example:** 0001213900-26-089203 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## PGIM PRIVATE CREDIT FUND (0001193125-26-349252)

- Gap: +1.00%
- Holdings identified: 186; current SOI rows without an identifier: 136
- Holdings with missing fair value: 5
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 168
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +1.00% ($4.3M): holdings $434.2M vs filed $429.9M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 2 rows sum to $4.3M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-349252 / soi_row 61516 (Controlled - Affiliated Investments - Equity, Entertainment Earth, LLC: $3.3M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## STEELE CREEK CAPITAL CORP (0001213900-26-089899)

- Gap: +300.00%
- Holdings identified: 295; current SOI rows without an identifier: 7
- Holdings with missing fair value: 3
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 0
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +300.00% ($323.0M): holdings $430.6M vs filed $107.7M. Hierarchical identifiers with a subtotal row at each level (industry, country, affiliation category), e.g. '... - Investments made in Austria - Capital Equipment'; these subtotal rows have no principal. These 64 rows sum to $323.0M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001213900-26-089899 / soi_row 140829 (Non-controlled/Non-Affiliated Investments -216.2% of Shareholder's Equity: $107.7M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## GOLUB CAPITAL PRIVATE INCOME FUND I (0002082559-26-000086)

- Gap: -3.10%
- Holdings identified: 310; current SOI rows without an identifier: 131
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -5.30% (-$23.3M): holdings $416.0M vs filed $439.2M. The money-market holding 'Morgan Stanley Institutional Liquidity Funds - Treasury Portfolio ...' has no fair value in SOI; its value ($9.6M) is only in the custom tag MoneyMarketFundsAtCarryingValue. This explains part of the shortfall; the rest is not identified.
- **Root-cause category:** custom_tags
- **Example:** 0002082559-26-000086 / soi_row 130821 (Morgan Stanley Institutional Liquidity Funds - Treasury Portfolio Institutional Share Clas: no fair value in SOI)
- **Fix or reason:** Not applied: the fair value sits only in a custom tag in NUM (stretch goal: recover custom-tag values from NUM).

## OFS CAPITAL CORP (0001487918-26-000078)

- Gap: +38.90%
- Holdings identified: 118; current SOI rows without an identifier: 94
- Holdings with missing fair value: 14
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 39
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +38.90% ($115.8M): holdings $413.6M vs filed $297.8M. Rows with neither cost nor principal (affiliated/controlled-investments table rows). 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 7 rows sum to $115.8M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001487918-26-000078 / soi_row 6058 (Pfanstiehl Holdings, Inc., Common Equity: $94.5M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## TRIPLEPOINT PRIVATE VENTURE CREDIT INC. (0001792509-26-000024)

- Gap: +1.88%
- Holdings identified: 449; current SOI rows without an identifier: 192
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 64
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** All remaining rows carry detailed instrument or equity/warrant identifiers; no structural total or duplicate row remains.
- **Root-cause category:** other
- **Example:** 0001792509-26-000024 / soi_row 173061 (Total Expert Inc common stock and warrant investment)
- **Fix or reason:** No additional rule: the remaining difference is not established from the data set.

## NEOSTELLAR CAPITAL CORP. (0001493152-26-036285)

- Gap: -16.50%
- Holdings identified: 39; current SOI rows without an identifier: 33
- Holdings with missing fair value: 8
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** 119 current-period SOI rows, none with 'Investment, Identifier Axis'; filed total $405.9M.
- **Root-cause category:** no_identified_holdings
- **Example:** 0001493152-26-036285 / soi_row 10586 (current-period row without an identifier)
- **Fix or reason:** None possible from SOI: no SOI row of this filing carries 'Investment, Identifier Axis' (holdings are on a custom axis), so no holding can be identified.

## KAYNE DL 2021, INC. (0001193125-26-342417)

- Gap: -5.98%
- Holdings identified: 239; current SOI rows without an identifier: 43
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 10
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -5.98% (-$21.1M): holdings $330.9M vs filed $352.0M. The money-market line 'Investments in Money Market Funds - Morgan Stanley Institutional Liquidity Fund ...' has no fair value in SOI; its value ($22.6M) is only in the custom tag MoneyMarketFundsAtFairValue.
- **Root-cause category:** custom_tags
- **Example:** 0001193125-26-342417 / soi_row 108152 (Investments in Money Market Funds - Morgan Stanley Institutional Liquidity Fund, Instituti: no fair value in SOI)
- **Fix or reason:** Not applied: the fair value sits only in a custom tag in NUM (stretch goal: recover custom-tag values from NUM).

## SILVER CAPITAL HOLDINGS LLC (0001193125-26-344601)

- Gap: +14.45%
- Holdings identified: 39; current SOI rows without an identifier: 62
- Holdings with missing fair value: 6
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +14.45% ($37.7M): holdings $298.3M vs filed $260.6M. Rows with neither cost nor principal ('Non-Controlled Affiliated Investments ...' repeats). 9% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 2 rows sum to $37.7M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** totals_counted
- **Example:** 0001193125-26-344601 / soi_row 138708 (Non-Controlled Affiliated Investments Goldman Sachs Financial Square Government Fund: $34.3M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## TCW DIRECT LENDING LLC (0001193125-26-346645)

- Gap: +64.49%
- Holdings identified: 44; current SOI rows without an identifier: 17
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 75
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +100.00% ($178.3M): holdings $356.7M vs filed $178.3M. Every holding is listed twice: once in the schedule (long identifier, with cost and principal) and once in the affiliated-investments table (short identifier, fair value only). These 18 rows sum to $178.3M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-346645 / soi_row 154979 (Precision Products Machining Group, LLC (fka H-D Advanced Manufacturing Company) Class A U: $46.6M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## GREAT ELM CAPITAL CORP. (0001193125-26-335023)

- Gap: -1.46%
- Holdings identified: 88; current SOI rows without an identifier: 48
- Holdings with missing fair value: 9
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 13
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -1.46% (-$4.0M): holdings $268.3M vs filed $272.3M. The baseline rule_cash dropped 'MFB Northern Inst Funds Treas Portfolio ... Money Market' ($3,966,000), which equals the shortfall; the filer counts it in its total.
- **Root-cause category:** cash_lines
- **Example:** 0001193125-26-335023 / soi_row 129396 (MFB Northern Inst Funds Treas Portfolio Premier CL Short-Term Investments Money Market Int: $4.0M)
- **Fix or reason:** Not applied in Part 3. The kit's rule_cash drops this filer's money-market line, but this filer counts it in its total; Part 2 should keep cash lines for filers whose total includes them.

## GOLUB CAPITAL PRIVATE INCOME FUND S (0002082557-26-000059)

- Gap: +1.59%
- Holdings identified: 310; current SOI rows without an identifier: 132
- Holdings with missing fair value: 1
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap -2.19% (-$5.4M): holdings $243.0M vs filed $248.4M. The money-market holding 'Morgan Stanley Institutional Liquidity Funds - Treasury Portfolio ...' has no fair value in SOI; its value ($9.4M) is only in the custom tag MoneyMarketFundsAtCarryingValue.
- **Root-cause category:** custom_tags
- **Example:** 0002082557-26-000059 / soi_row 130820 (Morgan Stanley Institutional Liquidity Funds - Treasury Portfolio Institutional Share Clas: no fair value in SOI)
- **Fix or reason:** Not applied: the fair value sits only in a custom tag in NUM (stretch goal: recover custom-tag values from NUM).

## INVESTCORP CREDIT MANAGEMENT BDC, INC. (0001193125-26-352658)

- Gap: +14.00%
- Holdings identified: 56; current SOI rows without an identifier: 74
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +14.00% ($19.0M): holdings $155.0M vs filed $135.9M. Rows with neither cost nor principal ('Investment in non-controlled, affiliated ...' repeats). 50% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 7 rows sum to $19.0M; without them the gap would be +0.00% (within tolerance).
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-352658 / soi_row 98153 (Investment in non-controlled, Affiliated Investment: $9.5M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## SCP PRIVATE CREDIT INCOME BDC LLC (0001193125-26-332724)

- Gap: n/a
- Holdings identified: 19; current SOI rows without an identifier: 29
- Holdings with missing fair value: 0
- No filed total in NUM: True
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 18
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. Holdings identified: 19, $131.1M.
- **Root-cause category:** no_filed_total
- **Example:** 0001193125-26-332724 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## SLR HC BDC LLC (0001193125-26-332723)

- Gap: n/a
- Holdings identified: 37; current SOI rows without an identifier: 4
- Holdings with missing fair value: 0
- No filed total in NUM: True
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 9
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** No undimensioned InvestmentOwnedAtFairValue fact at the period end in NUM. Holdings identified: 37, $96.7M.
- **Root-cause category:** no_filed_total
- **Example:** 0001193125-26-332723 / NUM: no InvestmentOwnedAtFairValue with dimn=0 at 2026-06-30 (SUB period)
- **Fix or reason:** None possible: the filing has no undimensioned InvestmentOwnedAtFairValue fact at the period end, so there is no reconciliation target.

## RAND CAPITAL CORP (0001193125-26-333983)

- Gap: +37.01%
- Holdings identified: 93; current SOI rows without an identifier: 45
- Holdings with missing fair value: 48
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 15
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +42.75% ($24.2M): holdings $80.7M vs filed $56.5M. Rows with neither cost nor principal (affiliated/controlled-investments table rows); in addition, 48 holdings have no fair value in SOI. 100% of these dollars repeat a fair value held elsewhere in the filing (copies), the rest are totals. These 7 rows sum to $13.4M; without them the gap would be +18.98%; the remainder is not identified from the data sets.
- **Root-cause category:** restated_copies
- **Example:** 0001193125-26-333983 / soi_row 53551 (BMP Food Service Supply Holdco, LLC - $7,235,000 Fourth Amended and Restated Term Note, $4: $4.3M)
- **Fix or reason:** Not applied in Part 3 (cleaning rules are Part 2's). Proposed rule: drop identifier-axis rows with neither cost nor principal that repeat a holding already in the schedule or add up the issuer's own instruments (affiliated/controlled-investments table rows).

## PRINCETON CAPITAL CORP (0001213900-26-090000)

- Gap: -10.60%
- Holdings identified: 31; current SOI rows without an identifier: 27
- Holdings with missing fair value: 26
- No filed total in NUM: False
- Custom tag used in the SOI: True; custom fair-value facts in NUM: 0
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** Gap +78.80% ($10.9M): holdings $24.7M vs filed $13.8M. 'Control Investments' is a category total tagged as a holding; 26 holdings have no fair value in SOI, so a shortfall remains. This row is $12.3M; without it the gap would be -10.60%; the remainder is not identified from the data sets.
- **Root-cause category:** totals_counted
- **Example:** 0001213900-26-090000 / soi_row 61513 (Control Investments: $12.3M)
- **Fix or reason:** Not applied in Part 3. Proposed Part 2 rule: extend rule_totals to subtotal rows the baseline regex misses (this filer's pattern is shown in the evidence).

## PARTNERS GROUP LENDING FUND, LLC (0001398344-26-014697)

- Gap: n/a
- Holdings identified: 0; current SOI rows without an identifier: 457
- Holdings with missing fair value: 0
- No filed total in NUM: False
- Custom tag used in the SOI: False; custom fair-value facts in NUM: 18
- Negative fair value tagged by investment type in NUM: 0
- **Evidence:** 457 current-period SOI rows, none with 'Investment, Identifier Axis'; filed total $520.6M.
- **Root-cause category:** no_identified_holdings
- **Example:** 0001398344-26-014697 / soi_row 14549 (current-period row without an identifier)
- **Fix or reason:** None possible from SOI: no SOI row of this filing carries 'Investment, Identifier Axis' (holdings are on a custom axis), so no holding can be identified.
