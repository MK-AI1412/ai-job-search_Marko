---
name: debug
description: >
  Systematic debugging discipline: reproduce first, hypothesis-driven investigation, binary-search
  isolation, root-cause fixes with regression proof — never guess-and-patch. Triggers on: /debug,
  debug this, why is this failing, find the bug, not working, root cause
---

# Debug — Hypothesis-Driven Debugging

## The discipline

Debugging fails when it becomes pattern-matching: seeing a symptom, recalling a similar past bug,
and applying that fix without confirming the mechanism. Every rule here exists to force the loop
back to evidence. **A fix applied without understanding the mechanism is a coin flip that also
destroys the evidence.**

## The loop

### 1. Reproduce before touching anything
Get a failing case you can re-run on demand — a command, a test, a minimal input. If you cannot
reproduce it, that IS the investigation (logs, timing, environment diffs), not a license to guess.
Record the exact reproduction command; it becomes your regression test later.

### 2. Read the actual error
The full error, not the summary line: stack trace bottom-up, the *first* error in a cascade (later
ones are usually fallout), exact line numbers, exact values in the message. Half of all bugs are
solved by genuinely reading what the error already says.

### 3. State a falsifiable hypothesis — out loud, before acting
"I believe X causes this, and if I'm right, then Y must be observable." If you can't phrase the
"then Y" part, you don't have a hypothesis, you have a hunch — gather more evidence first.
One hypothesis at a time; changing three things and seeing the symptom vanish teaches you nothing.

### 4. Instrument, don't stare
Add targeted logging/prints at the boundary of your hypothesis: what are the actual values, which
branch actually runs, what order things actually happen in. Reading code tells you what *should*
happen; only instrumentation tells you what *does*. Remove all instrumentation before finishing.

### 5. Binary-search the search space
- **In space**: cut the pipeline at the midpoint — is the data already wrong there? Recurse into
  the bad half. Works on call chains, data pipelines, config layers, middleware stacks.
- **In time**: `git bisect` (or manual commit-range halving) when it used to work. "What changed?"
  beats "what's wrong?" — recent diffs, dependency bumps, env changes are the prime suspects.
- **In input**: shrink the failing input until removing anything more makes it pass. The minimal
  case usually names the bug.

### 6. Confirm the mechanism before fixing
You're done investigating when you can narrate the full causal chain: "input A reaches function B
in state C, so branch D runs and produces E." If any link is "somehow", keep investigating. The
test: your explanation predicts *other* behavior you can check — go check one.

### 7. Fix the cause, prove it, then look for siblings
- Fix the root cause, not the symptom. A `null`-check that silences a crash without explaining why
  the value was null is symptom-patching — say so explicitly if you do it deliberately as triage.
- Re-run the exact reproduction from step 1 — it must now pass. Run the surrounding test suite —
  nothing else may break. A fix you didn't watch pass is not a fix.
- Ask: can this same mistake exist elsewhere? Grep for the pattern; sibling bugs travel in packs.

## Traps to name and avoid

- **The coincidence trap**: symptom vanished after your change ≠ your change fixed it (caches,
  timing, rebuilds lie). Revert the fix and confirm the bug comes back if there's any doubt.
- **The clean-code assumption**: "this function is obviously correct so the bug must be elsewhere"
  — the bug is *always* in code someone was sure about. Verify, don't vouch.
- **Fix-cascade**: your fix creates a new error, which you fix, which creates another. Two levels
  deep = stop, revert everything, re-derive the mechanism — the original diagnosis was wrong.
- **Environment blindness**: works-here-fails-there means diff the environments (versions, env
  vars, locale, filesystem case, time zone) before diffing the code.
- **Sunk-cost tunneling**: 30+ minutes with no new evidence on one hypothesis = the hypothesis is
  wrong. Write down what you've eliminated, zoom out one level, pick a different angle.

## Reporting

State: the mechanism (one paragraph of causal chain), the fix, the proof (reproduction now passes,
suite green — with the actual output), and any siblings found or triage notes. If not fully fixed,
report exactly what was eliminated and the strongest remaining hypothesis — a well-documented
dead end is real progress the next session inherits.
