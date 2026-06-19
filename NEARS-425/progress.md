# NEARS-425 QA progress (live)
device: emulator-5554 (Android 17/API 37) | branch feat/NEARS-417-search-input-dls @308a6710

## Live observations (Android emulator-5554)
- [PASS] empty basket: branded 96px disc + shopping_basket glyph; light=navy disc 425-empty-basket-light.png, dark=mint disc 425-empty-basket-dark.png; chrome "Your cart is empty" unchanged
- [PASS] empty search results (Item tab): generic INBOX glyph disc; light 425-empty-search-light.png, dark 425-empty-search-dark.png; "No item available" unchanged
- [PASS] empty store list (Stores tab): generic INBOX glyph disc (light) 425-empty-stores-light.png; "No store available" unchanged
- NO legacy 6amMart clip-art on any surface; NO question-mark fallback (all glyphs registered in NearsIcon._names)
- backstop: no_data_screen_test.dart = part of 16-test PASS set
## SCOPE/DRIFT note
- AC lists "empty orders" + "no-favourites" + "empty-address" — these surfaces do NOT route through NoDataScreen:
  - order_screen.dart uses OrderViewWidget with NearsEmptyState-style emptyIcon (local_shipping/cancel/receipt_long), NOT NoDataScreen
  - favourite_screen.dart + address_screen.dart use their own _emptyState (not NoDataScreen)
  So the NoDataScreen branded disc is exercised on: basket, search-items, search-stores, category-items, all-stores, reviews, no-saved-address. Orders/favourites/address are already-branded by a separate component (out of NEARS-425 file scope).
- [PASS] RTL (Arabic) empty basket: disc centered + symmetric basket glyph, Arabic empty text right-aligned, bottom nav mirrored — 425-empty-basket-rtl.png
