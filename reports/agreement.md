# Agreement report (Part 1, requirement 4)

**Release:** 2026q3 (2026_07, 2026_08, 2026_09). **Checked by:** Julio Sepulveda, 24 October 2026.

We do not use EdgarTools, so we compare our parsed holdings with the human-readable schedule of
investments of three filings, one from each monthly ZIP. "Ours" is the current-period holdings
written by `scripts/parse.py` (`outputs/interim/holdings.parquet`), before any Part 2 cleaning.
Our side is reproduced by `python scripts/agreement.py`, which writes
`reports/agreement_ours.csv`. The filing's side was read from each 10-Q in the SEC's inline
viewer (links below). Amounts in the documents are in thousands unless stated.

## Summary

| Filing (adsh) | Our holdings | Our fair value | Schedule of investments total | Agreement |
|---|---|---|---|---|
| OFS Capital Corp, 10-Q, 30 June 2026 (0001487918-26-000078) | 118 | $413,582,000 | $297,756 thousand | **Differs by +$115,826,000 (+38.9%)**: 10 duplicate holdings, explained below |
| TCW Steel City Senior Lending BDC, 10-Q, 30 June 2026 (0001193125-26-346670) | 23 | $463,025,006 | $463,025 thousand | Agrees |
| Robinhood Ventures Fund II, 10-Q, 30 June 2026 (0002131040-26-000008) | 79 | $19,600,000 | $19,600 thousand | Agrees |

In every case the schedule's total also equals the filing's own XBRL total in NUM
(`InvestmentOwnedAtFairValue`, no dimensions, at the period end), which is the figure Part 3
reconciles against.

## OFS Capital: the difference, explained

Document: https://www.sec.gov/ix?doc=/Archives/edgar/data/1487918/000148791826000078/ofs-20260630.htm

OFS's current-period SOI rows name their holdings in two styles:

| Identifier style | Example | Holdings | Fair value |
|---|---|---|---|
| Long, from the schedule of investments | "Portfolio Company Investment Type AI Pfanstiehl Holdings, Inc CE (400 Class A shares) Industry Pharmaceutical Preparation Manufacturing IAD 1/1/2014" | 108 | $297,756,000 |
| Short | "Pfanstiehl Holdings, Inc., Common Equity" (SOI row 6058) | 10 | $115,826,000 |

The 108 long-style holdings add up to exactly the schedule's total of $297,756 thousand. The 10
short-style holdings repeat holdings that are already in the schedule, with a fair value but no
cost, principal or rate. In the 10-Q, Pfanstiehl Holdings appears more than once, including in
the **Portfolio Concentration** table. The short-style rows are most likely that table's XBRL
facts: they carry the same identifier axis and date as the schedule, so the SEC's SOI extract
includes them alongside the schedule's own rows.
The largest is Pfanstiehl Holdings common equity, $94,550,000, counted once in each style.

The 10 short-style holdings are: Contract Datascan Holdings, Inc. (common equity, preferred
equity 1 and 2, warrants 1 and 2), DRS Imaging Services, LLC (common equity), Pfanstiehl
Holdings, Inc. (common equity), and SSJA Bariatric Management LLC (common equity 1, first lien
debt 1 and 2).

**Consequence.** Parsing is correct; the extract contains a second copy of some holdings. This
is a cleaning artifact (duplicate copies from another table), handed to Part 2: a rule that drops
these rows brings OFS from +38.9% to an exact match with its filed total.

## TCW Steel City Senior Lending BDC

Document: https://www.sec.gov/ix?doc=/Archives/edgar/data/2043133/000119312526346670/ck0002043133-20260630.htm

Our 23 holdings total $463,025,006; the schedule's total investments is $463,025 thousand. Each
holding was built from 2 SOI rows (the coalescing in Part 1, requirement 3), and the three largest
are Tidal Investments LLC ($45,309,783), Nexcess Digital Corp. ($42,469,512) and Centaur
Holdings III LLC ($40,826,094).

## Robinhood Ventures Fund II

Document: https://www.sec.gov/ix?doc=/Archives/edgar/data/2131040/000213104026000008/rvii-20260630.htm

Our 79 holdings total $19,600,000; the schedule's total investments is $19,600 thousand. We
checked two holdings by name: Adialante, Inc. and Apex Flux Inc. are each listed at $250,000 in
the schedule, as in ours. The schedule lists about 79 companies, in line with our count.

## Conclusion

Parsing agrees with the human-readable schedules for all three filings. The one material
difference (OFS, +38.9%) is not a parsing error but duplicate rows that the SEC's extract takes
from the Portfolio Concentration table; it is explained above and passed to cleaning (Part 2).
