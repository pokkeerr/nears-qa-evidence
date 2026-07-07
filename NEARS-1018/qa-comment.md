<!-- QA-evidence comment for NEARS-1018 — Atlassian MCP unresponsive at post time (2 attempts, timeout).
     Conductor: relay this verbatim as the QA comment. -->
**QA [8] verdict: FAIL** (fix-cycle 0) — device `emulator-5554` (Android), UserApp debug build from worktree `feat/NEARS-1018-banner-slides`, backend `:8000` (worktree-identical code, verified `git diff` vs primary HEAD), zone-1 guest session.

| AC | Result | Evidence | Logs |
|---|---|---|---|
| AC1 — banners 18 + 27 both render, own image/headline/CTA, no grey slide | **PASS** | Distinct `PhotoHeroCard-[<'banner-18'>]` / `-[<'banner-27'>]` in widget tree (stable keys); a11y: own LIMITED OFFER/headline/Claim Deal each; shared image `d-5bed135c7c.png` fetched once, HTTP 200. Shots: `ac1-slide-banner-18-source.png`, `ac1-slide-banner-27-dup-image.png` (+19/20) | clean |
| AC2 — each slide taps to its own target | **PASS** | 27 → Nears Mart (store 1); 19 → Fresh Mart Grocery (store 2); 18 → Nears Mart (store 1); module-switch gate fired. Shots: `ac2-tap-banner27/19/18-*.png` | clean (all `[NET] … 200`, no `[ERR]/[FAIL]`) |
| AC3 — banner 28 (NULL image) absent from carousel | **FAIL** | **5 slides / 5 dots** (expected 4); `banner-28` renders the stock placeholder. Root cause: `Helpers::get_full_url('banner', null, …)` substitutes `asset('public/assets/admin/img/900x400/img1.jpg')` — API never emits null `image_full_url`, so the Flutter null/empty guard can't fire (raw `"image": null` IS in the response). bug-null-image-banner-renders.{png,log} | clean (placeholder loads 200 — silent wrong-render) |
| AC4 — temp-close linked store → slide drops; restore | **PASS** (primary clause) | Store 1 closed via vendor-panel UI → carousel = 2 slides (19, 20), dots=2, no orphan gap (`ac4-store1-closed-2-slides.png`); re-opened → 5 slides restored (`ac4-store1-reopened-restored.png`); stores 2/3 untouched. All-filtered self-hide clause NOT demonstrable live (stores 2/3 settings 500 on both panels — pre-existing); code-verified (`slides.isEmpty → SizedBox`). | clean |
| AC5 — no image URL carries an appended list-index suffix | **PASS** (featured) | `libCachedImageData.db` request-key URLs: 4 clean, shared image cached once, zero `…png0`-style entries; no 404/image exceptions. `ac5-image-urls.log` | clean |

**Regression sweep:** module-choose layout intact; module-home main promo carousel cycles + taps navigate correctly; RTL (Arabic) carousel smoke clean. Dark mode not tested (deferred, light-first).
**Automated backstop:** `flutter test` full worktree UserApp suite — **1939/1939 passed**.

**Task bug (breaks AC3):** null-image featured banner renders as placeholder slide — contract never delivers null `image_full_url` (backend substitution); unit pin feeds a literal null and passes (unit-green / live-fail). Fix angles: guard on raw `image` field, and/or stop banner placeholder substitution server-side.

**Regression bugs (pre-existing):**
1. Main promo carousel still uses the index-suffix hack (`_prepareBanner`): with seeded dup + banner 1's missing file, 2 of 6 slides point at dead URLs (`…png4`/`…jpg5`, curl-verified 404), silently render fallback (no `[FAIL]` line). Tap pairing correct. bug-main-carousel-suffix-slide27.{png,log}. Recommend porting the 1018 slide model.
2. Store-settings 500 for stores 2/3 on vendor (`restaurant-index.blade.php:302`) AND admin (`vendor/view/settings.blade.php:341`) panels: `Undefined array key 1` — `delivery_time` "30-45"/"25-35" lack the unit suffix the blades explode() on. bug-vendor-storesetup-500-store2.log

[Evidence gallery (12 shots + 4 logs)](https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-1018)
