# QA Evidence — NEARS-1578

**PASS — express lane cycle 1: AC1 (dot/text agreement via shared isStoreCurrentlyOpen predicate) confirmed via automated test (data-gap falsifying scenario per ticket brief) + live device confirmation on real seeded stores across zone1/zone2, grocery/food/pharmacy modules; AC2 grep-confirmed; AC3 confirmed both by automated test AND live device (store id=9 Organic Shop active=0, store id=53 CarePlus Pharmacy active=0) — dot+text+NotAvailableWidget overlay all agree, no crash. Automated backstop 153/154 (1 pre-existing unrelated failure, confirmed pre-existing on parent commit).**

**4 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-live-open-stores.png"><img src="ac1-live-open-stores.png" width="240"></a><br><sub>ac1 live open stores</sub></td>
<td align="center" width="33%"><a href="ac1-storecardwidget-allstores.png"><img src="ac1-storecardwidget-allstores.png" width="240"></a><br><sub>ac1 storecardwidget allstores</sub></td>
<td align="center" width="33%"><a href="ac3-live-inactive-store.png"><img src="ac3-live-inactive-store.png" width="240"></a><br><sub>ac3 live inactive store</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="regression-food-module-inactive.png"><img src="regression-food-module-inactive.png" width="240"></a><br><sub>regression food module inactive</sub></td>
</tr>
</table>

---
*From `nears/docs/qa-evidence/NEARS-1578/` · public-repo scrub policy (no live secrets; verified clean).*
