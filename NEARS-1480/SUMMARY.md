# NEARS-1480 QA — dm.api header-first auth (curl / HTTP-level)

Backend: worktree feat/NEARS-1480-dm-header-auth @ 127.0.0.1:8091 (shared dev DB multi_food_db). DB read-only.
Tokens via read-only SELECT: DM id 1 (Ali Hassan), id 2. Endpoints: /api/v1/delivery-man/{profile, current-orders, message/list, get-disbursement-report}.

## AC1 header-only (Authorization: Bearer, NO ?token=) — PASS
profile 200 (id:1) | current-orders 200 | message/list 200 | get-disbursement-report 200
(current-orders + disbursement 403 only when limit/offset business params omitted — proves auth already passed; 200 with pagination.)

## AC2 query-only (?token=, NO header, backward-compat) — PASS
profile 200 (id:1) | current-orders 200 | message/list 200 | get-disbursement-report 200 — identical to AC1, no regression.

## AC3 invalid/missing/precedence — PASS
(a) invalid token in BOTH header+query -> 401 {"errors":[{"code":"token","message":"The selected token is invalid."}]}
(b) NO token -> 401 {"errors":[{"code":"token","message":"The token field is required."}]}
(c) valid HEADER + garbage ?token= -> 200 as HEADER's DM (id:1) — header-first precedence confirmed
(d) array token ?token[]= (non-scalar guard) -> 401 (not 500) — shape guard works

## Data ownership — PASS
T1 header -> profile id:1 ; T2 header -> profile id:2 (distinct DMs).

## Logs — clean (no 500s/exceptions in serve output; no delivery-man errors in laravel.log)
