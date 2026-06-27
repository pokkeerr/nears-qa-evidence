# NEARS-474 — QA evidence (fix-cycle 0, first full pass)

- **Device:** emulator-5556 (Android 17 / API 37) · **Build:** worktree `feat/NEARS-474-module-grid` @ `bfedc9ae` · backend local `multi_food_db` · **light mode** (dark deferred).
- **Verdict:** PASS

| AC | Result | Evidence | Logs |
|----|--------|----------|------|
| AC1 2-col grid (not vertical list) | PASS | `ac1-grid-2col-en.png`; widget tree: ModuleGrid→GridView(crossAxisCount 2)→3×_SectorGridTile | clean |
| AC2 glyph render (+ no photo/broken/?) | PASS (live glyph) | `ac1-grid-2col-en.png`; tree: each tile NearsIcon→Icon, no CustomImage | clean |
| AC2 image-fallback / empty-disc priorities | PASS (automated) | grid test: glyph→image(CustomImage)→bare disc; live-filtered (Parcel=parcel-type, module6=zero-store) | clean |
| AC3 RTL/Arabic | PASS | `ac3-grid-rtl-arabic.png`: fills R→L, internals centered, glyphs not mirrored | clean |
| AC4 dark mode | N/A (deferred, light-first) | — | — |
| AC5 shimmer grid-shaped | PASS (automated+code) | grid test: 2-col skeleton, no ListView, 4 tiles; live window sub-second on localhost | clean |
| AC5 empty/no-service NearsEmptyState | PASS (code unchanged) | diff: NearsEmptyState branch untouched by ticket; no zero-module seed zone to trigger live | n/a |
| AC6 tap-nav (each tile enters module) | PASS | live: tapped Grocery/Food/Pharmacy → each module home | clean |
| AC6 single-module auto-select (no grid) | PASS | `ac6-single-module-autoselect-nogrid.png`; log: sectors_shown{count:1,zone:3}→store_auto_opened{store:59,module:4} | clean |
| NEW narrow @~320dp no-overflow | PASS | `acNEW-narrow-320dp-no-overflow.png` (density 672, 2-line names fit, 0 overflow) + grid test @320dp 10/10 + 0 overflow whole session | clean |

**Automated:** `flutter analyze` (changed files) clean; grid test 10/10; home+splash suites 135/135.
**Regression sweep (home blast radius):** featured banner self-hides cleanly (NEARS-473), grid intact, Recommended-For-You / popular stores render, module nav works. 0 `[FAIL]`/`[ERR]`, 0 RenderFlex overflow across session.
**Followup (pre-existing, non-blocking):** `[WARN] payment-failed details parse failed: _TypeError` on `/api/v1/customer/order/payment-failed` — unrelated to this ticket, fires on first boot in every zone.
