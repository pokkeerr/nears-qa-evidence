# Wire counts (scratch-backend access log via QA recording proxy; storage/zone/distance noise filtered)

### A1. Store 4117 open (first entry)
```
03:23:26 GET /api/v1/stores/details/4117 -> 200
03:23:26 GET /api/v1/customer/cart/list -> 200
03:23:26 GET /api/v1/customer/wish-list -> 200
03:23:26 GET /api/v1/cashback/list -> 200
03:23:26 GET /api/v1/items/latest?store_id=4117&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
03:23:26 GET /api/v1/items/recommended?store_id=4117&offset=1&limit=50 -> 200
03:23:26 GET /api/v1/categories/offers?limit=10&offset=1&store_id=4117 -> 200
```
### A2. Offers chip tap + load-more (scrolled until the lazy list kept asking)
```
03:23:48 GET /api/v1/categories/items/offers?limit=10&offset=1&type=all&store_id=4117 -> 200
03:24:06 GET /api/v1/categories/items/offers?limit=10&offset=2&type=all&store_id=4117 -> 200
03:24:15 GET /api/v1/categories/items/offers?limit=10&offset=3&type=all&store_id=4117 -> 200
03:24:24 GET /api/v1/categories/items/offers?limit=10&offset=4&type=all&store_id=4117 -> 200
```
### A3. Sub-chip 144 (NEARS600 Deals): page 1, then load-more
```
03:25:16 GET /api/v1/categories/items/144?offers=1&store_id=4117&limit=10&offset=1&type=all -> 200
03:25:31 GET /api/v1/categories/items/144?offers=1&store_id=4117&limit=10&offset=2&type=all -> 200
```
### A4. Sub-chip 1 (General Items)
```
03:26:12 GET /api/v1/categories/items/1?offers=1&store_id=4117&limit=10&offset=1&type=all -> 200
```
### A5. Category tab All
```
03:26:40 GET /api/v1/items/latest?store_id=4117&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
```
### A6. Category tab 144, then Offers chip, then sub-chip 144 (x2: my second tap was a driver re-tap)
```
03:26:54 GET /api/v1/items/latest?store_id=4117&category_id=144&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
03:27:00 GET /api/v1/categories/items/offers?limit=10&offset=1&type=all&store_id=4117 -> 200
03:27:06 GET /api/v1/categories/items/144?offers=1&store_id=4117&limit=10&offset=1&type=all -> 200
03:27:12 GET /api/v1/categories/items/144?offers=1&store_id=4117&limit=10&offset=1&type=all -> 200
```
### A7. Sub-chip 1 with the response proxy-rewritten to an empty page (empty-state demo)
```
03:27:35 GET /api/v1/categories/items/1?offers=1&store_id=4117&limit=10&offset=1&type=all -> REWRITTEN(empty offers page for QA empty-state) 52B
```
### A8. Store 4118 open + Offers chip with backend DOWN (no request reaches the log: connection refused)
```
03:29:47 GET /api/v1/customer/wish-list -> 200
03:29:47 GET /api/v1/customer/cart/list -> 200
03:29:47 GET /api/v1/cashback/list -> 200
03:29:47 GET /api/v1/stores/details/4118 -> 200
03:29:48 GET /api/v1/items/latest?store_id=4118&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
03:29:48 GET /api/v1/categories/offers?limit=10&offset=1&store_id=4118 -> 200
03:29:48 GET /api/v1/items/recommended?store_id=4118&offset=1&limit=50 -> 200
```
### A9. Retry after backend restored
```
03:30:22 GET /api/v1/categories/items/offers?limit=10&offset=1&type=all&store_id=4118 -> 200
```
### A10. Exit store (back)
```
03:30:35 GET /api/v1/customer/order/running-orders?offset=1&limit=50 -> 200
```
### A11. Re-enter store 4117
```
03:30:55 GET /api/v1/stores/details/4117 -> 200
03:30:55 GET /api/v1/customer/cart/list -> 200
03:30:55 GET /api/v1/customer/wish-list -> 200
03:30:55 GET /api/v1/cashback/list -> 200
03:30:55 GET /api/v1/items/latest?store_id=4117&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
03:30:55 GET /api/v1/items/recommended?store_id=4117&offset=1&limit=50 -> 200
03:30:55 GET /api/v1/categories/offers?limit=10&offset=1&store_id=4117 -> 200
03:31:27 GET /api/v1/customer/order/running-orders?offset=1&limit=50 -> 200
```
### A12. Store 4118 with categories/offers delayed 6s (null-in-flight window)
```
03:31:58 GET /api/v1/stores/details/4118 -> 200
03:31:58 GET /api/v1/customer/cart/list -> 200
03:31:58 GET /api/v1/customer/wish-list -> 200
03:31:58 GET /api/v1/cashback/list -> 200
03:31:59 GET /api/v1/items/latest?store_id=4118&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price= -> 200
03:31:59 GET /api/v1/items/recommended?store_id=4118&offset=1&limit=50 -> 200
03:32:05 GET /api/v1/categories/offers?limit=10&offset=1&store_id=4118 -> 200
03:32:07 GET /api/v1/categories/items/offers?limit=10&offset=1&type=all&store_id=4118 -> 200
```
