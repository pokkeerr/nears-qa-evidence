# NEARS-3909 QA progress (emulator-5590, BRANCH bbbd63dfa vs BASE d160b0fa4, private DB multi_food_db_qa_bug3909)
Instrument: logging pass-through proxy :8141 -> :8140 (instrument-logproxy.py); both APKs built with API_HOST=10.0.2.2:8141. Gateway cancel simulated by the proxy 302 -> /payment-cancel for the DigitalPaymentFailedScreen leg only.
Case A (order module 1 cap 10 -> payload cod_eligible=false; module 2 cap 1000): probe-caseA.txt
Case B (order module 1 cap 1000 -> payload true; module 2 cap 10 [+ (1,400)=10 for B2]): probe-caseB.txt
- base A(a) cold prompt: no delivery-quote, Switch tap -> POST customer/order/payment-method 203 (COD wrongly offered)
- base A(b) DigitalPaymentFailed: delivery-quote {zone 400, module 1} -> COD wrongly offered -> POST 203
- base A(c) order details Pay Again: same quote, same POST 203
- base B2(b): quote {400,1}=false while payload true -> COD wrongly blocked (snackbar, no POST)
- branch A(a)/(b)/(c): NO delivery-quote, NO POST, snackbar (correct block)
- branch B(b)/B2(b): NO delivery-quote, POST payment-method 200 (correct offer)
