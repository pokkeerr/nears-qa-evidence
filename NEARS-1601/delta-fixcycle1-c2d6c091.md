# NEARS-1601 delta re-QA (fix_cycle 1) — c2d6c091 — PASS

Device emulator-5554 (448x997dp). APK md5 `c3f96339b7937fefff1c3d36c34dce46` (== local artifact).

## Focus stops, Burger Palace category rail (same store + same uiautomator method throughout)
| build | nodes/chip | focus stops |
|---|---|---|
| merge-base 38464d91 | 1 (label doubled inside node: 'Sides\nSides') | 6 |
| fix v1 6e9c6c21      | 2                                          | 12 |
| fix-cycle c2d6c091   | 1                                          | 6 |

## Offers chip — accessible name preserved, both branches
unselected: flags: isButton, isFocusable, hasSelectedState        label: "Offers filter"
selected:   flags: isSelected, isButton, isFocusable, hasSelectedState  label: "Offers filter"
Visible rendered text = "Offers" (see delta-offers-chip-rail-c2d6c091.png).

## Category chips — plain name, mutually exclusive with Offers
Offers active -> All/Sides/Drinks/Pizza/Burgers all isFalse.
Tap "Sides"  -> "Sides" isSelected, "Offers filter" back to isFalse.

## Visual: bounds pixel-identical to merge-base
Offers [182,2523][483,2631] w=301 | Sides w=214 | Drinks w=232 | Pizza w=211 | Burgers w=204

## Untouched-by-design: offer sub-category pills (~line 1792)
One node each (split did NOT reach them), own selected state intact.
Pre-existing doubled name: "Burgers\nBurgers", "Pain Relief\nPain Relief",
"Sushi & Japanese\nSushi & Japanese" — hand-rolled ConstrainedBox pill, untouched by
both d671b201 and c2d6c091. Followup, not a blocker.

## Spot-check outside store_screen
Cuisine rail: "All" isFalse / "American" isSelected; onRemove child unchanged —
SemanticsNode#764 Rect.fromLTRB(77.3, 15.0, 91.3, 29.0) actions: tap flags: isButton
label: "Clear Filter" (identical rect to pass 1).

## Arabic: SKIPPED live (not cheap). Static file read only, NOT observed:
ar.json offers_rail_label="العروض", offers_filter="تصفية العروض".

## Environment noise, NOT from this change
Inherited app data caused 4 [FAIL]s (LocalClient.cachedFetch: type 'String' is not a
subtype of type 'Map<String, dynamic>' in BannerRepository._getFeaturedBannerList) + one
ANR (Input dispatching timed out, waited 7794ms for KeyEvent) and SUPPRESSED the Offers
chip entirely. After `pm clear` + clean run: zero [FAIL], Offers chip renders. All
findings above are from the clean state.
