# QA Evidence — NEARS-338

**FAIL — orders-screen ACs 1-5 all pass live, but the shared PaginatedListView change introduces a duplicate-fetch race (store item search: offset=2 fired twice, duplicate cards rendered; reproduced 2/2)**

**11 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="01-orders-running.png"><img src="01-orders-running.png" width="240"></a><br><sub>orders running</sub></td>
<td align="center" width="33%"><a href="02-history-bottom-oldest.png"><img src="02-history-bottom-oldest.png" width="240"></a><br><sub>history bottom oldest</sub></td>
<td align="center" width="33%"><a href="03-order-25-detail.png"><img src="03-order-25-detail.png" width="240"></a><br><sub>order 25 detail</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="04-running-tab.png"><img src="04-running-tab.png" width="240"></a><br><sub>running tab</sub></td>
<td align="center" width="33%"><a href="05-cancelled-filter.png"><img src="05-cancelled-filter.png" width="240"></a><br><sub>cancelled filter</sub></td>
<td align="center" width="33%"><a href="06-cancelled-bottom-21.png"><img src="06-cancelled-bottom-21.png" width="240"></a><br><sub>cancelled bottom 21</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="07-home-stores-paginated.png"><img src="07-home-stores-paginated.png" width="240"></a><br><sub>home stores paginated</sub></td>
<td align="center" width="33%"><a href="08-store-search-paginated.png"><img src="08-store-search-paginated.png" width="240"></a><br><sub>store search paginated</sub></td>
<td align="center" width="33%"><a href="09-search-bottom.png"><img src="09-search-bottom.png" width="240"></a><br><sub>search bottom</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="10-search-duplicate-items.png"><img src="10-search-duplicate-items.png" width="240"></a><br><sub>search duplicate items</sub></td>
<td align="center" width="33%"><a href="11-orders-dark-mode.png"><img src="11-orders-dark-mode.png" width="240"></a><br><sub>orders dark mode</sub></td>
</tr>
</table>

### Other artifacts
- [`progress.md`](progress.md)

---
*From `nears/docs/qa-evidence/NEARS-338/` · public-repo scrub policy (no live secrets; verified clean).*
