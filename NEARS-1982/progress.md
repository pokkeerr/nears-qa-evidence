# NEARS-1982 — QA progress log (durable, appended live)

Branch `feat/NEARS-1982-substitution-selector` @ `c025308e`, base `feat/userapp-reskin2` @ `d552c9c3`.
Worktree (build source): `/Users/Apple/Projects/nears-NEARS-1982-substitution-selector`
Device: `emulator-5558` (lock acquired via `qa_lock_acquire`, key NEARS-1982, 981564 KB free).

## Static verification (pre-device)

- **Diff scope** = exactly 2 files: `D UserApp/lib/features/cart/widgets/substitution_preference_selector_widget.dart` (-54),
  `A docs/solutions/NEARS-1982-substitution-preference-selector-dead-code.md` (+239). No other file touched.
- **Deleted file absent** from the worktree: confirmed.
- **Residual references** to `SubstitutionPreferenceSelector` / `substitution_preference_selector`
  across `UserApp/lib` + `packages`: rc=1 (clean not-found, empty stderr). ZERO.
- **Surviving widget wired**: `SubstitutionPreferenceSection` declared in
  `UserApp/lib/features/checkout/widgets/substitution_preference_section.dart` and constructed in
  `UserApp/lib/features/cart/screens/cart_screen.dart` (one call site).
- **Pre-flight**: `AppConstants.baseUrl` = `http://10.0.2.2:8000` on Android (real local backend, not a
  demo host). Backend `http://127.0.0.1:8000/` -> HTTP 200. `adb reverse tcp:80 tcp:8000` present on 5558.

### AC3 clause "any dedicated tests for it are removed" — EMPTY TARGET SET (independently re-measured)

Instrument validity proven by positive control on the identical path set
(`UserApp/test`, `packages/nears_dls/test`):

| probe | rc | result |
|---|---|---|
| `SubstitutionPreferenceSelector` (subject) | 1 | not found, empty stderr |
| `substitution_preference_selector` (subject, filename/import form) | 1 | not found, empty stderr |
| `CartController` (POSITIVE CONTROL) | 0 | **60 files** matched -> instrument is live |
| `SubstitutionPreferenceSection` (control 2) | 1 | not found — surviving widget also has no test |

First attempt returned rc=2 (`No such file or directory`) twice: once because `UserApp/integration_test`
does not exist, once because zsh does not word-split an unquoted `$SET` variable. Both empty results were
therefore NO OBSERVATION and were discarded, not reported. Re-measured with explicit paths above.

**Conclusion: the removal clause had ZERO targets. No test was removed. This is an EMPTY clause, not work performed.**

## Per-AC results

### Install provenance (the stale-APK trap)

`scripts/qa-run.sh --print-root` -> `root: /Users/Apple/Projects/nears-NEARS-1982-substitution-selector (source: NEARS_ROOT)`.
Installed APK built at **`/Users/Apple/Projects/nears-NEARS-1982-substitution-selector/UserApp/build/app/outputs/flutter-apk/app-debug.apk`**,
mtime `Aug 14 15:02`, 112,741,162 bytes. The PRIMARY-tree APK is a different artifact
(`/Users/Apple/Projects/nears/UserApp/.../app-debug.apk`, `Aug 12 03:49`, 151,158,072 bytes) and was NOT installed.

### AC3 — live, PASS

Device `emulator-5558`, light mode. App pid 4734.

**Finder positive control (run BEFORE any assertion):** on the cart screen the finder resolved the
`Proceed to Checkout` CTA (`android.widget.Button`, bounds `[45,2719][1299,2875]`). The instrument is live,
so a subsequent "not found" would be a real absence.
First `ui_list` after wake returned 4 nodes / 0 labelled and the next dump failed outright
(`NOT ASSERTED: dump failed ... an empty result is NOT an empty screen`) — both discarded as NO OBSERVATION,
re-dumped after settle.

**Block renders.** Cart with 1 item (Banana, Fresh Mart Grocery). Live a11y nodes:

| node | content-desc | bounds |
|---|---|---|
| 10 | `Substitution Preferences` (section header) | `[45,1797][748,1881]` |
| 11 | `If an item is out of stock, what should we do?` | `[105,1956][907,2010]` |
| 12 | `Remove it from my cart` | `[105,2040][1239,2166]` |
| 13 | `I'll wait until it's restocked` | `[105,2166][1239,2292]` |
| 14 | `Please cancel the order` | `[105,2292][1239,2418]` |
| 15 | `Call me ASAP` | `[105,2418][1239,2544]` |
| 16 | `Notify me when it's back` | `[105,2544][1239,2659]` |

**5 rows, NOT chips** — all five share an identical x-extent (`105..1239`, 1134px full-bleed) and stack at a
uniform 126px vertical pitch. A chip rail would be variable-width and horizontally packed. Confirmed visually
in `ac3-cart-substitution-default.png`: five circular radio indicators, selected one filled mint with a check.

**Selection is live (`CartController.setAvailableIndex` / `notAvailableIndex`), proven two-sided by pixel diff
of the block region — no image was read to reach this verdict:**

| step | comparison | differing px / 701946 | verdict |
|---|---|---|---|
| CONTROL: two captures, no action between | A vs A2 | 0 (0.000%) | IDENTICAL — region is pixel-stable, so any later change is caused by the tap, not animation noise |
| tap `Please cancel the order` (non-default) | A vs B | 15665 (2.232%), bbox `(0,282,528,474)` | CHANGED |
| tap `Call me ASAP` (back to default) | B vs C | 15665 (2.232%), same bbox | CHANGED |
| round-trip | A vs C | 0 (0.000%), md5 both `1c08d0c97f24` | IDENTICAL — returned to the exact default state |

The diff bbox maps to absolute y `2322..2514` — spanning exactly two rows, `Please cancel the order` and
`Call me ASAP`, and no others. That is single-select radio behaviour (one row gains the fill, the previously
selected one loses it) and independently confirms `Call me ASAP` was the default.

**Logs — clean.** `ui_errors`: scanned 699 flutter-tag lines, **0 matches**. App-pid-scoped logcat
(`( 4734)`): 277 lines captured, grep for `[FAIL]|[ERR]|Unhandled|EXCEPTION CAUGHT|RenderFlex|overflowed|Exception:|E/flutter`
returned **rc=1, zero matches**. Capture control: the same 277-line filter does contain real app output
(`[NET] endpoint=/api/v1/stores/details/2 http_status=200`, `analytics: view_store`), so the filter was live,
not empty. All `E/` hits in the raw buffer belong to system pids 639/2576/1597 and are dated 08-13 (pre-session).

### Suites (run by me, pinned SDK `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9)

| suite | base `d552c9c3` | HEAD `c025308e` |
|---|---|---|
| UserApp `flutter test` | **+3757 ~2 -4** | **+3757 ~2 -4** |
| `packages/nears_dls` `flutter test` | (identical by construction — see note) | **+1177, All tests passed!** |

Base was measured, not assumed: the deleted file was restored with
`git show d552c9c3:<path>` and confirmed identical to base by blob hash
(`f1632d4f26cdfaf2730ccd0d464fc024d7eda116` on both sides) before the base run.
`git diff --name-only d552c9c3..c025308e -- packages/nears_dls` returns **zero files**, so the
nears_dls package is byte-identical at base and HEAD and the single run covers both.
`git diff --name-only d552c9c3..c025308e -- UserApp/test` likewise returns **zero files**.

The 4 UserApp failures are **red at base as well as HEAD**, in:

- `UserApp/test/features/category/category_screen_back_button_test.dart` — 1 (`standalone variant: showBackButton true => back arrow present (deep link)`)
- `UserApp/test/features/coupon/coupon_controller_test.dart` — 3 (min-purchase null `Get.context`; `applyTaxiCoupon` UC-03; NEARS-382 UC-07 free_delivery)

Neither file is under `features/cart`; grep for `Substitution|substitution|notAvailable` across both files
returns **rc=1 (no matches)**, so no failing test touches the changed surface.
Per instruction I do NOT claim "no new failure names" — that set is nondeterministic at identical counts
in this suite. The claim made is: identical counts base vs HEAD, and no failing test touches the changed surface.

### NFilterChip — component did not lose its last consumer

`grep -rln NFilterChip UserApp/lib` = **17 files while the base file was restored in the tree**, i.e.
**16 at HEAD** once `substitution_preference_selector_widget.dart` is removed. The deleted widget was one
of 17 consumers, not the last one. 16 live consumers remain (store/all-store screens, search, category,
checkout coupon + time-slot, address, home rails, item bottom sheet).

Live spot-check (search screen suggestion chips): `Rice` `[328,687][488,819]` and `Dove` `[518,687][694,819]` —
**variable width (160px / 176px) packed on a shared y**, i.e. genuine chip geometry, in clear contrast to the
substitution block's uniform full-bleed rows. Tapping `Rice` executed a real search (`Items (1)`, `Rice 5kg`,
`Nears Mart`), so the chip surface is live, not merely painted.

## RETRACTED FINDING — recorded because it nearly became a false bug report

Mid-run I observed the Basket **tab** cart (`CartScreen(fromNav: true)`) rendering the
`Substitution Preferences` header with **no card body and no option rows**, in both English and Arabic,
and I captured it as `bug-rtl-substitution-rows-missing.png`.

**That was a measurement artifact, not a defect.** `uiautomator` only reports on-screen nodes, the block sits
at the bottom of a long scroll, and my swipe had started at `y≈2000-2100` — on the **pinned** `Proceed to Checkout`
button, which is not part of the scrollable, so nothing actually scrolled and the dump was unchanged.
The tell that forced me to re-check rather than file it: `CartController.notAvailableList`
(`UserApp/lib/features/cart/controllers/cart_controller.dart`) is a **hardcoded, non-empty 5-element list**, so the
widget's `if (cart.notAvailableList.isEmpty) return SizedBox()` guard can never fire — a rendered header with
absent rows was therefore impossible, which meant my *observation* was wrong, not the app.

Re-measured by swiping inside the cart list (`y 1400 -> 500`, repeated), the full block renders on BOTH routes
and BOTH builds. The bug artifact was deleted; no bug is filed. **No new blank region exists.**

## Regression sweep

| # | surface | result |
|---|---|---|
| 1 | Cart, pushed route (`fromNav:false`) | header + helper + 5 rows; selection round-trip verified |
| 2 | Cart, Basket tab (`fromNav:true`), scrolled | full block renders — header `[45,496][748,580]`, helper, 5 rows `[105,739]..[1239,1369]` at 126px pitch |
| 3 | Checkout screen | renders **no** substitution control. Correct and pre-dating this ticket (`e3d12ffb`, NEARS-512, 2026-06-21). `grep SubstitutionPreferenceSection UserApp/lib/features/checkout/` matches only the widget's own definition file — no checkout call site. NOT filed as a regression of this delete. |
| 4 | RTL / Arabic, cart block, scrolled | PASS — header `تفضيلات الاستبدال` right-aligned `[869,466][1299,559]` (LTR was left-aligned `[45,1797][748,1881]`); helper `إذا نفد أحد المنتجات، ماذا نفعل؟` right-aligned; all 5 options translated, same full-width 126px pitch. Bottom nav mirrored (Home moved x`72..312` -> x`1032..1272`). |
| 5 | Empty cart | `Back / Basket / Your cart is empty` — clean empty state, no blank region |
| 6 | `NFilterChip` surface (search) | live and functional (see above) |

**Session-wide logs, final:** `ui_errors` scanned 1111 flutter-tag lines, **0 matches**. App-pid-scoped logcat
(pid 7591): 443 lines captured, error grep **rc=1, zero matches**; capture control shows real trailing app output.

## Device / build ledger

- HEAD APK installed for the AC3 verdict: built `15:34` from the worktree (`--print-root` -> `NEARS_ROOT` = worktree).
- A base-state APK (deleted file restored, blob-verified) was built at `15:31` and installed only to settle the
  retracted finding above; the tree was returned to HEAD (`git status --porcelain` clean) and HEAD rebuilt before
  the final observations.
- Dark mode never enabled (deferred, light-only per policy).



