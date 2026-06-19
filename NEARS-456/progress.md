# NEARS-456 QA progress (live, emulator-5554, UserApp debug, zone 2 Abu Dhabi unless noted)

- Boot: clean, /api/v1/config 200, no runtime errors. baseUrl resolves to http://10.0.2.2:8000 (local backend, OK).
- Pharmacy module IS seeded (module id 3, featured pharmacy stores in zone 1 & 2). Live pharmacy Featured rail reachable.

## AC-1 pharmacy Featured rail @ scale 1.0 — PASS
- Entered Pharmacy module; "Featured Store" rail shows dense pharmacy cards (name + address row + "X items" + "X.XX km from you" + "Closes 23:00").
- get_runtime_errors: none. ui_errors (logcat flutter): none. Shot 02.

## AC-2 pharmacy Featured rail @ scale 1.15 / 1.3 — PASS (store_card clean)
- OS font_scale set 1.15 then 1.30 (app clamps to 1.3; diagnostics confirm textScaler linear 1.2999x applied).
- @1.3 a RenderFlex overflow of 4.0px DID fire — but error-causing widget = home_screen.dart:324 Column (the "Deliver To" location HEADER), NOT store_card.dart. Logged as regression bug (pre-existing, unrelated file). Shot 04.
- After clearing + scrolling the pharmacy Featured rail (forcing StoreCard relayout) at 1.3: zero runtime errors from store_card. The card fix holds across 1.0/1.15/1.3.

## Regression bug (pre-existing) — home "Deliver To" header overflows 4.0px @ textScale 1.3
- evidence: bug-home-deliverto-header-overflow-textscale13.log

## Bottom-row distance-left / status-right (zone 2, distance SHOWN) — PASS
- Pharmacy + standard cards: "X.XX km from you" chip LEFT, open/closed status chip RIGHT (spaceBetween). Shot 05. No overflow.

## Phantom-gap (distance HIDDEN) — DRIFT, could not reproduce live
- Spawn premise "demo zone 1 coords 0,0 hide distance chip" is OUTDATED: no zone-1 store has 0,0 coords
  (all real Dhaka ~23.78-23.82/90.35-90.37); demo customer zone-1 address (id 46) is the zone-1 centroid,
  so getRestaurantDistance returns a small plausible value -> distance chip SHOWS in zone 1 too.
- distancePlausible=false (distance>100km) only occurs cross-continent, never for in-zone listings.
- Guard verified by inspection + backstop: store_card.dart gates BOTH the chip
  (`distancePlausible ? Flexible(...) : SizedBox()`) AND the 5px gap (`if (distancePlausible) SizedBox(...)`),
  so when distance is hidden the status chip sits at spaceBetween's right edge with NO phantom indent.
  The standard-card overflow test passes at 1.0/1.15/1.3 (it uses a plausible-distance store).

## AC-4 standard non-pharmacy cards — PASS (live + backstop)
- Grocery module: Best-Stores-Nearby + Top-Offers rails render name + rating "(5)" + delivery chip
  (3-5 days / 1-15 min / 2-3 hours) + address (single-line ellipsis, 419 intact) + closed status chip.
  No overflow, no clipping. Shots 08, 09.

## RTL Arabic — PASS
- Distance label "9.79 كم منك": digits "9.79" stay LTR, "كم منك" reads RTL — bidi intact (Text.rich two-style).
- Bottom row mirrors: status chip "23:00 يغلق" LEFT, distance chip RIGHT (mirror of LTR). No overflow. Shot 06.

## Dark + Light mode — PASS
- Dark: shots 02-06 (navy bg, mint/grey chips legible). Light: shot 07 (white card, dark text, mint chip). No overflow either theme.

## Automated backstop — PASS
- store_card_overflow_test.dart: 17/17 (incl. pharmacy-Featured @1.0/1.15/1.3 + long-name+address + standard-card @ all scales + 419 long-name guards; composition assertions present).
- adjacent: recommended_store_card + store_controller + most_popular_rail_semantics + item_shimmer_overflow = 30/30.

## VERDICT: PASS. One pre-existing REGRESSION bug (home "Deliver To" header overflows 4.0px @ textScale 1.3, home_screen.dart:324 — NOT this change's file).
