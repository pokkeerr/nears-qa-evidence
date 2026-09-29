# NEARS-3908 QA [8] evidence (API-only, backend @ e26154505, port 8190, DB copy multi_food_db_qa_bug3908)
Each run-*.json = request body, HTTP status, response (payment_token scrubbed), and DB state after (orders, order_payments, wallet_transactions).
- group flag+COD w=25: 200, wallet_paid 25 + amount_due 41.15 = total 66.15; 46.05 child confirmed (paid:wallet 25 / unpaid:cod 21.05), 20.10 child pending plain COD.
- group flag+COD w=50: 200, 46.05 child fully covered (0.00 cod row, confirmed), 20.10 child 3.95 wallet + 16.15 cod; debits 46.05 + 3.95.
- group flag+digital w=25: 200, both children failed until settled; payment-mobile intent = 41.15 (payment_requests row), not 66.15.
- group flag+digital w=25.125: wallet floored to 25.12, due 41.03, intent 41.03, 0.005 left in wallet.
- refusals (wallet 0, 0.004, 100): 403 partial_payment insufficient_wallet / wallet_covers_total, wallet+orders+wtx untouched.
- delivered spot check: fully covered COD child collected 0.00 cash; partly covered collected 16.15.
