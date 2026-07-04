---
name: building-local-ai-apps
description: Design patterns for local-first AI desktop apps — provider abstraction (Ollama / OpenAI-compatible gateways), RAG retrieval and ingestion hygiene, citation UX that loops back to sources, streaming and scoped cancellation, chat-loop details, and demo-corpus design. Use when building or reviewing a local AI app, a RAG/notebook product, chat UX, or preparing AI product demos. Distilled from Alchemy (a local NotebookLM clone).
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Building local-first AI apps

Patterns from building a NotebookLM-style desktop app (Tauri + React + LanceDB + Ollama/gateway).
Organized product-outward: providers → retrieval → citations → streaming → chat loop → demos.

## 1. Provider abstraction

- Route chat through a facade that speaks **Ollama OR any OpenAI-compatible gateway**
  (`/chat/completions`, `/models`, Bearer). Keep embeddings and OCR independently swappable
  (local Ollama, a bundled CPU model like Model2Vec/potion, or the gateway) — users on weak
  hardware want cloud chat with **local embeddings** so their documents never leave the machine.
- **Make all UI provider-aware.** Don't show "Ollama offline" to a gateway user who doesn't run
  Ollama; branch status copy and health checks on the active provider.
- **Reverse-engineering a gateway's real endpoints/auth:** its official CLI is usually a
  downloadable npm/JS bundle — `grep` it for the API host, paths, auth header scheme, and
  model-list shape. (IBM Bob: LiteLLM under the hood; static `bob_` keys use `Authorization:
  Apikey` + `X-API-KEY`, JWTs use `Bearer`; chat needs `x-instance-id`/`x-team-id` from
  `/admin/v1/profile`; usage endpoints are SSO-gated → link to the portal, don't fake accounting.)

## 2. Retrieval (RAG) patterns

- **Top-k retrieval biases to the largest sources** (more chunks = more chances), so corpus-level
  questions ("what documents do I have?") can miss small sources entirely. Not an embedding bug.
  Fix: inject the **full source-title manifest** into the system prompt, separate from the
  per-question excerpts.
- **Waterfill the corpus budget across sources** for whole-notebook generation instead of
  head-truncating (which silently drops later sources): allocate smallest-first so leftovers
  flow to bigger sources; mark truncation explicitly in the prompt.
- **Word-window chunking** (~280 words, ~40 overlap) is model-agnostic and good enough; store the
  chunk text on the citation so the UI never needs a second lookup.
- Chat + generation should return **numbered citations** the model must use (`[n]` hard-required
  in the system prompt), persisted with the message.

## 3. Ingestion hygiene

- **Duplicate detection at ingest, before embedding.** Same content in a collection silently
  poisons retrieval (the duplicate occupies top-k slots). Prefilter by char count, then exact
  content compare; fail with a friendly "Already here as \"Title\"". For URLs, fail fast on an
  exact URL match *before* fetching — "use Refresh instead".
- **Friendly display titles.** Filenames, slugs, and arXiv IDs make terrible titles and starve
  the source manifest. Heuristics first (markdown: first `#` heading), then a tiny LLM completion
  ("reply with only a 3–8 word title" + first ~1500 chars + filename). **Best-effort only** —
  titling must never fail an import. Skip when the name already contains whitespace (human-written).
- Store failed imports as error rows the user can see and retry, not silent drops.

## 4. Citation UX — close the loop

A citation that dead-ends at a snippet builds no trust. The full loop: inline marker → click →
source opens **scrolled to the highlighted passage**.

- **Inline `[n]` markers → clickable chips.** In react-markdown, a tiny dependency-free remark
  plugin walking mdast text nodes: regex `\[(\d{1,2})\]`, replace with `#cite-n` links (only for
  n ≤ citations.length; skip inside links/code), render via the `a` component override as
  superscript chip buttons with a hover preview (source title + snippet start).
- **Locating the passage in the source is a whitespace problem.** Chunks are space-joined word
  windows; stored content keeps newlines — so exact substring search fails. Match
  whitespace-tolerantly: regex-escape the first ~12 words joined with `\s+` to find the start,
  the last ~12 words (searched only within the chunk-length window) for the end. Highlight the
  range, `scrollIntoView({block:'center'})`.
- Add **find-in-source** (case-insensitive match count, prev/next, Enter cycles) — reading tools
  make the reader a feature, not a modal.
- **Drop raw similarity scores from the UI** (`1 - distance` means nothing to users).

## 5. Streaming and cancellation

- Stream **everything users wait on**: chat tokens *and* document generation (emit
  `artifact://token` events into a live preview that follows its tail). A spinner for a
  3-minute PRD reads as broken.
- **Scope cancellation tokens per activity** (`"chat"`, `"artifact"`) in a
  `HashMap<String, CancellationToken>` — one global token means starting a chat kills the running
  document build. Race with `tokio::select!`; a user-initiated stop is an *info* toast, not an error.
- On cancel of streamed chat, keep the partial text.

## 6. Chat-loop details that separate polished from janky

- **IME guard:** `if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing)` — without
  `isComposing`, CJK users send mid-composition.
- **Keep the composer typable while a response streams**; gate only submit.
- **Suggested follow-ups fill the composer** (and focus it) instead of firing immediately — users
  want to edit.
- **Failed sends hand the prompt back** to the composer; never eat typed text.
- Autoscroll only when already near the bottom; jump to latest on first load of a conversation.
- Destructive deletes go through an in-app confirm (never native `window.confirm`); wrap CRUD store
  actions in a shared `guard()` so backend failures surface as toasts instead of silent no-ops.
- Auto-open generated documents where the user acted; hide badges that repeat the title; strip a
  leading markdown heading from card previews so the title isn't shown twice.
- Harden one Modal (role, aria-modal, labelled-by, focus trap + restore, Escape) and every dialog
  inherits the a11y.

## 7. Demo corpus design (for screenshots and sales demos)

Fabricate an interlocking document set for a fictional company; design it so every feature has a
money shot:

- **6–9 documents of different types** (roadmap, customer interviews, metrics review, pricing,
  press-release draft, competitive intel, support report, capacity notes) that cross-reference the
  same numbers, names, and dates — grounded answers then cite *multiple* sources.
- **Plant 2–3 discoverable contradictions** (a price that differs between pricing doc and press
  release; a GA date that differs between roadmap and PR) so "find problems" features and
  contradiction questions surface real conflicts. Keep everything else consistent so *only* the
  planted conflicts fire.
- Include **quotable verbatims** (customer quotes, support tickets) — answers that quote read great.
- Name one file as a slug (`eng_capacity_h2_notes.txt`) to demo auto-titling; give markdown files
  clean `#` headings.
- Add a "not in the sources" question to the demo script to show honest refusal.
- Write a `DEMO-SCRIPT.md` with setup steps, per-feature questions, and where the planted
  conflicts are.

## Related skills

- `shipping-tauri-apps` — building, signing, and releasing the desktop shell.
- `driving-tauri-apps` — automating the running app for verification and screenshots.
