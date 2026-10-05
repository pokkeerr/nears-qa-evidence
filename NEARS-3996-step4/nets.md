# AC3 automated (one file per invocation, explicit SDK /Users/Apple/Tools/flutter 3.41.9, mem-guard cap 6 GB, tip cf67afd23)
```
rc=0 | baseline/store/store_discovery_family_characterization_baseline_test.dart | +72: All tests passed
rc=0 | features/store/store_discovery_owner_test.dart | +61: All tests passed
rc=0 | features/store/store_discovery_facade_wiring_test.dart | +17: All tests passed
rc=0 | features/store/store_discovery_extraction_source_scan_test.dart | +16: All tests passed
rc=0 | features/store/store_discovery_independent_pass_test.dart | +8: All tests passed
rc=0 | baseline/store/store_discovery_lists_baseline_test.dart | +20: All tests passed
rc=0 | baseline/store/store_catalog_requests_baseline_test.dart | +16: All tests passed
rc=0 | baseline/store/store_facade_scope_baseline_test.dart | +11: All tests passed
rc=0 | baseline/store/store_pagination_triggers_baseline_test.dart | +12: All tests passed
rc=0 | baseline/store/store_screen_load_order_baseline_test.dart | +11: All tests passed
rc=0 | baseline/store/store_screen_open_failures_baseline_test.dart | +13: All tests passed
rc=0 | baseline/browse/home_module_fanout_baseline_test.dart | +17: All tests passed
rc=0 | features/store/store_controller_test.dart | +60: All tests passed
rc=0 | features/store/store_controller_open_first_pagination_test.dart | +2: All tests passed
rc=0 | features/store/store_controller_nearest_fallback_test.dart | +6: All tests passed
rc=0 | features/store/nearest_store_origin_test.dart | +5: All tests passed
rc=0 | features/store/all_store_screen_error_retry_test.dart | +4: All tests passed
rc=0 | features/store/store_offers_owner_test.dart | +26: All tests passed
rc=0 | features/store/store_offers_facade_wiring_test.dart | +15: All tests passed
rc=0 | architecture/smart_management_only_builder_test.dart | +10: All tests passed
rc=0 | baseline/golden_manifest_check_test.dart | +5: All tests passed
rc=1 | features/store/store_offers_extraction_source_scan_test.dart | +10 -1: Some tests failed
rc=1 | common/widgets/item_view_closed_now_divider_test.dart | +0 -4: Some tests failed
DONE
```

EXPECTED-FAIL-BY-DESIGN (pending ruling): test/features/store/store_offers_extraction_source_scan_test.dart rc=1 (+10 -1). Failing test: "C4 the facade surface is unchanged control: the update() scan reads ids and skips a declaration; then no update id was added (base 55 id-less + 3 fab; tip 48 + 3 fab in the controller, 8 id-less in the owner, one of the 48 is the port bridge)"  -> `Expected: <48>  Actual: <39>` at test/features/store/store_offers_extraction_source_scan_test.dart:220. Same file on the pristine BASE worktree (0f4ab3979): rc=0, +11 All tests passed (so the failure is caused by this change: step 4 moved 10 id-less call sites into the owner, no update id or order changed). It does not decide the verdict.

PRE-EXISTING: test/common/widgets/item_view_closed_now_divider_test.dart rc=1 (+0 -4) at tip AND on pristine base 0f4ab3979 (+0 -4): `Found 3/4 widgets with text "closed_now"` (time-dependent), not ours.
