# NEARS-1659 QA progress (fix cycle 2)
Device emulator-5556 | APK md5 474def4c660688076a2fabfdb5e2b650 | worktree af4a5d03

- AC8 RTL: `/5` glyph order CORRECT (renders "3.4/5", not "5/"). Bars mirror (summary right, bars left).
  Percent labels left-aligned = RTL `end`. evidence ac8-reviews-rtl-arabic.png / ac8-rtl-panel-zoom.png
- AC2: navy bar #000080 EXACT, mint bar #00FF99 EXACT, /5 grey (154,154,166), Reviews hdr mint.
  BUT mobile average numeral = #34343F (NearsTokens.textBody), NOT navy. Unchanged at base
  (legacy publicSansBold also had no color). -> mis-specified AC.
- AC6 pull-to-refresh: fresh GET /api/v1/stores/reviews 200, list re-rendered. PASS
- AC3 skeleton: two-column (summary L, divider, 5 bars R), fills from top, no spinner. PASS
- AC9 loaded LTR panel+list. PASS
- AC4 error: NearsErrorRetry "Something went wrong/Please try again/Retry" + PAIRED [FAIL]
  endpoint=/api/v1/stores/reviews. Retry recovered -> 200. PASS
- FINDING: "5 Reviews" pill WRAPS to 2 lines in English mobile; sibling pills differ in height.
  Pills 65.7dp each, inner 55.7dp; "5 Ratings" ink 50.0dp 1 line; Reviews text 21.7dp tall = 2 lines.
