# NEARS-691 QA progress — CategoryLogic zone-decode fail-closed (first QA, fix-cycle 0)

Device: N/A (backend API). Worktree backend: `php artisan serve :8091` (multi_food_db, read-only).

| AC | Verdict | Evidence |
|----|---------|----------|
| 1 zero raw json_decode($zone_id) | PASS | ac1-ac2-static-grep.txt — only category_ids/brand_ids remain |
| 2 all zone queries via parseZoneIds | PASS | 17 parseZoneIds usages; diff shows all 16 zone decodes swapped |
| 3 malformed -> fail-closed (Group-B headline) | PASS | ac3-ac4-get_categories.txt — crafted [true]/{}/"2" -> ALL items_count=0 + has_offers=false, HTTP 200 |
| 4 valid -> unchanged (rail==grid parity) | PASS | cat6 z2 rail29==grid29, z1 rail15==grid15, cat9 z2 rail32==grid32 |
| 5 phpunit incl. Group-B mutation guard | PASS | ac5-phpunit-testdox.txt — 12/12 incl. test_rail_counts_crafted_zone_yields_zero; full Category* 44/44 |

Regression (pre-existing, NOT a 691 failure): category_stores (stores/list) cross-zone leak — regression-category_stores-leak.txt.
Live BE log: clean (be-log-check.txt).
