---
name: ship
description: >
  Code-change discipline from request to pushed commit: scope honestly, read before writing, match
  the codebase, verify by execution not inspection, report faithfully. Triggers on: /ship,
  implement this, build this feature, make this change, add support for, fix and push
---

# Ship — From Request to Verified Change

## The bar

A change is shipped when it is **verified by execution and honestly reported** — not when the code
looks right. Everything here serves that bar. The expensive failures in software are rarely typing
speed; they are building the wrong thing, breaking the thing next door, and declaring victory
early. Each phase below exists to kill one of those.

## Phase 1: Scope — build the thing that was asked

- Restate the request as acceptance criteria: 3–7 concrete, checkable statements of "done".
  If you can't, the request is ambiguous — resolve it (from the code, from conventions, or by
  asking ONE precise question) before writing code.
- Distinguish the request from your embellishments. No unrequested refactors, no speculative
  generality ("might need it later" = don't build it), no drive-by cleanups mixed into the diff —
  they bloat review and hide the actual change. Note improvement ideas for the report instead.
- Estimate blast radius up front: what calls this, what does this call, what shares this data?
  The grep for callers happens BEFORE the edit, not after the tests break.

## Phase 2: Recon — read before you write

- Find the closest existing analog to what you're building and study it: the codebase has already
  answered most style/structure/error-handling questions — your job is consistency, not
  originality. New code should read like the codebase wrote it.
- Locate: the conventions (naming, error handling, test patterns), the utilities that already
  exist (search before writing ANY helper — duplicating an existing util is the classic
  LLM-authored-code smell), and the tests covering the area you're touching.
- Run the existing tests for the area FIRST. A pre-existing failure discovered after your change
  looks like your fault and costs an hour of misdirected debugging.

## Phase 3: Implement — smallest correct change, in checkpoints

- Prefer the minimal diff that meets the acceptance criteria. Every touched line is review burden
  and regression surface; elegance that doubles the diff is not elegance.
- Work in verifiable increments: get one slice working end-to-end, verify, then extend — not
  five files of speculative edits followed by one big prayer of a test run.
- Handle the failure paths the codebase handles (look at the analog): empty input, not-found,
  permission denied, the error type callers expect. Swallowing errors to make tests pass is
  forbidden; if a case is deliberately unhandled, say so in the report.
- When stuck between two designs, pick the one that's easier to DELETE later. Most code is wrong
  the first time; reversibility beats theoretical optimality.

## Phase 4: Verify — execute, don't inspect

- "I read the code and it looks correct" is not verification. Run it: the test suite, AND the
  actual behavior end-to-end (call the endpoint, run the CLI, drive the flow) — tests verify what
  tests cover, which is never everything.
- Verify each acceptance criterion from Phase 1 explicitly, with evidence (command + output).
- Add/adjust tests for the new behavior — including the failure path you handled. A bugfix ships
  with the regression test that fails without the fix (run it both ways to prove it).
- Re-run the area's full test suite. Then check the blast radius from Phase 1: did the callers
  survive? Typecheck/lint if the project has them.
- If verification fails: fix and re-verify. Two consecutive fix-cascades deep = stop, revert,
  re-derive — the approach is wrong, not the details (see /debug).

## Phase 5: Ship — commit, push, report faithfully

- Commit with a message that says *what* (first line, imperative) and *why* (body) — the diff
  already shows the how. Unrelated changes go in separate commits.
- Push to the designated branch; never create a PR unless asked.
- Report against the acceptance criteria: each one pass/fail with its evidence. State plainly what
  was verified, what wasn't, and any deliberate scope cuts or known limitations. "Done" with a
  silent caveat is a lie with a delay on it — the caveat always surfaces, later and more
  expensively.

## Standing rules

- Never mark done what you didn't run. Never hide a red test in a green summary.
- Match surrounding code even where you'd personally choose differently — consistency outranks
  preference inside someone else's codebase.
- Comments only for what code cannot say (constraints, invariants, non-obvious whys) — never
  narration of the change itself.
- Secrets never in code, commits, or logs. Read a file before overwriting it. Destructive or
  irreversible actions get confirmed first.
- When the task turns out 3× bigger than the request implied (schema migration, API break),
  surface the fork in the road — don't silently commit the user to a week of consequences.
