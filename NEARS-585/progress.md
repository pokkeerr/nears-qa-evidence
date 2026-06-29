# NEARS-585 QA progress
Device: emulator-5556 | Branch feat/NEARS-585-recommended-rail-reskin @ 9163a3f1
Backstop: pinned test 3/3 GREEN (item_card_in_store_test.dart)

## Live (Spice Route Kitchen, store 49, food, zone2)
- AC1 PASS: rail cards have NO store/brand uppercase line (ac1-store-screen-top.png)
- AC2/AC6 PASS: rail image ~60% / detail ~40%; matches grid card composition
- AC3 PASS both paths: Chef Salad rc=26 -> star "4.9 (26)"; Pepperoni Pizza rc=0 -> soft mint NEW pill (ac3-new-pill-and-rating-rail.png)
- AC4 PASS: main grid ItemWidget renders clean, no layout shift; New-pill is pre-existing ItemWidget behavior, untouched by commit (ac4-main-grid-itemwidget.png)
- logs: clean (no [FAIL]/[ERR]/overflow) through store browse

## AC5 (regression) + states
- AC5 PASS: Most Popular Items rail ItemCard shows UPPERCASE brand line (NOODLE BAR/GOLDEN WOK), ~5:5 flex, star+rating, NO New pill (ac5-most-popular-brandline.png). Buy It Again uses ItemCard too, renders clean.
- STATE +add-to-cart: tapped Pepperoni Pizza (New-pill rail card) -> detail sheet -> Add To Cart -> cart=1, logs clean. Rail card fully interactive.
- STATE empty/loading: rail loaded without crash; logs 0 FAIL/ERR throughout.
