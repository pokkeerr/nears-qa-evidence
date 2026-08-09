# NEARS-1741 — freshness bracketing, reconstructed

**This run used the OLD cadence (probe at boot + 2 checkpoints), not the per-observation
cadence mandated mid-run after the NEARS-1640 / NEARS-1585 disproof.** Recorded here so the
bracketing is checkable by someone who was not present, and so the gap is explicit rather
than implied.

Device emulator-5558. App `com.izzes.nears`, installed path
`/data/app/~~fJd5nVqkMQh2KnTA1Oaymw==/com.izzes.nears-SpAVLmz_GBdXStrDNgjlRQ==/base.apk`
(path re-resolved with `pm path` at each md5 read, never cached).

`EXACT` = read from a logcat line or a file mtime. `APPROX` = I did not timestamp the probe
runs; the time is bounded by the surrounding recorded events.

| time | kind | what | result |
|---|---|---|---|
| ~18:12 | APPROX | install + md5 of installed artifact | `34fa2a7ef282439e1fe18abd90a9ccd8` |
| ~18:13 | APPROX | **symbol probe #1** (`getVM` reported `"pid":13970`) | PASS, neg-control absent |
| 18:14:47 | EXACT | obs `ac1-01-forgot-password-clean.png` | — |
| 18:14:53 | EXACT | logcat `[FAIL]` ×2, **pid 13970** | AC1 fault |
| 18:15:39 | EXACT | obs `ac1-02-error-panel.png` | — |
| 18:16:05 | EXACT | obs `ac1-03-panel-persists-9s.png` | — |
| 18:16:39 | EXACT | logcat `[FAIL]` ×2, **pid 13970** | AC1 retry-loop fault |
| ~18:16 | APPROX | md5 re-read (`md5-before`) | `34fa2a7e…` unchanged |
| 18:16:52 | EXACT | obs `ac6-01-edit-clears-panel.png` | — |
| 18:17:51 | EXACT | obs `ac1-04-recovered-verification-screen.png` | — |
| ~18:17:51 | APPROX | md5 re-read (`md5-after`) + **symbol probe #2** | `34fa2a7e…`; PASS, neg-control absent |
| 18:18:42 | EXACT | obs `ac3-01-cta-loading-spinner.png` | — |
| 18:20:20 | EXACT | logcat `[FAIL]` ×2, **pid 13970** | AC6 invalid-phone |
| 18:20:37 | EXACT | obs `ac6-02-empty-field-inline-error.png` | — |
| 18:20:53 | EXACT | obs `ac6-03-invalid-phone-toast.png` | — |
| 18:26:22 | EXACT | logcat `[FAIL]` ×2, **pid 13970** | AC5 Arabic RTL fault |
| 18:26:37 | EXACT | obs `ac5-01-rtl-arabic-clean.png` | — |
| 18:27:01 | EXACT | obs `ac5-02-rtl-arabic-error-panel.png` | — |
| 18:27:50 | EXACT | logcat `[FAIL]` ×2, **pid 13970** | desktop-branch submit failure |
| 18:28:19 | EXACT | obs `ac4-01-desktop-1400dp-ndivider-or-row.png` | — |
| 18:28:24 | EXACT | obs `ac4-02-desktop-snackbar-on-failure.png` | — |
| ~18:29 | APPROX | md5 re-read (`md5-final`) + **symbol probe #3** | `34fa2a7e…`; PASS, neg-control absent |

## What was and was not bracketed

**Not bracketed per-observation.** Only two AC observations sit adjacent to a probe
(`ac1-04` at probe #2, `ac4-02` at probe #3). The other ten sit inside a probe-to-probe
window. The widest such window is **probe #2 (~18:17:51) → probe #3 (~18:29)**, ~11 minutes
containing 7 observations — materially the same exposure as the 12-minute NEARS-1585 swap.
Under the new rule that is a real gap, and it is not closed by re-running the probe now.

## The continuity evidence that does cover the window

A reinstall of `com.izzes.nears` force-stops the running process, so a swapped build cannot
keep the old pid, and it would also have torn down the `flutter run` attach and the Dart VM
service.

- **App pid `13970` is constant across every logcat sample from 18:14:53 to 18:27:50** — the
  first AC1 observation through the desktop-branch observation. Probe #1 independently
  recorded `"pid":13970` via `getVM`.
- The **Dart VM service stayed up on the same port (`127.0.0.1:64938`) for the whole run**;
  probe #3 connected to it after the last observation.
- The **installed-artifact md5 was `34fa2a7e…` at all four reads**, with the path re-resolved
  each time.

So the chain is: probe #1 proves build X is running → process identity unbroken through the
drive window → probe #3 proves build X is still running. That is continuous rather than
point-in-time, and it is what actually rules out a swap here. It is **not** a substitute for
per-observation probing: it rules out a *reinstall during the window*, whereas the probe is
what identifies *which build* is running. Both edges of the chain are probes.

**Residual, stated plainly:** the setup/navigation before 18:14:47 and the post-run regression
sweep after ~18:29 are outside the pid-*sampled* window. Neither contains an AC observation.

---

## Correction (2026-08-09, post-run): the continuity record is CONTINUOUS, not sampled

My first write-up of this rested on 5 logcat instants with continuity *inferred* between them.
That understated it. The `flutter run` log is a continuous record of the same process:

- **`13970` is the ONLY distinct pid in the entire 1387-line run log** (`grep -ao "I/flutter
  ([0-9 ]*)" | sort -u` → one result), first line to last.
- **`Lost connection to device.` occurs exactly once, at line 1387** — the final line, my
  teardown. A mid-run process death would have printed it earlier.

So process identity is unbroken by a continuous record, not by interpolation between samples.

**Pid reuse is ruled out, not merely improbable.** A live pid cannot be reused, and this process
was alive continuously (no `Lost connection` until teardown). This does not need a
"negligible" hedge.

## Residuals named and rated

**1. In-process code change via the live VM service (hot reload) — the one path pid continuity
does NOT close.** A hot reload changes running code without touching the pid, and the
`flutter run` attach was up on `127.0.0.1:64938` for the whole window. Rated **very low, with
direct evidence rather than assertion**:

- **Zero reload/restart events in the run log.** `grep -c "Reloaded .* librar\|Restarted
  application\|Performing hot reload\|Performing hot restart"` → **0**. Negative control: the
  same pattern matches a synthetic `Reloaded 1 of 900 libraries in 300ms` line → 1, so the
  pattern works and the 0 is real. (Two earlier hits for a looser pattern were the startup key
  legend — `r Hot reload.` / `R Hot restart.` — not events.)
- **A reload could only have loaded identical source.** `git status --porcelain` over
  `*.dart`, `UserApp/`, `packages/` in the worktree is **empty** — no product-code edit ever
  landed there, before, during, or after the run.
- The VM service is host-local behind a random auth token (`3-wnuqXgq-s=`); I held the device
  lock; another worktree's `flutter run` targets its own device and its own port.

**2. Unbracketed edges.** Setup/navigation before 18:14:47 and the regression sweep after
~18:29. Neither contains an AC observation.

**Still true and not softened:** none of this is per-observation probing. The chain rules out
*reinstall* (pid) and *in-process replacement* (reload evidence); it is the two probes at the
edges that identify *which build* was running.
