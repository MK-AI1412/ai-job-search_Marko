---
name: context-engineering
description: >
  Writing instructions FOR AI systems: system prompts, CLAUDE.md files, skills, subagent briefs,
  tool definitions — specificity over adjectives, examples over descriptions, failure-mode-driven
  iteration. Triggers on: /context-engineering, prompt engineering, write a prompt, system prompt,
  improve this skill, write a skill, CLAUDE.md, tool description, agent instructions
---

# Context Engineering — Instructing Models So They Actually Comply

## The core insight

A prompt is a program whose interpreter is probabilistic. You don't get compliance by asking
nicely or emphatically — you get it by making the desired behavior the *easiest* behavior:
unambiguous, concrete, checkable, and reinforced by examples. Every instruction competes with
every other instruction and with the model's defaults for finite attention; **an instruction that
doesn't earn its tokens actively harms the ones that do.**

## Rules for any instruction (system prompt, CLAUDE.md, skill, brief)

### 1. Falsifiable or worthless
"Be concise" is a mood; "lead with the answer in the first sentence; total reply under 150 words
unless asked to elaborate" is an instruction. Test: could a third party look at an output and
verify compliance yes/no? If not, rewrite it until they could. Adjectives (robust, professional,
high-quality) are hope, not specification.

### 2. Examples outrank descriptions
One concrete input→output pair beats three paragraphs of characterization. For format-critical
outputs, show the exact format. For judgment-critical behavior, show a borderline case and the
correct call — the borderline examples are where all the information is; the easy cases teach
nothing.

### 3. State the negative space
Models fill gaps with defaults you didn't choose. Say what NOT to do, especially where the
default is plausible-but-wrong: "report findings; do NOT fix anything", "if the data is missing,
say so; do NOT estimate". Every observed failure mode earns an explicit prohibition — this is
how prompts are actually developed (see rule 7).

### 4. Structure is instruction
Order = priority: put the load-bearing rules first and last (middles get less attention in long
contexts). Group related rules under headers the model can anchor to. One rule per line. A
critical instruction buried in a paragraph of context is a critical instruction lost.

### 5. Give the escape hatch
Every "always X" needs an "unless Y, in which case Z" for the genuinely ambiguous case —
otherwise the model either breaks your rule (having decided it's absurd here) or follows it into
absurdity. Tell it what to do when uncertain: ask, or state assumptions and proceed — pick one
and say which.

### 6. Match register to stakes
Reserve MUST / NEVER / ALWAYS for the rules where violation is catastrophic. If everything is
critical, nothing is — a prompt that shouts throughout gets the compliance of one that never does.

### 7. Iterate on failures, not on rereads
You cannot improve a prompt by rereading it and adding more prose; you improve it by running it,
collecting the failures, and adding the *narrowest* rule that kills each observed failure.
Keep a handful of eval cases (inputs where it previously failed + the desired output) and re-run
them after every edit — prompts regress silently, and edits that fix one case routinely break
another. Delete rules you can't tie to a failure they prevent.

## By artifact type

- **System prompt / CLAUDE.md**: standing behavior only — identity, constraints, conventions,
  workflows. Anything task-specific belongs in the task turn. Prune quarterly: stale rules teach
  the model that your rules can be ignored ("that file it insists exists was deleted months ago").
- **Skill (like this one)**: a skill transfers *method*, not mood — decision rules, named failure
  modes / traps, and checkable outputs. The `description` field is the trigger: write it for
  retrieval (the phrases a user would actually say), not for elegance. Body = what to do; if you
  can't imagine an output violating a line, the line is decoration — cut it.
- **Subagent brief**: the agent starts blank. Context (2–5 sentences), exact deliverable with
  format and size cap, scope fence (what NOT to touch), evidence rule (claims need file:line /
  output / URL). The brief is a contract — write it so a wrong result is a *visible* breach.
- **Tool description (APIs, MCP)**: written for the model deciding *whether and how* to call —
  what it does, when to use it vs the adjacent tool, when NOT to, constraints on arguments,
  one worked example. Ambiguity between two tools = the model alternates between them randomly.
- **Structured output**: define the schema and enforce it mechanically (JSON schema, function
  calling) rather than begging in prose — "respond only with valid JSON" is a request; a schema
  is a constraint. Validate and retry on mismatch.

## Traps

- **The kitchen-sink prompt**: every rule ever conceived, none pruned. Length isn't the problem —
  *unweighted* length is. Ten rules the model follows beat eighty it averages over.
- **Instructing against the model instead of with it**: if a rule needs restating three times in
  growing caps, the design is fighting the grain — restructure the task (different decomposition,
  schema enforcement, a checking pass) instead of shouting louder.
- **Testing on the happy path**: prompts fail on edge inputs — empty data, contradictory
  instructions, absurdly long inputs, adversarial users. Eval cases must include them.
- **Anthropomorphic debugging**: "it's being lazy" isn't a diagnosis. The prompt under-specified
  something and the default filled the gap — find which gap, close it narrowly.
