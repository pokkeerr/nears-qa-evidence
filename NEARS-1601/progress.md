# NEARS-1601 — LIVE QA evidence (semantics trees, both branches)

Device **emulator-5556** (448x997dp, density 480). Fix APK md5 `06395b9316fabc85e927810551587120`
(worktree `feat/NEARS-1601-nfilterchip-semantics` @ `6e9c6c21`), verified identical before AND
after every observation below. Merge-base comparison APK md5 `2b9ffbb45025ac55f5051f34dde51231`
(detached @ `38464d91`). Flutter 3.41.9 (`/Users/Apple/Tools/flutter`). Light mode only.

## Oracle + positive control

Live readings come from the running app's VM service:
`ext.flutter.debugDumpSemanticsTreeInTraversalOrder`. Semantics were forced on by enabling
`AccessibilityMenuService` (a real AccessibilityService; leaves touch behaviour untouched).
Cross-checked against `adb shell uiautomator dump` = the actual Android AccessibilityNodeInfo
tree a screen reader consumes.

**Flag encoding in this Flutter version** — the dump does NOT print `isSelected: Tristate.X`.
It prints a flag list, and the three states are distinguished as:

| Tristate | rendered flags |
|---|---|
| `Tristate.none` (no selection concept — the PRE-FIX reading) | neither `hasSelectedState` nor `isSelected` |
| `Tristate.isFalse` | `hasSelectedState` present, `isSelected` ABSENT |
| `Tristate.isTrue` | `hasSelectedState` AND `isSelected` present |

**Negative control (same dump, proves `isFalse` != `none`):** a store card on the Food home,
which is a button with no selection concept, renders `flags: isButton, isFocusable` — no
`hasSelectedState`. So the oracle does distinguish "no selection concept" from "not selected".

**Positive control (proves the flag tracks the real prop, not a constant):** cuisine row before
and after one tap on "American" —

```
BEFORE   flags: isSelected, isButton, isFocusable, hasSelectedState   label: "All"
         flags: isButton, isFocusable, hasSelectedState               label: "American"
AFTER    flags: isButton, isFocusable, hasSelectedState               label: "All"
         flags: isSelected, isButton, isFocusable, hasSelectedState   label: "American"
```

## AC1 — native `Semantics(selected:)` on a live chip

Food home, `cuisine_filter_row.dart`. Flag and label read SEPARATELY:

```
SemanticsNode#185  flags: isSelected, isButton, isFocusable, hasSelectedState
                   label: "All"                 -> isSelected = Tristate.isTrue
SemanticsNode#186  flags: isButton, isFocusable, hasSelectedState
                   label: "American"            -> isSelected = Tristate.isFalse (NOT none)
SemanticsNode#187  ... label: "Indian"          -> Tristate.isFalse
SemanticsNode#188  ... label: "Italian"         -> Tristate.isFalse
SemanticsNode#189  ... label: "Japanese"        -> Tristate.isFalse
```

No label carries a state word. **PASS.**

## AC2 — 3 confirmed gap sites, NOT edited by this ticket

**category_screen.dart** (sub-category rail, Burgers category):
```
flags: isSelected, isButton, isFocusable, hasSelectedState   label: "All"
flags: isButton, isFocusable, hasSelectedState               label: "Classic Burgers"
```
after tapping "Classic Burgers" the pair inverts (chip still taps).

**add_address_screen.dart** (Label As):
```
flags: isSelected, isButton, isFocusable, hasSelectedState   label: "Home"
flags: isButton, isFocusable, hasSelectedState               label: "Office"
flags: isButton, isFocusable, hasSelectedState               label: "Others"
```
after tapping "Office" the selection moves to Office.

**search_screen.dart** (recent-search chip, after searching "burger"):
```
SemanticsNode#628  flags: isButton, isFocusable, hasSelectedState   label: "burger"
```
-> `Tristate.isFalse`, not silence. NOTE: BOTH search_screen chip sites hardcode
`selected: false`, so a selected branch does not exist at this surface by construction.

**PASS** — the component fix alone reached all three unedited files.

## AC3 — item_bottom_sheet, state announced exactly ONCE

**NewVariationView** (`Classic Cheeseburger`, Size group), after selecting Large:
```
SemanticsNode#1256  flags: isButton, isFocusable, hasSelectedState   label: "Regular"
SemanticsNode#1257  flags: isSelected, isButton, isFocusable, hasSelectedState
                    label: "Large, +<3 AED>"
```
**VariationView / legacy** (`Dove Whitening Body Spray`):
```
SemanticsNode#2249  flags: isSelected, isButton, isFocusable, hasSelectedState  label: "250 ml"
SemanticsNode#2250  flags: isButton, isFocusable, hasSelectedState              label: "500 ml"
```
Platform-layer node count per label = 1 (`uiautomator`: `Regular` x1, `Large, +3 AED` x1).
The removed `'selected'.tr / 'not_selected'.tr` word is gone from every label; state comes only
from the native flag. **PASS — no double-announce here.**

## AC4 — 4 independently-found gap sites

- **store_screen.dart** — gap closed BUT a new double-focus defect introduced; see
  `bug-store-screen-double-announce.log`. **FAIL.**
- **all_store_screen.dart** (veg/non-veg type chips):
  `isSelected+hasSelectedState "All"` / `hasSelectedState "Veg"` / `"Non-Veg"`; inverts on tap. PASS.
- **store_item_search_screen.dart** (ETA/Price/Organic/Brand): all four `hasSelectedState`
  when unselected; `ETA` gains `isSelected` on tap. PASS.
- **pharmacy_nearby_view.dart** — UNVERIFIABLE, policy-parked (Pharmacy is a hard stop this
  sprint; surface not driven).

## AC5 — onRemove semantics intact

Selected cuisine chip "American" keeps its nested remove node as a distinct child:
```
SemanticsNode#186  flags: isSelected, isButton, isFocusable, hasSelectedState
                   label: "American"
  └─SemanticsNode#208  Rect.fromLTRB(77.3, 15.0, 91.3, 29.0)
                       actions: tap
                       flags: isButton
                       label: "Clear Filter"
```
This is exactly the node `excludeSemantics: true` would have deleted — label + button role both
survive. Functionally: tapping it cleared the filter (selection returned to "All", the
"Clear Filter" node disappeared) WITHOUT firing the row's main action. **PASS.**

## Logs (all ACs)

Whole session: exactly ONE exception — `SocketException ... address = localhost` from the image
codec (the documented emulator/`APP_URL` env issue, images only). ZERO `[ERR]`, ZERO `[FAIL]`,
ZERO overflow warnings, no exception tied to any chip interaction.

## Automated backstop

- `packages/nears_dls` -> `flutter test test/elements/n_filter_chip_test.dart` — **23/23 pass**
  (incl. the 4 new NEARS-1601 cases).
- `UserApp` -> `flutter test test/common/widgets/item_modifier_dls_test.dart` — **14/14 pass**.
- These are isolation tests and structurally cannot catch the store_screen wrapper interaction.
