# NEARS-1558 — live QA record (phase [8])

**Verdict: FAIL** — 1 blocking defect (`bug-active-label-contrast`).

## Surfaces
Widgetbook storybook run as a **native Android app** (not the web canvas), so the
NEARS-1544 web route fail-open never applies. Two devices:

| Device | Use |
|---|---|
| `emulator-5556` | shipped `Gallery` + `Playground` use cases (AC1-4, AC6-8, universal props) |
| `emulator-5554` | scratchpad-only QA harness (AC4 Arabic 1.3x, AC5 pinned/floating hosts) |

Revision under test: `n_module_row.dart` @ 387 lines (single shared `_onMint`),
APK built 2026-08-03 20:11 from `packages/nears_dls` in this worktree.
**The file changed on disk at 23:00:26 mid-run** — see "Tree moved" below.

## Per-AC result

| AC | Result | Surface | Evidence |
|---|---|---|---|
| 1 token mapping | **FAIL** | 5556 Gallery | fill/size/corner/glyph correct; **active label 1.23:1** |
| 2 active tallest+most saturated, every index | PASS | 5556 Playground | 72dp mint vs 44dp glass, all 4 positions |
| 3 <2 modules renders nothing | PASS | 5556 Playground | count 0/1 = nothing, 2 = renders |
| 4 scroll @1.3x EN + AR | PASS | 5556 + 5554 | band 122→127dp, gaps 8dp, no overlap |
| 5 pinned + floating host | PASS | 5554 harness | pinned holds, floating re-enters |
| 6 RTL order reverses, glyphs unmirrored | PASS | 5556 + 5554 | index 0 rightmost |
| 7 new dot, active + inactive | PASS | 5556 | 8dp dot; 74dp cluster when active |
| 8 onSelected returns tile id | PASS | 5556 Playground | 4 taps, 4 distinct frames |
| isLoading / isVisible / isDisabled | PASS | 5556 Playground | footprint 122dp identical; nothing painted; taps blocked |

Logs clean on both devices (no exception / RenderFlex overflow / `[ERR]` / `[FAIL]`).

## Tree moved mid-run
A concurrent session began editing the component at 23:00:26, splitting `_onMint`
into `_activeGlyphOnMintDisc` / `_activeLabelOnNavyField` — i.e. fixing exactly the
defect measured here (its own comment cites the same **1.23:1**). That edit is
**incomplete**: `flutter analyze` reports 4 `undefined_getter` errors, so the package
does not currently compile and the automated backstop could not be run.
Re-QA is required against the final revision.
