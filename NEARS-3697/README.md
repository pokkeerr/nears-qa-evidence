# QA Evidence — NEARS-3697

**FAIL — AC1-4 pass live; page-level loading skeleton (search_result_widget.dart:100 + global_search_skeleton_list.dart) still shimmers popular-items thumbnails at 28dp vs 32dp real content, live pixel-measured (74px vs 84px @ 2.625px/dp)**

**6 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac-rtl-search-stores-thumbnails.png"><img src="ac-rtl-search-stores-thumbnails.png" width="240"></a><br><sub>ac rtl search stores thumbnails</sub></td>
<td align="center" width="33%"><a href="ac1-search-stores-thumbnails.png"><img src="ac1-search-stores-thumbnails.png" width="240"></a><br><sub>ac1 search stores thumbnails</sub></td>
<td align="center" width="33%"><a href="ac1-search-stores-zero-items.png"><img src="ac1-search-stores-zero-items.png" width="240"></a><br><sub>ac1 search stores zero items</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="ac2-global-search-stores-thumbnails.png"><img src="ac2-global-search-stores-thumbnails.png" width="240"></a><br><sub>ac2 global search stores thumbnails</sub></td>
<td align="center" width="33%"><a href="regression-favourites-no-thumbnails.png"><img src="regression-favourites-no-thumbnails.png" width="240"></a><br><sub>regression favourites no thumbnails</sub></td>
<td align="center" width="33%"><a href="regression-loading-skeleton-32dp.png"><img src="regression-loading-skeleton-32dp.png" width="240"></a><br><sub>regression loading skeleton 32dp</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-skeleton-size-mismatch.log`](bug-skeleton-size-mismatch.log)

---
*From `nears/docs/qa-evidence/NEARS-3697/` · public-repo scrub policy (no live secrets; verified clean).*
