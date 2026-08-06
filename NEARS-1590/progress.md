# NEARS-1590 — live QA progress log

Device `emulator-5556` (sdk gphone16k arm64, 1344x2992 @480dpi = 448x997 dp), light mode only
(dark deferred). Build: `flutter run` from worktree
`/Users/Apple/Projects/nears-NEARS-1590-food-modifier-sheet` (branch
`feat/NEARS-1590-food-modifier-sheet`), Flutter 3.41.9 (`/Users/Apple/Tools/flutter`).
Backend `php artisan serve :8000`, app `baseUrl` = `http://10.0.2.2:8000`.
Login `customer@nears.com` (user 6), zone 1 "Demo Zone — Dhaka".

| # | AC | Result | Evidence |
|---|----|--------|----------|
| AC1 | NAccordion + NBadge + NFilterChip Wrap, name + delta | PASS | Size/REQUIRED + "Large  +3 AED"; Toppings/OPTIONAL; legacy no-badge/no-delta |
| AC2 | Total recomputes both directions; cart agrees | PASS | 9→11→13→12→13→15→13→12; cart subtotal 14 AED; reopen 14 AED |
| AC3 | Zero new components | PASS | diff adds no classes; 6 DLS elements, all in catalog.yaml |
| AC4 | Groups expanded on first paint | PASS | chips present in a11y tree on open, no tap |
| AC5 | Chip label = state + delta | PASS (known gap) | selected: "Large, +3 AED, selected"; unselected: no state word |
| AC6 | Stepper names its own add-on | PASS | Add/Delete/Minus + "Extra Cheese"/"Bacon"/"Jalapeños" |
| AC7 | No truncation on 5-value group | PASS | 5 chips, 2 rows @448dp / 3 rows @360dp, no "view N more" |

## Risk probes
- Add-on zero state: compact mint "+", contributes exactly 0 (total held at base 9 AED). PASS.
- Decrement at qty 1 removes the add-on (row returns to compact). PASS.
- Chip geometry (the flagged NFilterChip full-width defect): NOT reproduced — `IntrinsicWidth`
  mitigation holds. Regular w=225 / Large w=351 share y=[1271,1403].
- Legacy Grocery (item 84): bare names, no delta, no badge; total 200→300 AED. PASS.
- RTL/Arabic: first chip on the right; `+` correctly leads the price run (bidi hazard did not
  materialise); NQtyStepper order does not flip. PASS.
- Cart-edit re-entry: selections pre-populated, total 14 AED, no drift. PASS.
- Small screen 360x640 dp (`wm size 1080x1920` + `wm density 480`): reflows to 3 rows, no overflow.
- Regression: empty-`food_variations` item renders compact sheet, no empty group header, no crash.

## Logs
Run log 1441+ lines, instrument proven live (captured `items/details/16`, `items/details/84`,
wish-list POST). Zero `[ERR]`/`[FAIL]`/overflow/exception during any AC.
Pre-AC only: location-screen snackbar (`access_location_screen.dart:456`) from zone navigation,
and pre-existing `[FAIL] /api/v1/coupon/list http_status=422`.

## Instrument validity
- `uinav.sh` SOURCED (not invoked); `ui_list` returned non-empty throughout.
- `ui_errors` asserted NOTHING — its logcat source had 0 `I/flutter` lines (0 valid samples).
  Reported as a SKIP, not a pass; the `flutter run` log was used instead and proven live.
- Add-on `+` had no separate a11y label (row merges name+price+button into one node); tapped via
  live-resolved node bounds, never a hardcoded coordinate.

---

# Cycle 2 — DELTA re-QA, AC5 only (2026-08-06)

Cycle-1 AC5 was reported "PASS (known gap, as specified)" because the packet instructed me to
accept the missing `not_selected` key. The team lead escalated it and was right: an unselected
chip announced `'{level}, {delta}'` then fell silent, so "this option is off" was
indistinguishable from "no information about this option". AC5 was genuinely UNMET in cycle 1.

**Build freshness (proven, not assumed):** APK rebuilt from the worktree and installed 18s before
first probe; `unzip -p app-debug.apk assets/flutter_assets/assets/language/{en,ar}.json` shows the
new `not_selected` key INSIDE the installed artifact. Not a stale APK.

| AC | Result | Evidence |
|----|--------|----------|
| AC5 | PASS | 7/7 Food chips + 2/2 legacy chips + 7/7 Arabic chips carry an EXACT terminal state token; 0 silent |

## Matching discipline (the trap)
`not_selected` contains `selected`, and the en VALUE "not selected" also contains "selected".
The Arabic pair repeats it: `غير محدد` contains `محدد`. Every check therefore compares the
**last comma-separated segment for exact equality** — never a substring/`in` test.

## Observed labels
- Food unselected: `Large, +3 AED, not selected` (delta retained, state explicit)
- Food selected:   `Large, +3 AED, selected`
- Legacy (no delta): `250 ml, selected` / `500 ml, not selected`
- Arabic: `Large, +د.إ. 3, غير محدد` → `محدد` on select; raw-key leaks found: 0
- Both directions demonstrated on Food, legacy, and Arabic.

## Instrument validity
- `uinav.sh` SOURCED, never invoked.
- `ui_errors` NOT used — established in cycle 1 as vacuous on this emulator (0 `I/flutter` lines
  reach its logcat buffer). Kept out of the evidence chain entirely.
- Log instrument: `flutter run` log, 943 lines, 298 `[NET]` entries, captured `items/details/16`
  and `/84` — proven live. Zero `[ERR]`/`[FAIL]`/overflow/exception across all of cycle 2.
- Per-sample validity counts reported for every sweep above.
