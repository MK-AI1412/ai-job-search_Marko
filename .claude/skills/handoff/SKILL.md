---
name: handoff
description: >
  Session continuity: write a compact state file before ending a session so the next session (or
  another agent) resumes in minutes without re-exploring — and load it on resume. Triggers on:
  /handoff, handoff, save state, wrapping up, continue tomorrow, resume, pick up where
---

# Handoff — Session State Transfer

## Why

Context dies with the session; the next session pays full price to rediscover everything — which
files matter, what was decided and why, which approaches already failed. A handoff file transfers
that state for a few hundred tokens. **The rediscovery tax is the single largest hidden cost of
multi-session work, and the "why" is what's lost first** — decisions get relitigated, dead ends
get re-entered, and gotchas get re-learned the hard way.

## Two modes

- **`/handoff`** (or session ending): write/update the handoff file, commit it if the repo is the
  workspace, confirm to the user in one line.
- **`/handoff load`** (or a session that starts with a handoff file present): read it FIRST, before
  any exploration, state the resumption plan in 2–3 lines, then continue the work — don't re-derive
  what the file already settles.

## The file

Location: `HANDOFF.md` at repo root (or `docs/HANDOFF.md` if the root is crowded). One file,
overwritten each time — it describes *current* state, it is not a log. Keep it under ~150 lines;
a handoff nobody reads is worse than none. Structure:

```markdown
# Handoff — <task name>            <!-- updated: <date>, branch: <branch> -->

## Goal
<1–3 sentences: what the overall effort is and what "done" looks like.>

## State: where things stand
- DONE: <shipped/working, with the proof — "tests pass", "PR #12 merged">
- IN FLIGHT: <started but unfinished, and exactly where it stops — file:line, failing test name>
- NOT STARTED: <known remaining work, in intended order>

## Key decisions (and WHY)
- <decision>: <the reason — this is the part that prevents relitigating>
- ...

## Dead ends — do not retry
- <approach tried>: <why it failed — the evidence, not just "didn't work">

## Gotchas discovered
- <non-obvious facts that cost time: "the test suite needs X env var",
  "file Y is generated, edit the template at Z instead", "CI redlines on W">

## Next steps (concrete, in order)
1. <specific action with file paths — executable by someone with zero context beyond this file>
2. ...

## Map (only what matters)
- <file/dir>: <one-line role in THIS task — not a full repo tour>
```

## Writing rules

- **Decisions need their why.** "Using approach B" is useless; "Using B because A breaks under
  concurrent writes (see failed test in commit abc123)" prevents a repeated week.
- **Dead ends are first-class.** Documenting what *didn't* work and why is often worth more than
  documenting what did.
- **Next steps must be executable cold**: paths, commands, names — "continue the refactor" fails
  the test; "extract the retry logic from `api/client.py:140-180` into `api/retry.py`, mirroring
  how `api/auth.py` does it" passes.
- **Evidence over optimism**: "DONE" requires the proof next to it. Anything unverified goes in
  IN FLIGHT with a note saying so.
- **Prune on every write**: resolved gotchas, completed steps, superseded decisions get deleted.
  The file describes now.
- If session context is nearly exhausted, write the handoff BEFORE it runs out — a handoff written
  from a compacted summary loses exactly the details that matter.

## Beyond files

- Commit the handoff with the work when the repo is the natural home (remote/ephemeral sessions:
  always — uncommitted files die with the container).
- For multi-agent work, the same discipline applies to subagent briefs and results: state, why,
  dead ends, next steps — a handoff is just a brief addressed to your future self.
