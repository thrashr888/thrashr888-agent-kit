---
name: presentation-redesign
description: Rebuild dense strategy decks for live presentation.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Presentation Redesign

Turn a dense, report-like PowerPoint into a deck people can actually present.
Use native PPTX editing, not exported screenshots as the source of truth. The
output is a live speaking deck; detailed jobs, measures, ownership, and source
material belong in a companion document or appendix.

## When to Use

Use when someone says a deck is too dense, repetitive, small, machine-made, or
hard to present. Also use for strategy decks that need a clearer executive
story, a source deck that needs a full visual rebuild, or a slide deck created
from a long document.

Do not use for a one-word copy fix, a single chart correction, or a detail-heavy
report that is meant to be read rather than presented.

## Prerequisites

- A source `.pptx` and the source material that governs facts, terminology, and
  ownership.
- `python-pptx` for native editing.
- `soffice` plus `pdftoppm` or `pdftocairo` for render verification when
  available.
- A clear audience and decision. For a continuing strategy-deck task, default
  to an executive working session and state that assumption in the plan.

## Non-negotiable Output Rules

1. **Every visible text run must be 28pt or larger.** This includes labels,
   captions, footers, and page numbers. Omit nonessential text instead of
   shrinking it.
2. **Zero empty placeholders.** An empty PowerPoint title placeholder still
   shows `Click to add title` in the editor. Remove its XML element; do not
   merely leave it blank.
3. **One idea per slide.** Move detailed inventories, ownership, and source
   tables to a companion document or clearly labeled appendix.
4. **No invented facts, metrics, customers, or milestones.** Compress source
   material; do not embellish it.
5. **Render every slide before delivery.** A valid PPTX can still have clipped
   text, broken fonts, or an ugly rhythm.

## Workflow

### 1. Establish the presentation brief

Write down the audience, decision, and speaking mode before touching the deck.
For a strategy presentation, choose a **Decide / Learn** composition: a small
number of ideas land in sequence. Do not use a report or dashboard composition.

Default story arc:

```
tension → strategic leverage → operating model → pillar moves
→ how the system compounds → delivery sequence → customer outcome → close
```

Use `references/executive-storyboard.md` for the slide-by-slide contract.

**Completion criterion:** every planned slide advances the story; no slide exists
only because a source document had a section heading.

### 2. Audit the source before redesigning

Extract the outline and render the existing deck. Inventory all source facts,
terminology, required labels, and visuals worth keeping. Distinguish:

- **Live-deck material:** tension, decision, strategic move, customer outcome.
- **Reference material:** exhaustive jobs, owners, dates, complete project lists.

Run the mechanical audit before and after editing:

```bash
python3 skills/presentation-redesign/scripts/audit_pptx.py \
  path/to/deck.pptx --min-font-size 28
```

**Completion criterion:** the design brief lists the facts that must survive and
the detailed material that moves out of the live story.

### 3. Distill copy before designing layouts

Write the slide headlines first. Each headline should make a claim or advance a
decision; it should not repeat a category name such as "Overview" or
"Customer outcomes."

Good live-deck pattern:

```text
Slide headline: Make the agent loop fast, governed, and programmable.
Evidence: Fast Terraform · Shift-left policy · tfctl
Customer change: Shorter wait, fewer scripts, earlier policy feedback.
```

Avoid turning every source paragraph into a bullet. Prefer a sharp sentence,
three named moves, and one consequence the audience can remember.

**Completion criterion:** an audience can explain the strategy from the headline
sequence without reading body text.

### 4. Build an intentional visual system

Start from the existing brand/template when one exists. Otherwise use a small,
high-contrast system:

- one accent color
- two background modes at most (for example, light analysis + dark chapter
  transitions)
- a deliberate type hierarchy
- a limited family of dividers, rules, and diagrams

Use dark slides as chapter transitions, not as decorative interruptions. Vary
compositions across the deck: a tension diagram, a capability flow, a timeline,
and an outcome slide should not all be card grids.

Do not use gradients, generic icon tiles, fake metrics, stock-art filler, or
rounded rectangles as a substitute for hierarchy.

**Completion criterion:** every slide treatment has a job, and repeated layouts
are reserved for repeated concepts such as pillars or timeline phases.

### 5. Remove empty PowerPoint placeholders

When creating slides from a layout, remove empty placeholders before adding
custom text. This fixes the editor-visible `Click to add title` defect.

```python
for shape in list(slide.shapes):
    if shape.is_placeholder and shape.has_text_frame and not shape.text.strip():
        shape._element.getparent().remove(shape._element)
```

Use the audit script to prove none remain. To remove them mechanically while
writing a new file:

```bash
python3 skills/presentation-redesign/scripts/audit_pptx.py \
  path/to/source.pptx --remove-empty-placeholders \
  --output path/to/cleaned.pptx --min-font-size 28
```

**Completion criterion:** the audit reports `empty_placeholders: []`.

### 6. Enforce projection-safe typography

Use 28pt as the hard floor. Typical working sizes:

| Role | Recommended size |
| --- | ---: |
| Cover or pillar headline | 56–72pt |
| Slide headline | 44–56pt |
| Primary claim / move | 32–40pt |
| Supporting explanation | 28–32pt |
| Anything smaller | Remove, merge, or move to the companion document |

Never solve overflow by shrinking text. Shorten copy, split the slide, or turn
the detail into an appendix.

**Completion criterion:** the audit reports no `small_text` findings at the
chosen threshold.

### 7. Render, inspect, and iterate

Use a real renderer and inspect every slide at presentation scale:

```bash
mkdir -p .pptx-render
soffice --headless --convert-to pdf --outdir .pptx-render path/to/deck.pptx
pdftoppm -png -r 144 .pptx-render/deck.pdf .pptx-render/slide
```

Review for:

- clipped or wrapped text
- contrast failures
- accidental empty space versus intentional pacing
- repeated composition
- title overlap
- missing or broken brand elements
- a story that becomes understandable only after reading the source document

Run `audit_pptx.py` again after the final render.

**Completion criterion:** every slide is presentation-readable, the narrative
works in order, the PPTX parses successfully, and the audit returns no defects.

## Common Patterns

### Strategy deck, not a report

Use 12–18 slides for a live executive deck. Keep the detail in a companion
roadmap. A good sequence uses a few sparse dark transitions to create pacing,
then lighter evidence slides to explain the move.

### Pillar architecture

For four strategic pillars, use this order:

1. Tension and strategic leverage
2. Four-pillar operating model
3. A transition plus one evidence slide per pillar
4. How the pillars compound
5. Delivery sequence and customer outcome
6. A closing portfolio test

### Reference material

If ownership or exhaustive project rows matter, place them in the Word roadmap
or a clearly separated appendix. Do not let a reference table become the
meeting's main slide.

## Troubleshooting

### `Click to add title` appears in PowerPoint but not the PDF

**Cause:** The layout created an empty title placeholder. Renderers usually hide
it; PowerPoint does not.

**Fix:** Remove the empty placeholder with the script or XML snippet in Step 5,
then reopen the actual `.pptx` and rerun the audit.

### Text fits in code but is unreadable on a projector

**Cause:** The deck was validated as a document rather than a live speaking
surface.

**Fix:** Raise text to at least 28pt. Remove secondary copy, split the slide, or
move it to the companion roadmap. Do not keep a tiny footer as an exception.

### Slides look polished individually but the deck still feels bad

**Cause:** The deck has no story or repeats one layout regardless of the idea.

**Fix:** Rebuild the outline from the tension, strategic leverage, pillar moves,
and customer outcome. Use a different composition for each idea type.

## Verification

Run all of the following before delivery:

```bash
python3 skills/presentation-redesign/scripts/audit_pptx.py \
  path/to/final.pptx --min-font-size 28
python3 -m zipfile -t path/to/final.pptx
```

Then render the final deck and inspect every slide. The audit must report zero
empty placeholders and zero text runs below 28pt.

## Resources

- `references/executive-storyboard.md`: Content and pacing contract for a
  12–18 slide strategy deck.
- `scripts/audit_pptx.py`: Checks font size, inherited text formatting, and
  empty PowerPoint placeholders.
