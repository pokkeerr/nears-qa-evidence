# NEARS-1517 — quantitative RTL mirror analysis (qa-NEARS-1517-2)

Light mode only (dark deferred). Device emulator-5554, UserApp debug from worktree
`nears-NEARS-1517-nicon-rtl` @ `8fc099e9`, APK installed 2026-08-11 04:22:55 local
(sha256 `249f179ef353…`), SDK `/Users/Apple/Tools/flutter` 3.41.9 (`meta: 1.17.0`).

## Instrument

Eyeballing an arrow is not a measurement. For each glyph: take its tight bounding box in the
LTR (English) capture and in the RTL (Arabic) capture, normalise both to 48x48 greyscale, then
compare `MSE(ltr, rtl)` against `MSE(ltr, mirror(rtl))`. The smaller one names the truth.

The test is falsifiable in the direction that matters: had the pre-fix double-flip still been
live, the *same* run would have printed a near-zero in the `mse_same` column instead. The large
`mse_same` values below are what a FAIL would have looked like, so a zero in `mse_flip` is
signal, not a tautology.

Script: `mirror_test.py` (session scratchpad).

## Results — 4 surfaces, 9 glyphs

| Surface | glyphs | mse_same | mse_flip | verdict |
|---|---|---|---|---|
| Profile/menu `chevron_right` (`menu_screen.dart:461`) | 6 | 5011.2 | 0.0 | mirrored |
| App bar back arrow (`n_appbar.dart`, observe-only) | 1 | 11697.4 | 0.0 | mirrored |
| Cart CTA `NButton.trailingIcon: 'arrow_forward'` (`cart_screen.dart:1616`) | 1 | 1477.8 | 10.8 | mirrored |
| Chat composer `send` (`chat_screen.dart:832`) | 1 | 12772.7 | 0.0 | mirrored |

Bounds corroborate independently — the glyph boxes land at exactly mirrored x:

- menu chevron: LTR `x 1189-1209`, RTL `x 135-155` (`1344-1209 = 135`)
- appbar back: LTR `(96,225,144,273)`, RTL `(1200,225,1248,273)`
- send button mint circle: LTR `x 1170-1312`, RTL `x 30-172`; glyph ink 972 px in both

Composite: `mirror-comparison-composite.png`.

## Not observed, and why

- **Chat image-preview gallery arrows** (`image_preview_widget.dart:301/332`, the reverted
  NEARS-1661 workaround) — both arrows require a message carrying >1 file. The DB holds exactly
  one message with a file and it has exactly one:
  `messages.id=75` -> `[{"img":"2026-08-10-nears1719fixture.webp"}]`. Unreachable without a DB
  write, which QA does not do. **unverifiable — data gap.**
- **`NStoreCard(showChevron: true)`** — its only host is `RecommendedStoreView`, rendered solely
  by `shop_home_screen.dart`. No shop/ecommerce module exists: active modules are grocery, food,
  pharmacy, parcel only. **unverifiable — no such module in this environment.**
- **`NActiveOrderBanner` chevron** — zero call sites in `UserApp/lib`; `widgetbook/lib` only.
  **not reachable in the UserApp** (scope error in the sweep list, not a defect).

## Logs

`flutter run` console, 2558 lines covering splash -> module home -> profile -> orders -> order
detail -> tracking -> conversation list -> chat -> two language switches -> Arabic navigation:
**0 `[FAIL]`, 0 `[ERR]`, 0 framework exceptions, 0 overflows.**

12 `FATAL EXCEPTION` blocks are all `UiAutomationService … already registered!` from
`com.android.commands.uiautomator` — two dump sessions colliding on one device. QA-tooling, not
the app. It matters because the failed dump leaves the previous `/sdcard/*.xml` in place, so a
following `cat` returns a **stale tree that reads as a live observation**.
