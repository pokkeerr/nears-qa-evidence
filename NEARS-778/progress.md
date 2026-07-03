# NEARS-778 QA progress (device emulator-5560)

VERDICT: PASS (light mode; dark deferred)

- Preflight: baseUrl->local (useHttps=false, 10.0.2.2:8000), backend up (config 200). PASS
- flutter test backstop: 1821 passed, 0 failed. PASS
- Boot: cold boot clean splash -> sector landing, ui_errors clean. AC1(boot) PASS

- AC1 module homes:
  - Food: rendered full (nav, category rails, products, Buy It Again + Most Popular). clean.
  - Grocery: rendered full (nav, category rails, products, Buy It Again). clean (x2).
  - Pharmacy: rendered full. clean.
  - Shop(ecommerce): NO module seeded in DB -> unverifiable-live (data gap). deletion-independent.
- AC2 (twin ProductWithCategoriesView): pharmacy category tabs (All/Cold&Flu/First Aid/Pain Relief/
  Personal Care/Vitamins) switch + products reload (All->PainRelief->Cold&Flu, products change). PASS.
  Shop variant = identical widget file imported by shop_home_screen -> code-proven survival.
- AC3 NearsBottomNav: full uiautomator dump shows all 5 tabs (Home/Categories/Search/Basket/Profile)
  clickable; Home/Basket/Profile switch verified; cart badge mint "1" renders on Basket after add. PASS.
  deleted bottom_nav_item_widget confirmed NOT live nav.
- AC4 blast-radius: cart (full), checkout (note "Add More Delivery Instruction" + address map thumbnail),
  order #171 detail + Order Tracking (Google Map/Map Marker/Live), store profile (Organic Shop), profile/menu
  -- all render clean. PASS.
  order tracking map = live GoogleMap + NearsMapPreview; deleted traking_map_widget had 0 refs.
- AC5 RTL: Arabic applied, menu + module home render clean, nav mirrored (Home right), cart badge intact,
  no overflow/RenderFlex. reverted to English. dark NOT checked (deferred). PASS.

Logs: clean throughout EXCEPT one transient [FAIL] burst (stores/module/banners http_status=null "api request
threw") coincident with emulator wlan0 reconnect at 17:18:05; NOT reproducible on clean reload; endpoints
untouched by deletion; correctly logged per contract (PII-safe, correlation_id). Environmental, not a defect.

Followups (unrelated to deletion):
- Shop/ecommerce module not seeded -> data DoR gap for full shop-home QA.
- James "My Orders" empty until pull-to-refresh after zone switch (backend returns 4 running orders correctly);
  stale-cache display quirk, low-confidence regression-candidate.
