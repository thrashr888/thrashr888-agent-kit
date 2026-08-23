---
name: copy-review
description: Review user-facing copy (websites, release notes, README, in-app strings) for machine-sounding writing, then codify the owner's voice in a repo WRITING.md. Use when asked to check copy for AI-isms, make text "read human", review marketing or landing-page text, fix writing that "sounds like AI", or set up a writing style guide. Not for project documentation structure (plans/specs/RFCs) — that's style-docs.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Copy Review

Turn "this reads like AI wrote it" into a repeatable process: review, let the
owner pick a voice, codify it as law, and gate future copy with a script.

Run the stages in order. The order is the point — fixing before the owner
picks a voice produces copy in *your* voice, which is the problem being
solved.

## Stage 1 — Review and report. Do not fix.

Extract every user-visible string from the surface (strip tags, decode
entities). Read it against the tell list:

1. **Em-dash pivots** and density above ~1 per paragraph
2. **Repeated-head-word triples** ("real X, real Y, real Z")
3. **One sentence architecture stamped across parallel items** — table rows
   or bullets that all run praise-pivot-caveat
4. **Winking at the reader** ("data instead of vibes", memes, swagger)
5. **Internal vocabulary on a public surface** — codenames, harness/tier/
   pipeline words the team uses but a visitor doesn't know
6. **Idioms recurring across documents** — the author's verbal tics
   (collect any the owner has flagged before; they repeat)
7. **Stacked adjectives** ("fastest accurate citations") and dangling
   comparatives ("best citations tested")
8. **Encoding artifacts** — `â` or `Ã` in rendered text means a byte-level
   edit double-encoded a UTF-8 file; fix the encoding, never the strings
9. **Search surface** (web pages only) — missing canonical, meta
   description, or structured data; a page that never says the phrases a
   searcher would type for it (see `references/seo.md`)

Report findings ranked by how loudly they read machine-made, and say which
sections are already clean. Stop there. The owner decides what changes.

## Stage 2 — Offer voices, one table per finding

For each flagged passage, present 3–5 rewrites in named brand voices chosen
for the audience. Reliable menu (see `references/voices.md` for the cheat
sheet): Google (plain benefit), Vercel (clipped, stat-forward), HashiCorp
(sober precision), Apple (two-beat headlines), Linear (quiet craft), Stripe
(measured technical), Tailscale (dry candor).

The owner picks **per row**, not one voice for everything. The picks are
data: they reveal that register scales with surface (headlines vs body vs
methodology vs micro-copy usually want different voices).

## Stage 3 — Codify the voice as WRITING.md

Write the inferred pattern into a repo-root `WRITING.md` — the writing
counterpart to a design system doc. Use `references/writing-md-template.md`
as the skeleton. It must contain:

- A register-by-surface table built from the owner's actual picks, with one
  live example each
- Sentence mechanics: the em-dash budget, the parallel-items rule, which
  of the owner's existing lines are grandfathered exceptions (name them)
- A vocabulary table translating the project's internal terms to public
  words
- Claims rules: numbers only when measured, baselines named, failures
  reported as plainly as wins
- For web surfaces: an SEO section — the named query vocabulary, the
  metadata checklist, and the rule that SEO lives in metadata and
  structure, never in the voice (see `references/seo.md`)
- The tell check from Stage 1, as a pre-publish checklist

Reference it from the repo's agent instructions (CLAUDE.md / AGENTS.md) so
every future session loads it.

## Stage 4 — Apply, then gate with the script

Apply the picked rewrites and vocabulary translations. Give parallel items
different sentence shapes as you go. Then run the mechanical check:

```
python3 scripts/tell-check.py <file-or-dir> [--banned words.txt]
```

It scans for encoding artifacts at the byte level, banned words, em-dash
density, repeated-head triples, and any terms from the vocabulary table
still present. Run it even on copy you just wrote — the spec catches its
own author, reliably. A human skim still matters afterward: the script
knows yesterday's tells, the reader finds tomorrow's.

## Hard-won specifics

- **Edit UTF-8 files with UTF-8-aware tools.** A `perl -pi` one-liner that
  emits a wide character into a byte stream double-encodes the whole file;
  the damage shows up later as `â` mojibake on the live site. Python with
  explicit `encoding='utf-8'` is safe; verify with a byte-level scan after.
- **Grandfather deliberately, not silently.** If the owner's own writing
  breaks a rule (a hero-line tricolon), name it in WRITING.md as the
  exception. Unexplained exceptions erode the rule.
- **Owner tics are per-owner.** Maintain the banned-words list from what
  they flag in review ("honestly", a pet idiom); these recur far more than
  generic AI phrases.
- **The acid test** for any sentence that survives the checklist: if it
  could open a LinkedIn post, rewrite it.
