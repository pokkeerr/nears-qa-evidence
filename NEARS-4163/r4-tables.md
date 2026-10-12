# NEARS-4163 re-QA cycle 2 (tip 8caa96595) - tables generated from r4-*.json

## C2: AC4b verbatim, RTL, per width x start x card count (base at load vs tip at load / max over walk incl. load / strict max excl. load)

(i) cur card at load tip>=base; (ii) controls present; (iii) every other card max-walk >= its at-load pct on base; (iv) fully-visible-set over walk ⊇ base fully-visible-at-load set. Strict = same with the load state excluded from (iii)/(iv).

| w | cell (cur) | base load | tip load | tip max-walk | tip strict max | base full | tip full(walk) | tip full(strict) | i | ii | iii | iv | PASS | STRICT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 375 | real3 s2 | [0, 0, 0] | [100, 21, 0] | [100, 99, 22] | [100, 99, 22] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 375 | n3 s0 | [96, 26, 0] | [100, 21, 0] | [100, 99, 22] | [100, 99, 22] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 375 | n3 s1 | [25, 0, 0] | [0, 99, 22] | [100, 99, 22] | [100, 99, 22] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 375 | n3 s2 | [0, 0, 0] | [100, 21, 0] | [100, 99, 22] | [100, 99, 22] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 375 | n5 s0 | [96, 26, 0, 0, 0] | [100, 21, 0, 0, 0] | [100, 100, 99, 99, 23] | [100, 100, 99, 99, 23] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 375 | n5 s1 | [25, 0, 0, 0, 0] | [0, 100, 22, 0, 0] | [100, 100, 99, 99, 23] | [100, 100, 99, 99, 23] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 375 | n5 s2 | [0, 0, 0, 0, 0] | [0, 0, 99, 22, 0] | [100, 100, 99, 99, 23] | [100, 100, 99, 99, 23] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 375 | n5 s4 | [0, 0, 0, 0, 0] | [100, 21, 0, 0, 0] | [100, 100, 99, 99, 23] | [100, 100, 99, 99, 23] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 576 | real3 s2 | [0, 0, 0] | [100, 71, 0] | [100, 100, 90] | [100, 100, 90] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 576 | n3 s0 | [94, 100, 0] | [100, 71, 0] | [100, 100, 90] | [100, 100, 90] | [1] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 576 | n3 s1 | [86, 0, 0] | [0, 100, 90] | [100, 100, 90] | [100, 100, 90] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 576 | n3 s2 | [0, 0, 0] | [100, 71, 0] | [100, 100, 90] | [100, 100, 90] | [] | [0, 1] | [0, 1] | Y | Y | Y | Y | PASS | PASS |
| 576 | n5 s0 | [100, 86, 0, 0, 0] | [100, 52, 0, 0, 0] | [100, 100, 100, 90, 100] | [100, 100, 100, 90, 100] | [0] | [0, 1, 2, 4] | [0, 1, 2, 4] | Y | Y | Y | Y | PASS | PASS |
| 576 | n5 s1 | [67, 0, 0, 0, 0] | [15, 100, 71, 0, 0] | [100, 100, 100, 90, 100] | [100, 100, 100, 90, 100] | [] | [0, 1, 2, 4] | [0, 1, 2, 4] | Y | Y | Y | Y | PASS | PASS |
| 576 | n5 s2 | [0, 0, 0, 0, 0] | [0, 0, 100, 90, 0] | [100, 100, 100, 90, 100] | [100, 100, 100, 90, 100] | [] | [0, 1, 2, 4] | [0, 1, 2, 4] | Y | Y | Y | Y | PASS | PASS |
| 576 | n5 s4 | [0, 0, 0, 0, 0] | [100, 52, 0, 0, 0] | [100, 100, 100, 90, 100] | [100, 100, 100, 90, 100] | [] | [0, 1, 2, 4] | [0, 1, 2, 4] | Y | Y | Y | Y | PASS | PASS |
| 768 | real3 s2 | [53, 0, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 768 | n3 s0 | [57, 100, 79] | [100, 100, 0] | [100, 100, 100] | [100, 100, 100] | [1] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 768 | n3 s1 | [100, 65, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [0] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 768 | n3 s2 | [53, 0, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 768 | n5 s0 | [70, 100, 66, 0, 0] | [100, 88, 0, 0, 0] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [1] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 768 | n5 s1 | [100, 52, 0, 0, 0] | [22, 100, 100, 0, 0] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [0] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 768 | n5 s2 | [40, 0, 0, 0, 0] | [0, 0, 100, 100, 24] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 768 | n5 s4 | [0, 0, 0, 0, 0] | [0, 0, 0, 86, 100] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 800 | real3 s2 | [53, 0, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 800 | n3 s0 | [57, 100, 79] | [100, 100, 0] | [100, 100, 100] | [100, 100, 100] | [1] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 800 | n3 s1 | [100, 65, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [0] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 800 | n3 s2 | [53, 0, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 800 | n5 s0 | [70, 100, 66, 0, 0] | [100, 88, 0, 0, 0] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [1] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 800 | n5 s1 | [100, 52, 0, 0, 0] | [22, 100, 100, 0, 0] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [0] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 800 | n5 s2 | [40, 0, 0, 0, 0] | [0, 0, 100, 100, 24] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 800 | n5 s4 | [0, 0, 0, 0, 0] | [0, 0, 0, 86, 100] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 900 | real3 s2 | [53, 0, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 900 | n3 s0 | [57, 100, 79] | [100, 100, 0] | [100, 100, 100] | [100, 100, 100] | [1] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 900 | n3 s1 | [100, 65, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [0] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 900 | n3 s2 | [53, 0, 0] | [0, 100, 100] | [100, 100, 100] | [100, 100, 100] | [] | [0, 1, 2] | [0, 1, 2] | Y | Y | Y | Y | PASS | PASS |
| 900 | n5 s0 | [70, 100, 66, 0, 0] | [100, 88, 0, 0, 0] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [1] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 900 | n5 s1 | [100, 52, 0, 0, 0] | [22, 100, 100, 0, 0] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [0] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 900 | n5 s2 | [40, 0, 0, 0, 0] | [0, 0, 100, 100, 24] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |
| 900 | n5 s4 | [0, 0, 0, 0, 0] | [0, 0, 0, 86, 100] | [100, 100, 100, 100, 100] | [100, 100, 100, 100, 100] | [] | [0, 1, 2, 3, 4] | [0, 1, 2, 3, 4] | Y | Y | Y | Y | PASS | PASS |

Rows: 40; PASS 40; STRICT PASS 40; failing rows: []

## RTL >=992 (5 widths x real3 + n3 starts 0-2 + n5 starts 0-4 = 9 cells each)

| w | cell s | load pct | all cards full by walk | all action buttons reachable | blank state | Commission rightmost | arrows (edge,points,ok) | dots (n,dx) | controls at load | PASS |
|---|---|---|---|---|---|---|---|---|---|---|
| 992 | real3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 992 | n3 s0 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 992 | n3 s1 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 992 | n3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 992 | n5 s0 | [100, 100, 100, 0, 0] | True | True | none | True | {'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 992 | n5 s1 | [0, 99, 100, 100, 0] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 992 | n5 s2 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 992 | n5 s3 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 992 | n5 s4 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1028 | real3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1028 | n3 s0 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1028 | n3 s1 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1028 | n3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1028 | n5 s0 | [100, 100, 100, 0, 0] | True | True | none | True | {'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1028 | n5 s1 | [0, 99, 100, 100, 0] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1028 | n5 s2 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1028 | n5 s3 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1028 | n5 s4 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1199 | real3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1199 | n3 s0 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1199 | n3 s1 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1199 | n3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1199 | n5 s0 | [100, 100, 100, 0, 0] | True | True | none | True | {'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1199 | n5 s1 | [0, 99, 100, 100, 0] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1199 | n5 s2 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1199 | n5 s3 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1199 | n5 s4 | [0, 0, 99, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1200 | real3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1200 | n3 s0 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1200 | n3 s1 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1200 | n3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1200 | n5 s0 | [100, 100, 100, 100, 0] | True | True | none | True | {'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1200 | n5 s1 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1200 | n5 s2 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1200 | n5 s3 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1200 | n5 s4 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1440 | real3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1440 | n3 s0 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1440 | n3 s1 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1440 | n3 s2 | [100, 100, 100] | True | True | none | True | n/a (no arrow shown) | n/a | False | PASS |
| 1440 | n5 s0 | [100, 100, 100, 100, 0] | True | True | none | True | {'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1440 | n5 s1 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1440 | n5 s2 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1440 | n5 s3 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |
| 1440 | n5 s4 | [0, 100, 100, 100, 100] | True | True | none | True | {'prev': ['R', 'right', True], 'next': ['L', 'left', True]} | (2, 0) | True | PASS |

Cells: 45; PASS 45

## C3: all-Shift synthetic cells (every card a Shift card), RTL, per width x card count x start

| w | cell s | cards whose action button was inside stage-outer AND hit-testable at some walk state | unreachable cards | last-card max visible % | all reachable |
|---|---|---|---|---|---|
| 375 | n3 s0 | [0, 1] | [2] | 22 | False |
| 375 | n3 s1 | [0, 1] | [2] | 22 | False |
| 375 | n3 s2 | [0, 1] | [2] | 22 | False |
| 375 | n5 s0 | [0, 1, 2, 3] | [4] | 23 | False |
| 375 | n5 s1 | [0, 1, 2, 3] | [4] | 23 | False |
| 375 | n5 s2 | [0, 1, 2, 3] | [4] | 23 | False |
| 375 | n5 s4 | [0, 1, 2, 3] | [4] | 23 | False |
| 576 | n3 s0 | [0, 1, 2] | none | 90 | True |
| 576 | n3 s1 | [0, 1, 2] | none | 90 | True |
| 576 | n3 s2 | [0, 1, 2] | none | 90 | True |
| 576 | n5 s0 | [0, 1, 2, 3, 4] | none | 100 | True |
| 576 | n5 s1 | [0, 1, 2, 3, 4] | none | 100 | True |
| 576 | n5 s2 | [0, 1, 2, 3, 4] | none | 100 | True |
| 576 | n5 s4 | [0, 1, 2, 3, 4] | none | 100 | True |
| 768 | n3 s0 | [0, 1, 2] | none | 100 | True |
| 768 | n3 s1 | [0, 1, 2] | none | 100 | True |
| 768 | n3 s2 | [0, 1, 2] | none | 100 | True |
| 768 | n5 s0 | [0, 1, 2, 3, 4] | none | 100 | True |
| 768 | n5 s1 | [0, 1, 2, 3, 4] | none | 100 | True |
| 768 | n5 s2 | [0, 1, 2, 3, 4] | none | 100 | True |
| 768 | n5 s4 | [0, 1, 2, 3, 4] | none | 100 | True |
| 800 | n3 s0 | [0, 1, 2] | none | 100 | True |
| 800 | n3 s1 | [0, 1, 2] | none | 100 | True |
| 800 | n3 s2 | [0, 1, 2] | none | 100 | True |
| 800 | n5 s0 | [0, 1, 2, 3, 4] | none | 100 | True |
| 800 | n5 s1 | [0, 1, 2, 3, 4] | none | 100 | True |
| 800 | n5 s2 | [0, 1, 2, 3, 4] | none | 100 | True |
| 800 | n5 s4 | [0, 1, 2, 3, 4] | none | 100 | True |
| 900 | n3 s0 | [0, 1, 2] | none | 100 | True |
| 900 | n3 s1 | [0, 1, 2] | none | 100 | True |
| 900 | n3 s2 | [0, 1, 2] | none | 100 | True |
| 900 | n5 s0 | [0, 1, 2, 3, 4] | none | 100 | True |
| 900 | n5 s1 | [0, 1, 2, 3, 4] | none | 100 | True |
| 900 | n5 s2 | [0, 1, 2, 3, 4] | none | 100 | True |
| 900 | n5 s4 | [0, 1, 2, 3, 4] | none | 100 | True |

## C6: arrow step semantics (RTL): per width totals (arrow steps = prev/next clicks; edge R must move toward LOWER card indexes, edge L toward HIGHER)

| w | cells | arrow expected | arrow opposite | arrow no-op | dot expected | dot opposite | dot no-op |
|---|---|---|---|---|---|---|---|
| 375 | 8 | 20 | 8 | 8 | 4 | 4 | 12 |
| 576 | 8 | 20 | 8 | 8 | 4 | 4 | 12 |
| 768 | 8 | 25 | 0 | 0 | 20 | 0 | 0 |
| 800 | 8 | 25 | 0 | 0 | 20 | 0 | 0 |
| 900 | 8 | 25 | 0 | 0 | 20 | 0 | 0 |
| 992 | 9 | 17 | 0 | 0 | 10 | 0 | 0 |
| 1028 | 9 | 17 | 0 | 0 | 10 | 0 | 0 |
| 1199 | 9 | 17 | 0 | 0 | 10 | 0 | 0 |
| 1200 | 9 | 9 | 0 | 0 | 10 | 0 | 0 |
| 1440 | 9 | 9 | 0 | 0 | 10 | 0 | 0 |
| TOTAL | 85 | 184 | 16 | 16 | 118 | 8 | 24 |

Per-cell counts are in r4-c2-rtl-matrix.json (cells[*].tip.c6 not stored there; derive from tip.steps[*].cls) and r4-c6-step-summary.json (per_cell).
