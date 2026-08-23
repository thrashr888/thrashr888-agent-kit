# SEO for copy-reviewed pages

Search guidance for when the surface is a web page. The governing rule:
**SEO lives in metadata and structure, never in the voice.** No sentence
gets longer to fit a keyword; copy that fails the tell check fails, and
searchability is not an excuse. Keyword-stuffed prose is itself a tell.

## Stage 1 additions — audit the search surface

When the surface is a web page, also check:

1. **Query vocabulary** — list the 3–6 phrases a searcher actually types
   for this product (category phrase, platform, the incumbent it replaces,
   the differentiator). Grep the page: does each appear at least once in
   prose that would survive review anyway? A page that never says its own
   category is invisible for it.
2. **Title tag** — name + category phrase, under ~60 characters. It is a
   copy surface; the register table applies.
3. **Meta description** — one plain-register sentence, ~150–160 characters,
   phrase up front. Missing on secondary pages is the common miss.
4. **One H1 per page.** A brand-terse H1 ("Your X, your Y.") is allowed
   only when the title tag, meta description, and lede carry the category
   phrase; otherwise the H1 must be descriptive.
5. **Canonical URL** on every page — especially on shared hosts
   (github.io, *.pages.dev) where duplicate paths resolve.
6. **OG/Twitter tags** with a real image, stated dimensions, and alt text.
7. **Structured data** — JSON-LD typed for the thing (SoftwareApplication,
   Article, …). The claims rules apply inside it: no aggregate ratings,
   review counts, or prices that aren't real.
8. **Anchored section ids** so deep links land, and descriptive alt text
   on every image, written in the house voice.

## Stage 3 additions — codify in WRITING.md

A web-surface WRITING.md gets an SEO section containing:

- The named query vocabulary for this product (the actual phrases).
- The metadata checklist above, with the project's real values as the
  examples.
- The competitor-naming rule: factual mentions are allowed once
  ("inspired by X, runs locally"); comparative superlatives ("the best X
  alternative") stay banned under the claims rules.
- The governing rule, verbatim: SEO lives in metadata and structure,
  never in the voice.

## Hard-won specifics

- The incumbent's name is usually the highest-value query term and the
  one the owner is squeamish about. Present it as a factual-mention
  option and let them decide; a page that never names the category
  leader forfeits every "X alternative" search.
- Meta descriptions are prose. The em-dash budget and tell check apply
  to them like any paragraph.
- One-page sites don't need robots.txt or a sitemap; canonical plus
  structured data do the work. Add a sitemap only when pages multiply.
