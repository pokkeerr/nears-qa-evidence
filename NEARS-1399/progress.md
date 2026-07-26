# NEARS-1399 QA progress
device=emulator-5556 branch=feat/NEARS-1399-nsurfacecard-reconcile started=2026-07-26T00:03:22Z
[AC1/AC2/AC8 site1 OrderItemWidget] order #158 details: white surface, radius, ambient shadow, NO hard border; bread cover img + text + x2 qty intact. logs clean. -> ac1-orderitemwidget-order158.png

[AC1 _RecommendedStoreCard :931] main home Recommended rail: border gone, ambient shadow, edge-to-edge cover, heart+discount overlays. RTL. -> ac1-recommendedstorecard-931-rtl.png
[AC2 store closed overlays] Food module list: CLOSED (مغلق) badge + grey scrim, favourite/discount overlays positioned. -> ac2-storecard-closed-overlays-rtl.png
[AC8 edge-to-edge covers] Grocery+Food store lists: real cover images edge-to-edge, no inner gutter (padding:zero works), 260-path via SizedBox verified by code+adjacent live. -> ac8-storecard-edge2edge-covers.png
[store card tappable] tapped Supermarket -> navigated to store page (single tap, no double-ripple).
[AC7] widgetbook demo_showcase 3/3 pass (incl RTL/LTR flip); nears_dls NSurfaceCard 22/22 pass (golden light+dark, AC8 verbatim, InkWell, padding).
[AC3/AC4] custom_card.dart DELETED; no dangling CustomCard refs (DetailsCustomCard is a separate class; only NEARS-1399 comments remain).
[backstop] flutter analyze 3 changed files: No issues. RTL store test 2/2. destination_resolver ISOLATED 11/11 (pre-existing full-suite flakiness, NOT this ticket).
[logs] session-wide: clean (no [FAIL]/[ERR]/overflow/exception).
[note] OrderInfoWidget :1641 parcel card is (parcel && isDesktop)-gated -> not reachable on phone form factor; like-for-like change (was isBorder:false -> elevated:true), verified by code + golden.
[note] NewOnMartView 260px rail not data-surfaced in dev zone (no 'new' stores) -> width:260 path verified by code (same SizedBox wrapper) + adjacent live horizontal rail.
[verify orientation] live pass done in Arabic/RTL light mode (satisfies light gate + RTL AC); LTR corroborated by light-mode golden tests + widgetbook LTR story.
