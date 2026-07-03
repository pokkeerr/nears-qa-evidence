# NEARS-772/773/777 i18n batch — QA progress
device: emulator-5556 (reclaimed stale NEARS-737 lock)
backstop: 4 locales x 1934 keys, sets identical, 0 placeholder mismatches (PASS)

## Live demonstrations (light mode; emulator-5558)
NEARS-772 bn: Settings, Login(full), Profile, Orders no_orders_yet/no_ongoing_orders/no_cancelled_orders, Store-closed banner (@time=08:00 live, · segments intact)
NEARS-772 es: Settings, Orders x3 empty states, Store-closed banner (@time=08:00 live), Home, Login(full)
Placeholder substitution PROVEN live in bn+es via store_closed @time; NO raw snake_case key seen anywhere.
only_quantity_available/add_to_cart_failed/store_closed_schedules_later: not live-triggerable (no low-stock seed; server-reject path; scheduleOrder variant) -> VERIFIED_STATIC (backstop parity + same trParams mechanism proven live).
NEARS-773: 3 keys present+translated all 4 locales (backstop). please_submit_a_valid_phone_number behind Firebase OTP invalid-phone (emulator-unreliable); no_note_found/please_upload_lower_size_file behind order-note/oversized-upload paths -> VERIFIED_STATIC.
NEARS-777: 6 ar keys resolve to Arabic via Laravel Translator against worktree data (incl trailing-dot/underscore keys); live HTTP hit PRIMARY backend (EN fallback, env artifact). VERIFIED.
Regression: en (launch home/login) + ar (onboarding+home RTL) render clean; no runtime errors across en->bn->es->ar switches.
