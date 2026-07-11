---
name: refactor-legacy
description: >
  Changing code you're afraid of, safely: characterization tests first, seams before surgery,
  strangler-fig migrations, behavior-preserving steps you can verify and revert individually.
  Triggers on: /refactor-legacy, legacy code, refactor this mess, technical debt, untested code,
  scared to touch, modernize, spaghetti, big rewrite
---

# Refactor Legacy — Changing Code You're Afraid Of

## The two rules everything follows from

1. **Legacy code's defining property isn't age or ugliness — it's absence of tests.** Without
   tests, every change is a bet with unknown odds. So the first move is never restructuring;
   it's building the safety harness that makes restructuring boring.
2. **Never mix behavior-preserving changes with behavior-changing ones in the same step.**
   A refactor commit must be provably a no-op (tests identical before/after); a behavior change
   must be visible and deliberate. Blend them and you can verify neither — when something
   breaks, you won't know which intent failed.

## Respect what's there (before changing anything)

That horrifying conditional encodes ten years of production incidents you weren't there for —
**ugly-but-battle-tested beats clean-but-unproven**, because the weird branches ARE the
requirements nobody wrote down. Before refactoring a region: `git log` it (the whys live in
commit messages), find what calls it, and treat every "this can't possibly be needed" as a
hypothesis to verify, not a deletion candidate. Chesterton's fence, operationalized: you may
remove the fence only after you can state why it was built.

## Step 1: Characterization tests — pin what IS

Write tests that capture *current* behavior — including current bugs and weirdness (pin them,
flag them for later triage; fixing them now violates rule 2). Technique: write a test with a
guessed expectation, run it, let the code tell you the real answer, make that the assertion.
Cover the inputs that matter: the happy path, the boundary catalog, and — critically — a few
real production-shaped inputs if you can get them. Golden-master testing (snapshot outputs for
a corpus of recorded inputs) is legitimate here and often the fastest harness for gnarly code.

You now have a tripwire: any refactor step that flips a characterization test just changed
behavior — revert, understand, retry smaller.

## Step 2: Create seams before surgery

A seam is a place where you can alter behavior without editing the code in place — and legacy
code's problem is usually that everything is fused (I/O inside logic inside globals). Minimal,
mechanical seam-making moves (each trivially behavior-preserving):
- Extract the tangled block into a named function — even with an ugly 8-argument signature;
  honesty first, beauty later.
- Split calculation from effect: pure logic goes into functions that take data and return data;
  the I/O crust stays thin at the edges. Pure parts become instantly testable.
- Introduce a parameter for a hard-wired dependency (the clock, the DB handle, the config).
Each seam expands what you can test, which expands what you can safely change — a ratchet.

## Step 3: Refactor in reversible steps

- Steps so small each is individually verifiable and individually revertible: rename; extract;
  inline; move; then re-run the harness. Commit at every green.
- Prefer mechanical/tool-driven transformations (IDE rename, automated codemods) over hand
  editing — mechanical steps have mechanical correctness.
- **The strangler fig for big migrations**: build the new path alongside the old, route traffic
  over incrementally (by feature, by caller, by percentage), keep the old path as the fallback
  until the new one has survived real load, then delete. At every intermediate moment the system
  works — there is no big-bang cutover night, no long-lived divergent branch.
- The big-bang rewrite is almost always the wrong call and always the seductive one: it freezes
  features for months, re-discovers the undocumented requirements one outage at a time, and the
  legacy system evolves under you while you chase it. Demand overwhelming evidence (framework
  EOL, security floor, cost cliff) before choosing it — "the code is embarrassing" is not evidence.

## Step 4: Leave it better, bounded

- Scope-box the campaign: refactor what the current task touches ("the boy-scout rule with a
  fence"), not everything sight-lines reach. Sprawling refactors that touch 80 files never land
  and rot in review.
- After behavior is pinned and structure is clean, THEN fix the pinned bugs — as explicit,
  separate, visible changes with their own tests (rule 2, other direction).
- Record what you learned in the code's vicinity (a README, an ADR, updated names): the next
  person's archaeology is your documentation's failure.

## Traps

- **"While I'm in here"**: the refactor that metastasizes into six unrelated cleanups in one
  diff. Every extra touched file dilutes review attention on the risky part.
- **Improving the code, breaking the callers**: legacy code's callers depend on its quirks
  (ordering, mutation, error types, even timing). The blast-radius grep comes before the change.
- **Deleting "dead" code by inspection**: in dynamic languages and reflective frameworks, the
  grep lies. Add a tripwire (log/metric on entry) and let production prove it dead first.
- **Refactoring without a customer**: restructuring for its own sake, justified by taste. The
  best refactors are pulled by a concrete need — the feature that's hard to add, the bug class
  that keeps recurring — because that need defines "better" objectively.
