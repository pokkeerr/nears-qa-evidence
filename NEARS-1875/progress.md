# NEARS-1875 phase [8] QA — progress checkpoint
Device emulator-5554 (1344x2992 @ 480), light mode, build afae2239, APK md5 3335639585e5d0094c502389bf621fb7.

- [AC2 / QA-3] LTR close top-RIGHT `[1200,219][1344,363]`, top 73 dp (NEARS-1874 seat preserved) — PASS. logs clean.
- [AC1 / QA-1] RTL close top-LEFT `[0,219][144,363]`; close-band MSE plain 257.170 vs mirrored 0.001 (463,880x) — PASS. logs clean.
- [AC1 / QA-2] RTL close unclipped, left inset 0, glyph 51 px in from x=0 — PASS.
- [AC1 arrows clause] prev/next NOT TESTED — unreachable by construction (single-element file array; no arrow nodes render).
- Regression (lightbox route): RTL Close tap dismisses; hardware BACK returns to chat; chat + conversation list intact; English restored.
- Automated: flutter test (3.41.9) test/features/chat/ = 138/138 pass; new AC7 test passes by name; count delta 31 -> 32.
