# QA Evidence — NEARS-2753

**Cycle 2 delta re-QA: FAIL -- remove-item DELETE now returns 200 (AC2 holds) but a NEW uncaught null-check crash in ItemController.setExistInCart is newly reachable via this ticket's own success path**

**6 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="after-remove-search-results-toast.png"><img src="after-remove-search-results-toast.png" width="240"></a><br><sub>after remove search results toast</sub></td>
<td align="center" width="33%"><a href="before-remove-search-results.png"><img src="before-remove-search-results.png" width="240"></a><br><sub>before remove search results</sub></td>
<td align="center" width="33%"><a href="bug-cart-remove-item-still-400.png"><img src="bug-cart-remove-item-still-400.png" width="240"></a><br><sub>bug cart remove item still 400</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="bug-raw-backend-toast-guest-session.png"><img src="bug-raw-backend-toast-guest-session.png" width="240"></a><br><sub>bug raw backend toast guest session</sub></td>
<td align="center" width="33%"><a href="bug-search-results-quick-remove-still-qty1.png"><img src="bug-search-results-quick-remove-still-qty1.png" width="240"></a><br><sub>bug search results quick remove still qty1</sub></td>
<td align="center" width="33%"><a href="regression-pass-in-cart-screen-remove-works.png"><img src="regression-pass-in-cart-screen-remove-works.png" width="240"></a><br><sub>regression pass in cart screen remove works</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-cart-remove-item-still-400.log`](bug-cart-remove-item-still-400.log)
- [`bug-cycle2-setexistincart-nullcheck-crash.log`](bug-cycle2-setexistincart-nullcheck-crash.log)
- [`bug-raw-error-toast-dump.xml`](bug-raw-error-toast-dump.xml)
- [`regression-clear-cart-400.log`](regression-clear-cart-400.log)

---
*From `nears/docs/qa-evidence/NEARS-2753/` · public-repo scrub policy (no live secrets; verified clean).*
