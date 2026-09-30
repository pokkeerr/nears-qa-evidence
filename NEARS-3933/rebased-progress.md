# NEARS-3933 delta re-QA after rebase (GREEN only) -- HEAD 05534f2c8 on base 59f8edffd
emulator-5554, own backend :8133 from fix worktree @ 05534f2c8, private DB nears_qa_3933 (re-created from read-only dump). Canary before/after: max(orders.id) 91415, id 228 = 0.
AC1 Cancel/back/scrim/drag each restore Today + slot 0 (4x 'checkout schedule restored date=0 slot=0'), label unchanged.
AC2 ASAP pre-open + Tomorrow tab + Cancel -> 91416 scheduled=0; Tomorrow 10:02 AM pre-open + Today tab + Cancel -> 91417 schedule_at 2026-10-01 10:03.
AC3 (a) 91418 schedule_at 2026-10-01 23:03, (b) Today tab + Schedule -> 91419 placed in range, sheet slot == label.
NEARS-3894 confirm sheet: Place Order -> confirm sheet -> 'Back to checkout' -> Place Order -> Confirm works after a Cancelled time-slot sheet.
Logs: 0 RangeError / 'cascade threw'. One transient [FAIL] get-surge-price transport_error=socket (ApiFailure sentinel) 18:37:17 on the single-threaded QA dev server; order outcome unaffected.
