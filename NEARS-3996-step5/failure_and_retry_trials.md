# Failure injection + retry, same ops on both builds (proxy mode file; the proxy answers 500 without reaching the backend; every injection restored to ok before the next action)

## A17-grid-error-first-page
- base: GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 500
- tip : GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 500
- screen text base==tip: identical
## A18-grid-retry-still-failing
- base: GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 500
- tip : GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 500
- screen text base==tip: identical
## A19-grid-retry-after-restore
- base: GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 200
- tip : GET items/latest?store_id=12&category_id=5&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 200
- screen text base==tip: identical
## A21-page2-error
- base: GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 500
- tip : GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 500
- screen text base==tip: identical
## A22-page2-retry
- base: GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 200
- tip : GET items/latest?store_id=12&category_id=0&offset=2&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_p -> 200
- screen text base==tip: identical
## A29-search-error
- base: GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 500
- tip : GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 500
- screen text base==tip: identical
## A30-search-retry-after-restore
- base: GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
- tip : GET items/search?store_id=12&name=milk&offset=1&limit=10&type=all&category_id=0&filter=%5B%5D -> 200
- screen text base==tip: identical

## error states observed (label text, identical on both): grid first-page failure = 'Something went wrong / Please try again / Retry' under the tabs; page-2 failure = inline 'Couldn't load more' + 'Retry'; in-store search failure = 'Something went wrong / Please try again / Retry' with the query kept in the field; Retry after restore reloads the list on both builds.

## paired failure logs (logcat 'flutter' tag, scoped to the injected endpoints; both builds): [FAIL] endpoint=/api/v1/items/latest http_status=500 type=ApiFailure x3 (A17, A18, A21); [FAIL] endpoint=/api/v1/items/search http_status=500 type=ApiFailure x1 (A29). Every generic error state has its paired [FAIL] line: no silent failure path. Unexpected [ERR]: 0 on both.
## other [FAIL] lines (identical on both builds, environment): FirebaseInitFailure, FcmTokenFetchFailure, FcmTopicConfigFailure, KilledLaunchNotificationFailure (no google-services.json in a worktree), ImageLoadFailure x4 (product images missing on the backend side)
