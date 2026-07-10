# NEARS-1039 QA progress — remove module-home Top Offers rail

Build: feat/NEARS-1039-top-offers-rail @4211c339, base feat/human-review @b113c55b
Device: emulator-5554 (Android), UserApp from worktree, backend :8000 (10.0.2.2:8000)

| AC | Result | Evidence |
|----|--------|----------|
| 1 Rail gone (grocery/food/pharmacy module homes, zone 2) | PASS | live: no "Top Offers Near Me" section on any; shop = code-identical single-line removal, no seeded shop module |
| 2 Reflow clean, no gap | PASS | visual: banner→categories→stores close up naturally; removed widget was self-hiding (SizedBox.shrink), no external spacer |
| 3 No dead top-offer fetch | PASS | [NET] log on load + pull-to-refresh (zone2 + single-store): stores/popular+latest called, NO top-offer-near-me; constant removed |
| 4 Other see-all intact | PASS | live: featured see-all renders (get-stores/all, 200); popular/recommended/nearby modes code-preserved; sort-chip absence expected |
| 5 Single-store hero resolves | PASS | live zone-3 qa.singlestore: NEARS-257 Fixture Store hero rendered, gap-free |
| 6 RTL/Arabic module home | PASS | live: Arabic grocery module home mirrors cleanly, no stray spacer, no rail |
| 7 Regression / errors | PASS | ui_errors clean; no RenderFlex/overflow; only unrelated get-zone-id 404 during out-of-zone location switch (properly [FAIL]-logged) |

Backstop: flutter test — running.
