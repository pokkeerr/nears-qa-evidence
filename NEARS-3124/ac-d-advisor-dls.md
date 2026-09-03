# AC (d) spot-check — advisor-dls.md (178 lines, H2 set = template) — 3 rules + 1 catalog note

## Rule 1 — Design authority, three tiers
**Brief (## Rules and standards, "Design authority — three tiers", items 1-3):**
> 1. `packages/nears_dls/lib/tokens/nears_tokens.dart` is ground truth and wins any disagreement, without exception.
> 2. Stitch project `14797906318983803103` is visual authority synced to code — authoritative for composition and screen intent, NEVER the arbiter of a hex value or a size.
> 3. Docs (`docs/design/*`, `DESGIN.md`) are descriptive; when one disagrees with the token file, the doc is the bug.

**Source docs/platform/design-system-nears.md:5-8:**
> **Design authority — three tiers (NEARS-1420):**
> 1. **Ground truth — `packages/nears_dls/lib/tokens/nears_tokens.dart`.** Every color, size, radius, shadow and motion value is defined there. It wins any disagreement, without exception.
> 2. **Visual authority, synced to code — Stitch project `14797906318983803103`.** Authoritative for composition and screen intent; **never** the arbiter of a hex or a size …
> 3. **Descriptive — this doc, `docs/design/*`, `DESGIN.md`, …** When one disagrees with the token file, the token file is right and the doc is the bug.

Verdict: traceable — condensed, every operative phrase kept.

## Rule 2 — token values (brief says "the file wins", so checked against the FILE)
**Brief (## Rules and standards, "Tokens", bullet 3):** space1 4 · space2 8 · space3 12 · space4 16 · space5 20 · space6 24 · radiusXs 6 · brSm 8 · brMd 12 · brLg 16 · brXl 24 · ctaHeight 52 · appBarHeight 60 · bottomNavHeight 64 · tapMin 44 · tapTarget48 · durFast 120ms · durBase 200ms · durModerate 300ms · durSlow 320ms · pressScale 0.97

**Source packages/nears_dls/lib/tokens/nears_tokens.dart (grep):**
- :173-178 space1=4, space2=8, space3=12, space4=16, space5=20, space6=24
- :197 radiusXs=6 · radius consts: 198:  static const double radiusSm = 8; // buttons, inputs (utility feel);199:  static const double radiusMd = 12; // CTAs, item images;200:  static const double radiusLg = 16; // surface cards (approachable);201:  static const double radiusXl = 24; // hero image card;202:  static const double radiusSheet =;204:  static const double radiusPill = 9999; // badges, chips, search field;
- :206-209 brSm/brMd/brLg/brXl = BorderRadius.circular(radiusSm/Md/Lg/Xl)
- :224 ctaHeight=52 · :226 appBarHeight=60 · :227 bottomNavHeight=64 · :228 tapMin=44 · :233 tapTarget48=48
- :315-318 durFast 120 · durBase 200 · durModerate 300 · durSlow 320 · :321 pressScale=0.97

Verdict: traceable — every value the brief states matches the token file.

## Rule 3 — Known trap `dls-semantics-missing-container-boundary`
**Brief (## Known traps, bullet 1):**
> **dls-semantics-missing-container-boundary** (high, NEARS-1130) — an interactive `Semantics(button: true)` wrapper in a DLS shape sets `container: true` or a merging ancestor absorbs it; any mechanism that isolates the label from the child tree (`excludeSemantics: true` OR `explicitChildNodes: true`) ALSO strips the descendant's tap action, so the wrapper re-supplies `onTap:` (and `enabled:`). Verify behaviourally — `hasAction(SemanticsAction.tap)` or a `performAction` round-trip — label-and-isButton assertions pass straight through this defect. Precedents NEARS-1101, 1130, 1478.

**Source docs/workflow/review-lessons.json:** status=active · severity=high · first_seen=NEARS-1130
> rule: An interactive Semantics(button:true, ...) wrapper in a Nears DLS shape must set container:true … otherwise a merging ancestor … absorbs the button node … any mechanism that isolates the wrapper's label from its child tree — excludeSemantics:true OR explicitChildNodes:true — ALSO strips the descendant's a11y tap action … So the wrapper MUST re-supply onTap: itself (and, where the shape has a disabled state, enabled:) … VERIFY BEHAVIORALLY … assert hasAction(SemanticsAction.tap) or do a performAction/tester.semantics.tap round-trip — label-and-isButton-flag assertions pass straight through this defect. Precedent: NEARS-1101 …, NEARS-1130 …, NEARS-1478 ….

Verdict: traceable — condensed with the source's own terms; severity, origin and precedents match.

## Catalog note — `NButton.notes.tertiary_on_navy`
Brief (Doc-sourced gotchas, bullet 3) vs packages/nears_dls/catalog.yaml:968: "tertiary resolves its label from the RESOLVED themeMode (p.isDark → textOnNavy), never Theme.of(context).brightness: a navy hero panel inside a light theme reports `light`" — verbatim in the catalog. Traceable.

Never-do list: all four mandatory items present (see ac-d-structural.txt).
