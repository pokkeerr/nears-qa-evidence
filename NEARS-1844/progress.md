# NEARS-1844 — QA [8] progress log

Device `emulator-5554` · installed APK md5 `963e1039fdd599fb10203e886033b786` (identical pre- and
post-observation) built 2026-08-11T00:56 from `/Users/Apple/Projects/nears-NEARS-1844-pagesize/UserApp`
@ `5985eca7` · Flutter 3.41.9 (`/Users/Apple/Tools/flutter`) · light mode only (dark deferred).

| # | AC | verdict | evidence |
|---|----|---------|----------|
| AC1 | one constant drives the Brands request limit + divisor | met (static) | `kBrandItemsPageLimit` is the sole occurrence on both sides; no `/ 10` left in `lib/features/brands/` |
| AC2 | one constant drives the Item request limit + `paginate` divisor | mis-specified (correct under the corrected reading) | `kItemViewAllPageLimit` on all 3 view-all feeds + `paginate`; `getBuyItAgain`'s `limit=25` deliberately literal |
| AC3 | load-more requests the right next page, does not fire past the last real page | met (Item, live) / unreachable by construction, NOT TESTED (Brands) | `wire-trace.log`, 3 fixtures + positive control |

Live AC3 (Item) — all three observed on the wire through a QA logging reverse proxy:
- header `(85)` unfiltered → load-more offsets **2,3,4** then stop (pre-fix would be 2..9)
- header `(22)`, search `rg`, inside the observable window (10,25] → **zero** load-more (pre-fix: 2 and 3)
- header `(49)`, search `c` → **exactly one** load-more, offset 2 (pre-fix: 2,3,4,5) — positive control

Brands half: `SELECT COUNT(*) FROM brands` = **0**, and `BrandsViewWidget` (the only entry to
`BrandsScreen`/`BrandsItemScreen`) is mounted solely in `shop_home_screen.dart`, which needs an
`ecommerce` module — the `modules` table has none. Doubly unreachable; NOT TESTED live.

Logs: 795 flutter lines from app pid 1926, **zero** `[ERR]`/`[FAIL]`, zero unhandled exceptions.

Regression: Buy-It-Again rail populates (1 item, matches the 1 eligible row in the DB) and still
requests `limit=25`; wallet history and unified search still request `limit=10`.
