# NEARS-1038 QA progress — cycle 0 (2026-07-10)

Build: worktree /Users/Apple/Projects/nears-NEARS-1038-store-sort @ 67bc9bda (base 7cf8783c).
Backend under test: worktree serve :8038 (OTEL_SDK_DISABLED=true). Baseline compare: primary :8000 @ base.
DB: multi_food_db (shared). Seeder Nears1038RatingSpreadQaSeeder APPLIED (user-approved, left in place):
- pre: 0 fixture reviews; 19/21/35 all AVG 5.00; 19+21 rating histogram NULL
- post: 8 fixture reviews (nears1038-21-1..4 @4-star, nears1038-19-1..4 @3-star); histograms written for 19/21
- spread: 35=5.00 > 21=4.20 > 19=3.40; rollback = seeder down() + cache:clear

## Curl matrix (all via :8038, headers zoneId [2] / moduleId 1 / lat 24.45 / lng 54.37 unless noted)

1. PASS — store_type=nearest p1+p2 (limit 10): distance strictly ascending across pages
   (857 → 10527 m), 0 overlap p1∩p2, 15/15 unique of total_size 15. Note: ALL zone-2 stores
   schedule-open at QA time (SQL `open`=1 for every row — verified in DB), so open-first is a
   tie live; open-first + id tie-break demonstrated by pinned feature suite (StoreListSortTest).
   Response open:0 rows (stores 8,9) = formatter `active` overlay, not the SQL sort key.
2. PASS — nearest with no coords / 0,0 / garbage ("banana"/"%%%") → id order identical to
   store_type=all in all 3 variants (no-op guard works).
3. PASS — top_rated → 35 (avg 5) > 21 (4.2) > 19 (3.4), matches DB AVG(reviews.rating).
   NULL-avg-last not demonstrable live (no histogram-bearing zero-review store in zone 2) —
   covered by feature suite.
4. PASS — GET /api/v1/stores/get-data?store_type=top_rated&rating_count=3 → HTTP 200, no SQL
   error (no avg_r/top_rated_avg alias collision), order 35 > 21 > 19.
5. PASS — regression: all/newly_joined/popular id-order + total_size identical base(:8000 @7cf8783c)
   vs worktree(:8038 @67bc9bda), zones 2 and 1, module 1 — 6/6 identical.
6. PASS — BE log: 0 local.ERROR lines in worktree laravel.log; only testing.ERROR fixture lines
   from phpunit runs (03:08–04:41, deliberate test paths). No store-endpoint errors during matrix.

## On-device (emulator-5554, worktree app → 10.0.2.2:8038)
Resumed 2026-07-10 (delta re-QA; prior QA killed mid-run). Reclaimed stale lock (dead pid 69305).
Build confirmed: flutter run pid points at worktree UserApp w/ -DAPI_HOST=10.0.2.2:8038; backend
serve :8038 cwd = worktree/Admin @67bc9bda. Zone 2 (Abu Dhabi), module 1 (Grocery & Food),
origin 24.45/54.37 (emu geo fix; loc perm granted). Surface = module-home Stores list
(all_store_filter_widget chip row: All / Newly joined / Popular / Top Rated / Nearest).

7. PASS — NEAREST chip (5th, origin-gated, visible + selected mint): tap → "15 stores near you",
   visual order distance-ASC end-to-end: Abu Dhabi Fresh Market 0.9km (store 8) → Fresh local 1.5
   → Fast Market 2.8 (21) → Organic Shop 3.8 (9) → Morning Mart 4.2 (20) → Supermarket 4.5 (22) …
   → Test Store 8.1 (35) → Vegan Market 9.0 (17) → Eco Market 9.5 (19) → Veggie Market 10.5 (18, last).
   Matches DB distance ref (857→10527m). No crash, no error toast, ui_errors empty, logcat clean.
   Shot: ondevice-nearest.png.
8. PASS — TOP_RATED chip (selected mint): tap → header "3 stores near you" (only the 3 rating-bearing
   stores pass filter), visual order rating-DESC: Test Store 5.0 (5) [store 35] > Fast Market 4.2 (5)
   [21] > Eco Market 3.4 (5) [19]. Exactly matches seeded spread + backend curl cell 3. No crash,
   no error toast, ui_errors empty, logcat clean. Shot: ondevice-top-rated.png.
9. PASS — logs-first gate: 0 Flutter [FAIL]/[ERR]/Exception/RenderFlex-overflow in app logcat during
   both interactions; 0 store-endpoint local.ERROR lines in worktree laravel.log.

VERDICT: PASS (6/6 backend curl reused + 2/2 on-device demonstrated + logs clean).
