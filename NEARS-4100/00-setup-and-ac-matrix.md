# NEARS-4100 QA setup + AC matrix (tested_sha cfea765bcba59efaa7f20a8cf05e63f7cec4f456, base 814f12893)

Setup: TIP server = worktree Admin @ cfea765bc on :8561; BASE server = scratch `git worktree add --detach` @ 814f12893 on :8562 (own composer install, own .env copy, tip's passport keys copied so one customer token works on both; `git diff 814f12893 -- Admin/app` = 0 bytes).
Both servers run `php -d pcre.jit=0 -S 127.0.0.1:<port> -t public server.php` (host PHP crashed on pcre2 JIT, DiagnosticReports php-2026-10-10-013442/013652; plain `artisan serve` cannot pass the ini flag).
Private DB `multi_food_db_qa4100` (clone of multi_food_db_test; digit_after_decimal_point set to 2 there; DB proof: business_name marker "NearsQA4100" served by BOTH servers via /api/v1/config; the shared DB serves "Nears"). multi_food_db never touched.
Method: real routes, BASE vs TIP with the same fixture spec, then OrderLogic::create_transaction (settle.php) and read order_transactions.
Harness caveat: fixtures are inserted orders (no placement), so item 51 stock drifted (reset to 97 once); early fixtures lacked item_details.id/delivery_address so 10 order-details page renders 500ed (the 10 `Undefined array key "id"` FAIL lines in log-scan-tip-session-summary.log, fixture artifacts, fixed before the later runs).

| AC | BASE | TIP | file |
|---|---|---|---|
| AC1 R1 web twin, prescription bonus 2, 6 -> 8 | order_amount 8.00, store_amount 10.00 | order_amount 6.00, bonus 2, store_amount 8.00 | ac1-ac2-vendor-twins.log |
| AC2 R2 API twin same + non-prescription 403 + cap | 8.00 / 10.00; 403 not_prescription; bonus 20 kept (28.00 store) | 6.00 / 8.00; 403 not_prescription unchanged; bonus 20 -> 8 persisted, order_amount 0.00 | same |
| AC3 R3 VAT 10%, bonus 2, basket 8 | preview 0.8 / blade total 6.80, saved 0.60 / 6.60 | preview 0.6 / blade total 6.60 = saved 0.60 / 6.60 (qty 3: 1.00 / 11.00 both sides) | ac3-r3-preview-vs-saved.log, e2e-chrome-log.md |
| AC4 R4 tips 1.5 + pkg 0.5, 10 | 8.00, adjusment +2.00, store_amount 6.50 | 10.00, 0.00, store_amount 8.50; growth qty 3 -> 14.00 / -4.00; twins keep packaging | ac4-r4-controls.log, ac1-ac2-vendor-twins.log |
| AC5 R5 flash qty 2 -> 3 | cols stuck 0.8/1.2 (vendor-only 0/2) vs 3.0 taken off | 1.2/1.8 (vendor-only 0/3), sum = discount off the basket | ac5-r5-flash.log, ac5b-... |
| AC6 R6 gate | edits closed/non-COD/payment/campaign/prescription orders; parcel/pos 500 | 403 order_closed / order_not_editable, nothing persisted (ajax + Toastr), cancle ungated, locked recheck | ac6-*.log |
| AC7 R7 | order_amount -12.00, store_discount_amount 20.00 | 403 discount_exceeds_basket, nothing stored | ac7-r7-discount-exceeds-basket.log |
| AC8 F1 | 8 placement pairs (API) | identical to base | ac8-f1-placement-base-vs-tip.log, ac8-source-pin.log |
