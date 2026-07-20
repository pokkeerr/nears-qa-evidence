# NEARS-1060 AC2 — COUNT cost reduced (live, DB::enableQueryLog + EXPLAIN)

Captured the real `paginate()` COUNT query (the `count(*) as aggregate` entry) via
`DB::enableQueryLog()` around a live `StoreLogic::get_stores(...)` call, for the two having-
triggering filter paths, first on the fix (AFTER) then on base `f91fb365` (BEFORE), fix restored
(md5 verified). Both paths run live even under default settings (they sit outside the
default_status block).

## currently_open filter

BEFORE (base `having('open','>',0)`) — whole query wrapped as a derived table + COUNT(*):
```sql
select count(*) as aggregate from (
  select *, IF((select count(*) from store_schedule where ...)>0,true,false) as open,
    ST_Distance_Sphere(...) as distance, CASE ... END as min_delivery_time,
    (select count(*) from items ...) as items_count,
    (select count(*) from campaigns ...) as campaigns_count,
    (select count(*) from reviews inner join items ...) as reviews_count,
    (select count(*) from orders ...) as orders_count
  from stores where ... having open > ?
) as aggregate_table
```

AFTER (`whereOpenNow` → whereExists) — plain COUNT(*), no wrap, withCount subqueries GONE,
zero correlated reviews subquery in the count:
```sql
select count(*) as aggregate from stores
where exists (select * from modules ...) and status = ?
  and (store_business_model = ? or exists (store_subscriptions ...))
  and exists (select * from zones ...) and module_id = ? and zone_id in (?)
  and exists (select 1 from store_schedule
              where store_schedule.store_id = stores.id and store_schedule.day = ?
                and store_schedule.opening_time < ? and store_schedule.closing_time > ?)
```

## rating_count=4 filter

BEFORE (base `having('avg_r','>=',?)`) — derived-table wrap incl. the correlated avg_r selectSub
+ all 4 withCount subqueries:
```sql
select count(*) as aggregate from (
  select *, ...distance, min_delivery_time, items_count, campaigns_count, reviews_count, orders_count,
    (select AVG(reviews.rating) from reviews inner join items on items.id=reviews.item_id
       where items.store_id=stores.id group by items.store_id having AVG(reviews.rating) >= ?) as avg_r
  from stores where ... having avg_r >= ?
) as aggregate_table
```

AFTER (`whereRaw(AVG_STORE_RATING_SUBQUERY >= ?)`) — plain COUNT(*), no wrap, withCount
subqueries dropped; avg subquery stays only as a WHERE-level predicate (inherent to the filter):
```sql
select count(*) as aggregate from stores
where exists (modules) and status = ? and (... subscriptions ...) and exists (zones)
  and module_id = ? and zone_id in (?)
  and (select AVG(reviews.rating) from reviews inner join items on items.id=reviews.item_id
       where items.store_id = stores.id) >= ?
```

## EXPLAIN (rating_count=4 COUNT, MySQL 8 TREE) — fewer subqueries / no materialize

BEFORE: `Materialize` into `aggregate_table` (derived table), carrying dependent Select #3
(avg, per-row), Select #4 (items_count projection, dependent), Select #5 (orders_count
projection, table scan on orders, dependent) — the withCount projections evaluated for every
candidate row then thrown away. Aggregate cost ≈ 122.

AFTER: NO `Materialize` / no `aggregate_table`; a single dependent Select #2 (avg) used as a
WHERE filter; the items_count/orders_count projection subqueries are GONE from the COUNT.
Aggregate cost ≈ 118. On the currently_open path the AFTER count has ZERO dependent reviews
subquery (only an EXISTS on store_schedule) vs BEFORE's full derived-table wrap.

Delta: derived-table materialization removed; the correlated rating selectSub + 4 withCount
subqueries no longer evaluated inside the COUNT. The structural win scales with candidate-row
count (each row previously ran 5 correlated subqueries inside the materialized derived table).
