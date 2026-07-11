---
name: incident-response
description: >
  Production firefighting discipline: stabilize before diagnosing, mitigate before root-causing,
  communicate on a clock, and convert every incident into a blameless postmortem with systemic
  fixes. Triggers on: /incident-response, production is down, outage, incident, users affected,
  rollback, sev1, everything is broken, postmortem
---

# Incident Response — Stop the Bleeding First

## The mode switch

An incident inverts normal engineering values. Normally you optimize for the *right* fix;
in an incident you optimize for **time-to-mitigation** — the elegant root-cause fix ships
tomorrow; the rollback ships in four minutes. Curiosity ("but WHY is it doing that?") is the
enemy of recovery: mitigate first, investigate on the corpse afterward. The discipline below is
about not needing to be smart under adrenaline — the checklist is smart so you don't have to be.

## Phase 1: Assess (minutes 0–5)

- Establish blast radius in user terms: who is affected, what can't they do, since when, is it
  worsening? "Errors are up" is not an assessment; "~30% of checkouts failing since 14:02, flat"
  is. This determines everything downstream — a sev-1 all-hands page and a quiet degradation
  get entirely different responses.
- **Declare it**: name it an incident, name a single incident lead, open one channel where all
  findings land. The costliest failure mode of group response is three people silently
  investigating the same dashboard while nobody watches the fourth.
- Preserve evidence *cheaply* as you go — screenshot the graphs, copy the error samples, note
  timestamps. Mitigations (restarts, rollbacks, cache flushes) destroy the crime scene; ten
  seconds of copying now saves the postmortem later.

## Phase 2: Mitigate (the only goal until users are OK)

- **First question, always: "what changed?"** Deploys, config pushes, feature-flag flips,
  dependency/provider changes, traffic pattern shifts, certificate expiries, cron jobs. The
  overwhelming majority of incidents are caused by a change — and the fastest mitigation is
  undoing it. Correlate the incident start time against every change stream you have.
- The mitigation hierarchy, fastest-first: **roll back** the change → **turn off** the feature
  (flag) → **shed or reroute** load (rate-limit, serve degraded, fail over) → **scale up** if
  it's genuinely capacity → targeted **hotfix** only when nothing above applies (hotfixes
  written under adrenaline have the highest defect rate of any code you'll ever write —
  smallest possible diff, second pair of eyes even at 3am).
- One mitigation at a time, with a stated expectation: "rolling back X; error rate should drop
  within 5 min." If it doesn't, say so and revert the mitigation — stacking three simultaneous
  fixes means never knowing what worked, and unwinding becomes its own incident.
- Beware the half-recovery trap: metrics improving ≠ resolved. Check the *user journey* end to
  end (retry storms, poisoned caches and queues, and lagged replicas all fake recovery).

## Phase 3: Communicate (on a clock, not on progress)

- Update stakeholders at a fixed cadence — every 15–30 min for a live sev — **even when the
  update is "no change, still investigating X."** Silence reads as either "resolved" or
  "abandoned," and both readings generate a second incident of pings into your channel.
- Format: impact (user terms) / current status / what we're trying / next update time. Never
  speculate on cause in stakeholder channels — early guesses fossilize into "what happened"
  before evidence exists.
- In the war room: findings stated with evidence and timestamps ("p99 jumped at 14:02, deploy
  D-4411 landed 13:58 — correlating"), theories labeled as theories. The channel log becomes
  the postmortem's timeline for free.

## Phase 4: Learn (within days, while memory is fresh)

- Root-cause properly now — the thing you deliberately skipped in phase 2. Apply /debug: the
  mitigation proved *what* fixed it, not *why* it broke. "Rolled back and it recovered" is a
  correlation, not a mechanism, and without the mechanism it WILL recur.
- **Blameless postmortem**: the question is never "who did it" but "what made this action
  reasonable at the time, and what would have caught it?" A person who fat-fingered prod had a
  system that let a fat-finger reach prod — fix the system. Blame produces hidden incidents,
  which produce worse incidents.
- Ask "why" past the trigger to the systemic layer: the bug is the trigger; the missing test,
  the alert that fired 40 minutes late, the runbook that didn't exist, the single point of
  failure are the causes worth fixing.
- Action items: few, owned, dated, and tracked like features — or the postmortem was theater.
  Prioritize by "detects it sooner / prevents the class / shrinks the blast radius", not by
  ease. And one honest question per incident: *did we need a human at all, or should this
  mitigation be automatic?*

## Traps

- **Fix-forward pride**: spending 40 minutes writing the proper fix while the rollback sat
  available the whole time. Roll back first; be proud tomorrow.
- **The 2am cowboy change**: an unreviewed, unlogged prod mutation that "should help" —
  now there are two incidents and one of them is unrecorded.
- **Alert trust erosion**: if this incident's alert was one everyone had muted, that's a
  first-class postmortem finding — a noisy pager is a broken pager.
- **Declaring victory at the graph**: closing the incident while queues drain, retries hammer,
  or data written during the window sits corrupted. The incident ends when the *data* is clean,
  not when the line comes down.
