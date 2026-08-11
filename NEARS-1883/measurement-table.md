# NEARS-1883 — rendered a11y baseline (replaces the `semanticLabel` source-grep census)

Build provenance: worktree `/Users/Apple/Projects/nears-NEARS-1883-measure` detached at
`7f836f8080d00f7c2a76a4871208c473413f902b` (live tip of `feat/userapp-reskin2` at measure time;
the packet's `01d4e861` had already moved). Flutter `/Users/Apple/Tools/flutter` 3.41.9.
APK md5 `62c3422710cecb8d757f7a7fd9b61659`; device `emulator-5554`; app `com.izzes.nears`
`firstInstallTime=2026-08-11 05:56:53` vs `lastUpdateTime=2026-08-12 02:45:58` (= this build).
Light mode only. Instrument = `uiautomator dump` (two-dump rule), extraction
`dumpnodes.py`, proven against known-present values before any absence was believed.

Rendered names are quoted VERBATIM. `""` = node present, name empty. "no node" = absent entirely.

## NEARS-1745 — Sign In (`_navyHeroView`, Android) — dump `1745-sign-in-a11y-dump.xml`

| # | Widget / class | Call site | Rendered accessible name (verbatim) | vs. census |
|---|---|---|---|---|
| 1 | hero back — `Semantics`+`InkWell` | `sign_in_screen.dart` `_heroBackButton` | Button `desc="Back"` | overstated |
| 2 | language pill — `Semantics`+`InkWell` | `sign_in_screen.dart:153` | Button `desc="Language\nLanguage"` — **doubled** | new defect |
| 3 | email/phone `EditText` (`EmailOrPhoneLoginField`) | `manual_login_widget.dart:282` | `hint="Email/Phone"`, `desc=""`, `NAF=true` | overstated |
| 4 | password `EditText` (`NInput`) | `manual_login_widget.dart:118` | `hint="Password"`, `desc=""` | overstated |
| 5 | show/hide password toggle (`NInput` managed) | `manual_login_widget.dart:126-127` | Button `desc="Show password"` | overstated |
| 6 | remember-me row `InkWell` | `manual_login_widget.dart:136` | View `desc="Remember me?"` clickable | overstated |
| 7 | remember-me raw `Checkbox` | `manual_login_widget.dart:144` | `text=""` `desc=""` `hint=""` `checkable=true` → **NO NAME** | **correct — real gap** |
| 8 | `NButton(text:'sign_in')` **primary, idle** | `manual_login_widget.dart:171` | Button `desc="Sign In"` `enabled=true` | overstated |
| 9 | `TextButton` forgot password | `manual_login_widget.dart:183` | Button `desc="Forgot Password?"` | overstated |
| 10 | `TextButton` create account | `manual_login_widget.dart:201` | Button `desc="Create Account"` | overstated |
| 11 | `NButton(variant: secondary)` OTP | `manual_login_widget.dart:224` | **no node** — gated on `onOtpViewClick != null`, manual passes none | not rendered |
| 12 | guest `TextButton` (`MergeSemantics`+`Semantics`) | `sign_in_screen.dart:262-267` | Button `desc="Continue as Guest\nCONTINUE AS GUEST"` — **doubled** | new defect |
| 13 | Terms of Service — `TextSpan`+`TapGestureRecognizer` | `sign_in_screen.dart:328` | Button `desc="Terms of Service"` | overstated |
| 14 | Privacy Policy — `TextSpan`+`TapGestureRecognizer` | `sign_in_screen.dart:342` | Button `desc="Privacy Policy"` | overstated |

Tree stability: 3 consecutive dumps hashed identical; `Sign In` `enabled=true`, `clickable=true`
in all three — the idle primary variant, per the packet's DUMP-IDLE-ONLY rule.

## NEARS-1746 — Phone Verification — dumps `1746-verification-a11y-dump.xml`

Reached live via `forget_pass_screen` → seeded phone `+971500000263` → Request OTP.
**Not environment-blocked.**

| # | Widget / class | Call site | Rendered accessible name (verbatim) | vs. census |
|---|---|---|---|---|
| 1 | `NAppBar` back | `verification_screen.dart:108-113` | Button `desc="Back"` | overstated |
| 2 | `PinCodeTextField` (6-cell OTP) hit area | `verification_screen.dart:230` | View `desc=""` `hint=""` clickable `NAF=true` → **NO NAME** | **correct — real gap** |
| 3 | `PinCodeTextField` inner `EditText` | same | `hint=""` `desc=""`, bounds 1 px tall `[147,1791][1197,1792]` → **NO NAME** | **correct — real gap** |
| 4 | `NButton(text:'verify')` **primary, idle, disabled** | `verification_screen.dart:285` | Button `desc="Verify"` `enabled=false` | overstated |
| 5 | `TextButton` resend | `verification_screen.dart:321` | Button `desc="Resent it"` (after the 50 s timer expires) | overstated |

Row 4 also settles a sub-question: the `_buildPrimary` `Semantics` wrapper is applied on the
**disabled** path too (`enabled` only flips the flag), so `onPressed: null` does not lose the name.

## NEARS-1754 — Sign Up terms row — dump `1754-sign-up-a11y-dump.xml`

Both call sites (`sign_up_widget.dart:620` and `:641`) pass `forDeliveryMan: true`, so the
`Checkbox` branch renders and the `'* '` branch does not.

| # | Widget / class | Call site | Rendered accessible name (verbatim) | vs. census |
|---|---|---|---|---|
| 1 | raw `Checkbox` | `condition_check_box_widget.dart:29` | `text=""` `desc=""` `hint=""` `checkable=true` → **NO NAME** | **correct — real gap** |
| 2 | "I Agree with all the" copy | `condition_check_box_widget.dart:72` | View `desc="I Agree with all the "`, **not clickable, not associated with the checkbox** | correct |
| 3 | terms link — `TextSpan`+`TapGestureRecognizer` | `condition_check_box_widget.dart:76-86` | Button `desc="Terms & Conditions"` | **overstated** |

Adjacent interactive elements on the same screen (same dump, no extra cost):

| Widget | Rendered name |
|---|---|
| hero back | Button `desc="Back"` |
| `EditText` full name | `hint="Full name"` |
| dial-code picker | ImageView `desc="+971"` (value only, no role/purpose) |
| `EditText` phone | `hint="5X XXX XXXX"` |
| `EditText` email | `hint="Email address"` |
| `EditText` password | `hint="Password"` |
| show/hide password ×2 | Button `desc="Show password"` (**identical name on two different fields**) |
| `EditText` confirm password | `hint="Confirm password"` |
| `EditText` refer code | `hint="REFER CODE(OPTIONAL)"` |
| `NButton(text:'sign_up')` primary, disabled | Button `desc="Sign Up"` |
| `TextButton` sign in | Button `desc="Sign In"` |

## NEARS-1752 — class-level rendered evidence + a call-site argument check

Settled by **class-level rendered evidence + a call-site argument check**, exactly as the owner
ruled — **not a per-element dump**. `OtpLoginWidget` stays unreachable (`isOtpViewEnable` has no
open setter; the DB row is absent), so its own elements were never dumped.

- Class-level rendered evidence: rows 7 and 8 of the NEARS-1745 table — an idle primary `NButton`
  renders `desc="<text>"`; a raw `Checkbox` inside an `InkWell`+`Text` row renders with no name.
- Call-site argument check (`otp_login_widget.dart`): `:144` `NButton(text:'sign_in'.tr, …)` and
  `:150` `NButton(text:'login'.tr, …)` — both default `variant: primary`, both non-empty `text`,
  neither passes `semanticLabel`. `:107` is a raw `Checkbox` inside the `:99` `InkWell` with a
  sibling `Text('remember_me'.tr)` — structurally identical to `manual_login_widget.dart:136-164`.

## Cross-cutting: does a non-primary `NButton` expose a name? — measured live

`NButton(variant: NVariant.tertiary, text: 'reset'.tr)` at
`search_filter_bottom_sheet_widget.dart:193` renders as Button `desc="Reset"`
(dump `nbutton-tertiary-reset-a11y-dump.xml`), alongside the sibling primary
`NButton(text:'apply_filters')` → Button `desc="Apply Filters"`.

So `_buildSecondary`'s `OutlinedButton(child: Text(text))` supplies the accessible name with **no**
`Semantics` wrapper and **no** `semanticLabel`. NEARS-1745 AC4 / NEARS-1746 AC4 (`TextButton` →
`NButton(variant: tertiary)`) therefore do **not** lose the name — but see the latent defect below.

## Latent defect — `semanticLabel` is silently dropped by `_buildSecondary`

`n_button.dart:146-158` resolves `semanticLabel` into `p`, but `_buildSecondary` (`:263-339`) never
renders it and `wrapUniversal` (`props/n_element.dart:80-90`) adds only `IgnorePointer`/
`NSkeletonBox`. So on `secondary`/`tertiary`/`ghost` the prop is inert.
**Unobservable today:** all three call sites that pass it — `existing_user_bottom_sheet.dart:121`,
`new_pass_screen.dart:123`, `forget_pass_screen.dart:321` — pass a value equal to `text`.

## Latent defect — the loading primary has no `Semantics` at all

`_buildPrimary` returns at `n_button.dart:179` when `isLoading`, before the `:225` `Semantics`.
Source-verified only; not dumped, per the packet's DUMP-IDLE-ONLY rule.

## The census's second overstatement mechanism — the `TextButton` counts are exactly doubled

Measured at this tip:

| file | `grep -c "TextButton"` | `grep -c "TextButton("` | `grep -c "TextButton.styleFrom"` |
|---|---|---|---|
| `manual_login_widget.dart` | 6 | **3** | 3 |
| `verification_screen.dart` | 2 | **1** | 1 |

A bare `TextButton` substring grep counts each button twice — once for the constructor, once for
its own `TextButton.styleFrom(` style argument. The packet's "1745 has 6 `TextButton`, 1746 has 2"
are those doubled figures. Real counts: **3 and 1**. On Android only 2 of the 3 in
`manual_login_widget.dart` render (`:183`, `:201`); `:423` is inside `webView()` → desktop only.
