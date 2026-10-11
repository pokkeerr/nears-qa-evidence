#!/bin/bash
# QA fixture generator for NEARS-4123 (clone multi_food_db_qa4123 ONLY; INSERT orders/order_details/offline_payments/refunds).
# usage: gen-fixtures.sh > fixtures-nears4123-clone-only.sql
echo "-- NEARS-4123 QA fixtures. TARGET: multi_food_db_qa4123 (private clone) ONLY. Never apply to multi_food_db."
echo "SELECT IF(DATABASE()='multi_food_db_qa4123','db ok',(SELECT 1 FROM information_schema.tables LIMIT 2));"
# ord ID STORE STATUS PAYSTATUS PAYMETHOD TYPE DM  [offline|refund|delivered]
ord() {
  local id=$1 store=$2 st=$3 ps=$4 pm=$5 type=$6 dm=$7 extra=$8
  local item=$([ "$store" = 2 ] && echo 2 || echo 395)
  local mod=$([ "$store" = 2 ] && echo 1 || echo 2)
  local ts="'2026-10-11 05:00:00'"
  echo "DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;"
  echo "UPDATE t_o SET id=$id, order_status='$st', payment_status='$ps', payment_method='$pm', order_type='$type', delivery_man_id=$dm, store_id=$store, module_id=$mod, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending=$ts, created_at=$ts, updated_at=$ts, schedule_at=$ts, otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;"
  if [ "$type" = parcel ]; then echo "UPDATE t_o SET store_id=NULL, module_id=5, parcel_category_id=1, payment_method='$pm' WHERE id=$id;"; fi
  case "$st" in
    canceled) echo "UPDATE t_o SET canceled=$ts WHERE id=$id;";;
    refunded) echo "UPDATE t_o SET canceled=$ts, refunded=$ts WHERE id=$id;";;
    failed) echo "UPDATE t_o SET failed=$ts WHERE id=$id;";;
    processing) echo "UPDATE t_o SET confirmed=$ts, processing=$ts WHERE id=$id;";;
    handover) echo "UPDATE t_o SET confirmed=$ts, processing=$ts, handover=$ts WHERE id=$id;";;
    delivered|refund_requested) echo "UPDATE t_o SET confirmed=$ts, processing=$ts, handover=$ts, delivered=$ts, refund_requested=$ts WHERE id=$id;";;
  esac
  echo "INSERT INTO orders SELECT * FROM t_o;"
  if [ "$type" != parcel ]; then
    echo "INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT $item,$id,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,$ts,$ts,total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;"
  fi
  case "$extra" in
    *offline*) echo "INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT $id,payment_info,'pending',method_fields,$ts,$ts FROM offline_payments WHERE id=50;";;
  esac
  case "$extra" in
    *refund*) echo "INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES ($id,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet',$ts,$ts);";;
  esac
}
# extra: courier accept_order spot check (unassigned claimable + unassigned canceled), returned parcel for the courier writer
ord 91591 39 handover unpaid cash_on_delivery delivery NULL
ord 91592 39 canceled unpaid cash_on_delivery delivery NULL

ord 91593 39 pending unpaid cash_on_delivery delivery 3
