# NEARS-1485 QA progress

Device: emulator-5556 (Pixel_10_Pro_2, 448x997dp, 837MB free)
Worktree: /Users/Apple/Projects/nears-NEARS-1485-profile-logout-mislabel @ ea62d8f1
Flutter 3.41.9 (/Users/Apple/Tools/flutter)

- automated backstop: pin profile_screen_no_delete_under_logout_test.dart 4/4 PASS

## AC1 device corroboration — drawer unreachability
- home_screen and cart_screen BOTH mount `endDrawer: const MenuDrawer()` with
  `endDrawerEnableOpenDragGesture: false` on the next line (verified in the worktree source).
- FIRST ATTEMPT INVALID: with Android gesture navigation on, a right-edge inward swipe is
  consumed by the SYSTEM BACK gesture — the app popped home_screen back to the sector screen
  and the following swipes landed on the wrong screen. Discarded.
- Re-run with `cmd overlay disable ...navbar.gestural` (navigation_mode=0, 3-button), freeing
  the right edge for the app.
- VALIDITY CONTROL: vertical swipe at the extreme right-edge column x=1340 scrolled the home
  feed (content-desc set changed; "Available Near You"/store rows appeared) => touch events at
  x=1340 genuinely reach the app.
- home_screen: 9 swipes, x0=1343 -> x1=250, y in {600,1400,2100}, dur in {250,500,900}ms.
  Result: 0/9 opened the drawer; bottom nav still present after each (did not navigate away).
- cart_screen: same 9-swipe matrix. Result: 0/9 opened the drawer; "Proceed to Checkout" still
  present after each.
- TOTAL 18/18 NO DRAWER. Unreachability premise CORROBORATED on device.

## AC2 — destructive control labelling + own confirmation (live, menu_screen + profile_bg_widget)
- Profile tab (features/menu/screens/menu_screen.dart) rows, live a11y tree:
  "Edit Profile", "My Address", "Delete Account", "Settings", ... and further down "Logout".
  "Delete Account" and "Logout" are SEPARATE rows with distinct labels.
- Tap "Delete Account" -> dialog reads verbatim:
  "Are you sure to delete your account?\nIt will remove your all information."
  (= are_you_sure_to_delete_account + it_will_remove_your_all_information). Dismissed with "No".
  Account intact afterwards (content-desc="Michael Brown" still present).
- SECOND destructive entry point, ProfileBgWidget (reachable: Profile tab -> Edit Profile ->
  update_profile_screen -> "More options" popup): single item "Delete Account", same dialog copy,
  dismissed with "No". Account intact.
- NO deletion was ever confirmed.

## AC3 — real logout exists and is reachable (live, menu_screen)
- Profile tab -> "Logout" -> dialog reads "Are you sure you want to log out?"
  (= are_you_sure_to_logout) — DISTINCT from the delete copy above.
- Confirmed "Yes" -> signed-out state observed: "Guest User" + "Log in/ Sign up" on the Profile
  tab; POST /api/v1/auth/guest/request 200 in the log.
- Re-login performed via the EMAIL field as michael.brown@demo.com -> "Michael Brown" +
  /api/v1/customer/info 200.

## AC3 (second pass) — snackbar captured
- Re-ran Profile tab -> Logout -> Yes, dumping ~1s after confirm.
- a11y tree carried content-desc="Logout Successful" TOGETHER WITH "Guest User" and
  "Log in/ Sign up". Screenshot ac3-logout-successful-snackbar.png.

## Regression sweep (bounded, 5 surfaces + 2 adjacent screens)
- Bottom-nav Home / Search / Categories / Basket / Profile all render (30 / 7 / 23 / 20 / 23
  distinct a11y labels respectively). No blank screen, no red screen.
- update_profile_screen (Edit Profile) renders: Name / E-mail / Phone (Non changeable) /
  Change Password / Update / More options.
- Store details (store 13) opened from home during browsing: 200.
- menu_screen delete row + logout row and profile_bg_widget popup delete item are all present
  and correctly labelled; neither file is in files_changed (three-dot diff = 3 files only).

## Logs
- Whole-session `flutter run` log: 0 lines matching [FAIL]|[ERR]|Unhandled|EXCEPTION CAUGHT|
  RenderFlex|overflowed.
- ui_errors: scanned 704 flutter-tag lines of a 60735-line buffer, 0 matches (non-vacuous count).
- HTTP: 170 responses logged, ALL http_status=200. Zero non-200.

## Notes on device state
- Emulator nav mode was temporarily switched to 3-button to free the right edge for the drawer
  test, and RESTORED to gestural (navigation_mode=2, gestural overlay [x]) afterwards.
- Device left signed OUT (guest) deliberately: leaving a released test account logged in is what
  produced the Sophie-logged-in surprise at the start of this run.
