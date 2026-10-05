# Wire counts per action, base vs tip (own recording proxy :8250 -> own php -S :8251; /storage and /public image noise filtered; "family" = items/latest, items/search, categories/items/*, stores/details, items/recommended, categories/offers)

| action | base total | tip total | base family | tip family | verdict |
|---|---|---|---|---|---|
| A01-open-store12-from-home | 9 | 9 | 4 | 4 | EQUAL |
| A02-grid-scroll-pages-2-3 | 2 | 2 | 2 | 2 | EQUAL |
| A03-scroll-top | 0 | 0 | 0 | 0 | EQUAL |
| A04-tab-FreshVegetables | 1 | 1 | 1 | 1 | EQUAL |
| A05-tab-GeneralItems | 1 | 1 | 1 | 1 | EQUAL |
| A06-tab-Milk | 1 | 1 | 1 | 1 | EQUAL |
| A07-tab-All | 1 | 1 | 1 | 1 | EQUAL |
| A08-offers-chip | 1 | 1 | 1 | 1 | EQUAL |
| A09-offers-sub-NEARS600Deals | 1 | 1 | 1 | 1 | EQUAL |
| A10-offers-sub-Burgers | 1 | 1 | 1 | 1 | EQUAL |
| A11-offers-then-normal-Milk | 1 | 1 | 1 | 1 | EQUAL |
| A12-tab-All | 1 | 1 | 1 | 1 | EQUAL |
| A13-filter-rating4 | 1 | 1 | 1 | 1 | EQUAL |
| A14-filter-discounted | 1 | 1 | 1 | 1 | EQUAL |
| A15-filter-price | 1 | 1 | 1 | 1 | EQUAL |
| A16-filter-clear | 1 | 1 | 1 | 1 | EQUAL |
| A17-grid-error-first-page | 1 | 1 | 1 | 1 | EQUAL |
| A18-grid-retry-still-failing | 1 | 1 | 1 | 1 | EQUAL |
| A19-grid-retry-after-restore | 1 | 1 | 1 | 1 | EQUAL |
| A20-tab-All-after-recovery | 1 | 1 | 1 | 1 | EQUAL |
| A21-page2-error | 1 | 1 | 1 | 1 | EQUAL |
| A22-page2-retry | 1 | 1 | 1 | 1 | EQUAL |
| A23-scroll-up-to-header | 0 | 0 | 0 | 0 | EQUAL |
| A24-instore-search-open | 0 | 0 | 0 | 0 | EQUAL |
| A25-search-query-e | 1 | 1 | 1 | 1 | EQUAL |
| A26-search-scroll-pages-2-3 | 2 | 2 | 2 | 2 | EQUAL |
| A27-search-new-query-NEARS | 1 | 1 | 1 | 1 | EQUAL |
| A28-search-no-results-zzzz | 1 | 1 | 1 | 1 | EQUAL |
| A29-search-error | 1 | 1 | 1 | 1 | EQUAL |
| A30-search-retry-after-restore | 1 | 1 | 1 | 1 | EQUAL |
| A31-search-sortfilter-organic | 1 | 1 | 1 | 1 | EQUAL |
| A32-back-from-search | 0 | 0 | 0 | 0 | EQUAL |
| A33-tab-Milk-then-search | 2 | 2 | 2 | 2 | EQUAL |
| A34-back-from-search-2 | 0 | 0 | 0 | 0 | EQUAL |
| A35-back-to-home | 1 | 1 | 0 | 0 | EQUAL |
| A36-open-store13-B | 2 | 2 | 0 | 0 | EQUAL |
| A37-storeB-scroll-page2 | 0 | 0 | 0 | 0 | EQUAL |
| A38-storeB-offers-chip | 0 | 0 | 0 | 0 | EQUAL |
| A39-back-to-home-from-B | 10 | 10 | 0 | 0 | EQUAL as a multiset (concurrent home-refresh requests landed in a different order) |
| A40-reenter-store12 | 9 | 9 | 4 | 4 | EQUAL as a multiset (concurrent home-refresh requests landed in a different order) |
| A41-store12-scroll | 1 | 1 | 1 | 1 | EQUAL |
| A42-back-to-home | 1 | 1 | 0 | 0 | EQUAL |
| A43-global-search-open | 20 | 20 | 0 | 0 | EQUAL as a multiset (concurrent home-refresh requests landed in a different order) |
| A44-global-search-Fresh | 2 | 2 | 0 | 0 | EQUAL |
| A45-open-store12-from-search | 9 | 9 | 4 | 4 | EQUAL as a multiset (concurrent home-refresh requests landed in a different order) |
| A46-store-from-search-tab-and-scroll | 2 | 2 | 2 | 2 | EQUAL |
| A47-back-to-search | 1 | 1 | 0 | 0 | EQUAL |
| A48-back-to-home | 14 | 14 | 0 | 0 | EQUAL as a multiset (concurrent home-refresh requests landed in a different order) |

Actions: 48. Identical sequence: 43. Identical multiset: 48. Total requests base=112 tip=112.

## Per-action request detail (tip == base on the multiset; shown once, tip order)

### A01-open-store12-from-home
- GET stores/details/12 -> 200
- GET customer/cart/list -> 200
- GET customer/wish-list -> 200
- GET cashback/list -> 200
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
- GET items/recommended?store_id=12&offset=1&limit=50 -> 200
- GET categories/offers?limit=10&offset=1&store_id=12 -> 200
- GET config/distance-api?origin_lat=24.4499983&origin_lng=54.4249983&destination_lat=24.46&destination_lng=54.38&mode=WALK -> 200
- GET vehicle/extra_charge?distance=6.46 -> 200
### A02-grid-scroll-pages-2-3
- GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
- GET items/latest?store_id=12&category_id=0&offset=3&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A03-scroll-top
### A04-tab-FreshVegetables
- GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A05-tab-GeneralItems
- GET items/latest?store_id=12&category_id=1&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A06-tab-Milk
- GET items/latest?store_id=12&category_id=7&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A07-tab-All
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A08-offers-chip
- GET categories/items/offers?limit=10&offset=1&type=all&store_id=12 -> 200
### A09-offers-sub-NEARS600Deals
- GET categories/items/144?offers=1&store_id=12&limit=10&offset=1&type=all -> 200
### A10-offers-sub-Burgers
- GET categories/items/14?offers=1&store_id=12&limit=10&offset=1&type=all -> 200
### A11-offers-then-normal-Milk
- GET items/latest?store_id=12&category_id=7&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A12-tab-All
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A13-filter-rating4
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=4&min_price=&max_price= -> 200
### A14-filter-discounted
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%22discounted%22%5D&rating_count=4&min_price=&max_price= -> 200
### A15-filter-price
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%22discounted%22%5D&rating_count=4&min_price=&max_price=359.0 -> 200
### A16-filter-clear
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A17-grid-error-first-page
- GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 500
### A18-grid-retry-still-failing
- GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 500
### A19-grid-retry-after-restore
- GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A20-tab-All-after-recovery
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A21-page2-error
- GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 500
### A22-page2-retry
- GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A23-scroll-up-to-header
### A24-instore-search-open
### A25-search-query-e
- GET items/search?store_id=12&name=e&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
### A26-search-scroll-pages-2-3
- GET items/search?store_id=12&name=e&offset=2&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
- GET items/search?store_id=12&name=e&offset=3&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
### A27-search-new-query-NEARS
- GET items/search?store_id=12&name=NEARS&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
### A28-search-no-results-zzzz
- GET items/search?store_id=12&name=zzzz&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
### A29-search-error
- GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 500
### A30-search-retry-after-restore
- GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
### A31-search-sortfilter-organic
- GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
### A32-back-from-search
### A33-tab-Milk-then-search
- GET items/latest?store_id=12&category_id=7&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
- GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=7&filter=%5B%5D -> 200
### A34-back-from-search-2
### A35-back-to-home
- GET customer/order/running-orders?offset=1&limit=50 -> 200
### A36-open-store13-B
- GET customer/suggested-items -> 200
- GET categories/popular -> 200
### A37-storeB-scroll-page2
### A38-storeB-offers-chip
### A39-back-to-home-from-B
- GET config/get-zone-id?lat=24.4499983&lng=54.4249983 -> 200
- GET home/all -> 200
- GET customer/info -> 200
- GET stores/get-stores/all?store_type=all&offset=1&limit=12 -> 200
- GET advertisement/list -> 200
- GET customer/order/buy-it-again?limit=25&offset=1 -> 200
- GET items/popular?type=all&offset=1&limit=25&min_price=0.0&max_price=9999999999.0 -> 200
- GET items/most-reviewed?type=all&offset=1&limit=25&min_price=0.0&max_price=9999999999.0 -> 200
- GET coupon/list -> 200
- GET module -> 200
### A40-reenter-store12
- GET stores/details/12 -> 200
- GET customer/cart/list -> 200
- GET customer/wish-list -> 200
- GET cashback/list -> 200
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
- GET items/recommended?store_id=12&offset=1&limit=50 -> 200
- GET categories/offers?limit=10&offset=1&store_id=12 -> 200
- GET config/distance-api?origin_lat=24.4499983&origin_lng=54.4249983&destination_lat=24.46&destination_lng=54.38&mode=WALK -> 200
- GET vehicle/extra_charge?distance=6.46 -> 200
### A41-store12-scroll
- GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A42-back-to-home
- GET customer/order/running-orders?offset=1&limit=50 -> 200
### A43-global-search-open
- GET config/get-zone-id?lat=24.4499983&lng=54.4249983 -> 200
- GET stores/get-stores/all?store_type=all&offset=1&limit=12 -> 200
- GET customer/order/buy-it-again?limit=25&offset=1 -> 200
- GET items/most-reviewed?type=all&offset=1&limit=25&min_price=0.0&max_price=9999999999.0 -> 200
- GET stores/latest?type=all -> 200
- GET items/popular?type=all&offset=1&limit=25&min_price=0.0&max_price=9999999999.0 -> 200
- GET campaigns/item -> 200
- GET stores/popular?type=all -> 200
- GET banners -> 200
- GET other-banners -> 200
- GET flash-sales -> 200
- GET categories -> 200
- GET customer/order/buy-it-again?limit=25&offset=1 -> 200
- GET advertisement/list -> 200
- GET campaigns/basic -> 200
- GET customer/notifications -> 200
- GET customer/info -> 200
- GET coupon/list -> 200
- GET customer/suggested-items -> 200
- GET categories/popular -> 200
### A44-global-search-Fresh
- GET search/unified?name=Fresh&offset=1&limit=20 -> 200
- GET search/global?name=Fresh -> 200
### A45-open-store12-from-search
- GET stores/details/12 -> 200
- GET customer/cart/list -> 200
- GET customer/wish-list -> 200
- GET cashback/list -> 200
- GET items/recommended?store_id=12&offset=1&limit=50 -> 200
- GET items/latest?store_id=12&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
- GET categories/offers?limit=10&offset=1&store_id=12 -> 200
- GET config/distance-api?origin_lat=24.4499983&origin_lng=54.4249983&destination_lat=24.46&destination_lng=54.38&mode=WALK -> 200
- GET vehicle/extra_charge?distance=6.46 -> 200
### A46-store-from-search-tab-and-scroll
- GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
- GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
### A47-back-to-search
- GET customer/order/running-orders?offset=1&limit=50 -> 200
### A48-back-to-home
- GET config/get-zone-id?lat=24.4499983&lng=54.4249983 -> 200
- GET home/all -> 200
- GET customer/info -> 200
- GET items/popular?type=all&offset=1&limit=25&min_price=0.0&max_price=9999999999.0 -> 200
- GET advertisement/list -> 200
- GET stores/get-stores/all?store_type=all&offset=1&limit=12 -> 200
- GET customer/order/buy-it-again?limit=25&offset=1 -> 200
- GET items/most-reviewed?type=all&offset=1&limit=25&min_price=0.0&max_price=9999999999.0 -> 200
- GET coupon/list -> 200
- GET module -> 200
- GET module -> 200
- GET stores/get-stores/all?featured=1&offset=1&limit=50 -> 200
- GET customer/address/list -> 200
- GET banners?featured=1 -> 200
