# NEARS-3933 QA progress (cycle 0)
Device emulator-5554 (Pixel_10_Pro AVD, light). RED = detached 7442596b1 (pkg ..nears_nears_3933_base); GREEN = f059cc176 (pkg ..nears_nears_3933_timeslot_cancel_revert). Own backend :8133 from the fix worktree, DB_DATABASE=nears_qa_3933 (private copy).
Selection state read from live a11y bounds + one pixel probe (selected tab = navy underline, selected slot = mint fill) -- Flutter does not expose selected state in the a11y tree.

RED (base): AC1 reopen shows Tomorrow still selected (red-ac1-*.png); AC2 order 91416 schedule_at 2026-10-01 06:03 while checkout said Instant; AC3 [FAIL] type=RangeError msg="checkout: place-order cascade threw" + error snackbar, no order (red-ac3-rangeerror-fail.log).
GREEN (fix): AC1 Cancel/system back/scrim/drag each restore (Today tab + slot 0 on reopen, 4x "checkout schedule restored"); AC2 ASAP pre-open -> 91417 scheduled=0; scheduled-tomorrow-10:02 pre-open -> 91419 schedule_at 2026-10-01 10:03; AC3a Cancel -> 91420 schedule_at 2026-10-01 23:03, no RangeError; AC3b Today tab+Schedule -> 91421 placed, sheet == checkout label, index in range.
Regression: Schedule path 91422 fee 6.00 shown==charged, exactly 1 surge call; Cancel after Tomorrow tab -> fee back to 3.00; 91423 Today 6:02 PM slot schedule_at 18:03; closed tomorrow tab: Cancel ok, Schedule -> Store is closed -> PlaceOrderBlocked (pre-existing guard); 1.3x text scale open/cancel clean; AR/RTL open/tab/cancel/reopen ok; mixed basket (flag 1 in COPY only) checkout has no Preference Time section.
Backstop: flutter test 3 new files 23/23.
Byproducts: bug-followup-tomorrow-default-slot-label-instant.log (pre-existing), bug-followup-nitemcard-overflow-1-3x.log (unrelated).
