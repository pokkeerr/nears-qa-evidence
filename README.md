# nears-qa-evidence

QA evidence for the **Nears** platform, one folder per Jira issue. Each folder's README is a rendered thumbnail gallery; click a thumbnail for full resolution. The matching NEARS-### Jira issue links here.

> Public repo so galleries render on GitHub. **Scrub policy enforced before every push** — no live secrets, no real PII. See below.

## Tickets

- [**NEARS-14**](NEARS-14#readme) — 0 shot(s)
- [**NEARS-30**](NEARS-30#readme) — 0 shot(s)
- [**NEARS-72**](NEARS-72#readme) — 19 shot(s)
- [**NEARS-75**](NEARS-75#readme) — 13 shot(s)
- [**NEARS-223**](NEARS-223#readme) — 2 shot(s)
- [**NEARS-226**](NEARS-226#readme) — 7 shot(s)
- [**NEARS-227**](NEARS-227#readme) — 8 shot(s)
- [**NEARS-238**](NEARS-238#readme) — 7 shot(s)
- [**NEARS-239**](NEARS-239#readme) — 1 shot(s)
- [**NEARS-240**](NEARS-240#readme) — 2 shot(s)
- [**NEARS-241**](NEARS-241#readme) — 3 shot(s)
- [**NEARS-243**](NEARS-243#readme) — 2 shot(s)
- [**NEARS-249**](NEARS-249#readme) — 3 shot(s)
- [**NEARS-250**](NEARS-250#readme) — 1 shot(s)
- [**NEARS-253**](NEARS-253#readme) — 2 shot(s)
- [**NEARS-257**](NEARS-257#readme) — 28 shot(s)
- [**NEARS-258**](NEARS-258#readme) — 4 shot(s)
- [**NEARS-259**](NEARS-259#readme) — 0 shot(s)
- [**NEARS-260**](NEARS-260#readme) — 3 shot(s)
- [**NEARS-261-252**](NEARS-261-252#readme) — 12 shot(s)
- [**NEARS-262**](NEARS-262#readme) — 2 shot(s)
- [**NEARS-265-266**](NEARS-265-266#readme) — 3 shot(s)
- [**NEARS-290**](NEARS-290#readme) — 6 shot(s)
- [**NEARS-291**](NEARS-291#readme) — 11 shot(s)
- [**NEARS-296**](NEARS-296#readme) — 1 shot(s)
- [**NEARS-298-301**](NEARS-298-301#readme) — 10 shot(s)
- [**NEARS-302**](NEARS-302#readme) — 9 shot(s)

## Scrub policy (mandatory)
1. **No live secrets** — no API keys (`AIzaSy…`), JWTs, bearer/access/refresh/client tokens, passwords, `.env` values. Text/log/json dumps are scanned before commit.
2. **No real PII** — only seeded *demo* accounts, redacted to `<demo-…>` in text.
3. **No internal page-source dumps** — admin HTML var-dumps excluded (see `.gitignore`).
4. Screenshots show app UI only — never a token/secret on screen.
