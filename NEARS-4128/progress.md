NEARS-4128 QA progress (tested sha 3b4adc9ea, emulator-5558, backend :8428 on multi_food_db_qa4128)
AC1 COD x4 sites: ar/es/en/bn text PASS at 448dp; es overflow at 320dp/1.0x and 360dp/1.3x (order header parcel row, request-card chip) -> FAIL (task bug)
AC2 canceled-by: 4 mapped values x en/ar/bn/es PASS; unknown/null empty cell PASS; RTL by pixel PASS; narrow 300dp wrap PASS; warn once/open PASS
AC3 37/37 PASS; AC4 PASS all 4 locales; AC5 PASS (key diff exact, positive control fish 1+1 on base, 0 on head)
Return-fee row (4117): not live-demonstrable on fixtures (return_fee=0 hides row); automated 29/29
