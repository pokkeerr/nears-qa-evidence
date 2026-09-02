# NEARS-2870 QA progress checkpoint

Device: emulator-5554 (Android, worktree package `com.izzes.nears.nears_nears_2870_chat_textfield_ninput`)
Backend: local `php artisan serve` on 127.0.0.1:8000 (Android via 10.0.2.2:8000)
Account: `customer@nears.com` (users.id 6) — the seeded chat fixture owner. Thread: admin ("Nears").

## AC1 [behav] — both composer fields render via NInput
- Mobile: hint "Type here....." visible, single soft-gray filled chrome, no double border. PASS.
- Desktop (via `wm size 2600x1400` / `wm density 160` desktop-breakpoint override on the same
  Android emulator — UserApp has no `web/` dir, NEARS-410 precedent): same NInput chrome
  rendered inside the "Live Chat" desktop card. PASS.
- Evidence: mobile-composer.png, desktop-composer.png.

## AC2 [ui] — visually matches DLS/Stitch chat frame
- Stitch frame `451558629d7047419b173b1540a2dc2a` (dark/RTL) mapped in
  docs/reskin/NEARS-412-help-chat-reviews-reconciliation.md; NInput chrome is itself the ported
  DLS visual per its own doc comment (pixel-identical to legacy `nears_input.dart`).
- Both arms: single filled+bordered NInput frame, no double-border/chrome artifact from the
  removed outer Container. PASS both arms.

## Regression sweep
- Multiline growth to 6 lines + internal scroll: typed 8 lines, screenshot shows exactly 6
  lines visible (Line4..Line8+cursor), Line1-3 scrolled off internally, no clipping/overflow.
  mobile-composer-multiline.png. PASS.
- Chat send: sent "NEARS-2870 QA send test" on mobile, "NEARS-2870 desktop send test" on
  desktop — both appeared in thread with fresh timestamp, composer cleared. PASS both arms.
- Attach-image icon: opened native photo picker on both arms, correctly positioned beside
  field (left in LTR, mirrors to right in RTL). PASS both arms.
- Length limit (1000 chars, Dimensions.messageInputLength): typed 1050 'A's, EditText text
  length capped at exactly 1000 on both arms (a11y dump). PASS both arms.
- Message list rendering/scrolling: unaffected across all navigations. PASS.
- RTL/Arabic (Get.updateLocale via VM-service evaluate — pty not used, but eval worked live
  on this nohup-backgrounded session): attach icon + send button + back button all mirrored
  sides correctly on both arms (a11y bounds before/after). mobile-composer-rtl.png,
  desktop-composer-rtl.png. PASS both arms.
- Dark mode: DEFERRED per policy — not exercised.
- Pre-existing UX-flagged item: desktop attach-icon Padding at chat_screen.dart:419 uses
  `EdgeInsets.symmetric(horizontal: ...)` (non-directional) instead of EdgeInsetsDirectional —
  confirmed still present, predates this ticket (diff only touches the TextField->NInput swap +
  dart-format). Symmetric-horizontal padding is direction-invariant so it renders identically
  under RTL (visually confirmed, no actual mirroring defect) — logged as regression-candidate,
  non-blocking.

## Logs
- Only line seen across the whole session: `[FAIL] ... type=LocationPermissionResolutionTimeout`
  from the initial location-permission grant during setup (before login) — unrelated to chat,
  reproduced once, never again. No chat-endpoint FAIL/ERR observed at any point.

## Automated backstop
- `flutter test test/` on the worktree: 5541 pass, 1 skip, 2 fail — both fails are
  `test/golden/dls_golden_test.dart` "DLS components — light/dark theme (variant: CI)"
  (0.20% pixel diff goldens). Reproduced IDENTICALLY on the unmodified base branch
  (`feat/userapp-reskin2`, primary tree, same 2 tests fail) — pre-existing golden flakiness,
  not caused by this ticket (no DLS package files touched by this diff).
