---
name: performance-tuning
description: >
  Measurement-driven performance work: profile before touching code, find the actual bottleneck,
  fix the biggest cost first, prove the win with before/after numbers under realistic load.
  Triggers on: /performance-tuning, too slow, optimize performance, speed up, latency, memory
  usage, profiling, bottleneck, high CPU
---

# Performance Tuning — Measure, Don't Guess

## The iron law

**No optimization without a profile; no "fixed" without a before/after measurement.** Intuition
about where time goes is wrong so reliably that acting on it has negative expected value — the
elegant-looking hot loop is cold, the innocent-looking logging call is 40% of runtime. Every
hour spent optimizing an unprofiled hunch is an hour spent making code more complex for a
speedup you cannot demonstrate.

## Step 1: Define "fast enough" before starting

A target, in numbers, tied to the user: "p95 page load under 1s", "batch completes inside the
4-hour window", "under 512MB so it fits the container". Without a stop condition, optimization
never ends — and past the target, every further change trades maintainability for speed nobody
perceives. Also fix WHAT you're optimizing: latency, throughput, memory, and p95-vs-mean are
different problems with different (often opposing) fixes.

## Step 2: Measure under realistic conditions

- Profile the real workload or a faithful replica — production-shaped data sizes, concurrency,
  and cache states. The empty-database benchmark is how "it was fast in dev" happens.
- Get the baseline number FIRST and save the exact command that produced it — this is the
  denominator of every claim you'll make later.
- Beware measurement traps: warm-up/JIT effects (discard first runs), caching between runs
  (a second run 100× faster usually means you measured the cache), noisy neighbors (run multiple
  iterations, report the distribution, not one lucky run).

## Step 3: Find the actual bottleneck

- Profile → sort by inclusive cost → follow the biggest number. The bottleneck is a *measurement
  result*, never a code-reading conclusion.
- Distinguish the four resource walls — CPU-bound, I/O-bound, memory-bound, lock/contention-bound
  — because the fixes don't transfer: parallelizing an I/O-bound task changes nothing;
  batching helps I/O and hurts latency.
- **Count the queries/calls, not just the time**: N+1 database queries, a network call inside a
  loop, re-reading a file per item — the most common real-world bottleneck is *quantity* of
  cheap operations, invisible in per-call timings.
- Amdahl's law as a triage filter: a component taking 10% of total time caps your best possible
  win at 10%. Don't start anywhere but the top of the sorted profile.

## Step 4: Fix in the order of leverage

Cheapest-to-safest ordering, try each level before descending:
1. **Do it less**: cache it, dedupe it, skip it when the result is unused, exit early.
   The fastest operation is the one that doesn't run.
2. **Do it in bulk**: batch the N calls into one (queries, writes, network round-trips).
3. **Do it with a better algorithm/structure**: the O(n²) hiding in `list.contains` inside a
   loop; a dict lookup replacing a linear scan. Algorithmic wins dwarf micro-tuning.
4. **Do it concurrently**: parallelize only what's truly independent — and only after 1–3,
   because parallelizing waste just wastes faster and adds bug classes.
5. **Do it in a faster medium** (rewrite, native extension, different storage): last resort,
   highest maintenance cost — demands the profile prove nothing above suffices.

One change at a time, re-measure after each — two simultaneous "optimizations" that net +5%
may hide one at +30% and one at −25%.

## Step 5: Prove it and guard it

- Report before → after with the same command, same conditions: "p95 340ms → 95ms, N=1000 runs".
  A speedup without numbers is a mood.
- Re-run the correctness tests — the classic optimization bug is being fast and wrong (dropped
  edge case, stale cache, race introduced by step-4.4).
- State the trade-offs taken: memory spent for speed, staleness window from caching, complexity
  added. If the win was under ~10%, say so and recommend reverting — small wins rarely pay
  their complexity rent.
- For load-bearing paths, leave a benchmark or perf test behind so the regression is caught by
  CI, not by users.

## Traps

- **Optimizing the benchmark, not the system**: micro-benchmark wins that vanish end-to-end
  because the real cost was elsewhere. Always confirm the win at the system level.
- **Cache as a reflex**: a cache is a correctness liability (invalidation, staleness, memory)
  bought for speed — it needs a hit-rate measurement to justify existing.
- **Premature distribution**: reaching for queues/shards/microservices when a query index or a
  batch fix delivers the same win at 1% of the operational cost. Scale-out is step 6, not step 1.
- **"Obviously slow" code cleanup during tuning**: mixing readability refactors into perf work
  destroys the attribution — you no longer know what changed the number.
