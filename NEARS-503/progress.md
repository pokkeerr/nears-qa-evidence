# NEARS-503 QA progress (live, append-only)
Device: emulator-5554 (Android 17 / API 37), worktree feat/NEARS-503-search-common-appbar
Backend: http://127.0.0.1:8000 (primary tree), zone 2 Abu Dhabi

## Live results (append-only)
- AC1 navy header (idle) consistent w/ Home: PASS — 01-idle-filter-icon.png
- AC2 trailing icon = sliders (idle): PASS — 01-idle-filter-icon.png (mint tune_rounded, not basket)
- AC3 filter icon idle opens sheet: PASS — 02-idle-filter-sheet-open.png
- AC4 no basket on appbar/field: PASS — 01 (only bottom-nav cart)
- CR-1 Apply Filters in idle (no data): PASS no crash, logs clean (no Null check operator / [FAIL])
- CR-1 Reset in idle: PASS no crash, errors clean
- RESULTS state filter icon present (AC2 results): PASS — 03-results-state.png
- RESULTS Apply Discounted filter (non-null path): PASS filtered correctly — 04
- RESULTS Reset->Apply: PASS full list restored, errors clean
- IDLE+typing suggestions overlay, filter button visible+tappable: PASS — 05
- RTL/Arabic: filter button on logical trailing end (visual left), no clipping: PASS — 06,07
- RTL idle Apply (CR-1): PASS no crash
- logcat scan: no Null check operator / [FAIL] / FlutterError / RenderFlex overflow
- Language restored to English; device clean
