# NEARS-1047 QA Progress — flash-sale details permanent-shimmer fix

Build: feat/NEARS-1047-flash-sale-details-setstate-build @05399a58 (worktree)
Device: emulator-5554 (Android 17 / API 37), light mode
Backend: 127.0.0.1:8000 live; DB multi_food_db flash_sales ACTIVE (start 2026-06-30, end 2026-07-15, now 2026-07-10)

## AC results
- AC#1 (live flash sale exists): PASS — grocery module-home rail shows Flash Sale LIVE + countdown + Banana/Red Apples/Orange Juice.
- AC#3 (details grid renders, no shimmer, no setState-during-build, items fires): PASS — real 3-product grid rendered; logcat NO "setState()/markNeedsBuild during build", NO GetBuilder "cannot be marked as needing to build"; [NET] GET /api/v1/flash-sales/items -> 200 observed. Shot: ac3-details-grid-rendered.png
- AC#6 (no double-fire): PASS — exactly 1 [NET] GET /api/v1/flash-sales/items dispatch per details open.
- AC#4 (blast radius, return to module-home): PASS — rail renders identically (Flash Sale/LIMITED TIME OFFER/LIVE/See All + Banana/Red Apples/Orange Juice cards); no flicker; logcat NONE for setState/markNeedsBuild/[ERR]/[FAIL]. Shot: ac4-module-home-rail-intact.png
- AC#5 (empty/ended sale -> error state, retry refetches): PASS — forced network failure (device airplane mode, shared backend untouched) drives the same productFlashSale==null path as an ended/403 sale: details showed NearsErrorRetry ("Something went wrong / Retry"), NOT stuck shimmer, with a paired PII-safe [FAIL] endpoint=/api/v1/flash-sales/items (silent-failure gate satisfied). Restored network + tapped Retry -> exactly 1 [NET] GET items -> 200 -> grid rendered. NO setState-during-build. Shots: ac5-error-retry-state.png, ac5-retry-recovered-grid.png
  - Note: the NearsEmptyState (loaded-but-zero-eligible) sub-branch was NOT live-triggerable (zone 1 has items for all 3 sales; DB read-only + a live sale rendered, so the fallback data-mutation clause did not apply) — covered by unit test flash_sale_details_states_test.dart state (b)/(b') which PASSED.

## Automated backstop
flutter test test/features/flash_sale + module_home_flash_order_test.dart => All 41 tests passed.

## Verdict: PASS
