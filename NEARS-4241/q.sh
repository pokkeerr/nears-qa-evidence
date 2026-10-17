#!/bin/bash
# usage: q.sh port "query"
curl -s -H 'moduleId:1' -H 'zoneId:[2]' -H 'latitude:25.2' -H 'longitude:55.3' -H 'Accept:application/json' "http://127.0.0.1:$1/api/v1/stores/$2" | jq -c '{total:.total_size, rows:[.stores[]|{id,open,avg:.avg_rating}]}'
