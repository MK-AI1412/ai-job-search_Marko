---
name: test-strategy
description: >
  What to test, at which level, and how to keep the suite trustworthy: behavior-driven coverage,
  the boundary catalog, deterministic fast suites, zero-tolerance for flakiness. Triggers on:
  /test-strategy, write tests, test coverage, what should I test, unit vs integration, flaky test,
  test suite, TDD
---

# Test Strategy — A Suite You Can Actually Trust

## What tests are for

A test suite's product is **permission to change code confidently**. Every property follows from
that: tests must fail when behavior breaks (or they're theater), must NOT fail when behavior
holds (or they're friction that trains people to ignore red), and must run fast enough that
people actually run them. Coverage percentage measures none of these — 100% line coverage with
assertion-free tests is worth exactly zero permission.

## Test behavior, not implementation

The test states a contract: *given this input/state, this observable outcome*. It should survive
any refactor that preserves the contract. The reliable smell of implementation-testing: heavy
mock-verification ("assert helper X was called with Y") — that pins *how* instead of *what*,
breaks on every refactor, and passes even when the actual behavior is wrong. Mock at system
boundaries you don't own (network, clock, external APIs); use real code inside your own module
graph unless there's a concrete speed/isolation reason.

## Choose the level deliberately

- **Unit** — pure-ish logic with many cases: parsing, calculation, branching rules. Milliseconds
  each; this is where the case-explosion lives (the boundary catalog below).
- **Integration** — where units meet reality: real database, real filesystem, real serialization.
  This is where the *actual* bugs live (schema mismatches, transactions, encoding) — a suite of
  1000 units and 0 integrations tests a fiction.
- **End-to-end** — a handful of critical user journeys, no more. E2E is slow and fragile by
  nature; every flow you add is a tax on every future run. The pyramid isn't dogma, it's
  economics: push each check to the cheapest level that can catch its failure.
- The best return-on-test in most codebases: integration tests of the module's public API —
  refactor-proof like E2E, nearly as fast as units.

## The boundary catalog — where bugs actually live

For each behavior, walk this list and test the ones that apply (bugs cluster at boundaries,
almost never in the middle of the happy path):
- Empty / zero / null / missing vs present-but-blank
- One / exactly-at-limit / one-past-limit / enormous
- Negative, non-ASCII & emoji, whitespace-padded, absurdly long strings
- Duplicates, already-exists, concurrent same-action (the double-click, the retry)
- The failure paths: dependency down, timeout, malformed response, permission denied —
  **error-path tests are the least-written and highest-value tests in real systems**
- Time: DST transitions, month/year boundaries, clock skew, "exactly at expiry"

Also: one test per bug ever fixed (write it failing first, watch it fail, then fix — a
regression test you never saw red proves nothing).

## Keep the suite trustworthy

- **Deterministic or deleted**: a flaky test is worse than no test — it costs CI time AND trains
  everyone to rerun-until-green, which is how real failures ship. Flakiness root causes are
  nearly always: real time (`sleep`, wall-clock), shared state between tests, unseeded
  randomness, network, or order dependence. Fix the cause (inject the clock, isolate the state,
  seed the RNG) — never bandage with retries or longer sleeps.
- **Independent tests**: any test runnable alone and in any order. Test A setting up state for
  test B is a suite that can never be parallelized or trusted.
- **One behavior per test, named as the contract**: `rejects_expired_token`, not `test_auth_3`.
  When it fails at 2am, the name should be the diagnosis.
- **Assert the outcome, precisely**: "no exception thrown" is not an assertion. But don't
  over-assert incidentals (exact message strings, dict ordering) that make true-negative
  failures on harmless changes.
- **Failure output is UX**: a good test failure shows expected vs actual and the scenario —
  the reader is future-you, annoyed, mid-incident.

## Writing tests for existing untested code

Characterization first: write tests that pin *current* behavior (even weird behavior — pin it
and flag it), get them green, THEN change code. Tests written after a change only ever confirm
the change; tests written before it protect everything else. If the code can't be tested without
heroics, that's the design telling you where its seams should be — extract the pure logic from
the I/O and test the logic directly.

## Traps

- **The mirror test**: reimplementing the production logic in the test to compute the expected
  value — now both are wrong together. Expected values in tests are literals, derived by hand.
- **Coverage worship**: chasing the number produces assertion-free tests of getters. Coverage is
  a *gap-finding* tool (what's untested?), never a target.
- **Snapshot everything**: giant auto-generated snapshots that everyone approves without reading
  on every diff. A snapshot nobody reads is a test nobody has.
- **Testing the framework**: asserting that the ORM saves or the router routes. Test YOUR
  contract; the framework has its own suite.
- **The slow-suite death spiral**: suite too slow → people skip it → breaks accumulate → suite
  distrusted → deleted. Speed is not a nice-to-have; it is the suite's survival condition.
