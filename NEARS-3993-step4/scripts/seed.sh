#!/bin/bash
# usage: seed.sh <mode> -- resets Emily's basket in the SCRATCH DB copy and re-seeds via the cart API (via the logging proxy :8593)
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s4/qa
mysql -u root nears_qa_3993s4 -e "delete from carts where user_id=2" || exit 1
mode=$1; [ "$mode" = empty ] && exit 0
TOK=$(cat $S/tok.txt)
post(){ # moduleId json
  curl -s -o /dev/null -w "add -> %{http_code}\n" -X POST http://127.0.0.1:8593/api/v1/customer/cart/add -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -H "moduleId: $1" -H "zoneId: [1]" -H "X-localization: en" -d "$2"
}
add(){ post 1 "{\"item_id\":$1,\"model\":\"Item\",\"price\":$2,\"quantity\":$3}"; }          # legacy grocery module row
addm(){ post "$4" "{\"item_id\":$1,\"model\":\"Item\",\"price\":$2,\"quantity\":$3}"; }     # row with explicit module id
case "$mode" in
  eggs) add 101 2.13 6;;
  1store) add 97 15.03 1; add 98 15.62 1; add 101 2.13 1;;
  3store) add 97 15.03 1; add 98 15.62 1; add 101 2.13 1; add 3 1.50 2; add 8 5.00 1; add 5 2.00 1; add 345 21.12 1;;
  q1) # single store 2: Banana, Tomato (10% discount), Dove 250ml (legacy variation, NEARS-4052 line price)
    add 3 1.50 1; add 5 2.00 1
    post 1 '{"item_id":84,"model":"Item","price":200,"quantity":1,"variation":[{"type":"250ml","price":200,"stock":1000}]}';;
  mixed) # grocery store 1 first ... restaurant store 5 (Garlic Bread) LAST
    add 97 15.03 1; add 98 15.62 1; addm 32 3.99 2 3; addm 33 5.49 1 3; addm 115 15.60 1 2; addm 118 17.33 1 2; addm 25 4.99 1 2;;
  foodfirst) # food rows FIRST, legacy grocery LAST
    addm 115 15.60 1 2; addm 118 17.33 1 2; addm 25 4.99 1 2; addm 32 3.99 2 3; add 97 15.03 1; add 98 15.62 1;;
  foodopts) # grocery Rice, then food row with options (Size Large + Lettuce/Tomato) + add-ons Extra Cheese x1, Jalapenos x3, then Margherita
    add 97 15.03 1
    post 2 '{"item_id":16,"model":"Item","price":8.99,"quantity":1,"variation":[{"name":"Size","values":{"label":["Large"]}},{"name":"Toppings","values":{"label":["Lettuce","Tomato"]}}],"add_on_ids":[1,3],"add_on_qtys":[1,3]}'
    addm 115 15.60 1 2;;
esac
