# NEARS-4117 QA progress (cycle 0) - emulator-5554, own backend :8417 (worktree 4a28118f9, clone DB multi_food_db_qa4117)
AC1 PASS en-collect-94171 'Collect Return Fee From Customer' (+ar)  | AC2 PASS en-paid-94172 'Collected ...' (+ar)
AC3 PASS en/ar/es/bn-refused-94173 neutral label; en-null-status-94175 (NULL status) neutral
AC4 PASS 3 states x EN+AR (12 files: *-full.png + *-feerow.png), AR parens glyph zoom ar-refused-94173-leftparen-glyph-zoom.png
AC5 PASS ac5-api-get-order-fields.txt; entries: History list (history_order_widget.dart:24 Navigator.push) live; Running list (order_widget.dart:29 Get.toNamed) live on 94174 only (terminal fixtures never appear in running lists); notification/splash/dashboard-from-notification not drivable
AC6 PASS grep re-run, see envelope; collect-money sheet on canceled 94171: en-canceled-94171-collect-money-sheet.png
AC7 PASS python3 -I parse of en/ar/bn/es; no raw key rendered in any dump
Logs: app-flutter-fail-lines-startup-stale-token.log = 9 pre-login cold-start 401s (stale stored token), none after login/AC actions.
