# NEARS-1475 — live QA progress log

Surface: Widgetbook storybook, **release web build** served from the ticket worktree
(`/Users/Apple/Projects/nears-NEARS-1475-module-switcher/widgetbook` →
`flutter build web --release` → `python3 -m http.server 8123` over `build/web`).
Driver: Python Playwright, single persistent Chrome session, **light mode only**
(dark deferred). Android `uifind.py` was **never used** — the whole run is off that path.

**Freshness:** every reading is a live DOM query against the same page object in the same
session, taken immediately after an explicit wait on a state-unique anchor
(e.g. `Grocery, 12 stores open, current module` only exists while the overlay is open;
the trigger's own node only reappears once the modal barrier is gone). Knob plumbing was
proved with a positive control before any knob-dependent claim
(`knobs={isVisible:false}` → trigger absent; `knobs={subtitles:false}` → row heights
55→49; `locale={name:ar-SA}` → barrier label becomes `إغلاق القائمة`).

| # | check | result |
|---|---|---|
| 1 | `flutter test` (packages/nears_dls) — run BEFORE any web build | 852/852 pass |
| 2 | `flutter analyze` (packages/nears_dls) | No issues found |
| 3 | Trigger renders inside NAppBar (AC3) | trigger node 44×44 @ x305.2,y8 inside the 56dp bar |
| 4 | Overlay opens below trigger, logical near edge (LTR) | menu x=305.2 == trigger x; first row y=64 (= 8+44+4+8 menu pad) |
| 5 | 4 module rows, one a11y node each | 4 × role=menuitem, merged labels |
| 6 | Selected row tint + mint check | Grocery row 11168 px `#D6F7E4` + 19 px mint |
| 7 | Unselected row | Food row 11350 px `#FFFFFF`, 0 mint |
| 8 | NEW tag on `isNew` row | Pharmacy row 364 px `#00FF99` badge |
| 9 | selectedId cycled → pharmacy | pharmacy tinted + check (19 mint), NO badge; grocery now white |
| 10 | Trigger mint dot when a module isNew | 36 px `#00FF99` at trigger top-end |
| 11 | `new module` knob off → dot clears | 0 mint px, same rect |
| 12 | Row tap fires onSelected with the picked id | snackbar `Switched to parcel` / `Switched to pharmacy` |
| 13 | Row tap dismisses the overlay | row nodes gone, trigger node back |
| 14 | Hardware/browser back dismisses | `go_back()` → rows gone, story URL unchanged |
| 15 | Tap-outside barrier exists | `Dismiss menu` role=button covering the panel |
| 16 | `isDisabled` → trigger renders, overlay never opens | group node present, button node gone, 0 rows after tap |
| 17 | `isLoading` → skeleton, not tappable | no trigger node; `#EBE7E7` skeleton pixels |
| 18 | `isVisible:false` → nothing painted | trigger node count 0 |
| 19 | Empty module list → NO trigger, no placeholder | gallery empty cell: pure `#000080`, zero navy-glass |
| 20 | Error → trigger keeps rendering | trigger node still present with `error:true` |
| 21 | Error overlay body = message + full-width retry | card 306..584 × 57..188, stacked |
| 22 | Retry is a live control | hover repaint `#FFFFFF`→`#EBEBF5`, 6882 px |
| 23 | RTL: trigger mirrors | x 305.2 → 1090.8, 16 px inset from the logical start edge, mirrored |
| 24 | RTL: overlay anchors to the trigger's logical near edge | menu right 1134.8 == trigger right 1134.8 |
| 25 | RTL: mint dot mirrors | mint at trigger top-LEFT, 0 mint at top-right |
| 26 | AC5 NAppBar regression (bell, cart badge, back, location) | all present + functional LTR and RTL; no switcher when the slot is unset |
| 27 | Runtime log across every run | clean — zero page errors, zero Flutter exceptions |

## Not verifiable on this surface (stated, not assumed)
- **1.3× text scale inside the overlay.** The popup opens as a route on the ROOT navigator, so it
  escapes the widgetbook TextScaleAddon's MediaQuery. Proven live: at factor 1.0 / 1.3 / 2.0 the
  overlay row heights are identical (55/55/49/48) while the in-story app-bar text node grows
  36→56 px. Harness artifact, not a product claim either way.
- **RTL mirroring of the row's INTERNAL layout** (disc leading / check trailing). Same mechanism —
  the route renders under the root Localizations (en/LTR); only the anchoring and the barrier label
  are captured at the call site, and both of those DID mirror.
- **`onRetry` actually firing.** The story's `onRetry` is a no-op and every tap inside the error
  card closes the overlay, so closure is not a discriminator. Covered by the unit test.
- **AC1 "replaces the module-home context" / "without losing the combined cart"** — no app call
  site exists yet (NEARS-1473).
- **AC2 persistence half ("after the user's last visit", "clears once seen")** — no persisted
  module-seen state exists; deliberately not invented.

---

## Delta re-QA — cycle 1 (after the `_NErrorEntry` inert-host swap)

Same worktree, still uncommitted. `flutter test` **855/855** and `flutter analyze` clean, both run
**before** the rebuild; then a fresh `flutter build web --release` served on a **new port (8124)** so
no asset from the first run's origin could be reused. Freshness discipline unchanged: live DOM
reads in one session after a state-unique anchor, `knobs={isVisible:false}` positive control run
first, Android `uifind.py` never touched.

| bug | status | measured |
|---|---|---|
| B1 error icon opacity | **FIXED** | icon core now `#BA1A1A` (== NearsTokens.error); contrast **6.46:1** (was `#E5A8A8` / 2.0:1) |
| B2 retry a11y node | **FIXED** | discrete `{"label":"Try again","role":"button","box":{x:321.2,y:108,w:248,h:44}}`; message is its own node at x=353.2,y=77,w=216,h=18 |
| B3 tap on inert message dismisses | **NOT FIXED — still reproduces** | clicked the centre of the message text's OWN live rect (461.2, 86.0) → overlay dismissed. Card measured **x 305.2..585.2 (280 wide)** from the retry node + 16 px padding, confirming the first run's 306..584. Every non-button point inside the card falls through (message centre, the 12 px inter-row gap, the bottom-left padding column). |
| B4 no-regression spot-check | **CLEAN** | overlay opens/lists/anchors identically (rows 55/55/49/48 at x=305.2); selected tint 11168 px `#D6F7E4` + 19 mint; NEW badge 364 px `#00FF99`; trigger dot 36 px; row select → `Switched to food` + dismiss; back-dismiss and tap-outside dismiss both work for the module list AND the error overlay; `isLoading`/`isDisabled`/`isVisible:false`/empty-gallery all byte-identical to cycle 0. Runtime log clean. |

**On the disagreement (B3):** the engineer's hypothesis was that x=445 landed on the modal barrier
because the card is "only ~280px wide". The card *is* 280 wide — but it starts at x≈305, so it ends
at x≈585 and 445 was always 140 px inside it. My original bounds were right; no correction needed.
The cycle-1 re-test removes the arithmetic from the argument entirely by clicking an element
resolved **by its visible text**, not by a computed coordinate.
