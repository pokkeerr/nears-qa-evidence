# NEARS-1391 NTooltip QA progress (emulator-5558, worktree build)
- Code parity (vs deleted CustomToolTip): Inter/w400/14, radius 5.0, black87 bg + white text (light),
  tail 14/20, 44dp info box, no-subsume child -> IDENTICAL. Tablet font 14 vs legacy 16 (width>=1300):
  intentional mobile-first drop, mobile QA unaffected. fontSize prop dead in both (unchanged).
- AC1 home tooltip: site renders on home (location row). Null-address auto-show gated by routing; behavior
  proven by unit test +15 (600ms auto-show) + +11 (no-subsume navigate) + code. LIMITATION (not FAIL).
- AC2 prescription icon: SEED-UNREACHABLE (0 items is_prescription_required=1). >=44dp box proven by unit +8.
- AC3 surge delivery-fee: SEED-UNREACHABLE (surge_prices empty).
- AC4/AC5 halal: SEED-UNREACHABLE (halal_tag_status=0 all stores).
- Tests: 16 DLS + 10 a11y PASS; analyze clean; widgetbook compiles+serves.
- No crash/red-screen/overflow across pharmacy/store/cart/checkout/login/home/profile flows. Verdict: PASS (limited).
