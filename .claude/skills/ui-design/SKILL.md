---
name: ui-design
description: >
  Visual and interaction design craft for building interfaces that look professionally designed:
  hierarchy, spacing systems, typography, restrained color, states, motion, and the polish details
  that separate amateur from finished. Triggers on: /ui-design, design a UI, make it look good,
  landing page, dashboard design, looks ugly, improve the design, frontend design, CSS styling,
  component design, make it beautiful
---

# UI Design — Making Interfaces Look Designed

## Where good UI actually comes from

Amateur UI fails not from missing decoration but from missing **decisions**: seven font sizes
because none was chosen, random padding because there's no scale, five competing accents because
nothing was subordinated. Professional UI is mostly the *absence* of noise — a few deliberate
systems (spacing, type, color) applied without exception. Taste, operationally, is consistency
plus restraint; both are checkable, so both are transferable.

## Start from hierarchy, not aesthetics

Before any styling: rank what's on the screen. What's the ONE thing the user came to do or see?
That gets visual dominance. Everything else steps down in clear tiers — secondary supports,
tertiary recedes until sought. If everything is emphasized, nothing is: **for every element you
promote, demote another.** Most "make it pop" requests are actually "the hierarchy is flat"
problems, and the fix is subtraction. Squint test: blur your eyes at the screen — the intended
priority should survive as blobs of contrast. If it doesn't, no color change will save it.

Express hierarchy through **size, weight, and color-contrast** — not through decoration
(borders, backgrounds, badges). A screen needs surprisingly few of these steps: e.g. dark
high-contrast text for primary, medium gray for secondary, light gray for hints — three levels,
used everywhere, no exceptions.

## The systems (decide once, never improvise)

**Spacing — the #1 amateur/professional divider.** Fixed scale, geometric-ish:
4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px. Every margin, padding, and gap comes from the scale
— a 13px gap next to a 15px gap reads as sloppy at a level viewers feel but can't name.
Two governing rules: **related things sit closer than unrelated things** (proximity IS grouping
— get it right and you can delete most borders and boxes), and **when unsure, add more space**,
especially around groups. Whitespace is not emptiness; it's the cheapest signifier of quality
there is. Cramped = cheap, always.

**Typography — one family, few sizes, weights do the work.**
- One typeface (a good neutral sans: Inter, system-ui stack). Two max, and only with a reason.
- A type scale, not ad-hoc sizes: e.g. 12 / 14 / 16 / 20 / 24 / 32 / 48. Body at 16px floor.
- Hierarchy via weight (400 / 500-600 / 700) before via size — subtler and tighter.
- Line height: ~1.5 for body, ~1.1–1.2 for large headings (big text with body line-height is a
  telltale amateur marker). Line length 45–75 characters — full-width paragraphs on wide screens
  are unreadable; cap the measure.
- Real hierarchy in text blocks: headings closer to the content below them than to the content
  above (a heading floating equidistant belongs to nothing).

**Color — neutrals do 90% of the job.**
- Build on a gray ramp (8–10 steps) and ONE accent. The accent is a scarce resource: primary
  action, active state, key highlight — if the accent appears everywhere it informs nowhere.
- Pure black (#000) and pure white surfaces read harsh; near-black text (e.g. gray-900) on
  off-white feels finished. Tint grays slightly toward the accent hue for cohesion.
- Semantic colors (red/green/amber) reserved for semantics — destructive, success, warning —
  never as decoration, or their meaning erodes.
- Contrast is non-negotiable: 4.5:1 for body text, 3:1 for large text and UI controls. Light
  gray text on white for "subtlety" is the most common accessibility failure — check, don't
  eyeball. Never encode meaning in color alone (add icon/label — colorblind users exist).
- Dark mode is its own design, not inversion: dark gray surfaces (not black), *desaturated*
  accents (saturated colors vibrate on dark), reduced elevation shadows, same contrast floors.

**Depth and shape — one language.** Pick either borders OR shadows as the primary separator and
stay with it. Shadows: subtle, layered, consistent light source (y-offset > blur spread lightly)
— a strong drop shadow is instant 2005. One border-radius scale (e.g. 6 / 10 / 16px by size);
mixed radii on sibling elements screams unfinished.

## States are the design (not an afterthought)

Every interactive element needs visible: default, hover, focus (a real focus ring — keyboard
users are users), active, disabled. Every data view needs designed: **empty** (the first-run
experience — an explanation and a next action, never a blank void or a lonely "no data"),
**loading** (skeletons that hold layout beat spinners; NEVER let content jump when it arrives),
**error** (what happened + what to do, in human words), and **overflow** (the name that's 3×
longer than your mock, the table with 10,000 rows, the zero, the 47-digit number). Design the
worst-case content first and the happy path inherits the robustness.

## Interaction and motion

- Feedback within 100ms for every action — instant state change, then async completion.
  Optimistic UI where reversal is cheap.
- Motion is communication, not garnish: 150–250ms ease-out for entrances and state changes;
  anything over 400ms is the UI making the user wait for its art. Animate opacity and transform
  (cheap, smooth), not layout properties. Respect `prefers-reduced-motion`.
- Hit targets ≥ 44px on touch. Destructive actions: separated spatially from safe ones, colored
  semantically, confirmed or undoable — "undo" beats "are you sure?" every time users are moving fast.
- Forms: label above field, inline validation on blur (not on every keystroke, not only on
  submit), error text next to the field it belongs to, the submit button states exactly what it
  does ("Create project", never "Submit").

## The polish pass (the visible 5% that reads as craft)

Before calling any UI done, one dedicated pass:
- Alignment: everything sits on a grid line — one 3px misalignment reads as broken trust.
  Optical alignment over mathematical (icons and triangles need nudging to *look* centered).
- Consistency sweep: same paddings on same components, same icon set at same stroke weight,
  same capitalization scheme everywhere (pick sentence case; commit).
- Numbers in tables: right-aligned, `font-variant-numeric: tabular-nums`, same decimal places.
- Text rendering details: real ellipsis for truncation with a title/tooltip carrying the full
  value; no orphan single word on a heading's second line; `text-wrap: balance` on headings.
- Interactive affordances: cursor changes, transitions on hover states (not just snaps),
  focus-visible styling that matches the design language rather than browser default.
- The 30-second zoom-out: view at arm's length and at mobile width. Does it hold?

## Traps

- **Decorating instead of structuring**: gradients, borders, and icons added to fix what is a
  hierarchy/spacing problem. Remove before you add — subtraction is the senior move.
- **Designing only the demo state**: perfect with 3 ideal items, broken with 0, 1, or 300.
- **Trend-chasing over legibility**: glassmorphism blur over busy backgrounds, 200-weight fonts,
  gray-on-gray minimalism — if users squint, the aesthetic failed at its one job.
- **Inconsistency compounding**: each one-off padding or shade seems harmless; twelve of them is
  why the page "feels off" in a way stakeholders can't articulate but always detect.
- **Skipping keyboard/screen-reader reality**: semantic HTML first (button = <button>, real
  <label>s, heading order), alt text that says what the image *means*. Accessibility retrofits
  cost 10× the up-front version — and the up-front version usually improves the visual design too.
