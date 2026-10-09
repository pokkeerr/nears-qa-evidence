
## Cycle 1 (delta) - HEAD 284e9f91d, emulator-5554 wm 640x1280@320dp (=320x640dp), light, backend :8491 clone multi_food_db_test_nears_4091
- AC-UI EN wallet 320dp: PASS - 'Referral Reversed for Order #1234' whole (2 lines), '#1234' visible, Debit, red, '- 5 AED' (c1-ac-ui-wallet-en-320dp-scrolled.png/.xml); cashback row 'Cashback Reversed for Order #1234' - 3 AED Debit whole. logs: wallet/transactions http_status=200, clean.
- Loyalty EN: PASS - 'Points Reversed for Order #1234' -10 points Debit whole (c1-ac-ui-loyalty-en-320dp.png/.xml). logs 200 clean.
- AR sanity: PASS - 'إلغاء مكافأة الإحالة للطلب #1234' - د.إ. 5 دَين, id visible (c1-ac-ui-wallet-ar-320dp.png/.xml). NOTE first AR load hit the error state because MY php serve died (socket error, paired [FAIL] logged); restarted server, Retry -> 200, rows render.
- Regression: PASS - credit 'Refund for Order #162' + 19 AED, debit 'Spend on Order # 1251' - 2 AED unchanged vs round 0 (diff of a11y text); only the referral title text changed.
- Automated: flutter test wallet+loyalty 193 passed.
