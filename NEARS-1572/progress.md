# NEARS-1572 — QA progress log

Worktree `/Users/Apple/Projects/nears-NEARS-1572-time-context-bar`, branch
`feat/NEARS-1572-time-context-bar`, HEAD `eceea37d` (verified, not the primary tree).
SDK `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9. Light mode only (dark deferred).

Surface: the widgetbook storybook served from THIS worktree
(`flutter run -d web-server --web-port 8099`), driven headless with the Python
Playwright driver. No emulator, no device lock taken, no DB touched.

## Harness integrity (NEARS-1544 fail-open)

The cataloged `?path=` deep link renders the widgetbook LANDING PAGE for every
component (identical sha256 `e1467f6489b003b7` across three different URLs while
`window.location.href` matched what was requested). Caught before any AC was
scored; see `bug-catalog-deeplink-fail-open.log`. Switched to the hash form
`#/?path=...`, which yields three distinct hashes.

Discrimination check on the working harness: the 13 boundary frames produced
**5 distinct band crops for 5 windows** — frames in the same window hash
identically, frames in different windows never do. The harness therefore
distinguishes content, rather than returning a constant.

Knobs were pinned through widgetbook's own `knobs={label:value}` query codec
(no slider dragging). Every frame asserts its own loaded URL and prints its own
`windowAt(...) => <window>` caption, read out of the semantics tree as text.

Sample validity: boundaries 13/13 frames valid (url_ok + band + label + caption);
state matrix 7/7 valid.

## Per-AC results

| # | Check | Result |
|---|---|---|
| 1 | Five windows render own label + glyph | PASS — all 5 labels distinct, all 5 glyphs painted, `bedtime` (lateNight) visible, NOT blank |
| 1 | Stitch frame diff | **NOT PERFORMED — no frame exists.** Compared against the written spec only |
| 2 | Boundary pairs 10:59/11:00, 14:59/15:00, 16:59/17:00, 21:59/22:00 (+4:59/5:00) | PASS — each pair differs in label AND band crop |
| 2 | Midnight wrap 23:59 / 00:00 / 00:30 | PASS — all three lateNight, band crops byte-identical (`bb19430812110e0e`) |
| 3 | Sliver hosts floating / pinned | UNIT-PINNED ONLY — storybook cannot host a CustomScrollView |
| 4 | 1.3x EN + AR, one line, no clip | PASS — EN 52->60, AR 56->66, band grows, long label ellipsizes |
| 4 | isLoading same footprint | PASS — caption displacement 0.0px vs resolved |
| 4 | isVisible:false paints nothing | PASS — caption displacement -52.0px (exactly the band height) |
| 5 | RTL glyph on right, no mirroring | PASS — label right edge lands at band_w - space4 - 20 - space2 in all 3 AR cases; glyphs identical to LTR |
| 6 | Fallback same fill/radius/padding, glyph-less | PASS — h=52 w=565.6 identical to resolved; label_dx=16 (no glyph slot) |
| 6 | now:null + no fallback renders nothing | PASS — no band, caption flush, -52.0px displacement, zero reserved gap |
| - | Glyph and label same ink (textStrong) | PASS — monochrome, no mint |

## Measured heights (real web fonts)

| case | rendered band height |
|---|---|
| EN 1.0x | 52.0 (== `heightFor(1.0)` / `baseHeight`) |
| EN 1.3x | 60.0 (== `heightFor(1.3)`) |
| AR 1.0x | 56.0 (**+4 over `heightFor`**) |
| AR 1.3x | 66.0 (**+6 over `heightFor`**) |

Arabic overflows the published `heightFor()` on real fonts; the component's
`minHeight` (not a fixed height) absorbs it, so nothing clips under the Column
host. Quantifies the slack a sliver extent needs — see the envelope followup for
NEARS-1574.

## Automated backstop

`flutter test` in `packages/nears_dls`: **1033 visible tests, 1033 success, 0
failures, 0 started-but-unfinished** — counted from testDone events, not read off
a summary line. The new file `n_time_context_bar_test.dart` was predicted at 53
tests from disk BEFORE running (30 literal declarations + 12 from the 13-row
boundary loop + 2 from the 2x2 height loop + 1 from the 2x loading loop + 8 from
the universal-props harness) and measured 53/53.

## Investigated and dismissed

Ghosted/doubled text on the States page fallback row. Reproduced identically with
the accessibility overlay off (same sha256), so not a capture overlay artifact —
but it disappears entirely at a normal 1000x1000 viewport, so it is a CanvasKit
artifact of the 4200px-tall capture viewport, not a component defect. Not filed.
