# NEARS-2202 — QA [8] progress checkpoint (fix_cycle 0, lane full)

Worktree `/Users/Apple/Projects/nears-NEARS-2202-item-reviews-pii` · branch `fix/NEARS-2202-item-reviews-pii` · HEAD `4e1e71b0` · base `07665afc`.
Backend under test: worktree `php artisan serve` on **:8311**. Control backend: primary tree (pre-fix) on **:8000**.
Device: `emulator-5556` (lock acquired via `qa_lock_guard`, key NEARS-2202).

**PII discipline observed throughout:** no response body, no field value, no screenshot of a payload or terminal
showing one was captured or written anywhere. All assertions are on field NAMES and counts.

## Anti-vacuity — observed review counts (DB-corroborated)

| fixture | store | store status | reviews observed in payload | distinct reviewers | DB active-review count |
|---|---|---|---|---|---|
| item 270 | 19 | active (status 1 / active 1) | **5** (get branch) | 2 | 5 / 2 reviewers |
| item 96 | 35 | active | **3** (get branch), **2** (paginate limit=2 offset=1, total_size 3) | 1 | 3 / 1 reviewer |
| item 508 | 47 | **temporarily closed** (status 1 / active 0) | **1** (HTTP 200) | 1 | 1 |
| item 172 | 10 | **deactivated** (status 0) | n/a — HTTP 404 `store_not_found` | n/a | n/a |

Every absence assertion below was made on a NON-EMPTY reviews array whose content (rating, comment,
item_name, attachment) was independently confirmed present.

## AC results

- **AC1 [api] — PASS.** item 270, no auth header, `moduleId: 1` → HTTP 200, 5 reviews, ratings `[5,3,3,3,3]`,
  5/5 non-empty comments, 5/5 non-null `item_name`, `attachment` on all. Payload key list = all 16 `reviews`
  table columns + `item_name` + `customer_name`; nothing but `customer` removed.
- **AC2 [api] — PASS by field ABSENCE.** `phone, email, cm_firebase_token, temp_token, wallet_balance,
  loyalty_point, social_id, ref_code` (+`zone_id`) — **0 of 9 present anywhere** in the payload; the whole
  `customer` object is gone (not blanked, not masked). Instrument proven live: the identical walker found
  **all 9** on the pre-fix backend for the same item + same 5 reviews.
- **AC3 [api] — PASS on BOTH branches, checked separately.** get() (item 96, no limit/offset): 3 reviews.
  paginate() (item 96, limit=2 offset=1): 2 reviews with total_size 3 > limit 2 — a genuinely partial page.
  Identical reduced key list on both; 0 leaked fields on both.
- **AC4 [behav] — PASS.** `ItemReviewsCustomerPiiTest` exists and runs; 7/7 tests, 107 assertions green
  (with `ItemReviewsActiveGateTest`). Message-pinned per field+branch. Real positive control
  (`test_pii_finder_detects_the_fields_on_a_raw_reviewer_payload`) asserts the finder DETECTS the fields
  AND that `assertNoReviewerPii()` throws on a raw User. RED leg corroborated live (see A/B log) rather
  than by re-running the mutation.

## Regression sweep

1. NEARS-1258 gate intact — item 172 → 404 `store_not_found`, no reviewer name / review text in body.
   Temporarily-closed store 47 → still HTTP 200 with reviews (status-only gate preserved).
2. Sibling `GET /api/v1/stores/reviews?store_id=19` unchanged — 5 reviews, flat `customer_name` on all,
   no `customer` object, no reviewer PII. (`zone_id` present there comes from the nested `item` row, not a
   User — pre-existing and not reviewer PII.) Deactivated store 10 → 404.
3. VendorApp — see findings; item-details reviews strip is blocked by a pre-existing defect.
4. Backstops: phpunit 7/7 (107 assertions); `flutter test review_widget_customer_name_contract_test.dart` 4/4.

## Artifacts

- `ac1-ac2-ac3-api-shape.log`
- `ac2-ac4-prefix-vs-postfix-ab.log`
- `bug-vendorapp-itemmodel-offset-type.log` + `bug-vendorapp-items-list-shimmer.png`
- `bug-vendorapp-customer-review-null-check.log`
