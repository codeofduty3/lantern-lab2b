# Audit of `rule_issuer_aggregates`

## Result

The audit sampled 20 of the 311 rows removed by
`clean.rule_issuer_aggregates` across 10 filings.

| Classification | Rows |
|---|---:|
| `correct_removal` | 20 |
| `wrongly_removed` | 0 |
| `unclear` | 0 |

Seventeen rows repeat a detailed position in a roll-forward,
controlled/affiliated-investment table, or other secondary table. Three are
visible subtotal or issuer-total rows. No sampled row represents a distinct
holding that was incorrectly removed. The rule, panel, and pipeline were not
changed.

## Sampling method

The fixed seed is `20261031`. The exact 311 rows affected by the rule after
`rule_totals` were reconstructed from the canonical holdings and current
transformation sequence. Filings with at least two removed rows were sorted by
accession, permuted with the fixed seed, and the first 10 filings were selected.
Two rows were then drawn without replacement from each selected filing with the
same seed. This produced 20 rows across 10 filings.

| Filing | Accession | Human-readable filing |
|---|---|---|
| Muzinich Corporate Lending Income Fund, Inc. | `0001213900-26-089203` | [primary document](https://www.sec.gov/Archives/edgar/data/1985375/000121390026089203/ea0301667-10q_muzinich.htm) |
| Blue Owl Capital Corp II | `0001655887-26-000016` | [primary document](https://www.sec.gov/Archives/edgar/data/1655887/000165588726000016/obdc-20260630.htm) |
| New Mountain Finance Corp | `0001496099-26-000029` | [primary document](https://www.sec.gov/Archives/edgar/data/1496099/000149609926000029/nmfc-20260630.htm) |
| FS KKR Capital Corp | `0001628280-26-053783` | [primary document](https://www.sec.gov/Archives/edgar/data/1422183/000162828026053783/fsk-20260630.htm) |
| TPG Twin Brook Capital Income Fund | `0001913724-26-000024` | [primary document](https://www.sec.gov/Archives/edgar/data/1913724/000191372426000024/tcap-20260630.htm) |
| Blue Owl Technology Income Corp. | `0001869453-26-000053` | [primary document](https://www.sec.gov/Archives/edgar/data/1869453/000186945326000053/ortic-20260630.htm) |
| Lafayette Square USA, Inc. | `0001628280-26-051793` | [primary document](https://www.sec.gov/Archives/edgar/data/1849089/000162828026051793/ls-20260630.htm) |
| TCW Direct Lending LLC | `0001193125-26-346645` | [primary document](https://www.sec.gov/Archives/edgar/data/1603480/000119312526346645/ck0001603480-20260630.htm) |
| HPS Corporate Lending Fund | `0001628280-26-056772` | [primary document](https://www.sec.gov/Archives/edgar/data/1838126/000162828026056772/hps-20260630.htm) |
| Blue Owl Capital Corp | `0001655888-26-000056` | [primary document](https://www.sec.gov/Archives/edgar/data/1655888/000165588826000056/obdc-20260630.htm) |

## Sample summary

| # | adsh | SOI row(s) | Removed identifier | Fair value | Structural reason | Classification |
|---:|---|---|---|---:|---|---|
| 1 | `0001193125-26-346645` | 169385 | SSI Parent, LLC (fka School Specialty, Inc.) Common Stock | $0 | Same common-stock position appears in the main schedule and again as a zero in a secondary table | `correct_removal` |
| 2 | `0001193125-26-346645` | 181711 | Xiphias Holdings, Inc., (fka Pace Industries, Inc.) Common Shares | $7,444,654 | Same shares repeated in the roll-forward | `correct_removal` |
| 3 | `0001213900-26-089203` | 99944 | Investments - non-controlled/non-affiliated - Warrants - Transportation Excluding Air/Rail | $256,052 | Industry subtotal containing one warrant detail | `correct_removal` |
| 4 | `0001213900-26-089203` | 99945 | Investments - non-controlled/non-affiliated - Warrants | $256,052 | `Total Warrants` row equals the warrant details | `correct_removal` |
| 5 | `0001496099-26-000029` | 137183 | NMFC Senior Loan Program III LLC | $157,872,000 | Issuer row repeats the membership-interest detail | `correct_removal` |
| 6 | `0001496099-26-000029` | 166839 | Sierra Hamilton Holdings Corporation | $2,000,000 | Issuer summary; retained ordinary-share rows total $2,001,000 after displayed rounding | `correct_removal` |
| 7 | `0001628280-26-051793` | 86623 | GELDO Inc. | $3,000,000 | Issuer roll-forward row repeats the preferred-equity holding | `correct_removal` |
| 8 | `0001628280-26-051793` | 168720 | Sparrow Rock, Inc. | $2,000,000 | Issuer roll-forward row repeats the preferred-equity holding | `correct_removal` |
| 9 | `0001628280-26-053783` | 43577;43578 | Accuride Corp, Preferred Stock | $0 | Same zero-valued preferred stock appears beside its industry-qualified detail | `correct_removal` |
| 10 | `0001628280-26-053783` | 44955;44956 | Affordable Care Inc | $14,400,000 | Short identifier repeats the $14.4M PIK loan with industry-qualified detail | `correct_removal` |
| 11 | `0001628280-26-056772` | 60633 | Compsych Investments Corp. | $0 | Short issuer row repeats the zero-valued delayed-draw line | `correct_removal` |
| 12 | `0001628280-26-056772` | 162947 | Rsource Holdings, LLC | -$1,871,000 | Short row repeats the delayed-draw loan while the funded term loan remains detailed | `correct_removal` |
| 13 | `0001655887-26-000016` | 53204 | Blue Owl Credit SLF LLC | $220,000 | Same affiliate interest appears with the “Affiliated” suffix | `correct_removal` |
| 14 | `0001655887-26-000016` | 53274 | Blue Owl Leasing LLC | $91,000 | Same affiliate interest appears with the “Affiliated” suffix | `correct_removal` |
| 15 | `0001655888-26-000056` | 126775;126776 | LSI Financing 1 DAC | $5,196,000 | Short affiliate row repeats the specialty-finance equity detail | `correct_removal` |
| 16 | `0001655888-26-000056` | 147254;147255 | OWL-HP FINANCE LLC | $40,871,000 | Short affiliate row repeats the specialty-finance equity detail | `correct_removal` |
| 17 | `0001869453-26-000053` | 126782 | LSI Financing 1 DAC | $2,064,000 | Short affiliate row repeats the specialty-finance equity detail | `correct_removal` |
| 18 | `0001869453-26-000053` | 126823 | LSI Financing LLC | $47,999,000 | Short affiliate row repeats the specialty-finance equity detail | `correct_removal` |
| 19 | `0001913724-26-000024` | 171041 | TB Senior Loan Fund 1, LLC | $32,615,000 | Short controlled-affiliate row repeats its LLC-interest detail | `correct_removal` |
| 20 | `0001913724-26-000024` | 174571 | Twin Brook Segregated Equity Holdings, LLC | $16,000 | Short row repeats its membership-interest detail | `correct_removal` |

## Evidence details

In the quoted text below, `|` separates HTML cells and `||` separates adjacent
HTML rows. The text otherwise follows the fetched primary document.

### TCW Direct Lending LLC

**1. SSI Parent common stock — `correct_removal`.** The schedule contains
`"SSI Parent, LLC (fka School Specialty, Inc.) (2)(3)(4)(6) | Common Stock | 0.0 % | 80,700 | 53,889 | —"`.
The zero-valued row is a repeated representation of that common-stock position
and not a distinct holding.

**2. Xiphias common shares — `correct_removal`.** The schedule contains
`"Xiphias Holdings, Inc., (fka Pace Industries, Inc.) (2)(3)(6) | Common Shares | 4.0 % | 20 | 29,765,769 | 7,444,654"`.
The roll-forward contains the same labeled shares at 7,444,654; the removed row
is therefore the duplicate copy.

### Muzinich Corporate Lending Income Fund, Inc.

**3. Transportation warrant subtotal — `correct_removal`.** The schedule shows
`"Transportation Excluding Air/Rail || Guardian Fleet Services, Inc. | Warrants | N/A | N/A | N/A | 12/18/2024 | N/A | 241,912 | $ | — | $ | 256,052 | 0.2 %"`.
The removed category value is exactly the Guardian warrant detail.

**4. Total warrants — `correct_removal`.** The schedule shows
`"Total Warrants | $ | — | $ | 256,052 | 0.2 %"`. The retained warrant details
are PayArc at zero and Guardian at $256,052, so the removed row is the category
total.

### New Mountain Finance Corp

**5. NMFC Senior Loan Program III — `correct_removal`.** The schedule shows
`"NMFC Senior Loan Program III LLC** || Investment Fund | Membership Interest (3)(12) | — | — | — | 05/2018 | — | — | $ | 160,000 | $ | 157,872 | 15.26 %"`.
The removed short issuer row and the retained membership-interest row both
carry fair value 157,872 thousand.

**6. Sierra Hamilton Holdings Corporation — `correct_removal`.** The schedule
shows the retained ordinary shares as
`"Sierra Hamilton Holdings Corporation || Energy | Ordinary Shares (2)(12) | — | — | — | 07/2017 | — | 25,000,000 | 11,502 | 1,800"`
and
`"Energy | Ordinary Shares (2)(12) | — | — | — | 07/2017 | — | 25,000,000 | 11,502 | 1,800 || Ordinary Shares (3)(12) | — | — | — | 07/2017 | — | 2,786,000 | 1,282 | 201"`.
Their sum is $2,001,000;
the removed issuer row displays `"Sierra Hamilton Holdings Corporation | 2,000"`.
This is an issuer summary with $1,000 display rounding.

### Lafayette Square USA, Inc.

**7. GELDO Inc. — `correct_removal`.** The schedule shows
`"Insurance || GELDO Inc. | (15)(19) | Preferred Equity | 6/17/2025 | 3,857,032 | $ 3,000 | $ 3,000 | 0.6 %"`.
The removed short issuer row repeats the same $3,000 thousand preferred-equity
position.

**8. Sparrow Rock, Inc. — `correct_removal`.** The schedule shows
`"Professional Services || Sparrow Rock, Inc. | (15)(25) | Preferred Equity | 11/12/2025 | 2,614,379 | 2,000 | 2,000 | 0.4 %"`.
The removed short issuer row repeats the same $2,000 thousand preferred-equity
position.

### FS KKR Capital Corp

**9. Accuride preferred stock — `correct_removal`.** The schedule shows
`"Accuride Corp, Preferred Stock | (ad)(v)(y) | Capital Goods | 2,422,249 | — | —"`.
The removed short identifier has zero fair value and repeats that zero-valued
preferred-stock position.

**10. Affordable Care Inc — `correct_removal`.** The schedule shows
`"Affordable Care Inc | (ac)(v) | Health Care Equipment & Services | 10.0 % | PIK | 06/2032 | 14.4 | 14.4 | 14.4"`.
The removed short identifier has the same $14.4M fair value; the
industry-qualified row remains.

### HPS Corporate Lending Fund

**11. Compsych Investments Corp. — `correct_removal`.** The schedule shows
`"Compsych Investments Corp (4)(5)(6) | 7/22/2031 | 43,333 | ( 187 ) | —"`.
The removed short row repeats the zero-valued delayed-draw position.

**12. Rsource Holdings, LLC — `correct_removal`.** The schedule shows the
funded loan at `"Rsource Holdings, LLC (4)(6)(9) | SF + | 4.75 % | 8.48 % | 11/10/2031 | 172,375 | 170,396 | 165,923"`
and the delayed draw at
`"Rsource Holdings, LLC (4)(5)(6) | 11/10/2031 | 50,000 | ( 662 ) | ( 1,871 )"`.
The removed short row repeats the delayed-draw value.

### Blue Owl Capital Corp II

**13. Blue Owl Credit SLF LLC — `correct_removal`.** The schedule shows
`"Blue Owl Credit SLF LLC(3)(5)(24)(26)(30)(31) | LLC interest | N/A | N/A | 244 | — | 244 | 220"`.
The retained detail differs only by the `"Affiliated"` suffix, so the short row
is a repeated affiliate entry.

**14. Blue Owl Leasing LLC — `correct_removal`.** The schedule shows
`"Blue Owl Leasing LLC(3)(5)(24)(26)(30)(31) | LLC Interest | N/A | N/A | 90 | — | 90 | 91"`.
The retained detail differs only by the `"Affiliated"` suffix.

### Blue Owl Capital Corp

**15. LSI Financing 1 DAC — `correct_removal`.** The schedule shows
`"Pharmaceuticals || LSI Financing 1 DAC(3)(4)(30)(31) | Specialty finance equity investment | N/A | N/A | 5,261 | — | 5,299 | 5,196"`.
The short affiliate row repeats the detailed $5,196 thousand position.

**16. OWL-HP FINANCE LLC — `correct_removal`.** The schedule shows
`"Buildings and real estate || OWL-HP FINANCE LLC(3)(5)(22)(26)(29)(30)(31) | Specialty finance equity investment | N/A | N/A | 40,923 | — | 40,924 | 40,871"`.
The short affiliate row repeats the detailed $40,871 thousand position.

### Blue Owl Technology Income Corp.

**17. LSI Financing 1 DAC — `correct_removal`.** The schedule shows
`"Pharmaceuticals || LSI Financing 1 DAC(3)(4)(30)(31) | Specialty finance equity investment | N/A | N/A | 2,073 | — | 2,105 | 2,064"`.
The short affiliate row repeats the detailed $2,064 thousand position.

**18. LSI Financing LLC — `correct_removal`.** The schedule shows
`"LSI Financing LLC(3)(5)(22)(26)(30)(31) | Specialty finance equity investment | N/A | N/A | 43,653 | — | 43,653 | 47,999"`.
The short affiliate row repeats the detailed $47,999 thousand position.

### TPG Twin Brook Capital Income Fund

**19. TB Senior Loan Fund 1, LLC — `correct_removal`.** The schedule shows
`"Multisector holdings || TB Senior Loan Fund 1, LLC (7) (14) (15) (16) | LLC Interest | 5/27/2026 | $ | 32,550 | $ | 32,615 | 1.21 %"`.
The short controlled-affiliate row repeats that interest at fair value 32,615
thousand.

**20. Twin Brook Segregated Equity Holdings, LLC — `correct_removal`.** The
schedule shows
`"Twin Brook Segregated Equity Holdings, LLC (14) (15) (16) | Equity - 2.11 % membership interest | 19 | 16 | 0.00 %"`.
The short row repeats the same $16 thousand membership interest.

## Wrongly removed and unclear

None in this sample.

## Scope note

This is a 20-row audit, not a guarantee that all 311 removals are correct. No
change was made to `rule_issuer_aggregates`, the panel, or the pipeline.
