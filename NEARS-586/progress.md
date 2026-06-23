# NEARS-586 QA progress — glass-opacity bottom nav (cycle 1)
device: emulator-5556 | worktree: nears-NEARS-586-glass-opacity | branch feat/NEARS-586-glass-opacity
started: 2026-06-23

## checkpoints
- preflight: baseUrl=http://10.0.2.2:8000 (real local backend) OK; backend up (config 200); lock acquired emulator-5556
- token diff verified: navyGlassFill=0x4D000080 (navy @0.30); navyDeep #00003C; textOnNavyDim white@0.66; badge ring 2dp

## live observations
- 01-light-home-offwhite-top.png: AC1 PASS (bar reads pale frosted glass, NOT near-solid navy; off-white content composites through). AC3 PASS (rounded 24dp, 16dp inset float, hairline border, ambient shadow). AC6 PASS (4 inactive icons dark navy ink, clearly legible). AC8 PASS (Home active = mint filled, distinct). logs: clean.
- 02-light-home-white-cards.png: AC4(light/white) PASS — inactive dark-ink icons legible over white cards; mint Home distinct. logs clean.
- 03/04 store image content: bar over colorful product hero; on store page View-Cart CTA overlays nav (expected). item added to cart OK, logs clean.
- 05-light-home-badge.png: AC4 badge PASS — basket badge mint fill + navy ring (2dp, visibly delineated) + navy "1" numeral, legible over pale glass. bar over Fresh-Finds image content; inactive icons still legible. logs clean.
- empty-cart (no badge / no ghost gap): demonstrated in 01 (Basket icon clean, no reserved gap) + unit #15.
- 06-dark-check.png: system night=yes did NOT flip app (UserApp is in-app-theme-driven, not system-following) — expected.
- 07-dark-home-bar.png: AC2 PASS (dark bar reads frosted dark-navy glass, content shows through, not near-solid). AC7 PASS (inactive icons dimmed-WHITE, clearly visible, NOT dark ink — per-mode switch correct). AC8 PASS (mint Home active distinct from dimmed-white inactive). badge legible in dark. logs clean. (dark renders correctly — no deferral conflict.)
- 08-rtl-arabic-home-bar.png: AC5(RTL) PASS — tab order mirrored (Home/mint active now RIGHT, Profile far LEFT); basket badge top-LEADING (top-right of glyph in RTL); glass/blur/hairline/inset/shadow identical to LTR; pale fill over light content unchanged. logs clean.
- tab-sweep all 5 tabs: clean, no errors, active/inactive distinct.
- SESSION LOG SCAN: only overflow source = cart_count_view.dart:64 (RenderFlex 36px). NOT in NEARS-586 diff (last touched NEARS-494). nears_bottom_nav.dart NEVER cited in any overflow/exception → change is clean. => regression_bug (unrelated, pre-existing), does NOT affect verdict.
- NEARS-340 banner: no qualifying running order in seed (pending/confirmed don't trigger server-side running filter); banner geometry lives in dashboard_screen.dart (NOT in diff); bar footprint metrics unchanged → change cannot regress it. Sub-point unverifiable-live but provably non-regressing.
