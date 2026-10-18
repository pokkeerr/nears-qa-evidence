#!/bin/bash
cd /private/tmp/claude-501/-Users-Apple-Projects-nears/1dde92d5-2f6b-4123-934a-308aa078e4e3/scratchpad/q4249
norm(){ jq -S 'walk(if type=="object" then with_entries(if (.key|test("_full_url$")) then .value="URL" else . end) else . end)' $1; }
while IFS='|' read -r n u z; do
 [ -z "$n" ] && continue
 ./q.sh 8918 base_$n "$u" "$z" >/dev/null; r=$(./q.sh 8917 new_$n "$u" "$z")
 norm base_$n.json > b.norm; norm new_$n.json > n.norm
 echo "$n: $(cmp -s b.norm n.norm && echo IDENTICAL || echo DIFF) $(echo $r | jq -c '{http,total,keys,ps}')"
done <<'LIST'
cat_unf|/api/v1/categories/items/11?limit=25&offset=1|[2]
cat_unf_p2|/api/v1/categories/items/11?limit=25&offset=2|[2]
cat_unf_sel|/api/v1/categories/items/11?limit=25&offset=1&pack_size=1_kg|[2]
cat_unf_417|/api/v1/categories/items/11?limit=25&offset=1|[417]
pop_unf_p2|/api/v1/items/popular?limit=25&offset=2|[2]
rev_f|/api/v1/items/most-reviewed?limit=25&offset=1&with_filters=1|[2]
rev_f_sel|/api/v1/items/most-reviewed?limit=25&offset=1&with_filters=1&pack_size=1_kg|[2]
disc_f|/api/v1/items/discounted?limit=25&offset=1&with_filters=1|[2]
latest_store|/api/v1/items/latest?store_id=12&category_id=0&limit=25&offset=1&with_filters=1|[2]
latest_store2|/api/v1/items/latest?store_id=2&category_id=0&limit=25&offset=1&with_filters=1&pack_size=1_kg|[2]
cat_f|/api/v1/categories/items/11?limit=25&offset=1&with_filters=1|[2]
cat_f_sel|/api/v1/categories/items/11?limit=25&offset=1&with_filters=1&pack_size=1_kg|[2]
cat_f_417|/api/v1/categories/items/11?limit=25&offset=1&with_filters=1|[417]
pop_f|/api/v1/items/popular?limit=25&offset=1&with_filters=1|[2]
pop_fsel|/api/v1/items/popular?limit=25&offset=1&with_filters=1&pack_size=500_ml&diet=veg|[2]
pop_unf|/api/v1/items/popular?limit=25&offset=1|[2]
pop_f417|/api/v1/items/popular?limit=25&offset=1&with_filters=1|[417]
LIST
