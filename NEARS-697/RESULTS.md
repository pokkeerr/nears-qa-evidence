# NEARS-697 — V1 controllers zone-decode fail-closed — QA evidence

**Verdict: PASS** · Backend live-API QA · worktree `feat/NEARS-697-v1controllers-zone-decode`
Build: PHP 8.5.6 / Laravel dev server on 127.0.0.1:9697 (worktree code, `CACHE_DRIVER=array` for fresh queries) · DB `multi_food_db` · fix-cycle 0.

## Static (AC1 / AC2)
- 0 raw `json_decode($zone_id, ...)` / `json_decode($request->header('zoneId'))` across the 7 controllers.
- 21 `Helpers::parseZoneIds()` calls: Banner 4 · Brand 3 · CommonCondition 2 · Coupon 3 · Customer 3 · FlashSale 4 · Wishlist 2 = **21**. All 7 controllers import `App\CentralLogics\Helpers`.

## Decode semantics — why the fix closes the hole (decode-semantics-prefix.txt)
Pre-fix `json_decode` fed straight into `whereIn`: `[true]`→`[true]` (MySQL casts `true`→`1` ⇒ **zone-1 leak**); `nears-697-garbage`→`null` ⇒ `whereIn(NULL)` **500-vector** (comment 11240). Post-fix `parseZoneIds` returns `[]` for every malformed input ⇒ `WHERE 0=1` ⇒ 0 rows / HTTP 200. Valid `[2]`→`[2]` byte-identical.

## Live endpoint matrix (HTTP status · data count). zone1=demo, zone2=Abu Dhabi(default).
| endpoint | valid`[2]` | valid`[1]` | `[true]` | `{}` | `[{"x":1}]` | garbage | absent |
|---|---|---|---|---|---|---|---|
| GET /banners | 200 b=5 | 200 b=4 | 200 b=0 | 200 b=0 | 200 b=0 | 200 b=0 | 200 b=5 (zone2) |
| GET /banners/{id} | 200 [] | 200 [] | 200 [] | 200 [] | 200 [] | 200 [] | 200 [] |
| GET /flash-sales | 200 sale | 200 sale | 200 empty | 200 empty | 200 empty | 200 empty | 200 sale (zone2) |
| GET /flash-sales/items | 200 n=2 | 200 n=3 | 403 not-found | 403 | 403 | 403 | 200 n=2 (zone2) |
| GET /customer/suggested-items | 200 n=5 | 200 n=5 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=5 (zone2) |
| GET /brand | 200 [] | 200 [] | 200 [] | 200 [] | 200 [] | 200 [] | 200 [] |
| GET /brand/items/{id} | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 |
| GET /common-condition/items/{id} | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 | 200 n=0 |
| GET /coupon/list/all | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 |
| GET /coupon/list (auth) | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 | 200 n=2 |

**No HTTP 500 on any endpoint/variant. No cross-zone leak on any endpoint** (malformed never returns the zone-1 rows that `valid[1]` proves exist for banners=4 and flash-items=3).

### Notes
- `flash-sales/items` malformed → **403 "flash sale not found"** = the endpoint's pre-existing graceful not-found path (`if(!$flash_sale)`), unchanged by this PR. Malformed zone ⇒ empty zone set ⇒ no flash sale ⇒ same 403 a genuinely-empty zone returns. Fail-closed: no 500, no leak (pre-fix `[true]`→zone-1 would have returned 3 zone-1 items).
- **AC5 backfill:** endpoints calling `Helpers::setZoneIds` (banners, banners/{id}, brand, flash-sales/items, suggested-items) backfill an **absent** header to the default zone (`is_default=1` = zone 2), returning zone-2 data — NOT empty, NOT all-zones.
- **Seed gaps (not failures):** brands table = 0 rows; common_conditions = 0 rows; no `created_by=store` banners; coupons all `default` type (no `store_wise`/`zone_wise` seed, so the zone-scoped coupon branch has no data to leak-test). For these the fix is code-verified + proven 200/fail-closed/shape-intact.

## AC6 phpunit (ac6-phpunit-result.txt)
- `V1ControllersZoneScopingTest` → 7/7 PASS, 58 assertions, 0 skipped.
- `ParseZoneIdsTest` → 2/2 PASS, 14 assertions, 0 skipped.

## Log gate (per-AC `[api]`)
No 500 / `[FAIL]` / exception in the serve log or `laravel.log` during the run window (17:43–17:48). The only ERROR lines in laravel.log are `testing.ERROR` phpunit fixtures from 08:27 (`/api/_sec_test/boom`, social-auth test) — unrelated to these endpoints.

## Regression-candidate confirmed (routed to PO, not this change) — bug-php85-integer-cast-deprecation.log
`CustomerController@info:200-201` uses `(integer)` casts → PHP 8.5 `Deprecated: Non-canonical cast` **notice** (build-time only, not fatal). Does NOT 500 suggested-items (different method, live 200 on all variants). Fix: `(int)`.
