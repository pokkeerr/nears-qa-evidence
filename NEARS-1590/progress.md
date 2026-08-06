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
