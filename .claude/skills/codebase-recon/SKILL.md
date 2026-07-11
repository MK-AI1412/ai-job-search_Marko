---
name: codebase-recon
description: >
  Fast codebase reconnaissance and change planning: search-driven navigation instead of reading,
  structure-first scanning, wedge techniques to find any behavior in minutes, and turning the map
  into a safe implementation plan. Triggers on: /codebase-recon, scan the codebase, where is this
  implemented, find where, map the architecture, plan this change, explore the repo, where should
  this code go, impact analysis
---

# Codebase Recon — Navigate by Search, Not by Reading

## The principle

You cannot read a codebase into your head, and you don't need to: **you need a map accurate
enough for the current task, built by search and sampling, not by reading.** Files are read
last, in targeted slices, after cheaper signals (structure, names, manifests, greps, git history)
have told you which twenty lines matter. Reading is the most expensive operation you have —
everything below exists to spend it precisely. Depth follows need: a rename needs one grep; an
architecture change needs the full map. Match the phase count to the stakes.

## Phase 1: The 5-minute structural scan (no file bodies yet)

Run these in parallel; together they give you 70% of the map:
- **Top-2-level directory listing** — directory names are the authors' own mental model.
  Note the obvious roles (api/, core/, models/, jobs/) and the mystery ones (misc/, utils2/).
- **Manifests and lockfiles** (package.json / pyproject / go.mod / Cargo.toml): the framework
  and key dependencies. This is the highest-leverage read in the repo, because **a recognized
  framework gives you the map for free** — its conventions dictate where routes, models,
  config, and tests live. Recon confirms conventions; it doesn't rediscover them.
- **Entry points**: main/index/app files, scripts section, Dockerfile CMD, CI workflow. What
  actually runs, and how.
- **Config and schema**: env examples, migration folder, schema files. The data model is the
  skeleton — a 2-minute skim of the schema/types often teaches more than an hour in handlers.
- **README + CLAUDE.md/CONTRIBUTING** — skim for build commands and stated architecture, but
  treat prose as *hypotheses*: docs rot, code is ground truth. When they disagree, code wins.

Write the emerging map down as you go (a scratch file): directory → one-line role, key deps,
entry points, open questions. Recon that lives only in your head is re-paid next session.

## Phase 2: Wedge in — finding any behavior in minutes

To locate where something happens, don't browse — drive a wedge from something *exactly
greppable* and expand:
- **The literal-string wedge** (fastest, most reliable): grep the user-visible artifact — the
  error message, button label, log line, URL path, config key. It lands you inside the exact
  code path in one hop. Truncate smartly: grep a distinctive 4–6 word fragment, since messages
  wrap and interpolate.
- **The symbol wedge**: found one relevant function/type? Its definition and its references ARE
  the local architecture. Trace: who calls this (callers = usage contexts) and what does it call
  (callees = dependencies). One hop each direction usually suffices.
- **The route wedge**: for anything user-triggered, find the route/command/handler table and
  follow the one route down. Handler tables are the codebase's own index.
- **The git wedge**: `git log --oneline -20 -- <area>` or a `git log -S "phrase"` (pickaxe) —
  who touched this last, in what commit, with what stated intent. For "why is it like this",
  blame beats reading every time.
- **The test wedge**: grep the tests for the feature name — a good test shows the setup, the
  API, and the expected behavior in twenty lines: executable documentation.

Search discipline: exact strings before regex, filename search before content search
(`glob **/auth*` before grepping "authentication"), case-insensitive when unsure, and constrain
by file type to kill noise. Two failed greps = wrong vocabulary — pull terms from the nearest
file you HAVE found, or from the manifest's dependency names.

## Phase 3: Read surgically, weighted by importance signals

- Read **signatures before bodies**: a file's exports/public functions/type definitions are its
  table of contents — skim those for the whole module before reading any implementation.
- Read the **types/schemas/interfaces fully** — they're dense, small, and constrain everything
  else. Bodies you read only where the task lands.
- Rank importance with cheap signals, not intuition: **churn** (`git log` frequency — hot files
  are load-bearing), **centrality** (imported everywhere = core; imports everything = wiring),
  and **test density** (what the authors bothered testing is what they feared breaking).
- For genuinely large scopes (audit-level breadth), fan readers out per subsystem
  (see /orchestrate) and keep only their structured maps — never serially read your way through
  breadth in the main context.
- Timebox honesty: if 15 minutes of recon hasn't found the wedge, the vocabulary is wrong or
  the behavior lives outside this repo (a service, a library, generated code). Widen the
  hypothesis, not the reading.

## Phase 4: From map to change plan

Recon's product is a plan you can defend:
1. **Find the analog first**: the existing feature most similar to what you're adding. Its
   structure is your template — where it puts the route, logic, model, and tests is where yours
   go. "Where should this code live?" is almost always answered by the analog, not by taste.
2. **Blast radius before design**: grep every caller/user of what you'll touch, check who shares
   the data you'll change. The list of affected sites determines whether this is an edit, a
   migration, or a redesign — better to know before the first line.
3. **Plan along the dependency direction**: data/schema first, then logic, then surface
   (API/UI) — each layer verifiable before the next builds on it. State the plan in file-level
   steps ("add column via migration X; extend service Y:fn; expose in handler Z; test at W").
4. **Name the risks the recon surfaced**: the module with no tests, the function with 40
   callers, the code that contradicts the docs. These get extra verification in /ship, and the
   user hears about them up front.
5. Big structural decisions discovered en route (schema break, cross-service change) escalate
   to /system-design — recon scopes the decision; it doesn't quietly make it.

## Traps

- **Reading as procrastination**: "I'll just read a few more files to be safe" — recon is done
  when the next concrete action is unambiguous, not when you feel fluent. Fluency comes from
  the doing.
- **Trusting names over behavior**: `validateUser()` that also creates sessions; `utils/` hiding
  the core algorithm. Names are claims; verify the load-bearing ones by reading the body or its tests.
- **Missing generated/vendored code**: grepping through build output, lockfiles, or vendored
  deps drowns the signal — exclude those dirs first; conversely, "nobody defines this symbol"
  often means codegen — check for generators before declaring magic.
- **The monorepo mirage**: finding *a* match and assuming it's *the* match — the same concept
  implemented three times in three packages. Count matches before choosing your wedge; two
  implementations of one concept is itself a finding worth reporting.
- **Map hoarding**: producing a beautiful full-repo map when the task needed three files.
  The map serves the change; recon effort tracks task size, always.
