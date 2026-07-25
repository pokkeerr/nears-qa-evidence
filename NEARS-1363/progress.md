# NEARS-1363 NSectionHeader QA progress
- AC1 standard title-only: PASS (home "What are you shopping for?") — ac1-home-standard-headers.png; logs clean
- AC1 standard title+action-link: PASS (module "Categories"+"See All", navy primaryColor + painted underline; tapped -> navigated) — ac1-categories-header.png; logs clean
- AC1 leading glyph: golden+unit covered (icon-and-action/rtl-icon-action/dark-standard goldens, unit px20/fill/color); live global-search flow not reached
- AC2 store headers: PASS (grouped basket) — injected CustomImage (Fresh Mart Grocery + "1 AED") + storefront fallback (Nears Mart, Daily Fresh Market + "9 AED"); 32dp box, navy name, right-aligned LTR subtotal, no overflow — ac2-grouped-basket-store-headers.png; logs clean
- AC4 boot: PASS clean boot to MainActivity; only FirebaseApp-no-google-services + android.xr + Google cert warnings (all env/pre-existing)
