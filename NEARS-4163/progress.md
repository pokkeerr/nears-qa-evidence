# NEARS-4163 QA progress (web, Playwright; tip :8163 bfdd86c24 vs base :8164 21af7dcc8; clone DB multi_food_db_qa4163)
- Rendered index on base = 2 (owl current()==2, startPosition '2'); cards [Commission, pkg2, pkg1]; 3 cards.
- AC1 FAIL: at 1028 on S1/S2/S3 tip == base: visible cards [1,2], Commission 0%; owl-nav/owl-dots carry `.disabled` (display:none) because Owl 2.2.1 Navigation.draw hides both when items().length(3) <= settings.items(3) (owl.min.js:870). No visible control.
- AC2 FAIL at 1028 (no control; Shift button x=-94). Reachable at 768 (2 prev clicks; Shift confirm dialog opens, cancelled; Switch NOT executed on purpose, clone kept for re-QA).
- AC3 PARTIAL: 375/576/768 pass (all 3 cards reachable by arrows+dots); 992/1028/1199/1200/1440 fail (no controls, Commission 0%/42%).
- AC4 FAIL: RTL tip with current plan = last card: all cards 0% visible (Owl 2.2.1 coordinates() center+rtl reads _coordinates[pos+1]); base RTL showed current card 100%.
- AC5: S2/S3 identical to S1.
- Backstop phpunit Nears4163PlanSliderTwinsTest: OK (7 tests, 116 assertions).
- Session note: lang/ar is session-scoped server side; LTR sessions reset to en, RTL runs use separate logins.

## RE-QA cycle 1 (tip 380b31e63 on :8163 vs base 21af7dcc8 on :8164; clone multi_food_db_qa4163; files prefixed r2-)
- Pre-flight: freshness check PASS on 8163/8164; ps eww PWD+DB_DATABASE confirm tip/base worktrees and the clone DB. Lessons selector (qa) = 17 active.
- AC1 PASS: S1/S2/S3 1028 LTR real 3 cards: base [0,100,100] (Commission 0%, btn not reachable) vs tip [100,100,100]; nav/dots disabled (expected). 4-card boundary at 1028 tip: centred, prev/next+dots present, all 4 reachable (clicks logged in r2-ac1-measure.json).
- AC2 behaviour at 1028/768/4-5 cards: Commission Shift reachable with visible controls (0 clicks at 3 cards 1028, 2 at 768, 2-3 at 4-5 cards); arrows never cover a Shift button (btn depth 0 all states). Final Switch: see r2-ac2-switch.json (run last).
- AC3 LTR tip matrix 80 cells (real3 x8 widths + 3/4/5 cards x 8 widths x first/mid/last): all cards reachable by visible controls or visible at load, all action buttons reachable, 0 console errors; dots==cards and active dot==current when dots visible; first/last arrow hides, dots stay. Resize: 3 cards == fresh; 4 cards: layout/controls == fresh but position resets to card 0 when the centre flag flips (start index != 0) - base keeps position.
- AC4(a) RTL>=992 3 and 5 cards all starts: PASS (all reachable, no blank, arrows mirrored, dots dx 0, Commission rightmost). RTL dots are Owl pages (2 dots for 5 cards).
- AC4(b) better-than-base literal table: 12/24 rows PASS, 12 FAIL (an 'other card' regresses vs base while current card improves) - see r2-ac4b-better-than-base-table.json. AC4(c): last-card Shift button unreachable at 375 and 768 (3 and 5 cards, synthetic all-Shift cells; real fixture last card is Renew) -> residual HIGH.
- AC5 PASS: S2/S3 identical to S1 at 1028 LTR+RTL (+4/5 card synthetic).
- Overlap -16px: max 14px visible-content penetration (576/768 real; 5-card >=992 next arrow; 1200/1440 both); never over a Shift button; 375 no overlap/clip.
- Controls: registration fragment tip==base; package-index slider tip==base; addon-activation 0 .dots-style2 elements on both (nothing to compare).
- Backstop phpunit Nears4163PlanSliderTwinsTest OK (9 tests, 203 assertions). laravel.log: no new lines in my run (only the 2 round-1 anonymous-probe [FAIL] lines of 13:51:20); serve log: 0 ERROR/Exception/Fatal.

## re-QA cycle 2 (final build VE768, tip 8caa96595) - checkpoints
- PREFLIGHT: tip :8163 pid 94849 PWD=.../nears-NEARS-4163-plan-modal-carousel-nav/Admin DB_DATABASE=multi_food_db_qa4163; base :8164 pid 94859 PWD=.../nears-NEARS-4163-base/Admin DB_DATABASE=multi_food_db_qa4163; backend-freshness-check PASS on both. Clone store 4 = subscription pkg 1 (SELECT); shared multi_food_db store 4 = commission (SELECT).
- C5 twin test: OK (10 tests, 239 assertions).
- NOTE: every tip vendor-panel page logs a browser console line "Failed to load resource: 403" for /vendor-panel/message/list = NEARS-4171 marked denial (X-Panel-Refusal: denied, {"code":"subscription"}) inherited via the rebase; base (pre-4171) answers 302. Not a 4163 AC action. r4-chat403-probe.json.
- C1 LTR: 80 tip cells + 8 base cells re-run (r4-ac3-tip-ltr-matrix.json) vs r2: 67 tip/base cells identical field-by-field; 13 cells differ at ONE sample each (the dot0 click, animation in flight at 550 ms). Old-code replica (route rewrite to the pre-VE768 init) vs new code on those 13: identical when settled (13/13, all fields); at 550 ms the old code differs from ITSELF between reps (4/13) and from r2 (11/13) = instrument sampling, not code. r4-ac3-ltr-diff.json, r4-ac3-ltr-AB-oldcode-vs-newcode.json.
- C2: RTL 375/576/768/800/900 x 8 cells = 40 rows, (i)-(iv) 40/40 PASS, strict (load excluded) 40/40. Wide >=992: 45/45. C3: 768/800/900 7/7 each, 576 7/7, 375 0/7 (last card 22-23%). C6 arrow steps: 216 = 184 expected / 16 opposite / 16 no-op (all at 375/576), 768/800/900: 75/75 expected.
- C5 twin test 10/239 OK. C4: Switch executed LAST: toast "Successfully Switched To Commission!" captured by init-script observer; reload shows Commission Base Plan; SELECT store 4 subscription -> commission (store_subscriptions.id 2 status 1 -> 0).
- AC1/AC5/AC2a/controls/resize re-proofs done (r4-ac1-ac5-measure.json, r4-ac2-measure.json, r4-ctrl*.json, r4-resize.json).
