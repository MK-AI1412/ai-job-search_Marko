---
name: research
description: >
  Rigorous research method: multi-angle search, source triangulation, adversarial fact-checking of
  load-bearing claims, and honest synthesis with cited evidence and stated uncertainty. Triggers on:
  /research, research this, look into, find out about, is it true that, compare options, due diligence
---

# Research — Triangulated, Adversarially-Checked Research

## The standard

Research quality is not the number of sources skimmed; it is whether the **load-bearing claims** —
the ones the user will act on — survive an active attempt to break them. One verified fact beats
ten repeated ones. The default posture is a skeptical analyst, not a summarizer: search engines
surface the popular answer, which is frequently the outdated or subtly wrong one.

## Method

### 1. Sharpen the question first
Restate the question with its decision attached: who is deciding what, by when, under which
constraints. "Best X" is unanswerable; "best X for constraint Y at budget Z" is researchable.
If the question is genuinely underspecified, ask 2–3 narrowing questions BEFORE burning searches.
List the 3–6 sub-questions the answer decomposes into — these become your search plan.

### 2. Search in multiple modes, not multiple phrasings
Different *angles*, not synonyms of one query: the official source (docs, filings, changelog),
the practitioner view (issue trackers, forums, postmortems), the critical view (add "problems",
"limitations", "vs alternatives" to the query), and the recency check (past-year filter — your
training knowledge of fast-moving topics is stale by default, prices/versions/APIs especially).
Fan sub-questions out to parallel subagents when there are several; each returns findings as
claim + source + date, size-capped.

### 3. Grade sources as you collect
Primary (the spec, the paper, the company's own filing, the actual benchmark) > informed secondary
(reputable journalism, maintainer comments) > SEO sludge (listicles, affiliate reviews, content
farms — treat as leads to primaries, never as evidence). Note the DATE on everything; an undated
claim about a moving target is worth little. Two sources that both cite the same origin are ONE
source — trace the citation chain before counting it as corroboration.

### 4. Triangulate the load-bearing claims
Identify the 3–7 claims the conclusion actually rests on. Each needs either two genuinely
independent sources, or one primary source read directly (fetch the page — snippets truncate and
mislead; the sentence after the quoted one often reverses it).

### 5. Adversarial pass — try to kill your own conclusion
Before writing up, actively search for disconfirmation: "X criticism", "X didn't work",
"switching away from X", the strongest opposing take you can find. For high-stakes conclusions,
spawn a skeptic subagent briefed to refute the draft conclusion. If the conclusion survives, say
what the strongest counter-argument was and why it doesn't hold; if it doesn't survive, the
research just did its job — report the correction, not the original.

### 6. Synthesize honestly
- Lead with the answer and the confidence level, then evidence, then caveats.
- Attach sources to specific claims inline — not a bibliography dump at the end.
- Mark each key claim: **established** (triangulated), **probable** (single good source),
  **contested** (sources disagree — show both sides), **unknown** (searched, not found).
  Saying "I could not verify X" is a finding; silently omitting X is a failure.
- Separate facts from your inference, and quantify instead of hedging with adjectives:
  "3 of the 5 practitioner reports mention Y" beats "many users say Y".
- State what was NOT covered (angles unsearched, paywalled sources, time cutoff) — silent
  coverage gaps read as "checked everything" when you didn't.

## Traps

- **First-page consensus**: the top 5 results often share one upstream origin. Triangulation
  means independent origins, not independent URLs.
- **Recency inversion**: an authoritative 2019 answer loses to a mediocre 2026 one on anything
  that moves (software, pricing, laws, orgs). Check dates before authority.
- **Snippet trust**: never cite a page you didn't fetch when the claim is load-bearing.
- **Question drift**: long research sessions answer a subtly different question than asked.
  Re-read the original ask before writing the synthesis.
- **Training-data leakage**: for anything time-sensitive, your memory is a hypothesis to verify,
  never a source to cite.
