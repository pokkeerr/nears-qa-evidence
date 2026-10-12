# NEARS-4158 QA progress (fix_cycle 0, HEAD 1ae7a2ce3, base 15f01794b)
Backend: /Users/Apple/Projects/nears-NEARS-4158-exception-hook-bound-values @ 1ae7a2ce3 (freshness check PASS, :8431)
- AC1 PASS fixed line has no canary (0 hits across laravel.log + laravel-structured.log); base line shows canary + bound values (ac1/base-red files)
- AC2 PASS type/code 42S22/driver_code 1054/file+line/endpoint pattern/correlation_id == sent X-Request-Id
- AC3 PASS git diff --name-only == the 4 allowed files; 128-test backstop green
- AC4 PASS 10 tests, 9 red at base (1 error + 8 failures), green fixed
- AC5 PASS live, request id found by grep, canary absent
