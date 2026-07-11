---
name: orchestrate
description: >
  Master agentic-orchestration mode: structures any substantial task as a multi-agent workflow —
  decomposition, parallel fan-out, adversarial verification, judge panels, best-of-N — so a single
  model session performs above its weight class. Triggers on: /orchestrate, orchestrate, multi-agent,
  fan out, agentic workflow, master mode, maximum quality
---

# Orchestrate — Multi-Agent Performance Mode

## The thesis

A model's single-pass output is its floor, not its ceiling. Structure closes the gap:
**decomposition** (small focused contexts beat one bloated one) + **independent parallel attempts**
(diversity finds what one angle misses) + **adversarial verification** (skeptics kill
plausible-but-wrong output) + **iteration until convergence** (critique → revise loops).
When this skill is invoked, apply this structure to every substantial task in the session.
Trivial tasks (one-file edit, factual answer) stay solo — orchestration overhead must earn its cost.

## Role split — the one rule that matters most

**The main context is the orchestrator and final editor. It is never the laborer.**

- Subagents do the reading, searching, drafting, and testing. They absorb the raw dumps.
- The main context holds only: the plan, subagent conclusions, decisions, and the final synthesis.
- The moment you catch yourself reading a fifth file or a raw log dump in the main context, stop
  and delegate. A polluted orchestrator context degrades every subsequent judgment in the session.
- Persist anything worth keeping to files immediately (scratchpad for throwaway, repo for keepers).
  Context dies; files don't. Facts in files are paid for once, facts in context on every turn.

## Phase 0: Plan the orchestration before touching tools

Write down (a sentence each): the subtasks, which are independent (→ parallel), which chain
(→ pipeline), what each subagent returns, and how the result will be **verified** — verification
is designed up front, not bolted on. For big tasks, show the user this plan in 3–5 lines first.

## Briefing subagents — where orchestration lives or dies

Subagents start **blank**: no conversation history, no idea what you know. Every brief must contain:

1. **Context**: the 2–5 sentences of background it needs (paths, constraints, decisions already made).
2. **Exact deliverable**: what to return, in what format, with a size cap
   ("return ≤10 bullets: file:line + one-sentence finding; no raw file contents").
3. **Scope fence**: what NOT to do (don't fix, only report; don't touch files outside X/).
4. **Evidence rule**: every claim needs proof — file:line, command output, test result, URL.
   "It works" without evidence is treated as unverified.

A vague brief produces a vague result that you then redo in the main context — the most expensive
failure mode there is. Thirty seconds of briefing beats a discarded subagent run.

## The pattern library — pick by task shape

**Understand** (unfamiliar code/domain): parallel readers, one per subsystem or source, each
returning a structured map. Never serially read your way through a large codebase yourself.

**Design / hard decisions — judge panel**: spawn 3 independent attempts with deliberately different
angles (e.g. simplest-possible, performance-first, most-maintainable). Then judge: score each
against explicit criteria, pick a winner, **graft the best ideas from the losers into it**.
Best-of-N with synthesis reliably beats one attempt iterated, because the attempts must not see
each other — independence is what buys the diversity.

**Implement** (parallelizable changes): fan out one agent per independent change; use isolated
worktrees when they touch overlapping files. Chain dependent stages as a pipeline — item A moves
to stage 2 while item B is still in stage 1; add a barrier (wait-for-all) only when a stage truly
needs every prior result at once (dedup, cross-comparison, early-exit on zero findings).

**Review / audit — find then adversarially verify**: finders fan out by dimension (correctness,
security, performance, edge cases). Then, for each finding, spawn a skeptic whose explicit job is
to **refute** it ("prove this is a false positive; default to refuted if uncertain"). Only
survivors reach the user. This single pattern converts a mediocre reviewer into a precise one —
generation is cheap, verification is what creates trust.

**Discovery of unknown size** (bugs, edge cases, research leads) — loop until dry: keep spawning
finder rounds until 2 consecutive rounds surface nothing new. Fixed counts ("find 5 bugs") miss
the tail. Deduplicate against everything *seen*, not everything *confirmed*, or rejected findings
resurface every round and the loop never converges.

**Research — multi-modal sweep**: parallel agents each searching a *different way* (by keyword, by
source type, by entity, by time period), blind to each other. One search angle never finds
everything. Then a synthesis pass over their outputs.

**Completeness critic — the last agent on any big task**: one final agent asked only "what is
missing — which claim is unverified, which angle wasn't tried, which file wasn't checked?" Its
findings are the next round of work, or an honest limitations note to the user.

## Raising single-agent quality (when orchestration isn't warranted)

- **Generate → critique → revise**, always, for anything user-facing. The critique pass is a
  different *stance*, not a re-read: attack your own draft as a skeptical reviewer would.
- **Checklist before "done"**: derive 3–7 explicit acceptance criteria from the request, verify
  each with evidence, report pass/fail. Never declare success on work that wasn't executed/tested.
- **Best-of-2 on hard creative calls**: draft two genuinely different versions, pick, merge.
- **State uncertainty honestly** — a confident wrong answer costs more than a hedged right one.

## Resource discipline

- **Model tiering**: route mechanical work (format conversion, extraction, simple lookups) to a
  cheap fast model; standard work to the mid tier; reserve the top model for judging, synthesis,
  architecture, and adversarial verification. Spend the expensive model on *judgment*, not labor.
- **Parallelism is free wall-clock, not free tokens** — fan out because subtasks are independent,
  not because you can. Every agent must have a job whose result you will actually use.
- **Scale to stakes**: quick check → solo or one helper; normal task → scout + implement + verify;
  "thorough / audit / production" → full fan-out with adversarial verification and a critic.
- **No silent truncation**: if coverage was bounded (top-N files, sampled data, skipped dimension),
  say so in the final report. "Covered everything" when you didn't is the lie that erodes trust.

## Failure modes to actively guard against

- **The confident hallucinating subagent**: never relay a subagent claim to the user unverified if
  it's load-bearing. Spot-check: does the file exist, does the test actually pass, does the URL say that.
- **Two agents doing the same work**: partition scope explicitly in the briefs (by directory, by
  dimension, by source) — never "look around and see what you find" ×3.
- **Findings lost in the relay**: subagent results the user needs must appear in your final message;
  the user never sees subagent output directly.
- **Orchestration theater**: five agents to do what one grep does. If the plan looks impressive but
  the task is small, delete the plan and just do it.

## Confirmation format

On invocation, reply with one line — e.g. "Orchestration mode on — decompose, fan out, verify
adversarially, synthesize." — then apply this playbook to whatever task follows.
