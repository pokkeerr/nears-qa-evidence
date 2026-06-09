# nears-qa-evidence

QA evidence (screenshots, logs, capture dumps) for the **Nears** platform, organized by Jira issue.
This repo exists so evidence is **durably linkable from Jira/Confluence without consuming Jira's
attachment storage** — Confluence embeds the images by raw URL, and the NEARS ticket links here.

> Companion to the main `nears` code repo. Each folder maps to a Jira issue: `NEARS-<id>/`.

## Why this repo is public
Public so that `raw.githubusercontent.com` image URLs **render inline in Confluence** (external
images render only from publicly reachable URLs). Because it is public, the scrub policy below is
**mandatory** — nothing here may contain a real secret or real-customer PII.

## Scrub policy (enforced before every push)
1. **No live secrets** — no API keys (`AIzaSy…`), JWTs (`eyJ…`), bearer/access/refresh tokens,
   client tokens, passwords, or `.env` values. Logcat/console dumps are scanned before commit.
2. **No real PII** — only seeded *demo* accounts are acceptable, and even those are redacted to
   `<demo-…>` placeholders in text summaries.
3. **No internal page-source dumps** — admin-dashboard HTML var-dumps (`*.html` Symfony dumps) are
   excluded (see `.gitignore`); they are kept local-only in the code repo.
4. Screenshots must show app UI only — never a token/secret on screen.

A push that would violate the above is blocked; sanitize or exclude the file instead.

## How evidence is linked to a ticket
```
GitHub (this repo)  →  Confluence "QA Evidence — NEARS-<id>" page (embeds raw URLs inline)
                    →  comment on NEARS-<id> with the Confluence/GitHub links
```

Raw image URL form:
`https://raw.githubusercontent.com/pokkeerr/nears-qa-evidence/main/NEARS-<id>/<file>.png`
