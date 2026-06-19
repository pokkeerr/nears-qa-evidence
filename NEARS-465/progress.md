# NEARS-465 QA progress (live checkpoints)

Device: emulator-5554 (Android) | Branch: feat/NEARS-465-scheduleat-nullsafe @ 386009ae | App: UserApp
Backend: php artisan serve :8000 up; queue:work running. baseUrl dev -> 10.0.2.2:8000 (correct for emulator).

## Data facts (READ-ONLY DB)
- 39 seeded orders, ALL is_guest=0, ALL scheduled=0, ALL schedule_at NON-null (= created_at).
- ZERO is_guest=1 orders -> guest track query (requires is_guest=1) returns 404/empty for any seeded order.
- ZERO scheduled=1 orders -> AC-2 live (scheduled time shows) NOT reachable with seed; covered by widget backstop.

## AC checkpoints
- AC-3 PASS: grep "scheduleAt!" in fix file = 0 occurrences (re-confirmed).
- Automated backstop PASS: flutter test test/features/order/ = 86/86, incl. NEARS-465 tests
  ("loaded WITH an order" asserts "16 Jun 2026" scheduled time shows = AC-2;
   "NON-scheduled order renders stepper, no crash, no scheduled time" w/ takeException()==null = AC-1/AC-4).
- LIVE guest-track input reached (Profile > My Orders): +971 phone + Order ID fields + Track Order btn render. shot 02.
- LIVE submit order_id=1 + seeded phone +971565811199 -> API [404] (order 1 is is_guest=0; guest query needs is_guest=1).
  No navigation to stepper (input gates Get.toNamed on response.isSuccess only). NO runtime error. shot 03.
- AC-1/AC-2 LIVE loaded-stepper UNREACHABLE with seed: guest input only navigates to GuestTrackOrderScreen on HTTP 200,
  and zero is_guest=1 orders exist -> cannot reach the loaded stepper (the crash site) via guest flow. DB read-only => not created.
- Regression: logged in as customer@nears.com (user 6, owns all 39 orders); My Orders list + order details render clean.
  Authed track screen (NEARS-459) CTA only on ongoing orders; seed has only delivered(26)/canceled(13) -> live CTA absent;
  covered by passing order_tracking_screen_test.dart in the 86/86 suite.
- get_runtime_errors across ENTIRE live session (guest home, track input, 404, login, order list, details) = NONE.
