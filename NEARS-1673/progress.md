# NEARS-1673 live QA progress (emulator-5560, worktree ef1885ca)

Build: UserApp debug APK built 2026-08-10 05:08 from
/Users/Apple/Projects/nears-NEARS-1673-cold-cache-interest-gate, installed 05:08:33
(md5 c09d8acc4b3857e67243e08dd038ce13, pre-filter only).
Backend: local `php artisan serve :8000`, app baseUrl http://10.0.2.2:8000 (200 on /config).
Cold-cache route used: **fresh install via `flutter run`** (route 1) — first-run onboarding
(language -> slides -> location permission) observed, so login + drift DB were wiped.
Account: sophie.davis@demo.com (module_ids NULL -> API sends [], verified read-only in DB and
in CustomerController.php:203). Zone 2, 3 modules visible.

- AC1 (QA-1) PASS — single tap on "Grocery & Food" (module 1, cold) opened
  "Choose Your Interests" with the grocery categories. Logs: GET /api/v1/categories -> 200,
  no [FAIL]/[ERR]/exception. Shot: ac1-cold-cache-first-tap-interests.png
- AC1 second observation PASS — switch to "Food & Restaurant" (module 2, cold) opened Interests
  on the single tap, showing module 2's OWN 10 food categories (Appetizers/Burgers/Pizza/Sushi),
  no grocery bleed. Logs clean.
- AC2 PASS (decisive form) — WARM cache + AIRPLANE MODE ON: switching to module 2 still opened
  Interests immediately from cache. If the fix had made the warm path await network confirmation,
  offline would have routed Home; it did not. Proves no added wait on the warm path.
  (Timing-by-polling was NOT used: a uiautomator dump costs ~5s, far coarser than the effect.)
- AC3 PASS — cold cache (cleared via language toggle, route 3) + airplane mode: tapping module 1
  did NOT open Interests, routed Home. No crash, no red screen, no gate-specific error screen.
  Home renders the app's standard full-screen "Oops! / No internet connection / Try Again"
  offline state — CONTROL: the same state appears offline without any module switch, so it is
  the normal offline Home, not an error raised by the interest gate.
  Logs: /api/v1/categories -> ApiFailure with correlation_id (properly paired failure logging,
  no silent failure path).
- REGRESSION (pre-existing, NOT this change): UncaughtAsyncError _TypeError
  "type 'String' is not a subtype of type 'Map<String, dynamic>'" at
  item_repository.dart:212 (_getRecommendedItemList) via LocalClient.cachedFetch, seen offline.
  File untouched by this diff; last changed 2026-08-03 (5b4b890d, NEARS-1417).
  Evidence: bug-recommended-items-typeerror-offline.log
- QA-5 PASS — two taps in quick succession on cold module 1 still opened Interests. Logs clean.
- QA-1b NEGATIVE CONTROL PASS — customer@nears.com (module_ids [1,2,4], identity confirmed on
  screen as "Customer Nears"), cold cache after logout: module 1 -> straight to Home, NO
  Interests; module 2 -> straight to its home rail, NO Interests. The gate does not over-fire.
- QA-4 module-switch flash: NOT OBSERVED across 6 switch observations (incl. one forced
  back-to-back 2->1 tap pair). Instrument caveat: a uiautomator dump costs ~1-8s on this device,
  so a sub-second flash CANNOT be excluded; against a localhost backend the window is tiny.
  Reported as "no flash seen", not as "no flash possible".
- QA-6a PASS — home pull-to-refresh: rail intact, no hang/double-load, logs clean.
- QA-6b PASS — Categories tab: rail + item grid populated on BOTH accounts, no stuck skeleton.
  NOTE / self-correction: an earlier reading of the module-1 HOME rail as "empty" was an
  artifact of the dump viewport + the fact that "Categories" is ALSO the bottom-nav tab label.
  The Categories tab reads the same categoryController.categoryList and was fully populated,
  disproving the empty-list inference. No defect.
- Automated backstop: category_controller_test.dart 45/45 GREEN, run by me on HEAD ef1885ca
  with the pinned SDK /Users/Apple/Tools/flutter (3.41.9).
