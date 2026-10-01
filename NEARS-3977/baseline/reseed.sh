#!/bin/bash
# reseed.sh : on the COPY via API only - remove every item-91 row of user 6, then add
# R1 (64g q3) then R2 (100g q1). moduleId header 1. Logs the request-log range.
B=/Users/Apple/.nears/qa/NEARS-3977/baseline
TOK=$(python3 -c "import json;print(json.load(open('$B/login.json'))['token'])")
H=(-H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -H 'moduleId: 1' -H 'zoneId: [2]')
S=$(wc -l < $B/requests.jsonl | tr -d ' ')
for id in $(mysql -u root -N -e "select id from nears_qa_cartrow.carts where user_id=6 and is_guest=0 and item_id=91"); do
  curl -s -o /dev/null -w "remove $id HTTP %{http_code}\n" -X DELETE "http://127.0.0.1:8101/api/v1/customer/cart/remove-item?cart_id=$id" "${H[@]}"
done
curl -s -o /dev/null -w "add 64g q3 HTTP %{http_code}\n" -X POST http://127.0.0.1:8101/api/v1/customer/cart/add "${H[@]}" -d '{"item_id":91,"model":"Item","price":100,"quantity":3,"variant":"64g","variation":[{"type":"64g","price":100}],"add_on_ids":[],"add_on_qtys":[]}'
curl -s -o /dev/null -w "add 100g q1 HTTP %{http_code}\n" -X POST http://127.0.0.1:8101/api/v1/customer/cart/add "${H[@]}" -d '{"item_id":91,"model":"Item","price":150,"quantity":1,"variant":"100g","variation":[{"type":"100g","price":150}],"add_on_ids":[],"add_on_qtys":[]}'
E=$(wc -l < $B/requests.jsonl | tr -d ' ')
echo "(QA reseed via API: request-log lines $((S+1))-$E are QA, not app)" >> $B/observations.txt
mysql -u root -N -e "select id,item_id,quantity,variation,price,module_id from nears_qa_cartrow.carts where user_id=6 and is_guest=0 and item_id=91 order by id"
