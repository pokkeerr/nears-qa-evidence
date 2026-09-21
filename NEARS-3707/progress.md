# NEARS-3707 QA progress checkpoint

## AC1/AC2 — modal-cancel site (cancellation_dialogue_widget.dart via Order Details)
STATUS: PASS (live, emulator-5558, order #91364)
- Backend killed -> tap Submit on cancel-reason dialog -> dialog STAYS OPEN, toast
  "Connection to API server failed due to internet connection" visible in a11y tree,
  exactly one [FAIL] endpoint=/api/v1/customer/order/cancel line per attempt
  (correlation_id=6c5c336b... then 2c93f465... on re-submit).
- Re-submit (2nd Submit tap, backend still down): dialog re-submittable, second
  independent [FAIL] line with a new correlation_id -> proves no duplicate/stuck state.
- Backend restarted -> Submit -> SUCCESS: dialog closes (Get.back() fired),
  Order Details shows Status: Cancelled, order removed from Ongoing list.
- Screenshot: docs/qa-evidence/NEARS-3707/ac1-modal-cancel-failure-toast.png

## AC1/AC2 — payment site (payment_incomplete_bottomsheet.dart)
STATUS: PASS (live, emulator-5558, order #91372, HealthCare Pharmacy zone-1 store)
- Placed a real Offline Payment order (#91372, order_status=failed, payment_method=
  offline_payment, no offline_payments row), abandoned on OfflinePaymentScreen, cold
  restarted the app -> DashboardScreen.initState() auto-showed PaymentIncompleteBottomSheet
  (the advisor-flagged site 5, with its togglePaymentIncompleteBottomSheet(false)-before-
  cancelOrder ordering caveat).
- Backend killed -> tap "Cancel Order" -> sheet STAYS MOUNTED (togglePaymentIncompleteBottomSheet
  flip did NOT tear it down, confirming the static-analysis note live), exactly one
  [FAIL] endpoint=/api/v1/customer/order/cancel line (correlation_id=252f641b...).
- Re-tap "Cancel Order" (still down): sheet still mounted, toast
  "Connection to API server failed due to internet connection" visible in a11y tree,
  a second independent [FAIL] line (correlation_id=a5add78b...) -> re-submittable confirmed.
- Screenshot: docs/qa-evidence/NEARS-3707/ac1-payment-site-incomplete-sheet-failure-toast.png
- Backend restarted -> tap "Cancel Order" -> SUCCESS: sheet closes, Get.offAllNamed fires,
  order #91372 now order_status=canceled in DB, no new [FAIL] line logged.

## Superseded notes (resolved — kept for the record)
Earlier attempts blocked by pre-existing environment friction (NOT caused by this ticket's diff):
- No payment-gateway module present (Gateways module physically absent per CLAUDE.md)
  -> "Pay Via Online" tiles (Paypal/Razorpay) render but have no working gateway to fail
     against without a real webview session.
- Offline-payment full checkout DOES work once a single-store zone-1 cart + a
  zone-matching address is used (confirmed live: Nears Mart store_id=1, zone_id=1,
  address id=53 zone_id=1). Order placement itself 403's before store opening hours
  (store_schedule opens 08:00, real device/backend time ~07:44) -- unrelated to the fix,
  purely fixture/timing. Waiting for real clock to pass 08:00 to complete
  Place Order -> OfflinePaymentScreen -> abandon -> cold restart -> dashboard
  PaymentIncompleteBottomSheet -> Cancel Order (forced backend-down failure).
- Automated backstop run in the meantime: `flutter test test/features/order/cancel_order_no_feedback_test.dart`
  -> 6/6 PASS (dialog stays mounted on failure, closes on success, single toast+log
  via ApiChecker for both a genuine 500 and the transport sentinel, 200 path unaffected).
- Static trace (all 3 payment call sites read): payment_failed_dialog.dart,
  digital_payment_failed_screen.dart, payment_incomplete_bottomsheet.dart all call
  `orderController.cancelOrder(...).then((success){ if(success){...} })` with NO
  unconditional Get.back()/dismiss anywhere else in the failure path -- identical
  shape to the modal site, and 100% dependent on the SAME shared choke point
  (OrderController.cancelOrder -> OrderRepository.cancelOrder) already proven live.
  payment_incomplete_bottomsheet.dart's `togglePaymentIncompleteBottomSheet(false)`
  pre-toggle (advisor's flagged caveat) read in splash_controller.dart: pure boolean
  flip, no Get.back()/Navigator call inside it, consumed only at next
  DashboardScreen.initState() -- cannot tear down the currently-mounted sheet.
