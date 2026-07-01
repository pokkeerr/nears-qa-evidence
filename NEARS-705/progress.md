# NEARS-705 QA progress (live) — category_stores() zone-scope dead-code fix

- Worktree: /Users/Apple/Projects/nears-NEARS-705-category-stores-deadcode
- Branch: feat/NEARS-705-category-stores-zone-deadcode
- Server under test: worktree Laravel on :8005 (shared :8000 runs pre-fix primary tree)
- Baseline (DB, multi_food_db, cat=6 mod=1): PRE-FIX unscoped=532 stores/92 zones; POST-FIX zone2=13 stores

## AC checkpoints (all observed live on :8005 worktree code)
- AC1 leak closed: PASS — total=13 all zone_id=2, 0 cross-zone; API ids == DB zone-2 set; pre-fix 532/92-zones vs post-fix 13. (ac1-leak-closed.log)
- AC2 parity: PASS — stores/list == stores/{id} identical zone-2 id set. (ac2-parity.log)
- AC3 three surfaces: PASS — CategoryController + StoreController + SearchController all 13/zone-2, identical set. (ac3-three-surfaces.log)
- AC4 all_zone_service bypass: PASS via integration test test_all_zone_service_returns_cross_zone (real HTTP getJson) + code guard; live seed has NO all_zone_service module (documented, cannot curl without DB write). (ac6-phpunit.log)
- AC5 fail-closed: PASS — {}, not-json, "2", null, [] all -> 0 stores; control [2] -> 13. (ac5-fail-closed.log)
- AC6 phpunit: PASS — 6/6, 45 assertions, 0 skip (2 non-blocking PHPUnit framework deprecations). (ac6-phpunit.log)
- Regression: CLEAN (regression.log). Logs-first: laravel.log empty, no 500s.
- VERDICT: PASS. No task_bugs, no regression_bugs.
