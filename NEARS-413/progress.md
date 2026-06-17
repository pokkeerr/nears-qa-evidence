# NEARS-413 Live QA progress (fix-cycle 0)

Device: emulator-5554 (com.izzes.nears v3.8.0, fresh build of 6726ba0f). Backend up (200), queue running.

## AC-1 Legal/HTML chrome — PASS
- Terms & Conditions: navy AppBar sampled (0,0,128)=#000080 across full width; white centred title; DLS white back chevron; white DLS card (brLg/surface3/elev1); FooterView guard present (no blank screen). No runtime errors.
- Backend serves EMPTY html for terms/privacy/about/shipping in this DB (data condition, not a defect) -> card renders empty body correctly. refund={}, cancellation=404 page (route not configured this DB).
- Diff is chrome-only: HtmlWidget body + onTapUrl(launchUrlString) UNTOUCHED. Body-renders-unchanged + external-link covered by html_viewer_chrome_test (green) + diff proof.
- Mint loader: const CircularProgressIndicator(mint) confirmed in source + test.

## AC backstop: ALL 156 tests passed (html/parcel/store/item/update incl. update_screen_blocking + campaign reskin).

## AC-2 Parcel chrome — PASS (resumed)
- parcelCategory ParcelAppBarWidget: navy bar (0,0,128)=#000080 across y=100-220 (NOT white); white location/title text; 107 mint-ish px in top-right = mint notification dot present; bell present. No separator.
- parcelLocation CustomAppBar: navy (0,0,128) y=110-190; "Change Address" opens address picker -> "Select From Map" opens Google Map ("Pick Location"/"Search Location") which renders & resolves. No errors.
- parcelRequest step-form: navy AppBar (0,0,128) y=110-170 full width; Sender/Receiver tabs + "Save & Continue" render. STOPPED before final submit (real-order safety) — verified up to submit button only.
- Map-picker screen's OWN AppBar is white = the shared Google Map location picker, NOT in this batch's diff (only html/parcel/campaign/update touched). Out of scope, pre-existing, not a regression.

## AC-3 Campaign chrome — PASS (backstop + diff; live unreachable = empty data)
- DB read-only: `campaigns` (basic) + `item_campaigns` tables BOTH EMPTY (0 rows); /api/v1/campaigns/{item,basic} return [] for all active modules (1/2/3/5). Live screen unreachable because there is no campaign to open a banner for. Read-only HARD RULE -> cannot seed. DATA condition, not a defect (same class as empty-HTML legal).
- campaign_screen.dart diff = chrome-only: AppBar leading white-circle (surfaceBg/elev1) back + navy arrow_back NearsIcon(mirrorForRtl); _CampaignPill -> NearsIcon('calendar_today'/'schedule') navy/mint pill (fix-cycle-1); desktop hero navyDeep + EdgeInsetsDirectional.start (RTL, fix-cycle-1); textOnNavy/Dim/mint tokens. STATIC schedule + daily-time text (no countdown, by design). Store/item grids render via untouched ItemView.
- itemCampaign screen NOT in this batch's diff (last touched 5068ac05) -> uses shared CustomAppBar (already DLS/navy app-wide, confirmed navy on parcel-location). No change, no regression.
- Backstop campaign_screen_reskin_test.dart GREEN: asserts navyDeep hero, static pills via NearsIcon (calendar_today/schedule, navy size14, no legacy icons), light+dark no-exception, RTL render + EdgeInsetsDirectional.start. (Desktop-width RenderFlex overflow lines in test = artificial narrow-viewport artifact, explicitly drained by tester.takeException; mobile path no-exception.)

## AC-4 Force-update gate — PASS (backstop + diff; live not safely reachable)
- Trigger (route_helper.dart:897): AppConstants.appVersion(3.8) < minimumVersion -> UpdateScreen(isUpdate:true); else maintenanceMode -> UpdateScreen(isUpdate:false). Backend config now: app_minimum_version_android=0, maintenance_mode=False -> gate INACTIVE. Reaching it live needs raising min_version above 3.8 in backend config = destructive DB/config mutation = FORBIDDEN (read-only HARD RULE). Not safely reachable -> backstop per spec.
- update_screen.dart diff: now wrapped in PopScope(canPop:false) (system/hardware back swallowed) + NO AppBar + NO back/close affordance; DLS re-theme of surface/heading/sub-text/icon-circle/CTA (NearsPrimaryButton 'update_now' -> store deep-link, untouched). isDark branch keeps heading/sub-text visible in dark.
- Backstop update_screen_blocking_test.dart GREEN: PopScope canPop==false; no AppBar/BackButton/CloseButton/back-or-close icons; maintenance variant equally blocking; light+dark+RTL render no-exception. Gate is NON-dismissable by construction.

## AC-5 RTL + Dark mode — PASS (live)
- DARK MODE: toggled on. Legal/Terms: AppBar 98% navy bg, back-chevron region 408 white px (VISIBLE), title region 609 white px (VISIBLE) -> NO navy-on-navy (BC-2/3 clean). Parcel bar: navy + 4868 white-text px + 107 mint-dot px -> visible. No errors.
- RTL/ARABIC: switched to عربى. Parcel ParcelAppBarWidget MIRRORS: mint dot flips LEFT (440px, RIGHT=0) vs LTR right (107px). Legal back-chevron MIRRORS to RIGHT (1398px right vs 273 left) via NearsIcon mirrorForRtl; title stays centered (571px). No errors. Both surfaces rendered correctly under combined dark+RTL.
- Campaign RTL backstopped GREEN (campaign_screen_reskin_test: EdgeInsetsDirectional.start + RTL no-exception; dark+light no-exception) — live unreachable (empty campaign data).
- App restored to English + light after the check.

## AC-6 analyze/build — PASS
- flutter analyze (5 changed files: html_viewer_screen, parcel_app_bar_widget, campaign_screen, update_screen, nears_icon): "No issues found!" zero new.
- Build current: app on emulator-5554 IS the 6726ba0f debug build (versionName 3.8.0), exercised live entire run. Final ui_errors sweep across whole session = CLEAN (no Flutter runtime errors anywhere).

## Backstop re-confirmed this run: campaign_screen_reskin + update_screen_blocking + html_viewer_chrome + parcel_app_bar_widget = ALL GREEN (28 tests).
