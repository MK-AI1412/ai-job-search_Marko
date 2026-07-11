---
name: optimize
description: >
  Puts Claude into token-efficient operating mode for the rest of the session: minimal reads,
  parallel tool calls, delegation of bulk work to cheap subagents, no rework loops — while keeping
  full quality and creativity on the actual deliverable. Triggers on: /optimize, token efficient,
  save tokens, optimize opus usage, reduce token usage, budget mode
---

# Optimize — Token-Efficient Operating Mode

## Overview

When invoked, adopt every rule below for the **remainder of the session** and confirm to the user in one short sentence that budget mode is on. These rules govern *how* you work, never *what* you deliver: CVs, cover letters, fit evaluations, and research keep their full quality bar and the mandatory verification checklist from CLAUDE.md. Spend tokens where they change the outcome; cut them everywhere else.

The single biggest token waste is **rework** — a wrong approach redone, a document recompiled five times, research repeated because it wasn't written down. Most rules below exist to prevent rework, not to make you terse.

---

## Rule 1: Think before touching tools

For any multi-step task, spend one moment planning the *minimal* tool sequence before the first call. Ask: what is the smallest set of facts I need, and what is the cheapest way to get each one? A 30-second plan routinely saves a 20-call meander.

## Rule 2: Read surgically, never broadly

- **Grep before Read.** Locate the exact lines with `Grep` (use `-n`, `-C` for context), then `Read` only that region with `offset`/`limit`. Never read a whole file to find one section.
- **Never re-read** a file you just wrote or edited — the harness tracks file state and would have errored on failure.
- **Read each reference file at most once per session.** The candidate profile, templates, and tracker CSV don't change under you; rely on what's already in context.
- **PDFs:** read only the pages you need to verify (page count, page breaks, signature block) — not the whole document.
- Prefer `Glob`/`Grep`/`Read` over `find`/`cat`/`grep` in Bash — cheaper and no permission friction.

## Rule 3: Parallelize everything independent

Whenever two or more tool calls don't depend on each other's results, issue them **in the same block**: multiple Greps, Read + WebFetch, several WebSearches, compile CV + compile cover letter. Sequential calls that could have been parallel waste both tokens and wall-clock time.

## Rule 4: Delegate bulk work, keep only conclusions

When a step means sweeping many files or many web pages, launch a subagent (Explore for codebase sweeps, general-purpose for research) and let *it* absorb the raw dumps — only its conclusion enters your context. Give the subagent a tight brief: exactly what to return, in what format, and a size cap ("return ≤10 bullet points, no raw quotes"). Run independent subagents concurrently in one message.

## Rule 5: Write intermediate results to disk, not context

Research findings, scraped postings, keyword lists, draft comparisons — persist them as files (scratchpad for throwaway, repo for keepers). A fact written to a file costs its tokens once; a fact held only in conversation gets re-paid on every future turn. This also survives compaction and future sessions.

## Rule 6: One compile loop, not five

For LaTeX work, front-load correctness so compilation converges fast:

1. Apply **all** known fixes from CLAUDE.md *before* the first compile: `lualatex` for CV, `xelatex` for cover letter, `\needspace{5\baselineskip}` before each `\cventry`, the itemize-outside-`\lettercontent` pattern, correct fonts.
2. Compile **both documents in parallel** in one Bash block.
3. Read the PDF once, note **every** problem (page count, orphaned titles, overflow), fix them **all** in one edit pass, recompile once.

Target: 2 compile cycles per document, not an incremental fix-one-thing loop.

## Rule 7: Web research — search once, well

- Craft one precise query instead of three vague ones; add a second only if the first genuinely fails.
- WebFetch a page **once**; extract everything you'll need (facts to verify, hiring manager name, tech stack, keywords) in that single pass and record it per Rule 5.
- Company-fact verification (required by the checklist) still happens — but each fact gets exactly one verification fetch.

## Rule 8: Output discipline

- Don't quote large blocks of files, postings, or LaTeX back to the user — reference `file:line` or summarize in a sentence.
- No progress narration between tool calls beyond a brief note at direction changes.
- Final replies: lead with the outcome, include only detail that changes what the user does next, in plain prose. Selectivity, not compression — never cryptic fragments.
- Never restate the verification checklist items that passed one by one; report "all N checks pass" plus any failures/warnings.

## Rule 9: Don't gold-plate

Stop when the task is done and verified. No unrequested extras, no speculative refactors, no "while I'm here" improvements, no offering three alternative drafts when one targeted document was requested. Creative effort goes *into* the requested deliverable (sharper positioning, better phrasing, smarter keyword mapping) — not around it.

## Rule 10: Session hygiene (tell the user when relevant)

- One application (or one coherent task) per session where possible; a fresh session is cheaper than dragging 50k tokens of an unrelated finished task through every subsequent turn.
- Suggest `/compact` when the conversation is long and the remaining work doesn't need the early history.
- Batch small related asks ("fix the date and the phone number and recompile") into one message rather than three round-trips.

---

## What NOT to cut — ever

- The **compiled-PDF verification** and **ATS extraction** checks from CLAUDE.md (mandatory).
- Independent verification of company-specific claims before they go in a cover letter.
- Reading a file before overwriting or deleting it.
- Asking the user when a decision is genuinely theirs (wrong deliverable = maximum token waste).

## Confirmation format

On invocation, reply with a single line such as:

> Budget mode on — surgical reads, parallel calls, delegated bulk work, one-pass compiles. Quality bar unchanged.

Then proceed with whatever task follows under these rules.
