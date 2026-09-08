# NEARS-3348 QA progress

verdict: PASS
device: web (Chrome DevTools MCP unavailable -- shared profile locked by concurrent sessions;
        fell back to uinav_web.sh's Playwright driver per documented fallback), isolated DB clone
        multi_food_db_qa3348, dedicated backend 127.0.0.1:8030

AC1 POS quantity=-1 (regression) -- PASS -- ac1-ac3-ac5-ac7-pos-live-http.log
AC2 Edit quantity=-1 (regression) -- PASS -- ac2-ac4-ac6-ac7-edit-order-live-service.log
AC3 POS addon qty<=0 (NEW) -- PASS -- ac1-ac3-ac5-ac7-pos-live-http.log
AC4 Edit addon qty<=0 (NEW) -- PASS -- ac2-ac4-ac6-ac7-edit-order-live-service.log
AC5 POS cross-store addon (NEW) -- PASS -- ac1-ac3-ac5-ac7-pos-live-http.log
AC6 Edit cross-store addon (NEW) -- PASS -- ac2-ac4-ac6-ac7-edit-order-live-service.log
AC7 happy path (POS + Edit) -- PASS -- both logs above

Bonus: POS defensive-cast (non-array add_ons/add_on_qtys) -- PASS -- pos-defensive-cast-live.log
Regression sweep: Vendor Store Panel POS (no add-ons) -- clean -- vendor-panel-pos-regression-sweep.log
Regression sweep: customer place-order path (NEARS-2920, untouched by diff) -- clean -- customer-path-regression-sweep.log
Automated backstop: 23/23, 60 assertions -- automated-backstop.log

Confirmed live (not a regression from this diff, already tracked separately, explicitly
scoped out by the ticket itself): NEARS-3404 (OrderTaxService::setPosCalculatedTax missing
status_code===403 check) and NEARS-3405 (OrderController::update() looping order_details before
its own 403 check) both reproduced live on the isolated clone -- see ac1/ac2 logs for the
signatures. Known pre-existing cosmetic gap (raw JSON 403 page, not a toast) per NEARS-3412 --
observed, not a new finding, not blocking.
