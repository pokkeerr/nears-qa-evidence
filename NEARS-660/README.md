# QA Evidence — NEARS-660

**PASS — logout clears userAddress PII + resets API header to guest/no-zone; cross-user zone bleed fixed (emulator-5554, com.izzes.nears, feat/NEARS-660-logout-clear-address @6cd242f7)**

**5 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-absent-guest-profile.png"><img src="ac1-absent-guest-profile.png" width="240"></a><br><sub>ac1 absent guest profile</sub></td>
<td align="center" width="33%"><a href="ac1-present-A-zone1-home.png"><img src="ac1-present-A-zone1-home.png" width="240"></a><br><sub>ac1 present A zone1 home</sub></td>
<td align="center" width="33%"><a href="ac2-B-no-zone-bleed-select-location.png"><img src="ac2-B-no-zone-bleed-select-location.png" width="240"></a><br><sub>ac2 B no zone bleed select location</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="ac5-checkout-prefill-A-1.png"><img src="ac5-checkout-prefill-A-1.png" width="240"></a><br><sub>ac5 checkout prefill A 1</sub></td>
<td align="center" width="33%"><a href="ac5-checkout-prefill-B-after-cycle.png"><img src="ac5-checkout-prefill-B-after-cycle.png" width="240"></a><br><sub>ac5 checkout prefill B after cycle</sub></td>
</tr>
</table>

### Other artifacts
- [`ac1-absent-after-logout.log`](ac1-absent-after-logout.log)
- [`ac1-present-prefs.log`](ac1-present-prefs.log)
- [`ac2-B-session-zone-clean.log`](ac2-B-session-zone-clean.log)
- [`bug-getzone-emptycoords-fail.log`](bug-getzone-emptycoords-fail.log)
- [`bug-paymentfailed-parse-warn.log`](bug-paymentfailed-parse-warn.log)
- [`progress.md`](progress.md)

---
*From `nears/docs/qa-evidence/NEARS-660/` · public-repo scrub policy (no live secrets; verified clean).*
