# App test that fails on an altered number

The app contract test was exercised against a deliberately altered generated
coverage value. `app/data/coverage.json` changed `filings_admitted` from `88`
to `89`, while `reports/coverage.json` remained unchanged.

Command:

```bash
pytest -q tests/test_app.py::test_coverage_matches_report
```

Observed result:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
_________________________ test_coverage_matches_report _________________________

>       assert response.json() == expected
E       AssertionError: assert {'filings_att...483659.0, ...} == {'filings_att...483659.0, ...}
E         Omitting 6 identical items, use -vv to show
E         Differing items:
E         {'filings_admitted': 89} != {'filings_admitted': 88}
E         Use -v to get more diff

tests/test_app.py:75: AssertionError
=========================== short test summary info ============================
FAILED tests/test_app.py::test_coverage_matches_report - AssertionError: asse...
1 failed, 1 warning in 0.51s
```

The generated file was restored to `filings_admitted: 88`, and the app tests
passed again.
