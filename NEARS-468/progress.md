# NEARS-468 QA progress — language-row polish (cosmetic)
Device: emulator-5556 | Worktree: nears-NEARS-468-lang-row-polish | branch feat/NEARS-468-lang-row-polish | fix-cycle 0
App: com.izzes.nears (UserApp), booted from worktree via dart launch_app pid 10079

## Checkpoints

### Entry B (Profile > Settings > Language bottom sheet) — DEMONSTRATED
- AC1 no code chip: PASS — a11y content-desc per row = "[flag]\n[name]" only; no EN/AR/ES/BN text node. Shot entryB-picker-english-selected.png
- AC2 English=GB: PASS — content-desc U+1F1EC U+1F1E7 (GB) + Union Jack glyph visible
- AC3 Arabic=AE: PASS — content-desc U+1F1E6 U+1F1EA (AE) + UAE flag glyph
- AC4 Spanish=ES, Bengali=BD: PASS — U+1F1EA U+1F1F8 (ES); U+1F1E7 U+1F1E9 (BD, Bangladesh, NOT Brunei BN)
- AC5 no tick + name not shrunk: PASS — no check node in sheet tree; selected English shows mint fill + mint ring, name full-size bold
- Flags render as real flag glyphs (no letter-pair fallback) on emulator font stack

### RTL (switch to Arabic, reopen picker) — DEMONSTRATED
- Picker re-rendered RTL: emoji+name rows start-aligned (flag at right edge, name to its left); no overflow/clipping, consistent row height. Shot entryB-picker-arabic-rtl.png
- Selection treatment moved to Arabic row: mint fill + mint ring, NO tick; name full-size bold
- Update commit path works: Settings reflected لغة: عربى

### Entry A (first-run onboarding language_screen via pm clear) — DEMONSTRATED
- Same LanguageCardWidget full-screen; identical correct flags (GB/AE/ES/BD), no chips, no tick, mint fill+ring on selected English. Shot entryA-firstrun-language-screen.png
- Note: top hero illustration shows old static flag PNGs inside phone artwork — fixed onboarding asset, NOT the row widget, out of scope, not a defect

### Automated backstop
- flutter test test/features/language/language_card_widget_reskin_test.dart → 7/7 PASS (chip-absence, no-tick, per-language flag mapping, countryCode fallback, CAP-L4 styling)

### Runtime
- No Flutter exceptions/overflows/red-screens in logcat across all navigated states

### Restore
- App restored to English (completed first-run in English; onboarding carousel shows English LTR)

VERDICT: PASS
