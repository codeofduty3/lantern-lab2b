# Unit economics (Part 5)

**Release:** 2026q3 (2026_07, 2026_08, 2026_09), 182 filings, 75.1 MB of ZIPs (1.5 GB unpacked).
**Machine:** Julio's laptop, Windows with WSL (Ubuntu 24.04), Python 3 in a virtual environment.
**Measured:** 25 October 2026 with `time`, one run per stage, ZIPs already downloaded except where stated.

> Status: acquire and parse are measured. The clean, reconcile and report stages, and the
> quality line, are filled in when Parts 2 and 3 are in the pipeline. Assumptions are marked
> **Assumption** and are the team's to confirm.

## Stage timings

| Stage | Wall-clock time | What it does |
|---|---|---|
| download (one month, 2026_08, 72 MB, from sec.gov) | 2.2 s | `curl` with our User-Agent; network-dependent |
| acquire | 21.3 s | unzip 3 months, write and verify the manifest, combine into 2026q3 |
| parse | 15.6 s | load, map by tag, label periods, coalesce, resolve conflicts |
| clean | _TBD_ | Part 2 |
| reconcile | _TBD_ | Part 3 |
| report | _TBD_ | Part 3 |
| **Total so far** | **39.1 s** | download + acquire + parse |

## The five lines

| Line | Value | How it was computed |
|---|---|---|
| Cost per completed task | about $0.000006 of compute per filing (about $0.0011 for the whole release, so far) | 39.1 s = 0.0109 h × $0.10/h ÷ 182 filings. **Assumption:** $0.10 per hour, the price of a small cloud VM comparable to a laptop. No model is used, so there is no model cost. |
| Latency | 39.1 s for the release so far; 0.21 s per filing | Measured above; to be updated with clean, reconcile and report |
| Human time replaced | ×0.5: 182 h ($21,840) · ×1: 364 h ($43,680) · ×2: 728 h ($87,360) | **Assumption:** an analyst needs 2 hours to reconcile one BDC filing by hand (find the schedule, total it, compare with the balance sheet, investigate the gap), at $120 per hour, for 182 filings |
| Quality | _TBD_: coverage of filings and dollars (Part 3); agreement with the filings (Part 4) | Part 1 already shows agreement on three filings: 2 exact, 1 explained (`reports/agreement.md`) |
| Scale | about 4 minutes and well under one cent of compute for all 22 releases since 2022q4 (so far) | The SEC lists 22 releases from 2022q4 to 2026_09 (13 quarterly to 2025q4, then monthly), 478.5 MB of ZIPs. Time grows with data size: 39.1 s for 75.1 MB is 0.52 s per MB, so 478.5 MB takes about 250 s. To be updated with the full pipeline. |

## Build versus buy

_To be written at the end, once all stages are in place._ Points to cover: the starter kit gave
us loaders, tag-based mapping, coalescing, the baseline rules, reconciliation and the
self-check; we did not use EdgarTools. What we still had to build: combining three monthly
releases into one quarter, the subsidiary rule for split holdings, the cleaning rules (Part 2),
the triage (Part 3), and the pipeline itself.
