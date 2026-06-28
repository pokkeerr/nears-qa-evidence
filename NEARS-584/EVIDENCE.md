# NEARS-584 — QA Evidence (Live API verification)

**Verdict: PASS** · Fix branch `feat/NEARS-584-item-list-rating-count` @ `69791407`
**Method:** FIXED backend stood up on `:8001` from the worktree `/Users/Apple/Projects/nears-NEARS-584-item-list-rating-count/Admin` with a **real `cp -R` copy** of the primary `vendor/` (NOT a symlink — a symlinked vendor resolves Composer's `App\` autoload base to the primary tree via PHP's symlink-resolved `__FILE__`, which would silently serve the OLD code). Primary `:8000` (no fix) used only as the OLD-baseline contrast. Primary tree never mutated.
**Env:** zone 1, module 1, store 38 (Tower Mart). Headers: `zoneId: [1]`, `moduleId: 1`, `X-localization: en`.

## DB ground truth (read-only SELECT)
```
id   rating_count  avg_rating  rating(JSON)
373  7             4.70        NULL
374  19            4.20        NULL
375  20            4.90        NULL
376  16            4.50        NULL
377  28            4.10        NULL
```
`rating` JSON is NULL → old `array_sum(json_decode(rating))` yielded 0; `rating_count` column is the authoritative value.

## AC1 — items/latest (product_data_formatting, multi branch)
`GET /api/v1/items/latest?store_id=38&category_id=0&limit=50&offset=1`
```
item   FIXED(:8001)        OLD(:8000)
373    rc=7  avg=4.7       rc=0  avg=4.7
374    rc=19 avg=4.2       rc=0  avg=4.2
375    rc=20 avg=4.9       rc=0  avg=4.9
376    rc=16 avg=4.5       rc=0  avg=4.5
377    rc=28 avg=4.1       rc=0  avg=4.1
```
PASS — matches DB exactly; avg unchanged.

## AC2 — productListDataFormatting (DIFFERENT formatter)
`GET /api/v1/items/popular?limit=50&offset=1` → 373 rc=7, 377 rc=28 (FIXED) vs 0 (OLD).
Top-5 by rating_count (FIXED): 359=30, 377=28, 384=26, 9=25, 367=25 — real column values.
`GET /api/v1/items/most-reviewed` → empty on BOTH FIXED and OLD: `most_reviewed_products` filters `->withCount('reviews')->having('reviews_count','>',0)`; the seed populated denormalized `rating_count`/`avg_rating` columns but created **zero `reviews` table rows**, so nothing qualifies. Data quirk, not a fix defect; same formatter is proven via `popular`.
PASS.

## AC3 — product_data_formatting via search
`GET /api/v1/items/search?name=Salt` → 373 rc=7, 375 rc=20 (FIXED) vs 0 (OLD).
`GET /api/v1/search/unified?name=Salt` → 373 rc=7, 375 rc=20, avg correct.
PASS.

## 3rd fix line — product_data_formatting single branch
`GET /api/v1/items/details/373` → FIXED rc=7 avg=4.7 · OLD rc=0 avg=4.7. PASS.

## AC4 — avg_rating undisturbed
Every response above: 373-377 avg = 4.7/4.2/4.9/4.5/4.1 identical between FIXED and OLD. PASS.

## AC5 — visual (verified at API layer)
Routing the emulator to the fixed backend was not feasible: the device targets `10.0.2.2:8000` = the shared primary backend (must not disturb), and a rebuild against `:8001` was out of scope for this env. Verified at the API layer instead:
- The grid card render is already shipped/proven (NEARS-492). `UserApp/lib/common/widgets/item_widget.dart:124`: `final bool hasRating = item!.ratingCount != null && item!.ratingCount! > 0;` — when `ratingCount > 0` the card shows the **star + (count)** row, else the mutually-exclusive **"New" pill**.
- The fix now makes the API return `rating_count` 7/19/20/16/28 for store 38's items, so those cards deterministically flip from the "New" pill to the star+count row.
PASS (API layer; env limitation stated).

## Regression
- Item 1 (genuine `rating_count=0`): FIXED detail rc=0 avg=0, FIXED grid rc=0 — still 0, still "New". No inflation. PASS.
- DB cross-check: API now mirrors the `items.rating_count` column exactly for 373-377. PASS.

## Logs
FIXED backend `storage/logs/laravel.log`: not created (no errors logged). Server stderr: no 4xx/5xx. All requests HTTP 200. CLEAN.
