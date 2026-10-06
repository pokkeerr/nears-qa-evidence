# cold-start probe: count get-zone-id per cold start (mixed basket, flag ON), noise check for the Q3 mixed cold start difference
START_N=900 source $S/lib.sh
for r in 1 2 3; do
  fresh mixed; settle 5 30
  n=$(reqs | grep -a -c 'get-zone-id'); tot=$(reqs | wc -l | tr -d ' ')
  echo "ZP $VAR r$r get-zone-id=$n total=$tot" >> $S/zp.txt
done
