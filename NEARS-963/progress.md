# NEARS-963 re-QA cycle 1 — progress checkpoint (a11y tail, UserApp)

Build: worktree fix/NEARS-963-a11y-tail (uncommitted MergeSemantics fix), fresh `flutter run`.
Device: emulator-5560 (AVD nears_qa_wave56). Verdict: **FAIL** (AC3 + AC4 not announced on-device).
Method: uiautomator dump = the Android AccessibilityNodeInfo tree TalkBack reads (confirmed
identical content-desc with TalkBack ON and OFF; home-screen labels prove the read is valid).

Build-freshness PROOF: AC5 toggle renders NEW labels "Grid view"/"List view" (added by this exact
uncommitted fix) live on-device -> the running build contains the fix. So AC3/AC4 empty labels are
the fix genuinely failing, not a stale build.

| AC | status | evidence |
|----|--------|----------|
| AC3 map zoom | FAIL | zoom +/- Buttons content-desc='' (TalkBack on & off); bug-ac3-map-zoom-still-empty-cycle1.log |
| AC4 search stars | FAIL | 5 stars content-desc='' [53..473,2007]; bug-ac4-rating-stars-still-empty-cycle1.log |
| AC4 store stars | FAIL | 5 stars content-desc='' [53..473,2001]; ac4-store-filter-stars-empty.png |
| AC5 grid/list toggle | PASS | "Grid view"(sel=true)/"List view"; tap flips sel; ac5-store-toggle-list-active.png |
| AC9 verified badge | PASS | content-desc="Verified" ImageView; ac9-verified-badge-pass.png |
| AC1 halal tooltip | not-live-triggerable | no halal seed item (item detail has no halal badge); same CustomToolTip MergeSemantics pattern -> structurally at-risk |
| AC2 love swiper | not-live-triggerable | "Items you love" section not rendered on home (seed/config gap); same MergeSemantics pattern -> structurally at-risk |
| AC6 no visual change | PASS | zoom/star/toggle bounds byte-identical to cycle 0; MergeSemantics adds no box |
| backstop test | green (non-authoritative) | a11y_tail_of_tail_963_test.dart 8/8 pass incl. +5 star/+6 zoom — flutter_test compiler merges regardless; NOT the gate |

Root cause lead: failing sites (AC3 zoom, AC4 stars) = MergeSemantics > Semantics(label,button) >
InkWell > BARE Icon -> label AND button role dropped on-device. Passing sites (AC5/AC9/home) = plain
Semantics with a wrapped child. MergeSemantics did not fix it; recommend the AC5 pattern.

Logs: no [FAIL]/[ERR] during any AC (clean); all NET 200. Not a crash — a silent a11y gap.
