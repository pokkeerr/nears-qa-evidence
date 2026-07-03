# NEARS-789 batch QA progress — 2026-07-03T09:26:05Z
Device: emulator-5556 | Worktree: nears-NEARS-789-vendor-s1 @ 5f6c543c
Test data: order 161 (COD pending, OTP 7364), order 171 (wallet paid 23.00), order 172 (partial 39.00: wallet 27 paid + cod 12 unpaid, coupon 4.00)

- AC1 (789a): PASS — order 171 details tree shows 'Paid' + 'Wallet' + 23 AED. shot ac1-order171-wallet-paid.png; logs clean.
- AC9 (816a): PASS — 35s window, poll hit /vendor/order?order_id=171 every ~10s (6 hits), a11y tree byte-identical, 0 errors.
- AC4 (793): PASS — 10 poll cycles, vendor-pid logcat = only masked API/[NET] lines, redactHeaders() token 7-char prefix, ZERO order-JSON/PII. evidence ac4-pii-window.log.
- AC10 (816b): PASS — admin fired status=processing 13:44:30; vendor details showed 'Order is Processing' at 13:44:37 (~7s, within one tick). shot ac10-order171-external-processing.png.
- AC3 (789c): PASS — 172 payment card: Wallet + '(Partial Payment)' + 27 AED, status Unpaid (partially_paid). shot ac3-order172-partial-sublabel.png.
- AC5 (796): PASS — 172 dotted breakdown: Total 39 / Paid By Wallet 27 / Due Amount (Cash On Delivery) 12, coupon -4; get_runtime_errors = none (no RangeError). shot ac5-order172-partial-breakdown.png. 1-row edge pinned by order_payment_helper_test.dart (cited).
- AC8 (798): PASS(2/3) — screen totals == orders.order_amount: 171=23.00 (normal), 172=39.00 (coupon). 161=20.00 pending check.
- AC12: PASS — Arabic RTL payment card (محفظة /(الدفع الجزئي)/غير مدفوعة الأجر) + billing المبلغ المستحق (الدفع عند الاستلام) د.إ 12; no overflow/errors. shots ac12-rtl-{payment,billing}-card.png. ar offline_payment key present in diff.
- AC2 (789b): PASS — order 161 payment card: 'Unpaid' + 'Cash On Delivery' (translated). shot ac2-order161-cod-unpaid.png. Confirm dialog flow works (Pending->Confirmed).
- AC6 (797a): PASS(live sheet-open + API gate + widget test) — swipe-to-deliver->picture->Complete Delivery OPENS VerifyDeliverySheetWidget (OTP sheet) live [shots ac6-*]. OTP pin ENTRY not adb-drivable (pin_code_fields TextInput won't attach on emulator, mServedView=null, 0 digits render = TOOLING GAP, not defect). Correct-OTP close+collect-cash chain PROVEN by build's widget test 'successful verification pops the sheet with result true' + shouldCollectCash unit tests, run live (21/21 pass).
- AC7 (797b): PASS — wrong OTP proven live via real vendor API PUT /vendor/update-order-status otp=1234 -> 403 {code:otp,'Not matched'}, order stays handover => app success=false => Get.back(result) NOT called => sheet stays open, no collect-cash. Widget test 'failed verification keeps the sheet open with no result' passes. evidence ac6-ac7-widget-tests.log.
- Automated backstop: flutter test 21/21 PASS (verify_delivery_sheet_widget_test + order_payment_helper_test + order_controller_poll_test).
- AC11 (818): PASS — network throttled (gprs/edge), rapid double-swipe on 172 confirmed->process slider: EXACTLY ONE update-order-status API call fired (1 Call/1 Response 200), status advanced one step confirmed->processing (NOT skipped to handover), 0 errors. slider inert during in-flight via disable:isLoading. shots ac11-slider-inflight.png + ac11-single-transition.log.
