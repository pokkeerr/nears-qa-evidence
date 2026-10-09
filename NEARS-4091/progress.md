
## Cycle 1 (delta) - HEAD 284e9f91d, emulator-5554 wm 640x1280@320dp (=320x640dp), light, backend :8491 clone multi_food_db_test_nears_4091
- AC-UI EN wallet 320dp: PASS - 'Referral Reversed for Order #1234' whole (2 lines), '#1234' visible, Debit, red, '- 5 AED' (c1-ac-ui-wallet-en-320dp-scrolled.png/.xml); cashback row 'Cashback Reversed for Order #1234' - 3 AED Debit whole. logs: wallet/transactions http_status=200, clean.
- Loyalty EN: PASS - 'Points Reversed for Order #1234' -10 points Debit whole (c1-ac-ui-loyalty-en-320dp.png/.xml). logs 200 clean.
- AR sanity: PASS - 'إلغاء مكافأة الإحالة للطلب #1234' - د.إ. 5 دَين, id visible (c1-ac-ui-wallet-ar-320dp.png/.xml). NOTE first AR load hit the error state because MY php serve died (socket error, paired [FAIL] logged); restarted server, Retry -> 200, rows render.
- Regression: PASS - credit 'Refund for Order #162' + 19 AED, debit 'Spend on Order # 1251' - 2 AED unchanged vs round 0 (diff of a11y text); only the referral title text changed.
- Automated: flutter test wallet+loyalty 193 passed.

## Cycle 1b (delta, device-free HTTP) - HEAD d48d75e56, backend :8493 worktree server, clone multi_food_db_test_nears_4091 (recreated mid-run after an external drop ~15:58)
- Trigger qa4091_block_refund (BEFORE INSERT wallet_transactions, order_refund) ON: every caller below answered the error (HTTP 500 errors[{code:'wallet'}] / error flash), order+refund_applied_at+admin digital_received+stock+DM current_orders+wallet+parcel_cancellations UNCHANGED, one [FAIL] line (order id/endpoint/type only). Trigger DROPPED (0 remaining), retry succeeded once (1 order_refund row each).
- Callers: vendor API 9221(paid)/9222(partial); DM API 9203/9204; store panel 9206 (+rerun 9209, fresh flash); admin /admin/order/status 9205; customer parcel cancel 9211; DM parcel cancel 9212; customer parcel return 9213; DM parcel return 9214; admin parcel cancel 9215; admin parcel return 9216.
- Wallet-off (wallet_status=0): vendor 9207 + DM 9208 cancel succeed, 0 credit rows, one '[WARN] refund recorded as manual' (reason wallet_status_off) each.
- Logs: c2-*.log
