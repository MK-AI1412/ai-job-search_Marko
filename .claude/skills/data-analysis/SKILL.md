---
name: data-analysis
description: >
  Empirical discipline for anything with numbers: inspect raw data before aggregates,
  distributions before means, hunt bias and leakage, treat surprising results as bugs until
  proven otherwise. Triggers on: /data-analysis, analyze this data, metrics, statistics, average,
  A/B test, dataset, csv analysis, ML evaluation, benchmark results
---

# Data Analysis — Numbers That Survive Scrutiny

## The prime directive

**A surprising result is a bug in the analysis until proven otherwise.** The prior on "exciting
discovery" vs "join duplicated rows / timezone shifted a day / nulls silently dropped" is not
close. The discipline below is ordered accordingly: data quality first, then description, then
inference — because every step trusts the one before it, and errors compound silently downward.

## Phase 1: Touch the raw data before ANY aggregate

- Look at actual rows — head, tail, and a random sample (the head is often unrepresentative:
  sorted, oldest, or test records). Twenty real rows calibrate you better than any summary.
- For every column you'll use: type as expected? Nulls — how many, and are they "missing" or
  "meaningfully absent"? Duplicates — and is each row really one observation? Ranges sane
  (negative ages, timestamps from 1970, prices of 0 that mean "unknown")?
- Ask what's NOT in the data: the deleted accounts, the failed requests that never logged, the
  users who churned before the survey. **Selection bias lives in the missing rows, and no
  amount of analysis of the present rows reveals it** — you have to reason about the collection
  process itself.
- Know each column's operational meaning, not its name: `created_at` of what event, in whose
  timezone? `revenue` gross or net, before or after refunds? Column names are marketing.

## Phase 2: Distributions before summary statistics

- Plot (or at least quantile: min/p25/median/p75/p95/max) every metric BEFORE citing its mean.
  Means are hostage to outliers and silence bimodality — the "average user" of a bimodal
  distribution doesn't exist, and decisions made for them serve no one.
- Default to median + a spread measure for skewed data (latency, revenue, counts — i.e. most
  real data). Report the mean alongside when totals matter.
- Check group sizes before comparing groups: "conversion doubled in segment X" where N(X)=7 is
  noise wearing a headline. State every N next to every percentage — no exceptions.
- Beware aggregation reversals (Simpson's paradox): any headline comparison should be re-checked
  within the 2–3 segments that plausibly confound it (time period, platform, cohort).

## Phase 3: Inference — separating signal from wishful thinking

- Correlation compatible with causation ≠ causation established. For any causal claim, name the
  counterfactual: what would these users have done *without* the treatment? If the design can't
  answer that (no control group, self-selected exposure), say "associated with", not "drives".
- **Metric movements need denominators checked first**: a rate can "improve" because the
  numerator rose or because the denominator quietly changed composition. Decompose before
  celebrating.
- Multiple comparisons: check 20 segments, expect one spurious p<0.05 on pure noise. The more
  slices examined, the higher the bar for any single slice's "finding" — and report how many
  slices were examined.
- Pre-state the hypothesis when possible. A pattern found by dredging is a *hypothesis to test
  on fresh data*, not a conclusion — the same data cannot both generate and confirm a hypothesis.

## For ML / model evaluation specifically

- **Leakage is the default assumption, not the exotic exception**: any feature computed with
  information unavailable at prediction time (post-event aggregates, target-derived encodings,
  train/test contamination through time or through duplicate entities) inflates metrics that
  then collapse in production. Audit every feature against "was this knowable at decision time?"
- Split by time (and by entity where entities repeat) — random splits on temporal data leak the
  future into training.
- Always run the dumb baseline (majority class, last value, mean). A model beating 50% on a 95/5
  imbalanced problem is worse than useless. Accuracy on imbalanced data is misdirection; use the
  metric aligned with the actual cost structure (precision/recall/calibration), and say why.
- Eyeball actual errors, not just the metric: read 20 misclassified examples. The metric says how
  wrong; the examples say *why* — and often reveal label noise or a data bug, not a model limit.
- "Too good" IS the alarm: a jump from 0.75 to 0.98 AUC is leakage until forensically proven
  otherwise. See prime directive.

## Reporting numbers

- Every claim carries its N, its timeframe, and its population ("checkout conversion, EU web
  users, last 30 days, N=48k" — not "conversion is up").
- Show uncertainty where it changes the decision: a ±4pt interval around a 2pt lift means the
  honest answer is "can't tell yet", and saying so is the deliverable.
- State the caveats you'd want known if you were the decision-maker: what was excluded, what
  couldn't be checked, which assumption is load-bearing. A number without its caveats is a
  future incident.
- Reproducibility floor: the query/script that produced each number is saved and re-runnable —
  "I can't regenerate that figure" retracts the figure.
