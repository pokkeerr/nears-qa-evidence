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
