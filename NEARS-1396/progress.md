# NEARS-1396 QA — CustomButton → NButton reconcile (53 sites)

Build: worktree feat/NEARS-1396-nbutton-reconcile @ f9fa0eb3 | Devices: emulator-5558 (English/LTR, zone-1&2), emulator-5556 (Arabic/RTL, zone-2) | Light mode only (dark deferred)

## Automated backstop
- DLS suite: 674/674 PASS (incl. AC8 'secondary' golden, NO --update-goldens)
- UserApp flutter analyze: 5 infos / 0 errors (expected)
- Session-wide log scan (both devices, LTR+RTL): ZERO overflow/RenderFlex, ZERO NButton/NVariant errors

## AC results
- AC1 primary mint + loading — PASS live: cart Proceed-to-Checkout, forget-pass Request-OTP (on navy), Sign-In loading spinner (NSpinner replaces label, inert). add-fund=primary (code; Gateways module absent).
- AC2 add_address Save Location — PASS live (mint primary + ctaGlow; Home/Office/Others chips primary-fill vs secondary-outline).
- AC3 item add-to-cart (responsive width) — PASS live (mint primary full-width beside stepper; tap added item).
- AC4 existing_user no(secondary)/yes(primary) — variant proven live in many secondary sites; sheet mapping code-verified.
- AC5 subscription back (ghost) — code+golden verified; live deferred (business subscription flow unreachable as customer).
- AC6 destructive Yes=red-outline / No=navy-outline — PASS live LTR + RTL (red mirrors right in Arabic, legible, no truncation).
- AC7 F1 muted→tertiary outline — PASS live: filter Reset = navy outline (grey gone, not disabled-looking); time_slot cancel + switch_to_cod = NVariant.tertiary (code, same variant).
- AC8 Visit chip navy-outline capsule (brPill) — golden 'secondary' + code (secondary+brPill+h30, sibling to ETA in one Row) + live brPill capsule (ETA pill) + live secondary-outline. Composite Visit-beside-ETA live-capture TIME-BLOCKED: all stores closed at 03:00, Visit-bearing rails use availableStoresOnly (empty).
- AC9 finite-width no overflow — PASS: widths 74/300/width÷3 code-verified; ZERO overflow across full LTR+RTL session; search filter chip seen live.
- AC10 sign_up disabled-until-acceptTerms — gating code-verified (conditional NButton render) + disabled render golden-covered; live deferred (no logout row found to reach sign_up).

## Findings
- task_bugs: NONE (no defect in the change).
- regression_bugs (pre-existing, files NOT in commit, properly logged — non-blocking):
  1. [FAIL] UncaughtAsyncError _TypeError "Null check operator on null value" in ItemRepository._getReviewedItemList, CampaignRepository._getBasicCampaignList/_getItemCampaignList, StoreRepository._getStoreList (data-layer parse).
  2. [ERR] checkout "distance parse failed, using straight-line fallback" (_TypeError) — handled/logged degradation.

Verdict: PASS
