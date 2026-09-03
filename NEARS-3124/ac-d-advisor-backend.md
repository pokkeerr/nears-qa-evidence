# AC (d) spot-check — advisor-backend.md (203 lines, H2 set = template) — 3 rules + sources

## Rule 1 — naming convention
**Brief (## Rules and standards, "Architecture and conventions", bullet 5):**
> Naming: snake_case files, PascalCase classes, camelCase variables; follow existing 6amMart patterns rather than introducing new ones. (CLAUDE.md §Conventions)

**Source CLAUDE.md:94 (§Conventions & gotchas):**
> - Naming: snake_case files, PascalCase classes, camelCase variables. Follow existing 6amMart patterns rather than introducing new ones.

Verdict: traceable — same words, only the sentence join (". Follow" → "; follow") differs.

## Rule 2 — global scopes are the only zone/store enforcement
**Brief (## Rules and standards, "Authorization and scoping", bullet 1):**
> Global scopes are the ONLY zone/store enforcement: no zone/store middleware exists anywhere; `ZoneScope`/`StoreScope` Eloquent global scopes are the entire mechanism, so any `DB::table()` write against a scoped model bypasses authorization by construction. (nears-reference.md §9, NEARS-1203)

**Source nears-reference.md:218-222 (§9):**
> ### Global scopes are the ONLY zone/store enforcement — raw writes bypass them (NEARS-1203)
> No zone/store middleware exists anywhere in this codebase — `ZoneScope`/`StoreScope` Eloquent global scopes are the *entire* enforcement mechanism, so any `DB::table()` write against a scoped model bypasses authorization by construction.

Verdict: traceable — heading + first sentence reproduced; "in this codebase" dropped, meaning intact.

## Rule 3 — Known trap `backend-log-bracket-token-outside-tag-vocabulary`
**Brief (## Known traps, bullet 1):**
> **backend-log-bracket-token-outside-tag-vocabulary** (Low, NEARS-2079) — a domain word in the leading bracket of a `Log::` message (`[api]`, `[zone]`) looks like a tag to every grep and matches none; check: `grep -nE "Log::\w+\('\[[a-z]" Admin/app` must return zero.

**Source docs/workflow/review-lessons.json (id lookup via jq):**
- status=active · severity=Low · first_seen=NEARS-2079
- rule (excerpt): "Putting a domain or subsystem word there ('[api]', '[zone]', '[cart]') looks like a tag to every grep and matches none … Reviewer check: grep -nE "Log::\w+\('\[[a-z]" Admin/app must return zero."

Verdict: traceable — severity, origin ticket and the reviewer-check regex are verbatim; the mechanism sentence is quoted.

## Bonus — Known trap `zone-decode-fail-open` (high, NEARS-549)
Source: status=active severity=high first_seen=NEARS-549; rule: "Raw json_decode($zone_id, true) fed straight into whereIn is fail-OPEN: a malformed/absent header … behind a !empty()/truthy guard — silently SKIPS the zone clause and returns cross-zone rows." Brief bullet 3 of Known traps says the same with the same terms. Traceable.

Never-do list: all four mandatory items present (see ac-d-structural.txt).
