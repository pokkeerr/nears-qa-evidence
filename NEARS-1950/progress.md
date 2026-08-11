# NEARS-1950 — phase [8] live QA progress

Build under test: worktree `nears-NEARS-1950-lightbox-gates`, branch `feat/NEARS-1950-lightbox-gates`,
commit `e63b22ba`, base `821ffdae`. Flutter **3.41.9** (`/Users/Apple/Tools/flutter`), `meta` pin `1.17.0`.
Device **emulator-5554** — 1344x2992 @ 480 (no `wm` override), top inset 159 px = 53.0 dp, bottom inset 72 px.
Disk before install: **1229856 KB = 1201 MB** free (floor 800 MB). Lock acquired via `qa_lock_acquire`
(`pid_kind=anchor`, pid 40511), no stale reclaim.

## Build freshness — two stage

| stage | measurement |
|---|---|
| pre-install artifact | md5 `62c3422710cecb8d757f7a7fd9b61659`, lastUpdateTime `2026-08-12 02:45:58` (a foreign build) |
| post-install artifact | md5 `3cc39a92dfe1d56a467806531fec23ac`, lastUpdateTime `2026-08-12 03:27:49` |
| post-observation artifact | md5 `3cc39a92dfe1d56a467806531fec23ac` — unchanged, no swap under the run |
| **live isolate** (VM service `getScripts` + `getObject`) | `package:sixam_mart/features/chat/widgets/image_preview_widget.dart`, source_len 14016: `top: !isDesktop, bottom: !isDesktop,` ×1, `left: !isDesktop` ×0, `right: !isDesktop` ×0. Positive control `class ImagePreviewWidget` ×1. **FRESH** — re-run after all observations, same result. |

The live-isolate probe reads the source text the **running** isolate compiled, so it *would* come out
differently on a stale (pre-fix) build — `left: !isDesktop` would count 1. It is a real discriminator,
not a restatement of the disk content.

## Observations

| # | check | result | evidence |
|---|---|---|---|
| 1 | Close affordance below the status bar | Close `[1200,219][1344,363]`; top 219 px vs 159 px inset = **60 px = 20.0 dp clear**. Glyph painted: 648/20736 non-black px, brightest `(255,255,255)`; control box directly below = 0 non-black. | `ac1-lightbox-close-and-pane.png` |
| 1b | Close is tappable | centre tap `(1272,291)` dismissed the lightbox back to conversation 47 (composer + `Add Image` present). Hardware BACK also dismisses. Reopen gives the identical bounds. | `ac1-lightbox-reopen.png` |
| 2 | Media pane inside the viewer, no RenderFlex overflow | live render tree: **0 `OVERFLOWING`** among **91 `RenderFlex`** nodes (token confirmed at `flutter/lib/src/rendering/flex.dart` `header += ' OVERFLOWING'`). Screenshot: **0** yellow overflow-stripe px. Backdrop ends at y=2920 = 2992 − 72 (bottom inset); below it is `#FCF9F8`. | `ac1-lightbox-close-and-pane.png` |
| 3 | No left/right clipping | image occupies rows 970-2313 and cols 0-1343 — a full **1344x1344** square, aspect-preserved width-fit, both edges present, nothing cut. | same shot |
| 4 | `ui_errors` | **exit 0**, `scanned 321 flutter-tag lines of 147515 buffer lines; 0 match(es)`. Non-vacuous. | — |
| 4b | pid-scoped log (own pid 1572) | 333 lines, **0** matches of `[FAIL]/[ERR]/Unhandled Exception/EXCEPTION CAUGHT/overflowed by/is not a subtype`. Instrument positive control on the same pipeline: 178 hits for a token known present. Buffer-wide selector also matched 0 foreign-pid lines this run. | — |

## NOT TESTED — recorded verbatim, never rounded up

- **prev/next arrows and `PageView` paging — NOT TESTED, unreachable by construction.** Confirmed
  read-only in `multi_food_db`: conversation 47's only attachment is `messages.id 75`, `file` =
  a **one-element** array (`2026-08-10-nears1719fixture.webp`). This is an observation about
  observability, not correctness.
- **Desktop / `Get.dialog` branch — NOT TESTED.** No desktop target exists (UserApp is mobile-only).
- **left/right insets in portrait — NOT TESTED.** No pool device presents one.
- **iOS `bottom` guard — N/A on Android**, unchanged by this diff.
