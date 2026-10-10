# NEARS-4110 QA (fix_cycle 0) - tested_sha 086fa3ee7 (base c891fda8c)

Surface: Laravel Admin panel only (no device, no lock). Real routes admin.order.edit-order then admin.order.update, plus a real Chrome DevTools UI pass (edit mode -> Submit).
FIX server: worktree Admin @086fa3ee7 on 127.0.0.1:8137 (cwd verified by lsof; backend-freshness-check PASS).
BASE server: scratch copy of worktree Admin with the 4 changed files replaced by `git show c891fda8c:<path>` on 127.0.0.1:8138 (diff -rq app/resources/routes/config = exactly those 4 files). Both `php -d pcre.jit=0 -S`, same DB.
DB: private clone multi_food_db_qa4110 (mysqldump --set-gtid-purged=OFF of multi_food_db; marker business_name NearsQA4110 served by /api/v1/config on both servers). multi_food_db never written.
Settings changed ONLY through the panel routes (business-settings/update-order, update-setup) + `artisan cache:clear` with DB_DATABASE=multi_food_db_qa4110. Clone-only DML (stated per case in the logs): fixture orders (inserted rows, label/delivery/additional/tips/pkg/coupon columns), VAT 5% order-wise setup switched is_active 0 for the ticket's no-tax figures (1 for the VAT run), stores.free_delivery 12 flipped for N2, items 51 discount/stock, free_delivery_over set to 6 / NULL for the legacy status=0 shapes (the panel clears it), one business_settings row deleted+restored for the missing-key preview test.
Real placement (UserApp API as james.wilson@demo.com) used for the placement-unchanged check and for real-placed edit cases.

| AC | BASE (c891fda8c) | FIX (086fa3ee7) | log |
|---|---|---|---|
| AC1 H1-A (placed delivery 0, orig 5, basket 8, 8.00), unchanged cart x2 | 13.00 / delivery 5 / adj -5.00 | 8.00 / 0 / 0, stable on 2nd submit | ac1-ac2-ac5-... |
| AC2 control paid-5 (13.00) under all-store | 13.00/5/0 | 13.00/5/0 (x2; label admin+stored 5 also 13.00) | same |
| AC2 by-amount over=6 placed waiver 8.00 | 8.00 | 8.00 | ac2-by-amount-... |
| AC2 reverse status=0 + over=6 left set, paid-5 | 8.00 / 0 / +5 (RED) | 13.00 / 5 / 0 | same |
| AC3 placed additional 2 (10.00): setting 3 / 1 / disabled | 11.00 / 9.00 / 8.00 | 10.00 / addl 2 / adj 0 each; control placed 3 stays 11.00 (3 settings) | ac3-ac4-ac5-... |
| AC4 disabled, tips 1.5 + pkg 0.5 (12.00) | 10.00 | 12.00, tips 1.5 pkg 0.5 kept | same |
| AC5 genuine qty change | n/a | reprices correctly under each fixture (12.00/-4, 4.00/+4, 14.00/-4, 16.00/-4, 6.00/+4, 9.00/-1 by-amount drop, 17.00/-9 over=0/NULL) | all |
| Placement unchanged | - | git diff OrderPlacementService+OrderLogic = 0 bytes; real API placement BASE==FIX under all-store (8.00/0/orig 1/label admin), by-amount (8.00 and 5.00), additional 3 (12.00) | placement-real-api-base-vs-fix.log |
Preview==save: every FIX edit step above prints previewTotal (edit-mode details page, real route) and equals the saved order_amount; BASE diverges (e.g. 12.4 vs 10.40 saved). Missing free_delivery_over row: BASE preview 500 ([FAIL] Attempt to read property "value" on null), FIX renders 8.00 / 13.00.
UI (Chrome DevTools): order 91576 (H1-A) edit mode Delivery fee 0.00 Total 8.00 -> Submit -> DB 8.00/0/adj 0 edited=1; order 91578 (additional 2, setting now 3) view Total 10.00, edit Additional Charge 2.00 Total 10.00 -> Submit -> DB 10.00/addl 2/adj 0. Console: no errors.
Backstop: phpunit --filter 'Nears(4110|4100|4099|4098|4083|4091|4102|4107)' DB multi_food_db_test_nears4110: 539 tests, 4165 assertions, OK (33 PHP deprecations, 0 failures). Nears4110 file = 37 tests. Strict-sites guard OK, Admin/OrderController 89 -> 89.
FIX server structured log, live window 17:25-17:40: 0 [FAIL]/ERROR lines (BASE log: 2 [FAIL] from the missing-key preview only).
