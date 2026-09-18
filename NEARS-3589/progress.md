# NEARS-3589 QA progress checkpoint

Device: emulator-5558 (sdk_gphone16k_arm64), UserApp debug, worktree
`/Users/Apple/Projects/nears-NEARS-3589-basket-uiux-findings`, branch
`feat/NEARS-3589-basket-uiux-findings`, HEAD df37e6767.
Backend: own `php artisan serve --port=8210` from this worktree (freshness-check PASS).
Account: customer@nears.com. Location: mocked Abu Dhabi (cmd location test-provider,
24.4539,54.3773). 2-store basket confirmed live (Fresh supermarket store 13 items
Dish Soap 500ml + Whole Milk 1L; Fresh local store 12 item Honey 500g — matches
NEARS-3590 fixture set, seed data carries accumulated quantities from prior QA runs).

## Source-verified (before device drive)
All 10 findings + AC-DLS/SHARED/ANALYTICS/LOG confirmed present in the diff
(3fc8ae4c3..HEAD) by reading the implementing lines directly — see full envelope.

## Environment bootstrap notes (not ticket defects)
- Fresh worktree needed: `Admin/.env` copy, `composer install`, `php artisan passport:keys`,
  `worktree-bootstrap-images.sh`.
- `UserApp/android/app/google-services.json` absent in worktree (gitignored) — copied from
  primary, then a second `client[]` entry added for the worktree-suffixed package id
  (`com.izzes.nears.nears_nears_3589_basket_uiux_findings`) so `Firebase.initializeApp()`
  and the `processDebugGoogleServices` Gradle task succeed for a per-worktree-suffixed
  UserApp build. Local, gitignored, not a product-code change.
- Google Maps SDK shows "Authorization failure" for the same suffixed package
  (API key not registered for this cert+package combo) — map tile rendering only;
  does not block the geocode/zone REST flow. Unrelated to this ticket, not filed
  (pre-existing infra gap affecting every worktree-suffixed UserApp build, not specific
  to NEARS-3589).
- Location mocking needed `cmd location providers add-test-provider gps` +
  `set-test-provider-location`, not `adb emu geo fix` (per pick-map-camera-idle memory).

## AC-by-AC status (live)
(being filled in as each is demonstrated)

## Delta re-QA (fix-cycle 2, HEAD aff907d16) — 2026-09-18

Device: emulator-5554 (5558 was occupied-without-lock; 5554 free + disk-precheck PASS,
1179164KB free). Own backend `php artisan serve --port=8210` from this worktree
(freshness-check PASS: `/Users/Apple/Projects/nears-NEARS-3589-basket-uiux-findings @
aff907d16`). UserApp `--dart-define API_HOST=10.0.2.2:8210`. Account customer@nears.com,
GPS mocked Abu Dhabi (same test-provider recipe). Basket carries a large accumulated
cross-session fixture (up to 7 stores from prior tickets' QA runs on this shared seed
account) — not this ticket's fault, noted per surface below.

- **BK1**: STILL FAIL. Tab-mode: CTA bottom=2611px, nav-icon-top=2710px -> gap=99px=33dp
  (required <=16dp). Improved from the prior 105dp but does not meet the AC. Cross-checked
  with a fresh dump (identical reading) and a pixel scan confirming the CTA's mint fill
  ends exactly at y=2611 (matches uiautomator bounds). Root-cause hypothesis (not proven,
  for the fix's next cycle): `tabModeBottomGap`'s doc comment assumes
  `MediaQuery.of(context).padding.bottom` is FOLDED to include the floating NBottomNav's
  full footprint (~104dp) under `extendBody:true`, but the observed 33dp gap is almost
  exactly `raw system safe-area (24dp, confirmed via `dumpsys window displays` ->
  overrideNonDecorInsets bottom=72px=24dp) + space2(8dp) = 32dp` — i.e. the live
  MediaQuery.padding.bottom in this build reads as the UNFOLDED raw inset, not the folded
  nav-bar-height value the comment/formula assumes. The widget test
  (`checkout_button_tab_mode_safe_area_test.dart`) passes because it hand-supplies
  `bottomSafe:34` (an iPhone-home-indicator-style MediaQuery override) rather than
  reproducing the real Scaffold+IndexedStack+extendBody fold — exactly the "unit test
  simulates the assumption, not the real widget tree" gap this delta-QA pass was asked to
  catch. Pushed mode (View Cart): CTA y=2719-2875, byte-identical to the prior PASS
  reading — unaffected, still correct.
- **BK6**: PASS. Collapsed single-row confirmed live: "If any product is not available:
  Call me ASAP" (a11y) / "Call me ASAP · Change" (visible), directly under the last
  basket item line before the Discount/Total block. Tap opens the same
  `NotAvailableBottomSheetWidget` bottom sheet. Default value hard-confirmed unchanged
  ("Call me ASAP", index 3) both before and after a live substitution_preference_set
  round-trip (set to "Notify me when it's back" then reverted to restore account state).
- **BK7**: PASS (mobile). Pixel-sampled the on-device discount row (not eyeballed): text
  colour (106,106,120) on white (255,255,255) -> WCAG contrast 5.32:1 (was 1.33:1, now
  >=4.5:1). Format is the same `−${amount}` (U+2212 MINUS SIGN) as desktop's own fix,
  confirmed byte-identical in source. Row confirmed fully ABSENT at a real discount=0
  store section live (Abu Nadia Grocery/Daily Fresh Market section showed Delivery
  Fee+ETA but no Discount row), and PRESENT with the correct format at a real
  discount>0 section (Fast Market, −82.72 AED).
- **BK2 a11y**: PASS. `uiautomator` dump shows TWO distinct nodes post-remove: "Removed
  from cart" (container, bounds [0,2323][1344,2680]) and "Undo" (clickable, bounds
  [876,2368][995,2500]) — independently focusable, single "Undo" label (not the prior
  doubled "Undo\nUndo" merge). Positive control in the same dump: "Removed from cart"
  present (tree was live). Double-tap idempotency re-confirmed live: 2 rapid taps on Undo
  (935,2434 x2, ~1s after the snackbar settled) produced exactly ONE
  `cart_remove_undone` log line (item_id:358, store_id:37) — the `identical(c, removed)`
  guard still holds.
- **48dp tap targets**: PASS. Remove control [1080,573][1224,717] = 144x144px = 48x48dp.
  Stepper Increase [1080,732][1224,876] / Decrease [826,732][970,876] = 144x144px each =
  48x48dp. Width-budget re-check: at a real 360dp logical width (`wm size 1080x2400`,
  density unchanged 480), RTL (Arabic via a local-only SharedPreferences language-key
  edit, not a DB write), and 1.3x text scale (`settings put system font_scale 1.3`,
  clamped by `MaterialApp.builder` per the guide) — individually and combined
  (RTL+narrow+1.3x) — the basket row's quantity column never overflows/wraps; qty values
  up to 2 digits (49, 17) render fully in all conditions. **Found an UNRELATED,
  pre-existing overflow** in `packages/nears_dls/lib/components/nitemcard/n_item_card.dart:438`
  (`_rowInfoBlock` Column, "RenderFlex overflowed by 15-19 pixels on the bottom") in the
  "You May Also Like" rail's `NItemCard` under narrow+1.3x-scale — NOT touched by this
  ticket's diff, filed as a regression_bug, does not affect this ticket's verdict.
- **`cart_quantity_changed`**: PASS. Live: `{item_id: 215, store_id: 13, from_qty: 49,
  to_qty: 48, ..., section: basket_lines, position: 1}` and a second row `{item_id: 334,
  ..., section: basket_lines, position: 2}` — section fixed from `cart_item` to
  `basket_lines`, position now a real 1-based value that varies per row (was always
  absent).
- **Spot-check** (property shapes unchanged from the earlier verified passes):
  `view_cart {value, currency, item_count, store_count:3, screen:basket,
  source:bottom_nav}` PASS. `remove_from_cart {item_id, price, quantity, value, store_id,
  method:remove_button, screen:basket, section:basket_lines}` PASS. `cart_remove_undone
  {item_id, store_id, quantity, screen:basket, section:basket_lines}` PASS.
  `substitution_preference_set {option:notify_when_back, is_default:0, screen:basket,
  section:substitution}` PASS.
- **AC-DLS (Widgetbook "Outlined Ring")**: **FAIL — task_bug.** The new
  `@widgetbook.UseCase(name: 'Outlined Ring', ...)` (added this fix cycle to close the
  prior AC-DLS storybook gap) exists in `widgetbook/lib/elements/n_icon_button_stories.dart`
  but was never wired into the generated `widgetbook/lib/main.directories.g.dart`
  (`build_runner` was not re-run/committed this cycle — that file's last touch is an
  unrelated ticket, NEARS-3637). Built + served the real release web build
  (`flutter build web --release` + `python3 -m http.server`) and deep-linked
  `#/?path=elements/icon_button/niconbutton/outlined-ring`: the app silently falls back
  to the "Welcome to Widgetbook" screen (confirmed via `web_find "Welcome to Widgetbook"`
  -> FOUND). Positive control: the SAME deep-link technique against the pre-existing
  `.../square` use-case does NOT show the Welcome fallback (confirmed NOT FOUND) — proving
  the driving method is sound and the "Outlined Ring" story is genuinely unreachable, not
  a wrong-URL artifact. Evidence: `bug-bk3-widgetbook-outlined-ring-unreachable.png` +
  `.log` (grep of `main.directories.g.dart` showing only Gallery/Playground/Square
  registered).
- Reused PASS (unaffected by this fix cycle, not re-driven): BK4, BK5, BK8, BK9, BK10,
  AC-SHARED — see the first-pass evidence (comment 20437 era) for original demonstration.
