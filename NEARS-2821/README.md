# QA Evidence — NEARS-2821

**FAIL cycle 2 - AC1/AC3 PASS (api, confirmed via worktree backend port 8001), AC2 FAIL - original TypeError gone but NEW crash exposed: OrderController.computeOrderFinancials addOns! null-check on order 91174 (add_ons also null, pre-existing unguarded code newly reached)**

**2 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac2-order91174-details-cycle2.png"><img src="ac2-order91174-details-cycle2.png" width="240"></a><br><sub>ac2 order91174 details cycle2</sub></td>
<td align="center" width="33%"><a href="ac2-order91174-details.png"><img src="ac2-order91174-details.png" width="240"></a><br><sub>ac2 order91174 details</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-item-details-list-not-map-typeerror.log`](bug-item-details-list-not-map-typeerror.log)
- [`bug-order-controller-addons-null-typeerror.log`](bug-order-controller-addons-null-typeerror.log)
- [`progress.md`](progress.md)

---
*From `nears/docs/qa-evidence/NEARS-2821/` · public-repo scrub policy (no live secrets; verified clean).*
