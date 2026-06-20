# NEARS-499 QA progress (live checkpoints)
Build: worktree feat/NEARS-499-store-list-sections (uncommitted on base 67b57c72) · device emulator-5554 · backend 127.0.0.1:8000
Gate fact (live get-stores total_size): z1 grocery/food/pharmacy=6,6,6 (all HIDE); z2 grocery=13(SHOW), food=5, pharmacy=5 (HIDE).

## AC1 food (z1): PASS — no "Best Stores Nearby" header anywhere; shot ac1-food-z1-top.png
## AC2 food (z1): PASS — Top offers HIDDEN (total_size=6<=10); main Stores list "Popular Restaurants / 6 restaurants near you" SHOWN w/ cards; shot ac2-food-z1-stores-list.png
## AC5 food (z1): PASS — body flows banner→categories→rails→Popular→Restaurants, no blank gap; ui_errors clean
## AC1 grocery (z1): PASS — no Best Stores Nearby; shot ac1-grocery-z1-top.png
## AC2 grocery (z1): PASS — Top offers HIDDEN; main "Stores / 6 stores near you" list SHOWN w/ filter chips; shot ac2-grocery-z1-stores-list.png; ui_errors clean
## AC1 pharmacy (z1): PASS — no Best Stores Nearby; shot ac1-pharmacy-z1-top.png
## AC2 pharmacy (z1): PASS — Top offers HIDDEN; main "Stores / 6 stores near you" SHOWN; shot ac2-pharmacy-z1-stores-list.png; ui_errors clean
## AC1 shop: no shop-type module seeded in z1/z2; code-confirmed shop_home_screen.dart has 0 BestStoreNearby refs (grep) -> PASS by code inspection
## AC3 grocery (z2): PASS — total_size=13>10 -> "Top offers near me" SHOWN + main "Stores / 18 stores near you" SHOWN; cards show distance "0.00 km from you" (no user-loc origin -> all 0, stable, no crash = NO-LOCATION AC PASS); shots ac3-grocery-z2-top-offers-rail3.png + ac3-grocery-z2-top-offers-final.png; ui_errors clean
## NO-LOCATION distance AC: PASS — Top offers renders gracefully, all 0.00 km, stable order, no crash
## AC1/AC2 food (z2): PASS — total_size=5<=10 -> Top offers HIDDEN, no Best Stores, "Popular Restaurants / 5 restaurants near you" SHOWN; shot ac1-food-z2-hidden-topoffers.png
## REGRESSION zone-flip (z2 grocery SHOWN -> z1 grocery): PASS — Top offers count flipped to 0, no stale state; shot regr-zoneflip-grocery-z1-hidden.png; errors clean
## REGRESSION per-module gate: PASS — same zone 2: grocery(13)=SHOWN, food(5)=HIDDEN -> gate is per-module not per-zone (correct)
## REGRESSION pharmacy (z2): PASS — total_size=5 -> Top offers HIDDEN, Stores "5 stores near you" SHOWN; shot regr-pharmacy-z2-hidden.png
## REGRESSION dark mode (grocery z2): PASS — Top offers rail + Stores render clean, no overflow/whitespace; shots dark-grocery-z2-topoffers.png + dark-grocery-z2-topoffers-rail.png
## REGRESSION RTL/Arabic (grocery z2): PASS — mirrored layout, "متاجر"(Stores) + Top offers render clean, no overflow/whitespace artifacts; shot rtl-grocery-z2-topoffers.png; errors clean
## REGRESSION RTL low-zone (grocery z1): PASS — Top offers HIDDEN, "متاجر / 6 المتاجر القريبة منك" SHOWN, NO whitespace gap; shot rtl-grocery-z1-hidden.png
## AUTOMATED BACKSTOP: gate test +2 pass; store_controller +33 pass; FULL UserApp suite +1245 All tests passed
## VERDICT: PASS
