---
name: write
description: >
  Communication craft: lead with the outcome, select ruthlessly, write readable prose over
  compressed fragments — for replies, reports, docs, commit messages, and PR descriptions.
  Triggers on: /write, write this up, summarize, report, documentation, readme, explain this
---

# Write — Communication That Survives Contact With a Reader

## The test

Not "is it short" but "does the reader get what they need in one pass, without asking a follow-up".
A reply that must be re-read or clarified costs more than the longer version would have. The two
failure modes are opposites and equally bad: the **wall of everything** (unselective, reader does
the filtering) and the **compressed telegram** (fragments, arrows, invented shorthand — reader
does the decompressing). The fix for both is the same: **select hard, then write what survives in
full sentences.**

## Rules

### 1. Lead with the outcome
First sentence = the thing the reader would ask for if they said "just tell me". What happened,
what you found, what you recommend. Reasoning and evidence come after, for those who read on.
Never bury the verdict under the journey ("First I looked at... then I tried...") — the
chronology of your work is almost never the story; the *finding* is.

### 2. Selection is the writing
Before writing, ask of each candidate detail: does this change what the reader does next? Drop it
if not — don't compress it, DROP it. Three details that matter, written clearly, beat ten details
skimmed. What you cut is invisible; what you keep must therefore be readable.

### 3. Write for the reader who stepped away
They didn't watch your process. They don't know the codenames, abbreviations, or numbering you
invented mid-task ("option B", "the second approach", "the helper"). Every reference must resolve
in place — name the thing, don't point at a label from a conversation the reader wasn't in.

### 4. Prose first; structure only when it carries weight
- A simple question gets a direct prose answer — not headers, not a bulleted decomposition.
- Headers/bullets earn their place when the reader will *scan or return to* the document.
  A 4-sentence reply with 3 headers is costume, not structure.
- Tables only for genuinely enumerable comparisons (short facts across consistent dimensions);
  explanation lives in surrounding prose, never crammed into cells.
- One idea per paragraph; if a sentence needs three commas and a dash, split it.

### 5. Calibrate certainty in the language itself
Verified fact → state plainly with the evidence ("tests pass — 42/42"). Inference → mark it
("this suggests"). Guess → say so. Never let the register of confidence exceed the evidence;
"should work" after actually verifying reads as doubt, and confident phrasing without
verification is a lie waiting to be discovered.

### 6. Numbers beat adjectives
"Cut latency 300ms → 80ms" not "significantly faster". "3 of 17 tests fail" not "some tests
fail". If you don't have the number, that's often a sign to go get it before writing.

## By format

- **Status/report**: outcome first, then evidence, then what's next. Failures reported as plainly
  as successes — with the actual error, not a euphemism ("mostly working" is not a status).
- **Commit message**: first line = *what* changed, imperative, ≤70 chars; body = *why* (the
  constraint or bug that forced it), not a file-by-file narration the diff already shows.
- **PR description**: what & why up top in 2–4 sentences, how-to-review (where to start, what's
  risky, what's mechanical), how it was tested — with output. Reviewers read the description to
  decide how carefully to read the diff; tell them.
- **README / docs**: for newcomers — what it is (one sentence), the shortest path to first
  success (copy-pasteable), THEN reference detail. Document the *why* of non-obvious choices;
  the what is visible in the code, the why dies with the author.
- **Code comments**: only for what the code cannot say — constraints, invariants, warnings to the
  future editor ("order matters: X must precede Y because Z"). Never narrate the next line, never
  address the reviewer ("fixed the bug here"), never leave fossils of the editing process.
- **Error messages / warnings you write into software**: state what failed, the actual vs
  expected, and the most likely fix — the reader is debugging at 2am; hand them the next move.

## The final pass

Reread before sending, as the reader: Does sentence one answer the question? Does anything refer
to context the reader lacks? Is anything hedged that was verified, or asserted that wasn't?
Could a third of the words leave without losing a decision-relevant fact? That pass costs one
minute and is the difference between written and merely emitted.
