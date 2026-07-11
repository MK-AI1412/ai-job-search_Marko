---
name: learn-new-tech
description: >
  Rapid mastery of an unfamiliar framework, API, language, or codebase: build the smallest thing
  that runs, break it deliberately, read only ahead of need — learning by collision, not by
  reading ahead. Triggers on: /learn-new-tech, learn this framework, new to this library,
  never used, get up to speed, how does this codebase work, unfamiliar
---

# Learn New Tech — Collision-Driven Ramp-Up

## The principle

Reading ahead of need feels productive and retains almost nothing; knowledge sticks when it
resolves a problem you actually hit. So the method is: get to a running artifact absurdly fast,
then learn by *colliding* with reality — break it on purpose, extend it slightly beyond the
tutorial path, and read documentation only at the moment a collision creates the question.
Depth-first on what you need now beats breadth-first on what you might need someday.

## Warning zero: your training data is stale

For any actively-developed technology, treat remembered APIs as hypotheses. Check the current
version, changelog, and migration guides FIRST — the classic failure is fluently writing last
year's API. When docs and memory disagree, docs win; when docs and observed behavior disagree,
behavior wins.

## The loop (new framework / library / language)

### 1. Orient — 15 minutes, hard cap
Official quickstart + one "architecture/concepts" page. Goal is the *shape*, not mastery: what
are the 3–5 core abstractions, what does hello-world look like, what does the community actually
use alongside it. Resist reading further — everything past the shape is better learned on demand.

### 2. Run the smallest real thing
Not the tutorial's polished example — the smallest version of *your actual use case* that
executes. Working code you can poke at is worth fifty pages of docs, because now every question
has an experiment attached.

### 3. Break it deliberately
This is the step everyone skips and the one that builds real understanding. Feed it a wrong
type, an empty input, a missing config, a huge payload. You learn: what the error messages look
like (you WILL see them again at a worse time), where the boundaries are, what fails loud vs
silently corrupts. Ten minutes of deliberate breakage buys hours of future debugging.

### 4. Extend one step past the beaten path
Tutorials work by construction. Add the one requirement your real use case has that the tutorial
lacks — auth, pagination, a second consumer, an edge-case input. The gap between "tutorial works"
and "my variant works" is where the actual learning is, and it's where you find out whether the
tech fits at all — cheaply, before commitment.

### 5. Read on demand, at the moment of collision
Each collision → the specific doc section, the GitHub issue, the source code of the function
in question. Reading with a live question converts to retained knowledge at maybe 10× the rate
of reading ahead. Keep a running `NOTES.md` of surprises — the things that violated your
expectations are exactly what future-you (and /handoff) needs written down.

## The loop (unfamiliar codebase)

1. **Make it run first** — build, test suite, the app itself. A codebase you can execute is
   explorable; one you can't is archaeology. Fixing the build IS step one, not an obstacle to it.
2. **Trace one real flow end-to-end** — pick a concrete user action and follow it: entry point →
   handler → logic → storage → response. One deep vertical slice teaches the architecture better
   than reading every directory shallowly. (Fan out /orchestrate readers for breadth *after* the
   spine is clear.)
3. **Read the tests as documentation** — tests state what the authors considered important and
   show every API's intended usage, and unlike comments they can't rot silently.
4. **Use git history as a teacher** — `git log --follow` on a confusing file; the commit messages
   explain the *why* that the code can't. `git blame` on a weird line usually resolves "why on
   earth" into "oh, that outage".
5. **Verify by prediction** — before running something, predict what it does; run it; investigate
   misses. Your model of the codebase is trustworthy when predictions stop missing — that's the
   signal you're ready to change it.

## Traps

- **Tutorial paralysis**: three tutorials deep, nothing of your own built. One tutorial, then
  build — the second tutorial teaches less than the first collision.
- **Premature abstraction of the new thing**: wrapping a framework you barely know in your own
  layer bakes your misunderstandings into an API. Use it raw until its idioms feel native.
- **Fighting the framework**: if you're contorting around the tool's grain, stop — either you've
  missed its intended idiom (search: "how does <tech> want you to <task>") or it's the wrong tool.
  Both are cheaper to learn now.
- **Copy-paste without a mental model**: pasted code that works teaches nothing until you can
  say what each line is for. Delete lines and see what breaks if you have to.
- **Assuming transfer**: "it's like X but for Y" is a useful on-ramp and a dangerous resting
  place — the differences from X are precisely where the bugs will live.
