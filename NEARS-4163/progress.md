# NEARS-4163 QA progress (web, Playwright; tip :8163 bfdd86c24 vs base :8164 21af7dcc8; clone DB multi_food_db_qa4163)
- Rendered index on base = 2 (owl current()==2, startPosition '2'); cards [Commission, pkg2, pkg1]; 3 cards.
- AC1 FAIL: at 1028 on S1/S2/S3 tip == base: visible cards [1,2], Commission 0%; owl-nav/owl-dots carry `.disabled` (display:none) because Owl 2.2.1 Navigation.draw hides both when items().length(3) <= settings.items(3) (owl.min.js:870). No visible control.
- AC2 FAIL at 1028 (no control; Shift button x=-94). Reachable at 768 (2 prev clicks; Shift confirm dialog opens, cancelled; Switch NOT executed on purpose, clone kept for re-QA).
- AC3 PARTIAL: 375/576/768 pass (all 3 cards reachable by arrows+dots); 992/1028/1199/1200/1440 fail (no controls, Commission 0%/42%).
- AC4 FAIL: RTL tip with current plan = last card: all cards 0% visible (Owl 2.2.1 coordinates() center+rtl reads _coordinates[pos+1]); base RTL showed current card 100%.
- AC5: S2/S3 identical to S1.
- Backstop phpunit Nears4163PlanSliderTwinsTest: OK (7 tests, 116 assertions).
- Session note: lang/ar is session-scoped server side; LTR sessions reset to en, RTL runs use separate logins.
