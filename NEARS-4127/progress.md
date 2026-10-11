# NEARS-4127 QA progress (phase 8, cycle 0)

Fixed arm: worktree HEAD b570a5884, php -S 127.0.0.1:8127 (freshness-check PASS). Base-RED arm: scratch copy with VendorAccountState.php + VendorMiddleware.php from 00e5d238e, 127.0.0.1:8128. Both read QA clone multi_food_db_qa4127 (marker migration applied on the clone only).

- AC1 PASS: fixed refuses the open owner session on the next request (302 to /login/vendor, "Your account has been suspended", not "session has expired", vendor guard logged out, further panel URLs redirect). Base: 200 panel = RED (all of mk-commission/mk-unsub/mk-unsub-app/mk-subscription).
- AC5 PASS: exactly 1 production.ERROR [FAIL] vendor.session_suspended per refusal (5 refusals, 5 lines), correlation_id == refused response X-Request-Id, fields {store_id, surface:web}; none for controls/employee/API; base 0 lines.
- AC2 PASS: reactivation: old tab stays dead, fresh login 200 dashboard, idle session C (no request during suspension) dead with "session expired" after reactivation (base: alive).
- AC3 PASS: ctl-expired-unsub/ctl-commission/ctl-subscription/ctl-none-live/pending identical base vs fixed, no session_suspended line.
- AC4 PASS: owner and employee API profile 200 before, 401 auth-001 "Unauthorized." after suspension, byte-identical base vs fixed (58 bytes), 0 session_suspended lines.
- Employee leg PASS: unchanged home redirect, tokens rotated at the toggle (len 60, first4 changed).
- Byproducts: SEC-4127-2 confirmed, SEC-4127-1 confirmed.
- Regression sweep PASS. Automated backstop: 93 tests, 860 assertions OK.
