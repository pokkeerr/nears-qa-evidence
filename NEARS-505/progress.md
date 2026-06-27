# NEARS-505 QA progress (emulator-5554, light mode, fix-cycle 1)

- Change present: search_screen.dart 2 SizedBox tokens (20->15, 10->5). Confirmed in diff + widget tree.
- AC1 compact chips: FALSE — chips full-width one-per-row (pre-existing NearsFilterChip Container(alignment) in Wrap). evidence: 01 / bug-fullwidth-chips.png
- AC2 tight Suggestions gap: FALSE — visible gap ~64 logical px vs ~18 for Popular Categories; token=5px correct but dominated by pre-existing GridView layout. evidence: 01 / bug-suggestions-gap.png
- AC3 both visible on idle: TRUE — chips + Suggestions + Popular Categories render. evidence: 01
- 5px judgment: NOT cramped (refutes reviewer fear); do not bump 5->10.
- Regression: chip-tap re-runs search OK; Clear All clears history OK; grid layout unchanged; RTL idle OK (02). Logs clean (no [FAIL]/[ERR]).
- Automated: flutter test test/features/search -> 49 passed.
- Verdict: FAIL (AC1+AC2 unmet live; causes pre-existing, outside the 2-line diff -> needs scope decision).
- Gallery: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-505 ; Jira comment id 11013 posted.

---
## DELTA RE-QA (fix-cycle 2) — 2026-06-28, emulator-5554
- AC#1 compact wrapping chips: PASS (IntrinsicWidth effective; multi-per-row wrap; long term no overflow). recheck-01-compact-chips.png
- AC#2 tight Suggestions gap: FAIL — visible gap ~67 logical px vs Popular Categories ~18 logical; ~53-logical dead band persists above grid row 1. recheck-02-suggestions-gap-STILL.png / bug-suggestions-gap-persists.png
- AC#3 both sections visible: PASS (reused + reconfirmed; all 3 sections render when logged in).
- Regression: chip tap re-search PASS; suggestion tap opens item PASS; Clear All PASS; RTL chips+card mirror PASS (AC#2 gap also visible in RTL).
- Logs clean (no [FAIL]/[ERR]). Tests 53/53.
- VERDICT: FAIL (AC#2). 2nd fix attempt on root cause unsuccessful -> approaching escalation cap.

---
## FINAL DELTA RE-QA (fix-cycle 3) — 2026-06-28, emulator-5554 (real status-bar inset, 448x997 logical, DPR 3.0)
Fix under test: padding:EdgeInsets.zero on suggestions GridView.builder (search_screen.dart:750) — removes inherited MediaQuery top safe-area inset (~53px).
- AC#1 compact wrapping chips: PASS (reuse + reconfirmed) — IntrinsicWidth chips Water/Cheese/Milk compact pills, multi-per-row. 01-ac2-suggestions-tight-gap.png
- AC#2 tight Suggestions gap: PASS (re-verified on real device) — measured Suggestions title->first-card = 5.0 logical px (was ~67); Popular Categories = 10.0px. Tight + comparable; ~53px dead band eliminated. Card height EXACTLY 64.0px (54px image, name not clipped). RTL: 5.0px gap, right-aligned, no overflow (02-ac2-rtl-idle-holds.png).
- AC#3 both visible idle: PASS (reuse) — Suggestions + Popular Categories render on idle.
- Regression (bounded): chip tap re-runs search (10 results "Water"); suggestion tap opens item (Orange Juice 1L detail); Clear All clears chips; RTL idle holds. All clean.
- Logs: /api/v1/customer/suggested-items [200], /api/v1/categories/popular [200]; no [FAIL]/[ERR]; no runtime errors; no overflow. (1 pre-existing unrelated [WARN] payment-failed parse on home flow.)
- Automated: flutter test test/features/search/ -> 55/55 pass.
- VERDICT: PASS. Final cycle clears the ticket.
