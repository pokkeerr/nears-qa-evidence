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
