# NEARS-3854 QA progress (phase 8, fix-cycle 0)

Build 205be4800, branch feat/NEARS-3854-group-badge-export.
Backend: /Users/Apple/Projects/nears-NEARS-3854-group-badge-export @ 205be4800. Port 127.0.0.1:8100, `php artisan serve --no-reload`, DB_DATABASE=nears3854_qa (a private copy of multi_food_db).
DB proof: the copy-only marker business_name="Nears QA3854 COPY" is returned by :8100/api/v1/config, while the shared DB keeps "Nears". The pre-existing `checked` update drained the copy's unchecked orders from 17 to 0; the shared DB still has 17.
Shared invariants before and after: business_settings id=228 = 0 and 0; max(orders.id) = 91415 and 91415.

| AC | status | evidence | logs |
|---|---|---|---|
| AC1 list badge + count | PASS | Walked 7 pages / 127 rows. All 30 grouped rows show "Group · N orders" with N = child_count (0 mismatches): 91391-94 show 4, 91179 shows 2, 91170/71 show 3. title=Multi-store basket, class `badge badge-soft-info ml-1`. Standalone rows (e.g. 91415, 91410) show no badge. Shot: ac1-list-en-badge.png | clean |
| AC2 AJAX search partial | PASS | GET /admin/order/search?search=9117 returns 200 JSON (_table): 91170/71 show "Group · 3 orders", 91179 shows "Group · 2 orders", 91172/75 show none. search=9139 gives 91391-94 "Group · 4 orders". search=91415 gives no badge. Parcel (module_id=5) search 15 and 91128 return 200 with 3 rows and 0 badges. Visible search box (full-page GET) shows the same badges. Shot: ac2-ajax-search-badge.png | clean |
| AC3 export CSV + XLSX | PASS | Clicked Export → Excel/CSV in the UI. Both files have 15 columns, the last being "Group id". Across 127 rows the last column equals DB order_group_id with 0 mismatches (30 grouped rows populated, the rest empty). XLSX: highestColumn O, merges A1:O1 and D2:O2. O3 matches N3 (fill 005D5F, bold, white, thin borders) and O4/O130 match N4/N130 (fill FFE599, thin borders). See export-parsed.txt | clean |
| AC-REG | PASS | Standalone rows are unchanged on all three surfaces. The vendor export (freshsupermarket, store 13, which holds grouped order 91391) has 14 columns ending at N, merges A1:N1 and D2:N2, O unstyled, no Group id. Pending/confirmed/delivered/canceled lists render fine, pending CSV export has 15 columns with 0 mismatches, parcel list renders | clean |
| AC-LOG | N/A | By diff reading: the export reads $order->order_group_id off the row, and the badge reads the eager-loaded group?->child_count with a null-safe fallback. No new lookup, try/catch or failure path | n/a |
| AC-TEST | PASS | phpunit Nears3854AdminGroupBadgeExportTest: OK (9 tests, 93 assertions) | n/a |
| Arabic/RTL | PASS | html dir=rtl, lang=ar. 2 → "مجموعة · 2 طلبان", 3 → "مجموعة · 3 طلبات", 4 → "مجموعة · 4 طلبات", title "سلة متعددة المتاجر". Visual check: the middle dot renders and the RTL layout is mirrored. Shot: ar-list-badge-rtl.png | clean |
| Zone-scoped admin / N+1 / fallback | PASS (feature test) | Zone admins 2-5 exist in the seed but have no known password, so I did not set one. Covered by the feature tests `test_zone_scoped_admin_sees_child_count_not_in_zone_row_count`, `test_list_page_with_two_groups_issues_exactly_one_order_groups_query` and `test_group_row_without_a_usable_child_count_falls_back_to_bare_group_badge`. No live fallback data (0 groups with child_count<2, 0 orphans) | n/a |

Screenshots have the customer-info cells masked in the browser (they contained phone numbers). export-parsed.txt has customer names replaced with [customer].
