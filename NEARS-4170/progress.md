# NEARS-4170 QA progress (checkpoints) - tip 1eec5a351 vs base bc9e01f8a, clone DB multi_food_db_qa4170
- pre-flight: preflight.txt (own artisan serve --no-reload :8170 BASE / :8171 TIP under a restart supervisor; both php 8.2.34; DB_DATABASE proven via ps eww; suspended_at on clone only; freshness PASS x2).
- AC3 A1: A1_login_set_cookie_names.txt. AC1/AC4/AC9 A2: A2_cookie_only_matrix.txt (13 routes x 4 actors, BASE gate passes, TIP 403/401 + cookie forgotten). A2b: panel pages + no-cookie controls.
- AC2 A3: A3_admin / A3_vendor / A3_employee / A3_suspend / A3_panel_reset (vendor) / A3_admin_reset (admin; no SMS OTP required on clone).
- AC9 forced logout A4: A4_forced_logout_final.txt (+run1). AC5 A5: A5_*_TIP_*.txt. AC7 A6.txt. A7 mixed jar: not reachable (guest:admin,vendor blocks 2nd login). R_sweep.txt regression.
- ENV: artisan serve (php -S) segfaults on any real PDF render (BASE too; php 8.2/8.3/8.5, fpm too) -> PDF-200 evidence via in-process kernel dispatch in php-cli with live-login cookies (A5). Gate-pass positive controls use nonexistent ids (404) / empty POST (422).
- Test passwords on the clone are redacted in this gallery (<redacted-clone-pw>).
