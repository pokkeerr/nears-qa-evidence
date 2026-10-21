# NEARS-4208 AC1 gate: refund-to-wallet on the twin (multi_food_db_qa4208)

Run live by QA: the real `php artisan orders:acceptance-timeout-sweep` (CLI) and real HTTP customer cancel against the worktree backend on :8742 (@71cc771a8), twin database only. Each fixture is an ASAP, unaccepted order cloned (orders + order_details) from a real API-placed wallet order (id 91417, placed through `POST customer/order/place`), offer stamped 6 min ago (grace 5 min), then ONE sweep, with before/after snapshots of the customer wallet, `admin_wallets.digital_received`, item stock and `user_notifications`.

**Verdict: PASS.** REQUIRED rows 1-3 pass on the twin; the flow stays on (no notify-only fallback, AC4/AC8 not held).

## Auto-cancel (admin sequence, canceled_by = system, reason acceptance_timeout)

| # | order | shape | `refundCreditPlan` (live helper) | resulting state | `order_refund` rows (credit) | customer wallet delta | `digital_received` delta | stock (qty 2) | customer notification rows | sweep output |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 REQUIRED | 91601 | wallet-paid, confirmed, 150.00 | attempt, amount 150, reason `attempt` | canceled / paid / system / acceptance_timeout / refund_applied_at set | 1 x 150.000 | +150.00 | -150.00 | +2 (restored) | 1 | offered=0 held=0 canceled=1 |
| - | 91602 | digital-paid, 100.00 | attempt, amount 100 | canceled / paid / system / acceptance_timeout / rfa set | 1 x 100.000 | +100.00 | -100.00 | +2 | 1 | canceled=1 |
| 2 REQUIRED | 91603 | partially paid, order 200.00 / paid 60.00 | attempt, amount 60 | canceled / partially_paid / system / acceptance_timeout / rfa set | 1 x 60.000 | +60.00 | -60.00 | +2 | 1 | canceled=1 |
| 3 REQUIRED | 91607 (child A, 120.00, coupon_discount_amount 20) of group 4208qa00-...-0003; sibling B 91608 (80.00, store 2, not yet due) | one child of a mixed basket | attempt, amount 120 | A canceled / system; B still `confirmed` | A: 1 x 120.000; B: 0 rows | +120.00 | -120.00 | A +2 (item 41); B's item 3 unchanged | A 1; B 0 | canceled=1 |
| 10 | 91604 | COD, pending, 45.00 | no attempt, reason `cod` | canceled / unpaid / system / acceptance_timeout / rfa null | 0 | +0.00 | +0.00 | +2 | 1 | canceled=1 |

Sibling B (91608) byte check (sha2 over id, order_amount, coupon_discount_amount, payment_status, order_status, delivery_charge, total_tax_amount, partially_paid_amount, scheduled, accepted_at, canceled, refund_applied_at, offer/hold columns, updated_at): before `fe3043053f88...` = after `fe3043053f88...`; its order_details hash and wallet-row hash (0 rows) identical before/after.

Row 4 (second run): every sweep re-run in this pass reported canceled=0; three concurrent sweeps over two due orders (91803, 91804) produced exactly 1 order_refund row each, 1 notification row each, stock +4 and wallet +43.00 in total (21 + 22).
Row 5 (failed credit rolls back + hold `refund_failed`): not reproducible live without breaking the wallet row; covered by the guarded PHPUnit `test_a_failed_credit_rolls_everything_back_and_holds_the_order_with_one_fail_line` (cited, not re-proven).

## Refundable vs "recorded as manual" shapes (read from the live helper `OrderLogic::refundCreditPlan`, and exercised on the twin)

| # | shape | classify / plan | live twin result |
|---|---|---|---|
| 6 | guest, paid (91701) | hold, reason `guest` | NOT cancelled, held (`acceptance_hold_reason=guest`, `acceptance_hold_at` set), 0 wallet rows, `digital_received` unchanged, `refund_applied_at` null |
| 7 | wallet_status = 0, paid (91702) | hold, `wallet_status_off` | same; held, 0 wallet rows |
| 8 | wallet_add_refund = 0, paid (91703) | hold, `add_refund_off` | same; held, 0 wallet rows |
| 9 | zero amount, paid | hold, `zero_amount` | PHPUnit only (cited) |
| 11 | part-paid order switched to cash | hold, `cod` | PHPUnit only (cited) |
| control | identical paid wallet-eligible order, all flags on (91704) | attempt, 75.60 | cancelled, +75.60 wallet, -75.60 digital_received, system / acceptance_timeout |

Held orders stay held and are never cancelled even after the flags were restored and the offer was backdated past the grace (sticky hold, `canceled=0` on the same sweep that cancelled the control).

## Measurements worth knowing (not defects of this ticket)
- `admin_wallets.digital_received` drops by the refunded amount for a **wallet-paid** order too, although a wallet payment never added to `digital_received` at placement (placing the wallet order 91417 left it at 1000.00). On the twin the fixture-backed balance went negative (-60.00) until the QA topped it back up. This is `OrderLogic::refund_before_delivered` (not in this ticket's diff: `git diff 22d44aa28 -- OrderLogic.php` empty). Logged as a regression_candidate (Low, accounting).
- The twin's `notify_order_updates` for customer 6 is 0: that customer gets no push and no `user_notifications` row (opt-out honoured, offer still visible through the poll). Set to 1 on the twin for the notification checks.
- FCM is configured against the real project; fixture/stale tokens answer 404/"muted", so each notice logs one `[FAIL] acceptance notice not sent {order_id, store_id, reason}` (allow-listed fields only). One push attempt per order was observed, never two.
