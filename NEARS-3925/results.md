# NEARS-3925 QA evidence (API-level, private DB copy multi_food_db_qa_bug3925, own server :8130 @ 9dcf18b66)

Model: SHOWN = exact-decimal client figure round((P - round(sum raw unit disc x qty,2)) * 1.05 + delivery, 2); BASE = same with the RAW discount (pre-fix charge semantics, computed not measured); CHARGED = persisted orders.order_amount from POST /customer/order/place. flag cross_module_basket=0.

## A. Single-store sweep: 7 flash items x qty 1..3 (21 placed orders)

|items|store|P|raw disc|shown disc|deliv|SHOWN|get-Tax preview|BASE(model)|CHARGED|chg-shown|chg-base|flash adm+ven|sum(line disc x qty)|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|390x1|39|26.98|4.8564|4.86|0.00|23.23|23.23|23.23|23.23|0.00|0.00|1.94+2.92|4.86|
|390x2|39|53.96|9.7128|9.71|0.00|46.46|46.46|46.46|46.46|0.00|0.00|3.88+5.83|9.72|
|390x3|39|80.94|14.5692|14.57|0.00|69.69|69.69|69.69|69.69|0.00|0.00|5.83+8.74|14.58|
|590x1|52|22.07|4.8554|4.86|7.50|25.57|25.57|25.58|25.57|0.00|-0.01|1.94+2.92|4.86|
|590x2|52|44.14|9.7108|9.71|7.50|43.65|43.65|43.65|43.65|0.00|0.00|3.88+5.83|9.72|
|590x3|52|66.21|14.5662|14.57|7.50|61.72|61.72|61.73|61.72|0.00|-0.01|5.83+8.74|14.58|
|664x1|57|47.74|12.4124|12.41|0.00|37.10|37.10|37.09|37.10|0.00|0.01|4.96+7.45|12.41|
|664x2|57|95.48|24.8248|24.82|0.00|74.19|74.19|74.19|74.19|0.00|0.00|9.93+14.89|24.82|
|664x3|57|143.22|37.2372|37.24|0.00|111.28|111.28|111.28|111.28|0.00|0.00|14.90+22.34|37.23|
|615x1|54|36.94|3.694|3.69|0.00|34.91|34.91|34.91|34.91|0.00|0.00|1.48+2.21|3.69|
|615x2|54|73.88|7.388|7.39|0.00|69.81|69.81|69.82|69.81|0.00|-0.01|2.96+4.43|7.38|
|615x3|54|110.82|11.082|11.08|0.00|104.73|104.73|104.72|104.73|0.00|0.01|4.43+6.65|11.07|
|105x1|1|10.58|1.4812|1.48|7.50|17.06|17.06|17.05|17.06|0.00|0.01|0.59+0.89|1.48|
|105x2|1|21.16|2.9624|2.96|7.50|26.61|26.61|26.61|26.61|0.00|0.00|1.18+1.78|2.96|
|105x3|1|31.74|4.4436|4.44|7.50|36.17|36.17|36.16|36.17|0.00|0.01|1.78+2.66|4.44|
|97x1|1|15.03|1.503|1.50|7.50|21.71|21.71|21.70|21.71|0.00|0.01|0.60+0.90|1.50|
|97x2|1|30.06|3.006|3.01|7.50|35.90|35.90|35.91|35.90|0.00|-0.01|1.20+1.81|3.00|
|97x3|1|45.09|4.509|4.51|7.50|50.11|50.11|50.11|50.11|0.00|0.00|1.80+2.71|4.50|
|101x1|1|2.13|0.213|0.21|7.50|9.52|9.52|9.51|9.52|0.00|0.01|0.08+0.13|0.21|
|101x2|1|4.26|0.426|0.43|7.50|11.52|11.52|11.53|11.52|0.00|-0.01|0.17+0.26|0.42|
|101x3|1|6.39|0.639|0.64|7.50|13.54|13.54|13.54|13.54|0.00|0.00|0.26+0.38|0.63|


## B. Group orders (flag cross_module_basket ON unless noted): group/validate top amounts.order_amount == group/place total_amount == sum(persisted child order_amount) == client model

|basket|validate total|place total|sum children|client SHOWN total|BASE(model) total|children (store: order_amount)|
|--|--|--|--|--|--|--|
|G0 388+390 @39 + 590x1 @52 (same module)|n/a (single-module group: no amounts key)|94.73|94.73|94.73|94.75|39: 69.16, 52: 25.57|
|G1 388+390 @39 + 51x3 @12|88.96|88.96|88.96|88.96|88.97|39: 69.16, 12: 19.80|
|G2 388+390 @39 + 664x1 @57 (up-flip)|106.26|106.26|106.26|106.26|106.26|39: 69.16, 57: 37.10|
|G3 388+390x2 @39 + 105x3 @1 + 590x1 @52|153.84|153.84|153.84|153.84|153.84|39: 92.40, 1: 35.87, 52: 25.57|
|G5 ticket shape 388+390 @39 + 196+198+199 @12 (child 69.13)|138.29|138.29|138.29|138.29|138.3|39: 69.16, 12: 69.13|

Flag OFF (business_settings 228 = 0 on the copy): same-module group G0 (39 + 52, both food) places 200, total 94.73 == sum children 94.73 (base model 94.75). Multi-module groups G1/G2/G3/G5 are refused 403 group_gate/empty_cart at both validate (valid:false) and place - pre-existing gate, untouched by the diff.

## C. Mixed store (flash + product-discount line) and controls (flag OFF)

|case|P|flash raw|non-flash raw|app-style (whole store disc rounded once)|fix (flash once + non-flash raw)|BASE(model, all raw)|CHARGED|
|--|--|--|--|--|--|--|--|
|M1 mixed 390x1 + 395x1 (store 39)|57.45|4.8564|5.4846|49.47|49.46|49.46|49.46|
|M2 mixed 390x2 + 394x2 (store 39)|98.4|9.7128|6.666|86.12|86.13|86.12|86.13|
|M3 mixed 390x2 + 392x2 (store 39)|138.62|9.7128|7.6194|127.35|127.36|127.35|127.36|
|N1 non-flash discount only 395x1|30.47|0.0|5.4846|26.24|26.23|26.23|26.23|
|N2 plain 388x1|43.75|0.0|0.0|45.94|45.94|45.94|45.94|
|N3 plain 388x2 + 395x1 (no flash)|117.97|0.0|5.4846|118.11|118.11|118.11|118.11|
|K1 coupon FOODIE15 + flash 388+390|70.73|4.8564|0.0|58.79|58.79|58.79|58.79|
|K2 coupon FOODIE15 + flash 390x1|26.98|4.8564|0.0|23.23|23.23|23.23|403 coupon min_purchase 25 not met|
|K3 coupon FOODIE15 + flash 390x3|80.94|14.5692|0.0|59.23|59.23|59.23|59.23|
