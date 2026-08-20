# WRITING.md template

Skeleton for the Stage 3 deliverable. Fill every bracket from the owner's
actual picks and the project's actual copy — a template with generic
examples teaches nothing.

```markdown
# WRITING.md

Source of truth for all user-facing words: [surfaces this covers]. The
companion to [DESIGN.md or equivalent] — that file governs how the product
looks; this one governs how it talks.

## The voice

[Two or three sentences. Who is speaking, to whom, and what they never do.
Derive from the pick pattern, not from aspiration.]

## Register scales with the surface

| Surface | Register | Model | Example |
| --- | --- | --- | --- |
| Headlines, card titles | [e.g. two beats, then stop] | [brand] | "[real line from the project]" |
| Body paragraphs | [e.g. plain declarative, numbers inline] | [brand] | "[real line]" |
| Methodology, claims, footnotes | [e.g. sober, zero personality] | [brand] | "[real line]" |
| Table cells, chips, micro-copy | [e.g. clipped fragments] | [brand] | "[real line]" |

Fragments are a micro-surface tool. In a paragraph, write sentences.

## Sentence mechanics

- Em dashes: at most one per paragraph, never as a dramatic pivot.
- Parallel items get different shapes — N table rows must not share one
  sentence template.
- [Grandfathered exceptions, named: e.g. "the hero tricolon stands".]
- One idiom per document, maximum.

## Vocabulary

| Internal | Public |
| --- | --- |
| [team term] | [visitor term] |

Banned outright: [owner's flagged tics], [project-specific banned words],
exclamation points.

## Claims

- Every number is one we measured, stated with its baseline and where to
  reproduce it. No number, no claim.
- Report failures as plainly as wins.
- Round to the precision the sample size supports.

## The tell check

Before publishing, run `[tell-check command]` and scan for:
1. Em-dash pivots and density above ~1 per paragraph
2. Repeated-head-word triples
3. One sentence architecture stamped across parallel items
4. Winking at the reader
5. Internal vocabulary on a public surface
6. Idioms recurring across documents
7. Encoding artifacts (`â`, `Ã`)

If a sentence could open a LinkedIn post, rewrite it.
```
