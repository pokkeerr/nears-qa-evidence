# NEARS-3935 QA progress (phase 8, cycle 0)

- Private DB nears_qa_3935 (fresh dump of multi_food_db 2026-09-30 13:14). Backend :8135 = worktree nears-NEARS-3935-server-amount-consumers @ feaa11718, `DB_DATABASE=nears_qa_3935 --no-reload`; proven via /api/v1/config footer_text marker QA3935-COPY-MARKER (shared still "Demo footer text @ 2025"). Trace proxy :8136 -> :8135 (app API_HOST=10.0.2.2:8136).
- Copy fixtures: business_settings id=109 loyalty_point_item_purchase_point 0 -> 100; module_zone id=1 (module 1, zone 1) maximum_cod_order_amount 500.00 -> 27.00 (set AFTER the COD order).
- Shared invariants BEFORE: business_settings id=228 = 0; MAX(orders.id) = 91415.
- Device emulator-5556, pkg com.izzes.nears.nears_nears_3935_server_amount_consumers, fix build feaa11718.
- AC1 PASS: COD #91416 (copy): checkout Total Bill 26.00 client; confirm sheet 28.40; 200 body total_ammount 28.4 (rid 70370d18-...); `📊 analytics: purchase {transaction_id: 91416, value: 28.4 ...}`; DB order_amount 28.40. Digital #91417 also purchase value 28.4 == body 28.4 == DB 28.40. Control: NEARS-3931 base recorded value 26.0 on identical basket.
- AC3 PASS: shared_prefs flutter.6ammart_earn_point = "28"; cold start -> "You will earn 28 points after completing this order" (client 26.00 would give 26).
- AC2 PASS: digital #91417 (Paypal, gateway never completed): PaymentScreen isCodEligible POST delivery-quote order_amount=28.4 -> cod_eligible=false (cap 27; 26.0 would be true). PaymentFailedDialog "Switch to Cash On Delivery" tap -> "Payment method is not available" (codEligible=false branch), no /order/payment-method call.
- AC4 PASS (live half): zero `placed amount fallback` lines in both placements; unit backstop covers fallback.
- Backstop: flutter test test/features/checkout/ test/helper/analytics_service_test.dart -> 881 passed.
- [8b] COD-cap candidate CONFIRMED (cod-cap-candidate/): checkout quote order_amount=24.65 -> cod_eligible=true (cap 27.00), COD offered + selected; confirm sheet 28.40 COD; ONE Confirm & place order -> 203 {"code":"order_amount","message":"Amount crossed maximum cod order amount"} (rid cf4ebcde-68c9-451b-8c07-ae8b0a86ee02); customer sees "Order Failed / Sorry, something went wrong / Amount crossed maximum cod order amount". No order created (MAX 91418). Secondary: no [FAIL] paired with the Order Failed screen (only [NET] http_status=203).
