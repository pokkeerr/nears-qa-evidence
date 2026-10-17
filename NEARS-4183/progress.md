# NEARS-4183 QA progress (HEAD b726c790d, base 964c61706)

Backend: own `php artisan serve` :8183 from this worktree @ b726c790d (freshness check PASS). Comparator (unflagged byte-compare only): primary tree @ 964c61706 on :8184.
Device: emulator-5554, UserApp built from this worktree, API_HOST via a QA response-mutating proxy (:8185 -> :8183) for forced failure / zero-result / delay only (request log: qa-proxy-request-log.log).
Light mode only. AR/RTL + EN verified.

| AC | verdict | evidence |
|---|---|---|
| 1 | PASS | api-t1.log (each filter alone == SQL truth, AND combos x every sort, total_size p1==p2); bounded lists api-t3.log |
| 2 | PASS | api-t2.log (z2 grocery: no free_delivery/cuisine/open_24h; z1 pharmacy no open_24h; options pruned at count 0 in sheet); positive controls = PHPUnit (automated) |
| 3 | PASS | api-t2.log (malformed x21 all 200; headers absent/0/empty; same-coordinate group zone 400 paged limit 3 == single page, 4 sorts) |
| 4 | PASS | api-t1.log: min_rating=4 -> {4,6}; 5 (3.90) and unreviewed {39,40,41,91112} out |
| 5 | PASS | live z1/z2 food Offers == SQL discounted-item set; coupon branch + once-only = PHPUnit StoreFilterB1Test (automated) |
| 6 | PASS | ac6-*.png; grep of 13 deleted symbols: base lib count >0 each, branch 0 each; analyze 0 errors/warnings (same 90 infos as base) |
| 7 | PASS | ac7-applied-bar-two-filters.png; badge==pill count; Clear; removal refetch |
| 8 | PASS (zero result via response-mutating proxy; unreachable by sheet because zero-count options are pruned) | ac8-*.png |
| 9 | PASS (latest, popular live; recommended via PHPUnit/API; featured has no UI entry point) | ac9-*.png, api-t3.log |
| 10 | PASS | ac10-local-cache-ids-per-signature.log (distinct `&flt=` ids + distinct bodies per signature) + unit tests |
| 11 | PASS | ac11-*.png |
| 12 | PASS | store_filter_synthetic_entry_test, store_filter_no_hardcoded_keys_test green; deleted-symbol grep |
| 13 | PASS (mirror line; Firebase init fails in worktree so FA/DebugView not observable) | logs in ac-notes below |
| 14 | PASS | ac14-*.png; `[FAIL] endpoint=/api/v1/stores/get-stores/all http_status=500 type=ApiFailure msg="filter_sort_apply_reload_failed" correlation_id=97814a60-...` == proxy log rid 97814a60-...; BE filters_block_failed = PHPUnit |
| 15 | PASS | phpunit-filters.log 245 tests OK; phpunit-storelist.log 29 OK; mutation check phpunit-mutation-check*.log: 5/5 predicate mutations killed |

Annotations on the two `FAIL` lines inside api-t1.log / api-t2.log:
- api-t2 "z2 food Offers 4 of 15": my SQL oracle counted inactive store 47 (`stores.active=0`, not in the base list either); 4 of 14 is correct (base list total 14).
- api-t1 `sort=top_rated`: the finding bug-top-rated-chip-vanishes-empty-list.

Analytics lines seen (debug mirror): filter_sheet_opened, filter_applied (section quick/sheet/sort, filter_key, value, applied_filters_count, result_count; fires after the reload succeeded), filter_removed, filters_cleared, filter_empty_result, select_store(filters_active, sort_key).
