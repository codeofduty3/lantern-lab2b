# Mutation test results

Each mutation was applied to the production implementation, exercised with the
named real-release test, and reverted immediately afterward. All commands used
`PYTHONPATH=src .venv/bin/pytest -q`.

| Rule | How it was broken | Failing test output | Restored |
|---|---|---|---|
| `transform_current_period` | Replaced the SUB-period comparison in `holdings.split_periods` with `is_current = True`. `test_transform_current_period_uses_real_sub_period` | `assert [True, True] == [True, False]`; `1 failed in 9.67s` | Yes |
| `transform_axis_identifiers` | Guarded the recovery assignment with `if False and mask.any()`. `test_transform_axis_identifiers_recovers_real_idless_filing` | `assert x["identifier"].notna().any()` produced `assert np.False_` for the 119 Neostellar current rows; `1 failed in 13.26s` | Yes |
| `transform_custom_fair_values` | Made the custom-fact fill condition permanently false. `test_transform_custom_fair_values_fills_real_num_values` | `assert len(filled) > 0` produced `assert 0 > 0`; `1 failed in 9.99s` | Yes |
| `transform_cleaning_attributes` | Returned the input unchanged before adding attributes. `test_transform_cleaning_attributes_covers_real_equity_control_unfunded` | `KeyError: 'security_class'`; `1 failed in 10.16s` | Yes |
| `rule_totals` | Replaced the computed drop mask with an all-false mask. `test_rule_totals_real_release_and_spares_borrower_names` | `assert drop[_row(... "Total Annex Cloud")]` produced `assert np.False_`; `1 failed in 9.90s` | Yes |
| `rule_issuer_aggregates` | Short-circuited the candidate scan before testing detailed sibling identifiers. `test_rule_issuer_aggregates_real_control_and_restated_rows` | `assert drop[cap] and drop[irgse]` produced `assert (np.False_)`; `1 failed in 9.42s` | Yes |
| `rule_cash` | Replaced the cash/money-market mask with an all-false mask. `test_rule_cash_real_money_market_and_spares_investments` | `assert drop[cash]` produced `assert np.False_`; `1 failed in 10.35s` | Yes |
| pipeline tolerance declaration | Removed `reconcile.tolerance` from the `clean` stage's declared params in `dvc.yaml`. `test_dvc_pipeline_has_five_script_stages_and_metric` | `assert 'reconcile.tolerance' in ['release']`; `1 failed in 0.96s` | Yes |
| admission logic | Changed the admission comparison from `abs(gap) <= tolerance` to `abs(gap) <= tolerance / 2`. `test_tolerance_parameter_controls_admission` | `assert bool(loose.loc[0, "admitted"])` evaluated to `False`; `1 failed in 0.99s` | Yes |
| no-filing-dropped | Ignored `soi_adsh` and built the reconciliation universe only from filings with holdings. `test_no_filing_with_soi_rows_is_silently_dropped` | `KeyError: 'z'` when looking up the zero-holding filing; `1 failed in 1.32s` | Yes |
