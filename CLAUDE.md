# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Vitnyr — a one-page marketing site for Igor Shatsev, an English coach in
Yerevan who also coaches chess and climbing as real disciplines in their own
right (English leads; chess and climbing are weighted secondary offers, not
proof-of-method — see "Content and positioning decisions" below).
Static HTML/CSS/JS, no build step, no framework, no package.json. Built
against a design guide called `onesignaturemove.pdf` (not in this repo);
`BUILD-NOTES.md` has the full phase-by-phase log, deviations from that guide,
and what's still outstanding (`og:url`/`og:image`/canonical still point at the
placeholder `vitnyr.example`, a below-the-hero visual check in a real browser).

Repo: https://github.com/Brychenka/Vitnyr-v2 (branch `main`). This
`site-v2/` folder is the repo root — there is no v1 in this repo; an earlier
four-page version was retired. It has disappeared from local disk twice
already (not recoverable from Trash either time) — it is not backed up
anywhere and should be treated as gone unless Igor says otherwise.

Reference source material lives in `reference/`: `onesignaturemove.pdf` (the
design build guide v2 was built against) and `vitnyr-brand-identity.md` (the
visual-identity spec — colors, type, logo geometry). Both used to live only
in `~/Downloads` as loose files and had already been lost once before being
copied in here; treat `reference/` as their only durable copy. The identity
file itself is stale on two points — it calls the coach "Leon" and frames the
English offering as IT-first — both **superseded by the decisions below**,
which is why this section exists.

## Working on this project: one chat per feature

Igor runs each new feature or content change as its own chat, with this repo
as the shared backbone between them. For that to work, a new chat should:

1. Read this file first — it's loaded automatically — plus `BUILD-NOTES.md`
   for the phase-by-phase build log and what's still outstanding. If there
   is an open work order, read it too: `JURY-PASS-II.md` (2026-09-12) holds
   the current staged plan, its standing orders, and — importantly — the
   findings that were **withdrawn or parked** because they collide with
   decisions already made. Check it before proposing a change to the main
   page, so a settled decision isn't re-opened as a fresh idea.
   Three further orders came out of a 2026-09-13 trifecta brainstorm. Igor
   dropped all three build plans 2026-09-15 — `TRIFECTA-A-SPECIMENS.md` and
   `TRIFECTA-C-MARK-NAV.md` are deleted outright; nothing in either was ever
   approved to build. `TRIFECTA-B-DOSSIERS.md` is kept, trimmed to its Stage
   B0 only: the positioning question it forced (**answered 2026-09-13:
   Weighted**, recorded below) and the still-open material-gap question
   (does real chess/climbing coaching material exist, is it bookable) that
   outlasts the retired order because any future chess/climbing feature runs
   into the same gap. A fourth idea (the mark as the page's index) was first
   drafted on `feature/navigator-order`; that draft is superseded — Trifecta
   Order D (`TRIFECTA-D-NAVIGATOR.md`) shipped all its stages to `main` on
   2026-09-15 and the mark now sits at §01.
2. Branch before changing anything: `git checkout -b feature/<name>` off an
   up-to-date `main`. Don't commit straight to `main`.
3. Verify before calling it done: both themes, both languages, ~375px and
   ~1280px, `prefers-reduced-motion: reduce`, no console errors, no
   horizontal overflow. The pane a chat previews in often repaints only on
   demand — don't trust a single screenshot for anything scroll- or
   time-driven; drive it with real frames (see `BUILD-NOTES.md`'s motion
   section for the pattern that surfaced real bugs this way).
4. Commit on the branch, then merge to `main` and push, so the *next* chat
   starts from a `main` that has this feature in it.
5. If the change touches anything visible, republish the live artifact —
   see below — **to the same URL**, so the link Igor already has stays
   correct instead of forking into a second, stale copy.

**Live artifact:** `https://claude.ai/code/artifact/f516ba87-7ade-47a6-b65c-c5944147006c`
(published as "Vitnyr Signature"). It's a single self-contained HTML file —
`style.css`, `theme.js`, and `main.js` inlined into `index.html` — because
the artifact host doesn't serve the repo's separate files. When republishing,
rebuild that inline version from the current repo files rather than editing
the artifact's HTML directly, or the two will drift. Read the live artifact
before editing it (the tool enforces this) so a concurrent chat's changes
aren't clobbered.

## Running it

No build or install step exists. Serve the folder statically and open it:

```
python3 -m http.server
```

Then visit `localhost:8000`. Opening `index.html` directly via `file://`
mostly works but skips the Google Fonts preconnect timing and some relative
paths are worth checking under an actual server.

There is no linter, but there is a test suite: `tests/` holds Playwright
tests (pytest), run with `tests/.venv/bin/pytest tests -q` (about 5 minutes; it
starts its own static server). It was brought back to fully green on 2026-09-21
(one known xfail, `specimen-register` naming "please" in its visible
explanation — see the reason in `tests/test_content.py`). Run it before and
after a change and read every failure rather than bulk-updating. Tests are no
substitute for looking, so also check manually: both
themes (Cream/Charcoal) and both languages (EN/RU), at both ~375px and
~1280px widths, with and without `prefers-reduced-motion: reduce`.

## Architecture

Four files, each with one job:

- **`index.html`** — all content, in both languages inline (see i18n below).
  Sections are marked with `<!-- SWAPPABLE BLOCK -->` comments where a
  positioning change (Framing A vs. the current Framing B) is meant to be a
  copy edit, not a restructure — the hero and the "who this is for" section.
- **`theme.js`** — loaded synchronously in `<head>`, render-blocking on
  purpose. Reads/writes `localStorage` (`vitnyr-theme`, `vitnyr-lang`) and
  stamps `data-theme` / `data-lang` on `<html>` *before first paint*, so
  there's never a flash of the wrong theme or language. Also gates the SVG
  wordmark behind a `document.fonts.load` check (see "Wordmark" below) and
  fires `vitnyr:langchange` on the document when the language switch button
  is used.
- **`main.js`** — everything else: Lenis smooth scroll wired into GSAP's
  ticker, the IntersectionObserver-driven reveal animation, the hero's
  line-mask entrance, animated counters, and the pointer dot — one dot that
  rides the pointer everywhere and eases its fill to the accent ink over a
  control (colour only — the 3× balloon was retired at C14). Plus a magnetic
  pull (`initMagnetic`) that nudges a hovered control toward the pointer:
  retired at C14, brought back at C16 scoped to non-text controls only
  (`.tool, .view__back` — the switches, collage icon-nav, "Back to top",
  "Back"; C17 adds the §04 `.origin__mark`), never on `data-magnetic` text
  links, which keep the dot's colour cue but no movement. `.origin__mark` is
  also a `.reveal` target, so `initMagnetic` hands the transform channel back
  from the reveal on first hover (`transitionProperty = 'opacity'`) — a
  transient transform releasing the channel, per the motion rules below. See
  `BUILD-NOTES.md`. Wrapped in one IIFE,
  no exports, no modules. GSAP + CustomEase + Lenis are loaded from CDN
  `<script>` tags in `index.html`, in that order, before `main.js`.
- **`style.css`** — one `:root` token block (colors, fonts, easing, spacing)
  feeding every rule below it; no other file defines a color or a duration.

Plus **`assets/collage/`** — the `#collage` view's photographs, two widths
each (`<slug>.jpg` ~450w, `<slug>@2x.jpg` ~900w), grayscaled at display time
by the per-theme `--collage-filter` token. As of 2026-09-06 these were
**temporary non-Igor placeholders** (see `assets/collage/PLACEHOLDERS.md` and
`BUILD-NOTES.md` → "Collage Stage 3"); chess and climbing are now real photos
of Igor, but the English group (6 frames) still ships on stock stand-ins.
**2026-09-17: Igor lifted the artifact hold** — no shoot is scheduled yet, and
he'd rather the live artifact track `main` in the meantime than sit stale, so
normal republishing (step 5 above) applies even while the English stand-ins
are still up. When the real shoot lands, swap the files, do the deferred
`<picture>`/WebP half of the Stage 3 spec (`collage-plan.md`), and republish
once more in that same pass.

### i18n: dual-language DOM, not a template system

There's no i18n library. Every translatable string exists twice in the DOM,
picked with CSS:

- Short strings: `<span data-en="..." data-ru="...">` — `theme.js`'s
  `applyLang()` copies the right attribute into `textContent` on load and on
  language switch.
- Longer blocks (paragraphs, headings that differ enough in length to need
  separate layout): two full elements marked `data-l="en"` / `data-l="ru"`,
  and CSS hides the inactive one: `html[data-lang="en"] [data-l="ru"] {
  display: none }`. The hero title uses this pattern, which is why `main.js`
  has to specifically re-measure and re-run the hero animation on language
  switch (masked lines in the hidden language have zero height and can't be
  measured until they're the visible ones).

When adding copy, match whichever pattern the surrounding block already
uses — don't invent a third mechanism.

### The reveal/motion system

Only one easing curve exists on the whole page: `cubic-bezier(.16, 1, .3,
1)`, defined once as `--e` in CSS and once as a GSAP `CustomEase` named
`'brand'` in `main.js`, so they can't drift apart. Only one reveal rhythm
exists (`.reveal` class: 24px rise + fade, 0.9s, 0.08s stagger, fires once
via IntersectionObserver, not scroll position — see the comment block above
`buildReveals()` for why ScrollTrigger was deliberately dropped for this).
Don't introduce a second easing curve or a second reveal timing; extend the
existing `D` duration table in `main.js` instead if a new animation is
needed.

**Layout must not occupy the transform channel.** The reveal is
`transform: translateY(24px)` and any parallax is a transform too, so
anything that offsets, overlaps or nudges an element for *layout* reasons
has to do it with grid placement, margins or `inset` — never `translate`.
A transform carrying layout has to be composed with every animation that
later targets the same element, and the two fight. This is not
hypothetical: the `gsap.set('.line__inner', {y:'110%'})` bug in
`BUILD-NOTES.md` put `NaN` in GSAP's transform cache and every later tween
on those elements silently rendered nothing. If a composition can only be
built with `transform`, say so and stop rather than taking the channel.

Everything animation-related is additive: with JS absent, GSAP failed to
load, or `prefers-reduced-motion: reduce`, the page must render fully
readable with no hidden content. That's why `.reveal`'s hidden state only
applies under `html.js`, and why there's a `failsafe()` sweep in `main.js`
that forces-shows anything left stuck.

### Color system (do not add a third color)

Two fixed pairs only, swapped wholesale via `data-theme` / prefers-color-scheme:

- `--bg`/`--fg`/`--fg2`/`--rule` — the theme pair (charcoal-on-cream or
  cream-on-charcoal).
- `--amber` = the specimen (the error under examination). `--green` = the
  target (correct form, interaction, achieved outcome). Referenced as
  `--ink-specimen` / `--ink-target` in component CSS — use those semantic
  names, not the raw color variables, when styling something new.

One derived alias exists: `--cursor-active-ink` (the pointer dot's fill over a
control) resolves to `--ink-target` on charcoal and `--ink-specimen` on cream
— Igor's call at C15, green read muddy on the warm ground. It's an alias to
the existing two inks, not a third colour.

Accent color (amber/green) is only ever used as non-text ink — rules,
underlines, glyphs, display numerals — **never as text under 24px**, because
amber fails 4.5:1 on cream body text and green fails it on charcoal body
text. This is verified and documented in `BUILD-NOTES.md`; don't reintroduce
small colored text without rechecking contrast in both pairs.

No gradients, no shadows, no rounded corners anywhere except the cursor dot
(`border-radius: 50%` on `.cursor__dot`) — that's a deliberate exception, not
a precedent.

### Wordmark SVG

The header/footer Vitnyr mark is hand-placed SVG (`<path>` glyphs from the
brand pack, `<text>` set at Lora's own advances) — comments in `index.html`
say not to regenerate or redraw it. It's held at `opacity: 0` until
`theme.js` confirms Lora has actually loaded (`lora-ready` class), because
the text nodes are positioned assuming Lora's exact letter widths and would
misalign in a fallback face.

## Outstanding / placeholder content

Search for `PLACEHOLDER`, `fill in`, and `.ch__todo`. The Telegram, LinkedIn
and Instagram handles are live in `index.html`; `og:url`, `og:image`, the
canonical/hreflang links, `sitemap.xml` and `robots.txt` still point at the
placeholder `https://vitnyr.example/` until the real domain exists. `BUILD-NOTES.md` lists these plus
what's been visually verified vs. only checked by measuring the DOM.

## Content and positioning decisions (already made — don't re-litigate)

These came out of direct conversation with Igor, not from the design guide or
the brand file, so nothing in the code will tell a new chat about them:

- **Real material only.** No invented clients, results, testimonials, or
  statistics — ever. Every claim on the page is either real or a clearly
  marked placeholder (see above). If a feature needs a proof point that
  doesn't exist yet, it gets a placeholder, not a plausible-sounding
  fabrication.
- **The three confirmed facts, worded exactly this way:** 10 years coaching,
  100+ one-on-one clients, a **2100 chess rating stated without FIDE**
  (Igor's own correction — don't add "FIDE" back in), **7c redpoint indoor**
  and a **7C Kilter boulder** (climbing grades, not to be merged into one
  generic "7c"). Nothing beyond these should be asserted about outcomes.
- **"Igor Shatsev" everywhere, including in Russian.** Igor was explicit:
  *"I need to be Igor Shatsev everywhere on the website."* Don't swap in
  "Vitnyr" or a transliteration as the personal name in either language —
  Vitnyr is the umbrella brand, Igor Shatsev is the person, and both stay
  visible together.
- **Positioning: Framing B (broad), chosen over Framing A (IT-first).**
  The brief's original open question. The `<!-- SWAPPABLE BLOCK -->` comments
  in `index.html` mark where Framing A would be a copy edit — the general
  "who this is for" rows plus the promotable `.it-row` — should positioning
  ever pivot, but that pivot hasn't happened and shouldn't be assumed.
- **Funnel/structure: single page, unified, trifecta in the hero headline.**
  v1 (now gone, see above) tried separate pages per discipline; v2 followed
  `onesignaturemove.pdf`'s one-page structure instead, and Igor approved
  keeping the English/chess/climbing trifecta together in the hero headline
  over a copywriter rewrite that would have led with English alone.
- **Positioning: chess and climbing are full disciplines, weighted behind
  English — not proof-of-method** (decided 2026-09-13, superseding the
  original credibility-anchor framing where the trifecta worked only as
  proof the English method transfers). English still leads and stays
  visibly the largest, first offer; chess and climbing are real, bookable,
  secondary disciplines with their own material — not disinterested evidence
  for someone else's coaching. This answers `TRIFECTA-B-DOSSIERS.md`'s Stage
  B0.1 with its **Weighted** option, not **Equal** — so §04's mark still
  rests with English (C6) and the raised dim floor (J7) both stay intact,
  and nothing about the hero, the JSON-LD `jobTitle`, or existing metadata
  changes on the strength of this decision alone (an "Equal" positioning
  would have forced all three). What still has to be answered before any
  future chess/climbing feature moves — see `TRIFECTA-B-DOSSIERS.md`'s
  remaining B0.2 — is the actual session material for chess and climbing
  coaching: does it exist yet, is it bookable today. Until that lands, this
  is a documentation-only change: don't restructure `#disciplines`, rewrite
  §06, or touch metadata on the strength of this decision alone. (B0.2 was
  since answered by Stage 5's real chess/climbing specimens, landing before
  the §04-into-§03 fold below — `#disciplines` no longer exists and contact
  is now §05, so read those two sentences as history, not current structure.)
- **One *file*, even where there's more than one view.** Igor asked for the
  photo collage as a separate page (2026-09-04), which qualifies the rule
  above rather than reversing it. The constraint that decides the shape:
  the live artifact is a single self-contained HTML file, so a second
  `.html` is unreachable from it and its content silently disappears from
  the link Igor already shares. So a "page" here is a full-screen view
  inside `index.html`, routed by URL hash, that *behaves* like one —
  deep-linkable, own header, own way back, browser back works, theme and
  language persist with no flash, focus moves to the destination heading on
  navigation (not just scroll — see the skip-link bug in `BUILD-NOTES.md`),
  and scroll resets. Apply the same reasoning to any future "separate
  page": ask what it does to the artifact before splitting a file. Inside
  that view, the photos are grouped into three domain sections —
  **English, then chess, then climbing** (2026-09-05), unnumbered so the
  view doesn't continue the page's 01–05 count. See `BUILD-NOTES.md`'s
  "Collage → three domain groups" entry and `reference/collage-shotlist.md`
  (v2).
- **Contact channels: Telegram, LinkedIn, Instagram, in that order** — Igor's
  own answer when asked. Real handles are still outstanding (see above); the
  order and the choice of exactly these three platforms is settled.
- **Five specialist review already done once** (`BUILD-NOTES.md`'s "The five
  specialist passes" section: colour, logo, copy, type, motion) — a useful
  pattern to reuse for a future feature that touches several disciplines at
  once, but don't assume it needs repeating for a narrow, single-discipline
  change.
- **§04 "Three domains" was folded into §03 Specimens, not deleted**
  (2026-09-18, page-length concern from Igor). §01's origin mark and §03's
  specimens already establish English/chess/climbing as three separate real
  disciplines, so a standalone fourth section re-arguing the same point was
  cut length rather than content — but chess's and climbing's eligibility
  bar, session format, and "coaching runs now" availability line (the only
  parts of §04 that weren't duplicated elsewhere) moved into their own
  `.specimens-group` in §03 rather than being deleted with the rest. English
  lost its §04 card outright since it duplicated the hero. See
  `BUILD-NOTES.md`'s "§04 'Three domains' folded into §03 Specimens" entry
  for the full before/after. Don't propose re-adding a standalone domains
  section without knowing this was a deliberate merge, not an oversight.
