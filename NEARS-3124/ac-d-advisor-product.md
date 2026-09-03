# AC (d) spot-check — advisor-product.md (174 lines, H2 set = template) — 3 rules + owner queues

## Rule 1 — the four principles in priority order
**Brief (## Rules and standards, "Principles…", items 1-4):**
> 1. Ease & speed first. The customer's effort and delivery time are the top metric. Fewer taps, faster path, less waiting — this beats every other consideration, including price.
> 2. Only show what's real and available. Never surface a store/product/module that isn't actually serviceable in the customer's zone …
> 3. Nearest-in-zone, not nearest-by-distance. "Near" = assigned to the customer's active zone (§21). …
> 4. Serve the resident, not just the passer-by. Favour the ongoing customer↔local-store relationship over one-off transactions.

**Source nears-reference.md:54-64 (§0):**
> **Principles a change is judged against (in priority order):**
> 1. **Ease & speed first.** The customer's effort and delivery time are the top metric. Fewer taps, faster path, less waiting — this beats every other consideration, including price.
> 2. **Only show what's real and available.** Never surface a store/product/module that …
> 3. **Nearest-in-zone, not nearest-by-distance.** "Near" = assigned to the customer's …
> 4. **Serve the resident, not just the passer-by.** Favour the ongoing …

Verdict: traceable — verbatim (bold markers dropped, line-wrap joined).

## Rule 2 — ticket-creation discipline
**Brief (## Rules and standards, "Ticket hygiene and AC wording", bullet 1):**
> Only create Jira tickets for items the user explicitly confirmed; any URL/domain/value given "as an example" is illustrative — never actionable. (CLAUDE.md §Ticket-creation discipline)

**Source CLAUDE.md:26:**
> > **Ticket-creation discipline.** Only create Jira tickets for items the user explicitly confirmed. Any URL/domain/value given "as an example" is illustrative — never actionable.

Verdict: traceable — verbatim.

## Rule 3 — Known trap `new-doc-not-registered-in-catalog`
**Brief (## Known traps, bullet 2):**
> **new-doc-not-registered-in-catalog** (Low, NEARS-1844) — a committed `docs/**/*.md` absent from `docs/catalog.json` fails `scripts/docs-catalog-check.sh` (ORPHAN); a stub entry fails too (INCOMPLETE needs domain + surface + summary). A doc-producing ticket's DoD includes the registration.

**Source docs/workflow/review-lessons.json:** status=active · severity=Low · first_seen=NEARS-1844
> rule: A committed docs/**/*.md that is absent from docs/catalog.json fails scripts/docs-catalog-check.sh (ORPHAN -> rc=1), and a stub entry also fails (INCOMPLETE requires domain + surface + summary). Authoring the doc and registering it are two steps; the second is silent until the gate runs.

Verdict: traceable — same terms; severity + origin match. (Live corroboration: this run's regression-b shows the ORPHAN/INCOMPLETE sections of that very check.)

## Owner queues (## Rules and standards, "Decision tiers", last bullet) vs design §10:233-234
Brief: `project = NEARS AND labels = advisor-decided` / `project = NEARS AND labels = waiting-on-owner AND status = Blocked` — byte-equal to the design table rows and to owner-queue.sh output (ac-f-owner-queue.txt).

Never-do list: all four mandatory items present + a fifth product-specific item (never accept a widening) — see ac-d-structural.txt.
