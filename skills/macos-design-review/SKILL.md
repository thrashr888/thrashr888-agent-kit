---
name: macos-design-review
description: Audit a macOS app against native-Mac behavior using the six-clause "Mac formula" (system settings, menu bar, keyboard, undo, direct manipulation, state restoration), then fix and triage. Use when asked to review an app "as a Mac app", check HIG or macOS conventions, audit the menu bar / keyboard reach / undo / drag-and-drop / window state, or distill Apple's principles into a DESIGN.md. Not for web-page interface checks (web-design-guidelines) or visual/accessibility-only passes (rams).
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# macOS Design Review

Distill Apple's macOS principles into one testable formula, audit the app
against it with parallel read-only agents, then split the findings into
fix-now, backlog, and doc-rot. Works on any macOS app with a searchable
frontend (Tauri, Electron, Swift/AppKit); examples assume a webview app.

The formula — Apple's HIG behavioral principles in one line:

> **The system is law, the menu is the index, the keyboard is complete,
> undo beats confirm, objects are direct, state survives.**

Each clause distills specific Human Interface Guidelines pages — the
official citations, clause by clause, are in `references/apple-sources.md`.
Cite them when the owner asks where a rule comes from; consult them for
edge calls the briefs don't cover.

Visual style is deliberately out of scope: a repo's own DESIGN.md owns
look-and-feel. This skill audits *behavior* — the part that makes an app
feel native regardless of its visual language.

## Stage 1 — Anchor the formula in the repo

If the repo has a DESIGN.md (or equivalent), add a short section stating the
formula and one 2–3 line rule per clause, each cross-referenced to rules the
doc already has — prescriptive but never fictional (check the code first:
does a native menu exist? does anything persist state?). End the section
with the tiebreaker: **"When a rule here conflicts with a web idiom, the Mac
wins."** If there is no design doc, put the section in CLAUDE.md instead.
This anchor is what future agents (and Stage 2's auditors) cite.

## Stage 2 — Fan out the audit, one agent per clause

Launch parallel **read-only** subagents, one per clause, each returning
findings with `file:line` evidence, worst first, no fixes. Full briefs with
search checklists and classification rubrics: `references/clause-briefs.md`.
The one-line version of each:

1. **System is law** — hardcoded px type, animations over the repo's
   duration cap or unguarded by `prefers-reduced-motion` (including
   rAF/WebGL loops the CSS guard can't reach), hardcoded colors, handlers
   that intercept ⌘C/V/X/Z/A/F outside editors.
2. **Menu is the index** — inventory the native menu, inventory the app's
   actual commands and shortcuts, diff both directions. Also diff the menu
   against any in-app shortcuts list; hand-maintained parallel lists drift.
3. **Keyboard is complete** — clickable non-buttons without a keyboard
   path, hover-only reveals without focus-within, icon buttons without
   labels, overlays without Escape/focus-restore, mouse-only affordances
   (selection toolbars raised on `mouseup`, drag-only canvases).
4. **Undo beats confirm** — list every confirm dialog and every destructive
   action; classify each as recoverable or not. The two violation shapes:
   confirms guarding recoverable acts (tell: dialog copy that argues the
   action is safe), and unrecoverable acts with no guard at all.
5. **Objects are direct** — right-click coverage per object type, menu
   parity across views of the same object, drag-in, drag-out, copy/export
   coverage, and actions the API/agents can take that the UI cannot.
6. **State survives** — window geometry persistence, panel/selection/draft
   restore, scroll position, navigation history, in-progress text flush on
   quit.

## Stage 3 — Synthesize

Write one consolidated review: a per-clause verdict paragraph (lead with
whether the clause holds), findings ranked by severity, and a separate
**outright bugs** list — things broken regardless of the formula (double-
bound shortcuts, dead menu items, shadowed system shortcuts, stacked-dialog
Escape). Keep `file:line` on every claim. Also list **doc rot**: design-doc
rules that mandate deleted helpers or contradict the code — a stale rule
makes future agents write broken imports.

## Stage 4 — Triage with the owner

Present three tiers and let the owner pick the cut line:

- **Fix now** — the outright bugs, plus any unrecoverable destroy with no
  confirm and no undo (user-authored config deleted on a single click is
  the classic case).
- **Backlog** — everything else, filed in the owner's tracker (bd issues,
  Apple Reminders, GitHub issues — match their habit), one item per theme,
  each self-contained with `file:line` pointers so a future session needs
  no context from this one.
- **Doc fixes** — update the design doc where it lies about the code.

## Stage 5 — Fix and verify

For the fix-now tier:

- Prefer the smallest mechanism the codebase already has. Example: a toast
  system with an optional click handler is a complete undo affordance —
  snapshot the deleted object, delete immediately, restore on click.
- Static analysis only ever says "risk" for runtime behavior. Before
  reporting a keyboard/menu/focus bug as confirmed — and after fixing it —
  verify live (for Tauri apps, the driving-tauri-apps skill). Say plainly
  which findings were verified live and which are still static inferences.
- Run the repo's full quality gates before handing back.

Webview-specific traps that recur in these fixes:
`references/webview-gotchas.md`.

## Optional seventh sweep — system integration

When the owner asks for maximum thoroughness, add one more agent: Services
menu, Spotlight/Quick Look, share sheet, dock menu, Handoff, and
sheets-vs-windows conventions. Most apps legitimately skip most of these;
flag only absences that contradict what the app already claims to be.
