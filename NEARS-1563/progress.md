# NEARS-1563 — live QA checkpoint (fix cycle 1)

Surface: Widgetbook web storybook (`widgetbook/build/web`, `--debug`, Flutter
3.41.9), served from the run worktree on `http://127.0.0.1:8899`. On-device is
blocked by NEARS-1534. Light mode only (dark deferred).

Bundle provenance, checked before any conclusion was drawn:
- `main.dart.js` mtime `2026-08-04 02:32:01`, 15050106 bytes; component
  `n_module_row.dart` mtime `02:28:41` — bundle is newer, so it contains the fix.
- HTTP server cwd verified via `lsof` = `<worktree>/widgetbook/build/web`.
- Served bytes == disk bytes: sha256
  `7962be8ff57dacb2412435f0824a7ad8d127fa6610126fd58010ab45c15e12a3` on both.

Driving: label-driven only — nav leaves and tiles resolved from the Flutter-web
semantics tree and clicked at their live rects. No URL deep-links (`?path=` is
accepted into `href` but never routed), no hardcoded coordinates.

Measurement: numeric, not visual. An ancestor scroll shifts every laid-out node
by the same amount, so the ancestor's offset is read as the screen-y of a case's
semantics rect, and the row's offset as the screen-x of its tiles. Clipped nodes
report clipped rects, so only unclipped nodes are used for deltas.

| # | AC | Result | Evidence |
|---|----|--------|----------|
| 1 | Mount-time, no interaction — the page must not move on its own | PASS | first paint offset 0.0 with tiles 220 px below the fold; 62 scroll steps across 3 geometries, every step's shift == wheel delta exactly |
| 2 | Selection change — the row scrolls, the page must not | PASS (row half live; page half see note) | tap → row scrolls 18.0 px, everything outside the row unmoved |
| 3 | Row reveal works in BOTH directions, minimum scroll | PASS | trailing 18.0 px → parks on the edge (centre offset 160.8, a re-centre would be ~0); leading 2.0 px = exactly its overhang |
| 4 | An already-visible tile moves nothing | PASS | tap Parcel at offset 18 → dx +0.0 on all 7 tiles |
| 5 | RTL / Arabic — same, both directions | PASS | +18.0 then −2.0, each exactly the tile's overhang |
| 6 | loading / error / resolved toggles — no exception | PASS | 7 transitions + isVisible control, 0 pageerrors, 0 console errors |

Automated backstop (own run, worktree, Flutter 3.41.9): `flutter analyze` — no
issues; `flutter test` — **980 passed, 0 failed**.
