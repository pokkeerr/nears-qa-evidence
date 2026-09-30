# NEARS-3925 round-2 QA (fix cycle 3, rule W2) - build fix/NEARS-3925-flash-discount-rounding @ a04c58436

Backend: /Users/Apple/Projects/nears-NEARS-3925-flash-discount-rounding @ a04c58436 (own `artisan serve --no-reload` :8130, dead HTTPS_PROXY), DB copy multi_food_db_qa_bug3925 (proved via GET /api/v1/config admin_free_delivery.status=false; shared DB has status 1). Flag cross_module_basket=0 unless stated. Order-wise VAT 5%, precision 2, store 39 free delivery (0).

Measured = persisted orders.order_amount / real endpoint responses. Computed = exact-decimal `app` = round((P - round(flashRaw+nonFlashRaw)) x 1.05 + delivery), `old` = round((P - round(flashRaw) - nonFlashRaw) x 1.05) (previous fix build 1c04b0f semantics), `base` = all raw. old/base columns are COMPUTED, not measured on those builds.

## A1. All 36 mixed baskets (390 x{1,2,3} + 389/392/394/395 x{1,2,3}), placed on the fix build: charged == app 36/36; AC2 identities 36/36; get-Tax preview total == charged 36/36

|basket|P|flashRaw|nonFlashRaw|APP|old rule|base|CHARGED|preview|store_disc|flash adm+ven|AC2|
|--|--|--|--|--|--|--|--|--|--|--|--|
|390x1 + 389x1|57.56|4.8564|2.4464|52.77|52.77|52.77|**52.77**|52.77|2.45|4.85|ok|
|390x1 + 389x2|88.14|4.8564|4.8928|82.31|82.31|82.31|**82.31**|82.31|4.89|4.86|ok|
|390x1 + 389x3|118.72|4.8564|7.3392|111.85|111.85|111.85|**111.85**|111.85|7.34|4.86|ok|
|390x2 + 389x1|84.54|9.7128|2.4464|76.00|76.00|76.00|**76.00**|76.00|2.45|9.71|ok|
|390x2 + 389x2|115.12|9.7128|4.8928|105.54|105.54|105.54|**105.54**|105.54|4.89|9.72|ok|
|390x2 + 389x3|145.70|9.7128|7.3392|135.08|135.08|135.08|**135.08**|135.08|7.34|9.71|ok|
|390x3 + 389x1|111.52|14.5692|2.4464|99.23|99.23|99.23|**99.23**|99.23|2.45|14.57|ok|
|390x3 + 389x2|142.10|14.5692|4.8928|128.77|128.77|128.77|**128.77**|128.77|4.89|14.57|ok|
|390x3 + 389x3|172.68|14.5692|7.3392|158.31|158.31|158.31|**158.31**|158.31|7.34|14.57|ok|
|390x1 + 392x1|69.31|4.8564|3.8097|63.67|63.67|63.68|**63.67**|63.67|3.81|4.86|ok|
|390x1 + 392x2|111.64|4.8564|7.6194|104.12|104.12|104.12|**104.12**|104.12|7.62|4.86|ok|
|390x1 + 392x3|153.97|4.8564|11.4291|144.56|144.56|144.57|**144.56**|144.56|11.43|4.86|ok|
|390x2 + 392x1|96.29|9.7128|3.8097|86.91|86.91|86.91|**86.91**|86.91|3.81|9.71|ok|
|390x2 + 392x2|138.62|9.7128|7.6194|127.35|127.36|127.35|**127.35**|127.35|7.62|9.71|ok|
|390x2 + 392x3|180.95|9.7128|11.4291|167.80|167.80|167.80|**167.80**|167.80|11.43|9.71|ok|
|390x3 + 392x1|123.27|14.5692|3.8097|110.13|110.13|110.14|**110.13**|110.13|3.81|14.57|ok|
|390x3 + 392x2|165.60|14.5692|7.6194|150.58|150.58|150.58|**150.58**|150.58|7.62|14.57|ok|
|390x3 + 392x3|207.93|14.5692|11.4291|191.03|191.03|191.03|**191.03**|191.03|11.43|14.57|ok|
|390x1 + 394x1|49.20|4.8564|3.3330|43.06|43.06|43.06|**43.06**|43.06|3.33|4.86|ok|
|390x1 + 394x2|71.42|4.8564|6.6660|62.90|62.89|62.89|**62.90**|62.90|6.67|4.85|ok|
|390x1 + 394x3|93.64|4.8564|9.9990|82.72|82.72|82.72|**82.72**|82.72|10.00|4.86|ok|
|390x2 + 394x1|76.18|9.7128|3.3330|66.29|66.29|66.29|**66.29**|66.29|3.33|9.72|ok|
|390x2 + 394x2|98.40|9.7128|6.6660|86.12|86.13|86.12|**86.12**|86.12|6.67|9.71|ok|
|390x2 + 394x3|120.62|9.7128|9.9990|105.96|105.96|105.95|**105.96**|105.96|10.00|9.71|ok|
|390x3 + 394x1|103.16|14.5692|3.3330|89.52|89.52|89.52|**89.52**|89.52|3.33|14.57|ok|
|390x3 + 394x2|125.38|14.5692|6.6660|109.35|109.35|109.35|**109.35**|109.35|6.67|14.57|ok|
|390x3 + 394x3|147.60|14.5692|9.9990|129.18|129.18|129.18|**129.18**|129.18|10.00|14.57|ok|
|390x1 + 395x1|57.45|4.8564|5.4846|49.47|49.46|49.46|**49.47**|49.47|5.48|4.86|ok|
|390x1 + 395x2|87.92|4.8564|10.9692|75.69|75.70|75.70|**75.69**|75.69|10.97|4.86|ok|
|390x1 + 395x3|118.39|4.8564|16.4538|101.93|101.93|101.93|**101.93**|101.93|16.45|4.86|ok|
|390x2 + 395x1|84.43|9.7128|5.4846|72.69|72.70|72.69|**72.69**|72.69|5.48|9.72|ok|
|390x2 + 395x2|114.90|9.7128|10.9692|98.93|98.93|98.93|**98.93**|98.93|10.97|9.71|ok|
|390x2 + 395x3|145.37|9.7128|16.4538|125.16|125.17|125.16|**125.16**|125.16|16.45|9.72|ok|
|390x3 + 395x1|111.41|14.5692|5.4846|95.93|95.92|95.92|**95.93**|95.93|5.48|14.57|ok|
|390x3 + 395x2|141.88|14.5692|10.9692|122.16|122.16|122.16|**122.16**|122.16|10.97|14.57|ok|
|390x3 + 395x3|172.35|14.5692|16.4538|148.40|148.39|148.39|**148.40**|148.40|16.45|14.57|ok|

## A1b. The 13 baskets where app / old rule / base differ

|basket|P|app formula|old rule (1c04b0f)|base (all raw)|CHARGED (a04c584)|old rule vs app|
|--|--|--|--|--|--|--|
|390x1 + 392x1|69.31|63.67|63.67|63.68|**63.67**|old == app|
|390x1 + 392x3|153.97|144.56|144.56|144.57|**144.56**|old == app|
|390x2 + 392x2|138.62|127.35|127.36|127.35|**127.35**|old differed by 0.01|
|390x3 + 392x1|123.27|110.13|110.13|110.14|**110.13**|old == app|
|390x1 + 394x2|71.42|62.90|62.89|62.89|**62.90**|old differed by -0.01|
|390x2 + 394x2|98.40|86.12|86.13|86.12|**86.12**|old differed by 0.01|
|390x2 + 394x3|120.62|105.96|105.96|105.95|**105.96**|old == app|
|390x1 + 395x1|57.45|49.47|49.46|49.46|**49.47**|old differed by -0.01|
|390x1 + 395x2|87.92|75.69|75.70|75.70|**75.69**|old differed by 0.01|
|390x2 + 395x1|84.43|72.69|72.70|72.69|**72.69**|old differed by 0.01|
|390x2 + 395x3|145.37|125.16|125.17|125.16|**125.16**|old differed by 0.01|
|390x3 + 395x1|111.41|95.93|95.92|95.92|**95.93**|old differed by -0.01|
|390x3 + 395x3|172.35|148.40|148.39|148.39|**148.40**|old differed by -0.01|

## A2. Flash-only sweep, 7 items x qty 1..3 = 21 placed: charged == exact-decimal client figure == get-Tax preview 21/21

|item x qty|P|shown disc|SHOWN|get-Tax preview|base(model)|CHARGED|flash adm+ven|
|--|--|--|--|--|--|--|--|
|390x1|26.98|4.86|23.23|23.23|23.23|**23.23**|4.86 (line disc x qty 4.86)|
|390x2|53.96|9.71|46.46|46.46|46.46|**46.46**|9.71 (line disc x qty 9.72)|
|390x3|80.94|14.57|69.69|69.69|69.69|**69.69**|14.57 (line disc x qty 14.58)|
|590x1|22.07|4.86|25.57|25.57|25.58|**25.57**|4.86 (line disc x qty 4.86)|
|590x2|44.14|9.71|43.65|43.65|43.65|**43.65**|9.71 (line disc x qty 9.72)|
|590x3|66.21|14.57|61.72|61.72|61.73|**61.72**|14.57 (line disc x qty 14.58)|
|664x1|47.74|12.41|37.10|37.10|37.09|**37.10**|12.41 (line disc x qty 12.41)|
|664x2|95.48|24.82|74.19|74.19|74.19|**74.19**|24.82 (line disc x qty 24.82)|
|664x3|143.22|37.24|111.28|111.28|111.28|**111.28**|37.24 (line disc x qty 37.23)|
|615x1|36.94|3.69|34.91|34.91|34.91|**34.91**|3.69 (line disc x qty 3.69)|
|615x2|73.88|7.39|69.81|69.81|69.82|**69.81**|7.39 (line disc x qty 7.38)|
|615x3|110.82|11.08|104.73|104.73|104.72|**104.73**|11.08 (line disc x qty 11.07)|
|105x1|10.58|1.48|17.06|17.06|17.05|**17.06**|1.48 (line disc x qty 1.48)|
|105x2|21.16|2.96|26.61|26.61|26.61|**26.61**|2.96 (line disc x qty 2.96)|
|105x3|31.74|4.44|36.17|36.17|36.16|**36.17**|4.44 (line disc x qty 4.44)|
|97x1|15.03|1.50|21.71|21.71|21.70|**21.71**|1.50 (line disc x qty 1.50)|
|97x2|30.06|3.01|35.90|35.90|35.91|**35.90**|3.01 (line disc x qty 3.00)|
|97x3|45.09|4.51|50.11|50.11|50.11|**50.11**|4.51 (line disc x qty 4.50)|
|101x1|2.13|0.21|9.52|9.52|9.51|**9.52**|0.21 (line disc x qty 0.21)|
|101x2|4.26|0.43|11.52|11.52|11.53|**11.52**|0.43 (line disc x qty 0.42)|
|101x3|6.39|0.64|13.54|13.54|13.54|**13.54**|0.64 (line disc x qty 0.63)|

Note: the harness sweep.py's float `rd()` reports 105x3 as 36.16 (27.30*1.05+7.5 = 36.165 exact tie); exact decimal half-up = 36.17 = charged = preview. Half-cent ties on a Dart double are outside this ticket.

## A3. Groups (AC3), total shown == placed == sum of children
|case|flag|validate total|place total|sum children|client shown|children|
|--|--|--|--|--|--|--|
|G5 ticket shape 388+390 @39 + 196+198+199 @12 (store-12 distance 2.884 -> delivery 7.21)|ON|138.29|138.29|138.29|138.29|39: 69.16 (flash 1.94+2.92), 12: 69.13|
|same, store-12 distance 3.0042 (delivery 7.51)|ON|138.59|138.59|138.59|138.59|39: 69.16, 12: 69.43|
|G1 388+390 @39 + 51x3 @12|ON|89.26|89.26|89.26|89.26|39: 69.16, 12: 20.10|
|G2 388+390 @39 + 664x1 @57 (up-flip)|ON|106.26|106.26|106.26|106.26|69.16, 37.10|
|G3 388+390x2 @39 + 105x3 @1 + 590x1 @52|ON|154.14|154.14|154.14|154.14|92.40, 36.17, 25.57|
|G0 388+390 @39 + 590x1 @52 (same module)|ON|n/a (no amounts key, single-module)|94.73|94.73|94.73|69.16, 25.57|
|G0 same-module group|OFF|n/a|94.73|94.73|94.73|69.16, 25.57|
|G1/G2/G3/G5 multi-module|OFF|valid:false|403 group_gate empty_cart|-|-|pre-existing gate, untouched|
(Base-model group totals were 138.30 / 94.75 / 89.27, i.e. the cent the fix removes.)

## A5/A6. Controls and the live mixed placement (flag OFF)
|case|P|APP|CHARGED|store_disc|flash adm+ven|get-Tax disc / tax|
|--|--|--|--|--|--|--|
|395 alone (non-flash)|30.47|26.24|**26.23** (byte-identical to base; pre-existing 1c case)|5.48|0|5.4846 / 1.2493|
|388 alone|43.75|45.94|**45.94**|0|0|0 / 2.1875|
|388x2 + 395x1|117.97|118.11|**118.11**|5.48|0|5.4846 / 5.6243|
|FOODIE15 + 388+390|70.73|58.79|**58.79** (coupon 9.88)|0|1.94+2.92|14.74 / 2.7995|
|FOODIE15 + 390x3|80.94|59.23|59.23 (coupon 9.96)|0|5.83+8.74|24.53 / 2.8205|
|FOODIE15 + 390x1|26.98|-|403 coupon min_purchase 25 not met after discount (pre-existing gate; paired [FAIL] get_calculated_tax logged)|||
|**390x2 + 392x2 (live mixed)**|138.62|127.35|**127.35** (order 91528)|**7.62**|3.88+5.83 = **9.71** (sum 17.33)|17.33 / 6.0645|
Coupon FOODIE15 had expired 2026-09-06 in the dump; the copy's coupon row was extended (copy only, fixtures.sql).

## A7. laravel.log (worktree Admin/storage/logs/laravel.log, server env `production`, window 06:39:37 -> end)
0 SQLSTATE / TypeError / Undefined / Division lines. ERROR lines: Firebase/FCM token failures (dead proxy, expected), 3x `[FAIL] get_calculated_tax` http 403 code coupon (expired coupon, paired failure log), 1x OAuth denied (my first, stale token 401). `testing.*` lines in the same file at 06:35-06:38 come from another session's phpunit runs (TypeError in Nears3839 `group_order_validate_failed` is a deliberate test fixture), not from this server.

## B. Device (UserApp from worktree @ a04c58436, UserApp/ and packages/ byte-identical to base 23141efe0; emulator-5590; API_HOST=10.0.2.2:8130; logged in as customer@nears.com; carts seeded in the COPY DB)
|basket|app Subtotal|app Discount|app VAT|app Delivery|APP TOTAL (displayed)|get-Tax preview|placed order_amount (copy DB)|
|--|--|--|--|--|--|--|--|
|(a) mixed 390x2 + 392x2|138.62|17.33|6.06|Free|**127.35**|127.35 (disc 17.33, tax 6.0645)|127.35 (order 91528; store_disc 7.62, flash 3.88+5.83)|
|(b) flash-only 388 + 390|70.73|4.86|3.29|Free|**69.16**|69.16 (disc 4.86, tax 3.2935)|69.16 (order 91529; flash 1.94+2.92)|
|(c) non-flash 395|30.47|5.48|1.25|Free|**26.24**|26.24|26.23 (order 91530; pre-existing one-cent, out of scope)|
Files: dev-{a-mixed,b-flashonly,c-nonflash}-summary.png/.xml (checkout Order Summary, uiautomator dump; positive control: the dump lists Subtotal/Discount/VAT/Delivery Fee/Total Amount nodes).
App logs during the run: [FAIL] geocode-api (no map key on emulator), FcmTopicConfigFailure, 3x `[ERR] checkout: distance response shape invalid, using straight-line fallback` (no delivery address selected; store 39 is free delivery so no effect) - all unrelated to money, paired log lines present.
