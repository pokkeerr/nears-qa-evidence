# NEARS-3956 QA [8] (cycle 0) - progress / index

Lane build d1a86f5c1 (UserApp only, no Admin diff: `git diff --stat a9ded9971 d1a86f5c1 -- Admin` = 0 files). Control = a9ded9971.
Backend: own `php artisan serve --no-reload` from the CONTROL worktree (nears-NEARS-3956-base @ a9ded9971, Admin identical in both trees), DB = private copy multi_food_db_qa_bug3956 (config shows guest_checkout_status=1, a value only the copy has; shared = 0). Logging proxy (method/path/status/error-code/auth-shape/rid only; no bodies, no tokens) in front.
Device: emulator-5610 (spare AVD Pixel_10_Pro_2 booted by this run). Suffixed lane build for behaviour cells; unsuffixed lane build from a scratch detached worktree (with google-services.json, scratch only) for the real FA events (C7/C8).
Times are host-local (UTC+4); device clock is ~6s behind.

| cell | file |
|---|---|
| C0 BEFORE (defect) | c0-before-defect.log, c0-before-dialog-inert.png |
| C1/C4 AFTER switch-to-cash + forced roster failure + Retry/Leave | c1-c4-after-recovery.log, c1-*.png, c4-*.png, c4-failed-roster-a11y-dump.xml |
| C2 cancel | c2-after-cancel.log |
| C4b locked + failed roster, Leave | c4b-locked-leave.log, c4b-*.png |
| C5 verification ON | c5-verification-on.log, c5-*.png |
| C6 short password | c6-short-password.log |
| C7 analytics (real FA) | c7-analytics-fa.log |
| C8 basket empty flag 0/1 | c8-basket-empty-flag0-flag1.log, c8a-*.png, c8b-*.png |
| C9 AC6 negatives + positive controls | c9-*.txt, c9b-*.txt |
| C10 unchanged paths | c10-unchanged-paths.log, c10d-cod-group-before-after.log, c10d-*.png |
| C11 a11y / Arabic | c11-arabic-failed-roster-a11y-dump.xml, c11-arabic-retry-leave.png |
| backstop | automated-backstop.txt |

## Delta cycle (C12): AC7 payment-SUCCESS sub-cell driven live
Harness (least invasive, no product code, no server-tree edit): the logging proxy answers the stub `GET /payment/paypal/pay` (Gateways module absent) with `302 -> <baseUrl>/payment-success` after 28s. The real `PaymentController@success` runs (200); the app's own webview URL check (`OrderService.paymentRedirect`) then routes. Gateway-confirm is simulated on the PRIVATE COPY only (children set pending/paid before the redirect), identical in every cell; the proxy rule is the only thing that fakes the gateway.
| cell | build | file |
|---|---|---|
| C12a guest+Create account success | lane d1a86f5c1 | c12a-lane-adopted-payment-success.log, c12a-*.png |
| C12b same on control | a9ded9971 | c12b-control-guest-payment-success.log, c12b-*.png |
| C12c plain guest success | lane + control | c12c-lane-plain-guest-payment-success.log, c12c-control-plain-guest-payment-success.log, c12c-*.png |
| C12d logged-in user success | lane | c12d-lane-loggedin-payment-success.log, c12d-*.png |
| C12e payment-FAIL redirect (info) | lane, adopted | c12e-lane-adopted-payment-fail.log, c12e-*.png |

## Delta2: success path re-taken with the REAL hook (supersedes the hand-set pending/paid rows of C12)
C12a-d rows above are OBSERVED-under-simulation (hand-set pending/paid). The d2-* files re-take them with the real success hook:
method = place the group in-app; GET /payment-mobile creates the payment_requests row (success_hook order_group_place, paypal, group id) via PaymentController::groupPayment -> Payment::generate_link; then on the private copy set is_paid=1 + transaction_id (as a gateway callback does) and call order_group_place(row) via DB_DATABASE-pinned artisan tinker; DB then shows EVERY child order_status=confirmed + payment_status=paid. Proxy 302 stub /payment/paypal/pay -> /payment-success as before. The 'payment Incomplete / Pay Now' Home observation of C12a is WITHDRAWN (harness artifact: payment-failed excludes confirmed orders; absent in d2 runs).
Files: d2-c12a-*.log/png (lane adopted), d2-c12d-* (lane logged-in), d2-c12c-* (lane + control plain guest), d2-c12b-* (control guest+create-account).
