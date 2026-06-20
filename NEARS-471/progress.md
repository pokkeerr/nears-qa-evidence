# NEARS-471 QA progress (fix-cycle 0) — appbar padding
Device: emulator-5554 (Pixel_10_Pro, 1344x2992 @480dpi). Worktree boot.

## LTR (English), address-set state — VERIFIED
- AC1 leading location row clickable node leading edge = x45phys = 15.0 logical px (paddingSizeDefault). NOT flush. PASS
- AC2 trailing bell node ends x1299, right-gap = 15.0 logical px. Symmetric with leading. PASS
- AC3 inset value = paddingSizeDefault(15.0). appbar bg sampled (0,0,128)=#000080 navy. PASS
- AC5 navy color (0,0,128) confirmed; height/bell/dot unchanged vs code. PASS
- Shot: 01-ltr-appbar-address-set.png
- Regression: location selector tap opened Location/Set-Location screen (Home/Demo Zone, Home/Abu Dhabi list). PASS
- Note: post-getZone "Change Location" location-confirm toast auto-shows on each Home mount (pre-existing, overlays the search-pill band).

## RTL (Arabic) — VERIFIED (AC4)
- Switched app language EN->AR via Settings>Language>عربى>Update. Home appbar re-rendered RTL.
- Row MIRRORED: location selector (تسليم إلى) now on logical-leading=RIGHT, node right-edge x1299 -> 15.0 logical inset from right.
- Notification bell now on logical-end=LEFT, node left-edge x45 -> 15.0 logical inset from left.
- Both symmetric at 15.0 logical (paddingSizeDefault). Navy bg (0,0,128) holds. PASS
- Shot: 02-rtl-arabic-appbar.png

## Regression sweep
- Bell tap -> Notifications screen opened (order notification list). PASS. Shot 05.
- Location selector tap -> Location/Set-Location screen opened. PASS.
- appbar navy #000080 + height + bell + mint dot unchanged vs code (only Container padding changed). PASS
- Search pill uses identical EdgeInsetsDirectional.only(start/end: paddingSizeDefault=15) inset (code L537-545) = same 15 logical leading as appbar. Live pixel-measure blocked by persistent post-getZone location-confirm toast overlaying the pill band; verified structurally.

## Device-size coverage (AC6)
- Tested on emulator-5554 = Pixel_10_Pro (1344x2992 @480dpi, devicePixelRatio 3.0) — a STANDARD/large device.
- Pixel 4a (5.8") and Pixel 6 (6.1") NOT available in the pool (only one emulator booted). NOT-VERIFIED on those exact sizes (no silent cap). The inset is a fixed DLS token (15 logical px), density-independent, so it renders identically in logical px across screen sizes; the row is Expanded+Flexible so it adapts. Comfortable on the tested device.

## not-set location branch
- Could NOT reach live: requires AddressHelper.getUserAddressFromSharedPref()==null (no saved address). The seeded account has an address; clearing it = prefs/DB mutation (read-only QA constraint). Verified structurally: not-set branch (L382-458) has EdgeInsets.symmetric(horizontal: paddingSizeSmall=10) INNER pad on top of the 15px page inset => leading ~25px (pre-existing/intended per scope; NOT a fail).
