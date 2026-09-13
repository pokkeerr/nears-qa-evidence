# QA progress — NEARS-3551 (FINAL)

## AC1 — flutter analyze 522 -> 446, unawaited_futures-only, confined
- Base measured at merge-base 22ecb7149 (temp worktree, pubspec.lock identical, reused .dart_tool): 522 issues (469 unawaited_futures + 53 avoid_void_async)
- HEAD f2b75496 (UserApp): 446 issues (393 unawaited_futures + 53 avoid_void_async)
- Delta: -76, entirely unawaited_futures (avoid_void_async unchanged 53->53)
- File-level diff: every file that lost a warning is either lib/features/store/screens/store_screen.dart
  or under test/** — zero files gained a warning, zero files outside stated scope changed.
- VERDICT: PASS. Evidence: analyze-base-522.txt, analyze-head-446.txt

## AC2 — store-screen test failures don't reproduce (closed by evidence, no code change)
- Full unfiltered `flutter test` (no path filter): 5882 total, 20 failures, matches ticket's
  cited baseline exactly. Failures grouped by file (9 files, 20 tests) - IDENTICAL identity to
  ticket text: api_error_extractor_test.dart(2), splash_controller_test.dart(1),
  notification_repository_error_flags_test.dart(2), payment_webview_exit_dialog_routing_test.dart(2),
  payment_screen_error_retry_test.dart(8), staples_repository_failure_log_test.dart(1),
  item_repository_condition_wise_403_test.dart(2), campaign_repository_non_map_body_test.dart(1),
  cart_repository_qty_status_test.dart(1). Sum = 20. Zero new failures anywhere else.
- The 4 AC2-named files: store_screen_fab_scoped_rebuild_test.dart, store_screen_null_config_fab_test.dart,
  store_deeplink_zone_scope_test.dart appear in the full-suite log with 0 [E] markers (clean).
  store_details_distance_priming_test.dart does not appear at all in the full-suite log output
  (see followups - flutter-test tool silently drops this file from multi-file invocations;
  reproduces on `flutter test test/features/store/` too, 392/392 - exact match to ticket's own
  cited evidence). Verified directly via standalone run: 4/4 pass clean.
  ac2-4-named-files-standalone.log / store-dir-392-standalone.log
- VERDICT: PASS.

## Regression sweep (43 touched files: 42 test files + store_screen.dart)
- Cross-checked all 42 touched test file names against the 20-failure list: ZERO overlap.
- store_screen.dart production changes: no store_screen test appears in the 20 failures.
- Confirmed no Admin/backend files touched (git diff --stat vs merge-base: UserApp/** + 1 solution
  doc only).
- VERDICT: clean.

## Automated backstop
- `flutter analyze` (UserApp): 446 issues, exit 1 (expected — pre-existing warnings remain,
  out of this ticket's scope per its own Scope-out section)
- `flutter test` (UserApp, full unfiltered): 5862/5882 pass, 20 pre-existing failures (same
  identity as base), exit 1 (expected — "Some tests failed" is the tool's own summary line
  for known pre-existing failures, not a NEW regression)
