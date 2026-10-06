#!/bin/bash
# usage: seed.sh <3store|1store|empty>  -- resets Emily's basket in the SCRATCH DB copy and re-seeds via the cart API (via logging proxy)
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3/qa
mysql -u root nears_qa_3993s3 -e "delete from carts where user_id=2" || exit 1
mode=$1; [ "$mode" = empty ] && exit 0
TOK=$(cat $S/tok.txt)
add(){ # item price qty
  curl -s -o /dev/null -w "add item=$1 qty=$3 -> %{http_code}\n" -X POST http://127.0.0.1:8493/api/v1/customer/cart/add -H "Content-Type: application/json" -H "Authorization: Bearer $TOK" -H "moduleId: 1" -H "zoneId: [1]" -H "X-localization: en" -d "{\"item_id\":$1,\"model\":\"Item\",\"price\":$2,\"quantity\":$3}"
}
if [ "$mode" = eggs ]; then add 101 2.13 6; exit 0; fi
addv(){ # item price qty variation-json
  curl -s -o /dev/null -w "addv item=$1 -> %{http_code}\n" -X POST http://127.0.0.1:8493/api/v1/customer/cart/add -H "Content-Type: application/json" -H "Authorization: Bearer $TOK" -H "moduleId: 1" -H "zoneId: [1]" -H "X-localization: en" -d "{\"item_id\":$1,\"model\":\"Item\",\"price\":$2,\"quantity\":$3,\"variation\":$4}"
}
adda(){ # item price qty add_on_ids add_on_qtys
  curl -s -o /dev/null -w "adda item=$1 -> %{http_code}\n" -X POST http://127.0.0.1:8493/api/v1/customer/cart/add -H "Content-Type: application/json" -H "Authorization: Bearer $TOK" -H "moduleId: 1" -H "zoneId: [1]" -H "X-localization: en" -d "{\"item_id\":$1,\"model\":\"Item\",\"price\":$2,\"quantity\":$3,\"add_on_ids\":$4,\"add_on_qtys\":$5}"
}
if [ "$mode" = addon ]; then add 97 15.03 1; adda 17 12.99 1 '[1,3]' '[1,2]'; add 115 15.60 1; exit 0; fi
if [ "$mode" = variant ]; then add 97 15.03 1; addv 84 200 1 '[{"type":"250ml","price":200,"stock":1000}]'; add 3 1.50 1; exit 0; fi
if [ "$mode" != mixed ]; then add 97 15.03 1; add 98 15.62 1; add 101 2.13 1; fi
if [ "$mode" = 3store ]; then
  add 3 1.50 2; add 8 5.00 1; add 5 2.00 1
  add 345 21.12 1
fi
if [ "$mode" = mixed ]; then
  # grocery store 1 (min 20) ; pharmacy store 7 (min 3, free delivery) ; restaurant store 4 Burger Palace (min 8, cutlery) ; restaurant store 5 Pizza Heaven (min 10, below)
  add 97 15.03 1; add 98 15.62 1
  add 32 3.99 2; add 33 5.49 1
  add 115 15.60 1; add 118 17.33 1
  add 25 4.99 1
fi
