# NEARS-2084 — QA [8] evidence (fix_cycle 0, first pass)

Device: emulator-5556 (Pixel_10_Pro_2), physical 1344x2992 @ density 480, no `wm` override.
Build: `flutter build apk --debug` from worktree `/Users/Apple/Projects/nears-NEARS-2084-header-a11y`
at HEAD `371bef88` (base `a72e6af6`), SDK `/Users/Apple/Tools/flutter` 3.41.9.
APK built 20:45 (source commit 20:39) — newer than source, installed with `adb install -r`.
Backend: local `php artisan serve --port=8000` (HTTP 200 on `/api/v1/config`); app dev host `10.0.2.2:8000`.
Login: `customer@nears.com` on the target emulator; saved delivery address present.
Theme: light only (dark deferred).

## Instrument discipline
Every reported dump also resolved a positive control of the same widget class:
- dashboard-tab arm -> `Basket` (android.widget.Button) exit 0 @ 912,2776 (also the ARM DISCRIMINATOR: bottom nav present)
- pushed arm        -> `Clear` exit 0 @ 1053,339, and `Basket` exit 1 (no bottom nav = pushed arm confirmed)
Dumps were always taken twice (first dump routinely returns nothing).

## Per-label results — exit code AND resolved bounds

### Dashboard-tab arm (the fix) — SearchScreen(fromDashboardTab: true)
| label | exit | centre | resolved bounds | area |
|---|---|---|---|---|
| `Filter` | 0 | 1227,339 | [1155,267][1299,411] | 144x144 px (48dp) — own node, NOT page-sized |
| `Search for items...` | 0 (unique; was exit 3 pre-fix) | 585,339 | [45,267][1125,411] | own node |
| `Deliver To:` | 0 | 1000,213 | [701,189][1299,237] | own node |
| `Basket` (control) | 0 | 912,2776 | [1032,2680][1272,2872] | bottom nav present |

No `android.widget.Button [0,0][1344,2920]` page-sized node anywhere in the dump: the
merged viewport-child node measured pre-fix by [6] is gone.

`ui_tap "Filter"` @ 1227,339 -> filter sheet opened (`Apply Filters`, `Scrim`, `Sort by`
all present in the next dump). Repeated logged-out AND logged-in.

### Pushed arm (built-in positive control) — module home -> search bar -> /search
| label | exit | centre |
|---|---|---|
| `Filter` | 0 | 1227,339 |
| `Search for items...` | 0 | 585,339 |
| `Deliver To:` | 0 | 1000,213 |
| `Clear` (control) | 0 | 1053,339 |
| `Basket` | 1 (no bottom nav — arm confirmed) | — |

Geometry identical on both arms: `Filter` [1155,267][1299,411], centre 1227,339 — the
expected coordinate. Nothing moved.

### Results state (query typed, dashboard arm)
Back `[45,189][129,273]` @ 87,231 exit 0 · `Filter` @ 1227,375 (`[1155,303][1299,447]`) exit 0 ·
`Deliver To:` @ 1021,231 exit 0 · `Search for items...` @ 585,375 exit 0 · `Basket` exit 0
(bottom nav intact). All separate nodes; header shifts down 36px because the results state
adds the back row — expected, same on both arms.

### Filter-sheet dismissal (dashboard arm)
`Close` (X) -> returns to dashboard arm, 5 bottom-nav buttons at y 2680-2872 intact,
`Filter`/`Deliver To:`/`Basket` all still exit 0.
`Apply Filters` -> sheet gone (`Apply Filters` exit 1), same three labels still exit 0.

### GlobalSearchScreen (module-selection home -> "Search all categories")
Shares SearchNavyHeaderWidget. `Back` exit 0 @ 87,231 · `Deliver To:` exit 0 @ 1021,231 ·
`Recent searches` exit 0 @ 280,612 · `Clear All` exit 0 @ 1197,612 ·
`Search all categories` exit 0 @ 672,375 · `Filter` exit 1 (correct — this screen has no
filter control). No regression.

### RTL / Arabic (live, dashboard-tab arm)
App language switched to عربى at runtime.
`فلتر` exit 0 @ 117,345 (`[45,273][189,417]`) — mirrored, matches the nav guide's ~117,339
prediction (6px: the AR header row sits at y=273 vs 267 in LTR, Arabic line metrics) ·
`البحث عن العناصر...` exit 0 @ 759,345 · `تسليم إلى:` exit 0 @ 344,216 ·
`سلة التسوق` (control) exit 0 @ 432,2776.
`ui_tap "فلتر"` opened the sheet (`تطبيق المرشحات` / `تمويه` / `الترتيب حسب`).

### a11y traversal order (dashboard arm, idle)
From the exposed AccessibilityNodeInfo tree, in document order:
1 `Deliver To: …` (View, [701,189][1299,237])
2 EditText hint=`Search for items...` [45,267][1125,411]
3 EditText hint=`Search for items...` (clickable) same bounds
4 `Clear` Button [981,267][1125,411]
5 `Filter` Button [1155,267][1299,411]
then body, then the 5 bottom-nav buttons.
The decorative location-pin icon is NOT a separate stop — confirmed, [7]'s prediction holds.
No back arrow on the idle tab root (it only exists in the results state), and `Clear` sits
between the field and `Filter` — both expected, neither a defect.
Live TalkBack utterance-by-utterance confirmation was NOT run — see the envelope.

## Logs
`ui_errors`: 396 flutter-tag lines scanned, 0 matches (mid-run) and 29 lines / 0 matches
(final, after a deliberate buffer clear + re-exercise, so the assertion is not vacuous).
Whole-session `logcat` grep for `[FAIL]` / `[ERR]` / `Unhandled Exception` / `RenderFlex` /
`overflowed`: zero hits. The search API answered `http_status=200` throughout.

## Automated
- UserApp `flutter test` (pinned SDK, this worktree): **+4050 ~2, 0 failed, 0 error events**
  = 4052 visible, exactly baseline 4049 + the 3 new tests.
- `packages/nears_dls`: **1186/1186 pass** — matches baseline.
- New pin file alone: 3/3 pass.
- FALSIFIABILITY: the same test file copied into a detached worktree at base `a72e6af6`
  FAILS its arm pin —
  `Expected: {'label': 'filter', 'hasTapAction': true, 'isPageSized': false}`
  `Actual: {'label': 'search_for_items\nfilter', 'hasTapAction': true, 'isPageSized': true}`
  — i.e. it reproduces the absorption mechanism pre-fix. The pushed-arm control test passes
  at base, as it should.
