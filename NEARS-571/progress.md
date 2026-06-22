# NEARS-571 QA progress (live)
- AC1+AC3 mint v4 (no client id): PASS — 8faf7c46.. then 51694b53.. (different, valid v4)
- AC1 honor valid v4: PASS — 3f9a1c2e.. echoed unchanged
- AC1 reject/log-injection: PASS — malformed/trailing-space/wrong-version/oversized all replaced w/ fresh v4; trailing-newline via unit tests (FIX-4 /D)
- AC4+AC2 one [FAIL] per request: PASS — id 11111111.. -> exactly 1 [FAIL] structured + 1 laravel.log; correlation_id==X-Request-Id; type+endpoint+message present (FIX-2/FIX-3)
- AC5 PII-safe: PASS — token+name+phone+email+lat/lng+query in request; NONE in structured log; context=type+endpoint(path) only; data/data_payload stripped (FIX-5)
- AC7 exact names: PASS — header X-Request-Id, field correlation_id
- AC8 degraded JSON+channels+OTel-off: PASS — 6/6 valid JSON; stack=[single,structured]; otel logs exporter null; user_context false; laravel.log still written; no collector errors cold-boot
- AC9 joinability: PASS(design) — correlation_id promoted, trace_id kept in context; local correlate by X-Request-Id (566)
- AC6 phpunit: PASS — 346/346 (4881 assertions, 0 fail); 15 NEARS-571 tests green
- Regression: clean — 404/401/403 shapes preserved; /config 200 body intact
VERDICT: PASS
