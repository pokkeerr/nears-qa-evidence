# QA Evidence — NEARS-3649

**PASS — CP1/CP2 security fixes verified live (wrong/correct current password, rate-limit 6th=429, session A/B revocation, email dispatch confirmed), CP3/CP4/CP5 layout+copy verified EN+AR+landscape+isDesktop, AC-ANALYTICS all 5 result values fired w/ correct properties, AC-LOG wrong/rate-limit/timeout all correlate FE<->BE, AC-DLS/SHARED catalog+storybook+goldens present, automated backstop 7+31+2 tests green**

**9 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="cp3-strength-bar-visible-weak-en.png"><img src="cp3-strength-bar-visible-weak-en.png" width="240"></a><br><sub>cp3 strength bar visible weak en</sub></td>
<td align="center" width="33%"><a href="cp4-change-password-layout-ar-rtl.png"><img src="cp4-change-password-layout-ar-rtl.png" width="240"></a><br><sub>cp4 change password layout ar rtl</sub></td>
<td align="center" width="33%"><a href="cp4-change-password-layout-en.png"><img src="cp4-change-password-layout-en.png" width="240"></a><br><sub>cp4 change password layout en</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="cp4-isdesktop-legacy-path.png"><img src="cp4-isdesktop-legacy-path.png" width="240"></a><br><sub>cp4 isdesktop legacy path</sub></td>
<td align="center" width="33%"><a href="cp4-landscape-ar-scroll-reachable.png"><img src="cp4-landscape-ar-scroll-reachable.png" width="240"></a><br><sub>cp4 landscape ar scroll reachable</sub></td>
<td align="center" width="33%"><a href="p29-CP1-only-new-confirm-no-current-password__crop.png"><img src="p29-CP1-only-new-confirm-no-current-password__crop.png" width="240"></a><br><sub>p29 CP1 only new confirm no current password crop</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="p29-CP3-strength-bar-rule-text__crop.png"><img src="p29-CP3-strength-bar-rule-text__crop.png" width="240"></a><br><sub>p29 CP3 strength bar rule text crop</sub></td>
<td align="center" width="33%"><a href="p29-CP4-bottom-pinned-button__crop.png"><img src="p29-CP4-bottom-pinned-button__crop.png" width="240"></a><br><sub>p29 CP4 bottom pinned button crop</sub></td>
<td align="center" width="33%"><a href="p29-CP4-empty-top-hero-duplicate-title__crop.png"><img src="p29-CP4-empty-top-hero-duplicate-title__crop.png" width="240"></a><br><sub>p29 CP4 empty top hero duplicate title crop</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-firebase-unguarded-login-block.log`](bug-firebase-unguarded-login-block.log)

---
*From `nears/docs/qa-evidence/NEARS-3649/` · public-repo scrub policy (no live secrets; verified clean).*
