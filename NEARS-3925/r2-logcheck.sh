F=/Users/Apple/Projects/nears-NEARS-3925-flash-discount-rounding/Admin/storage/logs/laravel.log
S=$(grep -n "^\[2026-09-30 06:39:37\]" $F | head -1 | cut -d: -f1)
tail -n +$S $F | grep "^\[[^]]*\] production\." > /private/tmp/claude-501/-Users-Apple-Projects-nears/272c552a-66ed-4d99-a9d9-aa7b921f5263/scratchpad/qa3925r2/log_prod_window.txt
W=/private/tmp/claude-501/-Users-Apple-Projects-nears/272c552a-66ed-4d99-a9d9-aa7b921f5263/scratchpad/qa3925r2/log_prod_window.txt
echo "prod lines: $(wc -l <$W)"; echo "SQL/TypeError/undefined: $(grep -cE 'SQLSTATE|TypeError|Division by zero|Undefined (variable|index|array key)|Call to (undefined|a member)' $W)"
grep "\.ERROR" $W | sed -E 's/^\[[^]]*\] production\.ERROR: //; s/ \{.*//' | sort | uniq -c | sort -rn
