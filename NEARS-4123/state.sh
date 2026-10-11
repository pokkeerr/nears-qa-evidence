#!/bin/bash
# Read-only SELECT readout in the probe state-file shape. usage: state.sh "<label>" <order_id>...
# store -> vendor wallet mapping: store 39 -> vendor 37, store 2 -> vendor 2.
DB=multi_food_db_qa4123
q() { mysql -u root "$DB" -N -e "$1"; }
echo "== $1  ($(date '+%Y-%m-%d %H:%M:%S'))"; shift
for id in "$@"; do
  q "select concat('order ',id,': order_status=',order_status,' pay=',payment_status,' pm=',payment_method,' dm=',ifnull(delivery_man_id,'-'),' conf=',ifnull(confirmed,'-'),' picked=',ifnull(picked_up,'-'),' delivered=',ifnull(delivered,'-'),' canceled=',ifnull(canceled,'-'),' refunded=',ifnull(refunded,'-'),' rrc=',ifnull(refund_request_canceled,'-'),' pending=',ifnull(pending,'-')) from orders where id=$id"
  q "select concat('  order_transactions rows=',count(*),' store_amount=',ifnull(sum(store_amount),0),' admin_commission=',ifnull(sum(admin_commission),0)) from order_transactions where order_id=$id"
  q "select concat('  refunds=',ifnull(group_concat(refund_status),'-'),'  offline_payments=',(select ifnull(group_concat(status),'-') from offline_payments where order_id=$id),'  order_payments rows=',(select count(*) from order_payments where order_id=$id)) from refunds where order_id=$id" | grep . || echo "  refunds=-  offline_payments=$(q "select ifnull(group_concat(status),'-') from offline_payments where order_id=$id")"
done
q "select concat('store39 vendor37 wallet total_earning=',total_earning,' collected_cash=',collected_cash) from store_wallets where vendor_id=37"
q "select concat('store2 vendor2 wallet total_earning=',total_earning,' collected_cash=',collected_cash) from store_wallets where vendor_id=2"
q "select concat('dm3 wallet total_earning=',total_earning,' collected_cash=',collected_cash) from delivery_man_wallets where delivery_man_id=3"
q "select concat('dm3 current_orders=',current_orders,' order_count=',order_count) from delivery_men where id=3"
q "select concat('customer6 wallet_balance=',wallet_balance) from users where id=6"
q "select concat('user_notifications(user6) rows=',count(*)) from user_notifications where user_id=6"
q "select concat('admin: order_transactions total rows=',count(*),' sum_admin_commission=',sum(admin_commission)) from order_transactions"
