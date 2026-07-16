# NEARS-1229 QA progress — live API verification
Build: feat/NEARS-1229-reviews-status-gate @ 463ac2a1 · backend served from worktree on 127.0.0.1:8091 · DB multi_food_db (read-only)

- AC1 active store w/ reviews (35): GET /stores/reviews?store_id=35 → **200**, 5 reviews, customer_name/rating/item_name present (5x "Customer Nears") — PASS (ac1-store35-reviews.json)
- AC2/AC3 deactivated store: seed has NO deactivated store with reviews (only active 19/21/35 have reviews). Live: store 10 (status=0) → **404 {errors:[{code:store_not_found}]}**, 0 PII fields in body — gate fires live. Deactivated-WITH-reviews leak case covered by automated StoreReviewsActiveGateTest test 1 (fixtures deactivated store + review, asserts 404 + PII-absent, pre-fix RED proof). PASS (ac2-store10-deactivated.json)
- PIN temp-closed store 8 (status=1, active=0): → **200** (empty list — store 8 has 0 seeded reviews; pin substance = 200-not-404, active column does NOT trip gate) — PASS (pin-store8-tempclosed.json)
- CONTRACT nonexistent 999999: → **404 {errors:[{code:store_not_found}]}** — PASS (contract-999999.json)
- PARITY: details/10 and details/999999 both → 404 {errors:[{code:store_not_found,message:Store not found}]} — identical shape to reviews 404 — PASS (parity-details-10.json, parity-details-999999.json)
- REGRESSION details endpoint (NEARS-1113 untouched): details/35 + zoneId [2] → 200 "Test Store"; without zoneId → 403 out_of_zone (pre-existing zone middleware, NOT a regression); reviews flow on active store works — PASS (regression-details-35.json)
- phpunit (worktree): StoreReviewsActiveGateTest + StoreActiveScopeTest → **OK, 7 tests / 83 assertions** (1 PHPUnit deprecation, framework-level). Private test DB used (NEARS-1199) — product DB untouched.
- Worktree git status after phpunit: **clean** — no NEARS-1242 lang/config contamination.
- BE-log check ([api], scoped grep on worktree laravel.log): 404 paths emit the intended structured `[FAIL] store reviews: store not found` lines with correlation_id + store_id only (PII allow-list OK); live hits at 15:33 for store 10 + 999999 match my curls. No unexpected/unrelated errors. VERDICT: clean.

