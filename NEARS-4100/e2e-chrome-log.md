# NEARS-4100 QA Chrome DevTools end-to-end (tip server :8561, private DB multi_food_db_qa4100, order-wise 10% VAT on)

Admin login via /login/admin (captcha pre-filled field, admin@admin.com), real UI clicks, console errors: none.

1. Plain pending COD order 92080 (stored 8.80): order page shows the Edit button -> Edit -> "Yes" -> edit mode renders Vat/tax + 0.80, Total 8.80 -> Submit -> "Yes".
   Saved row: total_tax_amount 0.80, order_amount 8.80, adjusment 0.00. Rendered preview == saved.
2. Bonus order 92081 (ref_bonus_amount 2, stored 6.60; the blade HIDES Edit for bonus orders, so edit mode was entered by a direct POST admin.order.edit
   from a helper page carrying Chrome's own CSRF token): edit mode renders Referral Discount - 2.00, Vat/tax + 0.60, Total 6.60 (BASE would render 0.80 / 6.80).
   Item modal: quantity 2 -> 3 -> Update: preview now Vat/tax + 1.00, Referral Discount - 2.00, Total 11.00 -> Submit -> "Yes".
   Saved row: ref_bonus_amount 2, total_tax_amount 1.00, order_amount 11.00, adjusment -4.40. Rendered total 11.00 == saved 11.00; settlement store_amount 13.00.
3. Refusal through the UI: plain order 92082 -> edit mode -> status flipped to handover in the DB -> Submit -> "Yes": server refused at the locked recheck
   (laravel.log: [FAIL] order edit refused at the locked recheck, order_id 92082, order_status handover, reason order_closed, status 403, request_id; no amounts).
   order + order_details + stock byte-identical before/after.
