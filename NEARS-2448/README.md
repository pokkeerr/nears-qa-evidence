# QA Evidence — NEARS-2448

**FAIL - AC1 gap confirmed live (invalid campaign id -> unhandled TypeError, screen stuck); AC2/AC3/AC4 + regression sweep PASS live on emulator-5558**

**6 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-success-state-header-store-list.png"><img src="ac1-success-state-header-store-list.png" width="240"></a><br><sub>ac1 success state header store list</sub></td>
<td align="center" width="33%"><a href="ac1-transport-failure-NErrorRetry.png"><img src="ac1-transport-failure-NErrorRetry.png" width="240"></a><br><sub>ac1 transport failure NErrorRetry</sub></td>
<td align="center" width="33%"><a href="ac2-retry-recovers-to-loaded-state.png"><img src="ac2-retry-recovers-to-loaded-state.png" width="240"></a><br><sub>ac2 retry recovers to loaded state</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="ac4-empty-state-not-error.png"><img src="ac4-empty-state-not-error.png" width="240"></a><br><sub>ac4 empty state not error</sub></td>
<td align="center" width="33%"><a href="bug-invalid-campaign-id-stuck-blank-CONFIRMED-LIVE.png"><img src="bug-invalid-campaign-id-stuck-blank-CONFIRMED-LIVE.png" width="240"></a><br><sub>bug invalid campaign id stuck blank CONFIRMED LIVE</sub></td>
<td align="center" width="33%"><a href="regression-rtl-arabic-NErrorRetry.png"><img src="regression-rtl-arabic-NErrorRetry.png" width="240"></a><br><sub>regression rtl arabic NErrorRetry</sub></td>
</tr>
</table>

### Other artifacts
- [`blocked-device-pool.log`](blocked-device-pool.log)
- [`bug-invalid-campaign-id-CONFIRMED-LIVE.log`](bug-invalid-campaign-id-CONFIRMED-LIVE.log)
- [`bug-invalid-campaign-id-unhandled-typeerror.log`](bug-invalid-campaign-id-unhandled-typeerror.log)
- [`live-qa-session-summary.log`](live-qa-session-summary.log)

---
*From `nears/docs/qa-evidence/NEARS-2448/` · public-repo scrub policy (no live secrets; verified clean).*
