-- rerun of the store-panel failure with a fresh-flash-proof order
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=9203;
UPDATE t_o SET id=9209, order_status='pending', canceled=NULL, canceled_by=NULL, refund_applied_at=NULL; INSERT INTO orders SELECT * FROM t_o;
DROP TEMPORARY TABLE IF EXISTS t_d; CREATE TEMPORARY TABLE t_d AS SELECT * FROM order_details WHERE order_id=9203;
UPDATE t_d SET id=92090, order_id=9209; INSERT INTO order_details SELECT * FROM t_d;
UPDATE delivery_men SET current_orders=3 WHERE id=1;
