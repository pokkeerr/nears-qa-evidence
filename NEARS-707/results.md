# NEARS-707 — Live QA evidence (phase 8, fix-cycle 1)

**Verdict: PASS** (task ACs) — 1 pre-existing non-blocking regression_bug filed separately.

- **Build under test:** worktree `feat/NEARS-707-getcombined-brandids-guard` (uncommitted fix, base `feat/userapp-reskin`@6d859fc3)
- **Backend:** worktree `Admin/` on `php artisan serve :8091`, dev DB `multi_food_db` (read-only, no mutation)
- **Fix:** `SearchController::get_searched_products` L58 `->when(is_array($brand_ids) && count($brand_ids) > 0, ...)`
- **Endpoint:** `GET /api/v1/get-combined-data?list_type=item&data_type=searched`
- **Headers:** `zoneId:[2]` (Abu Dhabi), `moduleId:1` (Grocery & Food), lon 54.37 / lat 24.45
- **Search term:** `Apple` → 6-item unfiltered baseline (ids 254,263,290,293,308,96)

## Per-AC (live curl)
| AC | Request (…&name=Apple) | Expected | Result | Evidence |
|----|------------------------|----------|--------|----------|
| 1 | no `brand_ids` | 200 unfiltered (was 500) | **200**, 6 items | ac1-no-brandids.snapshot.json |
| 2 | `brand_ids=[]` | 200 unfiltered | **200**, 6 items | ac2-empty-array.snapshot.json |
| 3 | `brand_ids=5` (scalar int) | 200 unfiltered (delta path) | **200**, 6 items | ac3-scalar-5.snapshot.json |
| 4 | `brand_ids="foo"` (scalar str) | 200 unfiltered | **200**, 6 items | ac4-scalar-foo.snapshot.json |
| 4b | `brand_ids=foo` (bare→null) | 200 unfiltered | **200**, 6 items | ac4b-bare-foo.snapshot.json |
| 5 | `brand_ids=[999999]` (nonexistent) | 200, narrows | **200**, 0 items (vs 6 unfiltered → real filter) | ac5-nonexistent.snapshot.json |
| 6 | log check across all above | no new TypeError/500 | **0 new** TypeError (log 77 lines unchanged) | worktree laravel.log |

AC5 positive brand-match (branded item present when its real brand id requested) is not seedable
live — dev DB has **0 brands / 0 ecommerce_item_details** and the read-only rule bars seeding.
Proven by phpunit against the isolated test DB (DatabaseTransactions):
`test_searched_populated_brand_ids_filters_by_brand`.

## Before/after (pre-fix primary :8000, same requests)
- no `brand_ids` → **500** ; scalar `brand_ids=5` → **500** ; `brand_ids=[]` → 200.
- Exact pre-fix error: `count(): Argument #1 ($value) must be of type Countable|array, {string|int} given`
  (`type: TypeError`, `endpoint: /api/v1/get-combined-data`) — see bug-prefix-500-reference.log.

## Regression smoke (worktree :8091 — unchanged params still behave)
| Param | Request | Result |
|-------|---------|--------|
| category_ids array | `category_ids=[4]` | 200, narrows to [254,290] |
| category_ids array | `category_ids=[10]` | 200, narrows to [263,293,308] |
| store_id | `store_id=17` | 200, narrows to [254] |
| price band | `min_price=1&max_price=5` | 200, narrows to [290] |
| filter | `filter=[top_rated]` | 200, reordered |
| filter | `filter=[popular]` | 200, reordered |
| zone scoping (695) | `zoneId:[3]` | 200, 0 (Apple items are zone 2) |
| zone scoping (695) | `zoneId:garbage` | 200, 0 (fail-closed) |

## Automated backstop
`vendor/bin/phpunit --filter GetCombinedDataBrandIdsGuardTest` → **OK, 4/4 tests, 31 assertions**
(2 unrelated PHPUnit deprecations). Test DB only; dev DB untouched.

## Non-blocking finding (regression_bug — pre-existing, out of scope)
Scalar `category_ids=5` and `category_ids="foo"` → **500** on both primary (pre-fix) and worktree
(post-fix). Same latent `count()`-on-json-scalar bug as NEARS-707, but at L53 (`category_ids`,
un-guarded) — the fix only closed the L58 `brand_ids` analogue. Not caused by this change, not in
NEARS-707 scope. Evidence: bug-category-ids-scalar-500.log.
