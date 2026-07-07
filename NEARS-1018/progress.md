# NEARS-1018 QA progress (fix-cycle 0)
Device: emulator-5554 (lock held). App: worktree UserApp debug. Backend: :8000 (worktree-identical code, verified via git diff).
- Zone-1 switch done via GPS fix + Pick Location (guide 5.4b drift noted: header = one a11y node -> map picker).
- API probe: featured zone-1 = banners 18,19,20,27,28; banner 28 image NULL -> backend substitutes placeholder image_full_url (Helpers::get_full_url banner placeholder). 
- Widget tree: _BannerDots count = 5 -> banner-28 RENDERS. AC3 candidate FAIL.
- Logs after zone switch: clean (no ERR/FAIL/404).

## Final AC results (fix-cycle 0)
- AC1 PASS — slides banner-18 + banner-27 both render (unique ValueKeys in tree; a11y: own LIMITED OFFER/headline/Claim Deal each; same shared image = correct; no grey slide; no image errors in logs).
- AC2 PASS — tapped 27 -> Nears Mart (store 1), 19 -> Fresh Mart Grocery (store 2), 18 -> Nears Mart (store 1). Logs clean.
- AC3 FAIL — banner 28 (image NULL) RENDERS as 5th slide: backend substitutes placeholder image_full_url (Helpers::get_full_url 'banner' default), Flutter null/empty guard can't fire. Dots=5 (expected 4). task_bug, breaks_ac.
- AC4 PASS (primary) — store 1 temp-closed via vendor panel UI -> slides 18/27/28 dropped, dots=2, no orphan gap; re-opened -> restored (5 slides). All-filtered self-hide clause NOT demonstrable live: stores 2/3 settings pages 500 on BOTH panels (pre-existing delivery_time parse bug), DB read-only; clause is code-verified (slides.isEmpty -> SizedBox).
- AC5 PASS — image cache DB (request-key URLs): 4 clean URLs, shared image cached ONCE, zero suffixed (.png0/.jpg1...) entries; no 404/image exceptions in logcat for featured.
- Regression: module-choose layout intact; module home main carousel = pre-existing suffix path (see bug-main-carousel-suffix-slide27.log); RTL Arabic carousel clean; dark mode NOT tested (deferred, light-first program rule).

## Delta re-QA (fix-cycle 1, 2026-07-07)
Fix: skip guard re-keyed on RAW `image` field — hasRealImage(raw, full) in both featured loops (additive raw-image field on Banner/BasicCampaignModel). Hot-restarted the same emulator-5554 session.
- AC3 PASS — 4 slides / 4 dots; carousel cycle period 4 = [18,19,20,27]; banner-28 key absent from every widget-tree dump; its (NM|NM|NM) window signature gone. Shot: delta-ac3-4-dots-carousel.png
- Sweep PASS — all 4 slides render own headline/CTA (a11y per position); 18+27 dup pair intact as distinct slides; tap banner-19 -> Fresh Mart Grocery (store 2) (delta-tap-banner19-fresh-mart.png). Logs + runtime errors clean.
- Backstop: banner suite 29/29 green; new pin feeds the REAL contract (null raw image + placeholder image_full_url -> skipped).
VERDICT: PASS (delta).
