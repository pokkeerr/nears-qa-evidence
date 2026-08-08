# NEARS-1660 — live QA progress log (fix_cycle 0)

Device `emulator-5558` (448x997 dp, light mode, en + ar) · branch
`feat/NEARS-1660-message-bubble-dls` · base `5a8ae670` ·
Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 (pubspec.lock `meta: 1.17.0`) ·
installed APK md5 `9e305c6dda046b504a2784c9acc2a1fe` (identical before AND after every
observation; equals the md5 of the artifact built from this worktree).

Fixture: `customer@nears.com` (users.id 6 -> user_infos.id 3, "Customer Nears"),
conversation 46, peer user_infos.id 111 = vendor 1 "Demo Store", 15 messages.
Confirmed read-only against `multi_food_db`. Zero DB writes issued by QA.

| # | AC | Verdict | Method | Evidence |
|---|----|---------|--------|----------|
| 1 | no `roboto*` / `Dimensions.fontSize*` left | PASS | code count | 16 matching lines at base -> 0 on branch |
| 2 | `primaryColor` text colour kept | PASS | code count | 2 at base -> 2 on branch (lines 327, 353) |
| 3 | order card content + ordering | PASS | widget test **and** live via response-rewriter proxy | `ac3-ac4-order-card-and-image-bubbles-ltr.png` |
| 4 | plain + image bubbles unchanged | PASS | live, both sender sides | `ac4-ltr-plain-bubbles-both-sides.png`, `ac3-ac4-...png` |
| 5 | accepted visual drift recorded | n/a (pre-authorised) | - | - |
| 6 | RTL alignment flips; id/prices do not mirror | PASS | live, Arabic | `ac6-rtl-arabic-alignment-flip-and-order-card.png` |

Log gate: 168 `flutter` logcat lines scanned across the whole session,
**0** matches for `[FAIL]` / `[ERR]` / `Exception` / `RenderFlex` / `overflowed` /
`Failed assertion`; **0** non-200 `http_status=` lines.

Automated backstop: `flutter test` (UserApp) = `+3121 ~2 -6`; the 6 failures are the
documented pre-existing baseline by composition (`coupon_controller_test` x3,
`dls_golden_test` x2, `category_screen_back_button_test` x1), extracted with
`grep -E '\[E\]$'` over the full 17467-line output, not a tail.
`message_bubble_dls_test.dart` alone = 11/11 pass.
