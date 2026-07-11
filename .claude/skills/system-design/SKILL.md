---
name: system-design
description: >
  Architecture and design decisions before code: constraints first, genuinely different options,
  explicit trade-off evaluation, reversibility as tiebreaker, ADR-style decision records.
  Triggers on: /system-design, design this system, architecture, how should I structure,
  which approach, design decision, tradeoffs
---

# System Design — Decide Before You Build

## The failure this prevents

Most bad systems were built *well* — the execution was fine; the framing was wrong. Design
discipline exists to catch the wrong framing while it still costs a conversation instead of a
rewrite. The counterpart trap is over-design: architecture astronautics for a problem a 50-line
script solves. Both are killed by the same move: **size the decision first, then spend
proportionally.**

## Step 0: Size the decision

- **Reversible in under a day** (naming, internal structure, a library behind an interface):
  decide fast with defaults and conventions, note it in one line, move on. No options matrix.
- **Expensive to reverse** (data schema, public API shape, sync-vs-async, service boundaries,
  build-vs-buy, storage choice): run the full method below. These are the decisions that outlive
  everyone's memory of why they were made.

## Step 1: Constraints before solutions

Write down, before proposing anything:
- **Hard requirements** — what must be true (functional, scale, latency, budget, compliance,
  deadline). Attach numbers: "fast" is not a requirement; "p95 under 200ms at 100 rps" is.
- **Actual scale, not aspirational scale** — design for 10× current load, not 1000×. The
  1000×-ready system costs you every single day while you wait for growth that may never come.
- **What's already true** — existing stack, team skills, operational maturity. A technically
  superior choice nobody can operate at 3am is inferior.
- **The non-goals** — explicitly listing what this does NOT need to handle kills half of all
  scope creep at birth.

If the requester can't supply the load-bearing constraints, that's the first deliverable:
the 2–3 questions whose answers change the design.

## Step 2: Generate genuinely different options

2–3 options that differ in *kind*, not in detail — different data flow, different consistency
model, different buy/build split. One real option plus two strawmen is theater; the test is that
each option would be someone's honest first choice under slightly different constraints. Always
include the boring option (the simplest thing using what already exists) — it wins more often
than it should, and when it loses you'll know precisely why, which becomes the justification.
For high-stakes calls, develop options as independent subagents blind to each other
(see /orchestrate's judge panel) — independence buys real diversity.

## Step 3: Evaluate against the constraints, not against vibes

- Score each option against the Step-1 constraints explicitly. A comparison table is fine, but
  the decision lives in prose: which constraint dominated and why.
- Name each option's **failure story**: how does it break at 10× load, under partial failure,
  when requirements shift in the most likely direction? An option whose failure story you can't
  tell is under-analyzed, not safe.
- Surface the **second-order costs** the matrix hides: operational burden, migration path,
  hiring/onboarding, vendor lock-in, testing difficulty.
- **Tiebreaker: reversibility.** When options score close, pick the one that's cheapest to
  *change your mind about* later. You are designing under uncertainty; the option that preserves
  the ability to be wrong is worth a sizeable performance handicap.

## Step 4: Record the decision (ADR)

One short file per expensive decision (`docs/decisions/NNN-<slug>.md`):
**Context** (the constraints that mattered) → **Options considered** (one line each, including
the rejected ones and the killing reason) → **Decision** → **Consequences** (what gets harder,
what we're betting on, what would trigger revisiting). Ten minutes of writing; the alternative
is relitigating the decision every six months from memory, or worse, silently reversing it.

## Standing rules

- Interfaces before internals: agree on the contract (API shape, schema, message format) first —
  internals can churn freely behind a stable contract; contract churn breaks everyone.
- Design the failure paths with the same care as the happy path: what happens on timeout,
  partial write, duplicate delivery, poison message? "It won't happen" is not a design.
- Every layer of indirection must name the concrete flexibility it buys. "Might need it later"
  buys nothing and costs comprehension forever (YAGNI applies to architecture doubly).
- A design isn't done when nothing more can be added; it's done when the remaining simplification
  would violate a Step-1 constraint. Complexity must always be able to point at its requirement.
