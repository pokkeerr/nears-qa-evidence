# Maestro nightly (NEARS-4276): BLOCKED

- reason: env file /private/tmp/claude-501/-Users-Apple-Projects-nears/fd1b9d8b-2d3b-43b6-8df4-c4b32ae6ea5a/scratchpad/qa4276/c1/does-not-exist.env is missing or unreadable
- ref: None @ None
- serial: None (AVD None), backend port None, clone `None`
- wall: 3 s

| flow | verdict | wrapper rc | JUnit | note |
|---|---|---|---|---|

## Self-check (AC3)


## Teardown


Known egress: api.copilot.mobile.dev (TLS, about 6 KB per maestro test; accepted, blocking it is NEARS-4277)

nothing is published automatically: screenshots are never scrubbed (maestro-pilot.md §9.6); check them, then run a row's publish line by hand:

