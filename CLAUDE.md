# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Vitnyr: the site of Igor Shatsev, an English coach in Yerevan who also
coaches chess and climbing as real disciplines in their own right (English
leads; see "Decisions" below). Four pages, home, `/english/`, `/chess/` and
`/climbing/`, plus a notes library at `/notes/`. Static HTML/CSS/JS, no
framework, no package.json. Live at `vitnyrcoach.com` on Cloudflare Pages:
`build.sh` copies the publishable files into `dist/` and minifies the CSS
and JS there; `functions/_middleware.js` rewrites the `<head>` of any
`?lang=ru` page for crawlers, which never run `theme.js`.

Repo: https://github.com/Brychenka/Vitnyr-v2 (branch `main`). This
`site-v2/` folder is the repo root. It has disappeared from local disk twice
(not recoverable from Trash either time); GitHub is its only backup.

`reference/` holds the source material: `onesignaturemove.pdf` (the design
guide v2 was built against) and `vitnyr-brand-identity.md` (colours, type,
logo geometry), whose only durable copies are here. The identity file is
stale on two points (it calls the coach "Leon" and frames English as
IT-first); the decisions below supersede it. Also there: the collage shot
list, the nav-icon design handoff and the portrait grade scripts.

The docs: `BUILD-NOTES.md` is the build log (what changed, when and why,
with the bugs worth remembering). `SITE-PLAN.md` is the one open work order:
the steps still to do and the questions only Igor can answer. Finished work
orders were removed on 2026-11-21; they are in git history.

## Working on this project: one chat per feature

Igor runs each feature or content change as its own chat, with this repo as
the shared backbone. A new chat should:

1. Read this file (loaded automatically), then `SITE-PLAN.md`, and
   `BUILD-NOTES.md` for anything it touches.
2. Branch before changing anything: `git checkout -b feature/<name>` off an
   up-to-date `main`. Don't commit straight to `main`.
3. Verify before calling it done: both themes, both languages, ~375px and
   ~1280px, `prefers-reduced-motion: reduce`, no console errors, no
   horizontal overflow, and the test suite. A preview pane often repaints
   only on demand, so don't trust a single screenshot for anything scroll-
   or time-driven; drive it with real frames.
4. Commit on the branch, then merge to `main` and push, so the next chat
   starts from a `main` that has the feature.
5. If the change is visible, republish the live artifact to the same URL,
   so the link Igor has stays correct.

**Live artifact:** `https://claude.ai/code/artifact/f516ba87-7ade-47a6-b65c-c5944147006c`
("Vitnyr Signature"). It holds all four pages: home (`index.html`) plus
`english.html`, `chess.html`, `climbing.html`, `style.css`, `theme.js`,
`main.js` and `assets/`. Build the bundle with
`python3 tools/artifact/build.py <repo> <out-dir>` (it reads committed files
only and rewrites root-absolute links to relative ones), then publish
`index.html` with the rest as `files` to the same URL. Never edit the
artifact's HTML directly. Read the live artifact before publishing (the tool
enforces this) so a concurrent chat's changes aren't clobbered.

## Running it

Serve the folder and open it:

```
python3 -m http.server
```

Then visit `localhost:8000`. The pages use root-absolute paths (`/assets/`,
`/english/`), so `file://` doesn't work. Fonts, GSAP and Lenis are served
from the repo (`assets/fonts/`, `assets/vendor/`); nothing loads from a third
party.

Tests: `tests/` holds Playwright tests (pytest), run with
`tests/.venv/bin/pytest tests -q` (about 6 minutes; it starts its own static
server; `open_site(path="chess/")` opens a discipline page). One known xfail
(`specimen-register` naming "please" in its visible explanation; the reason
is in `tests/test_content.py`); `test_collage_view_switcher` is
occasionally flaky and passes on a rerun. Run the suite before and after a
change and read every failure rather than bulk-updating. Tests are no
substitute for looking.

## Architecture

Shared files, each with one job, plus one HTML file per page:

- **`index.html`, `english/index.html`, `chess/index.html`,
  `climbing/index.html`**: each page's content, both languages inline (see
  i18n). Each carries its own head, JSON-LD and share card and loads the
  shared files by absolute path, with a `?v=` cache key per file (bump it
  on every change; `/assets/*` is cached for a year, so vendor and font
  files carry their version in the name). **The four-page rule:** the
  masthead, footer and contact section are copies, so a change to one goes
  to all four; `tests/test_seams.py` fails if they drift. `main.js`'s
  initialisers return early when their section is missing, which is how one
  script serves every page. `<!-- SWAPPABLE BLOCK -->` marks where a
  positioning change (Framing A vs. the current Framing B) would be a copy
  edit.
- **`notes/`** is generated: `python3 tools/notes/build.py` builds every
  note, the index, the sitemap entries and the share cards' text from
  `tools/notes/*.py` and the frame of `english/index.html`. Never edit
  `notes/**/index.html` by hand; re-run the generator after changing the
  English page's masthead, contact or footer (a test fails until you do).
  Adding a note: the checklist is in `SITE-PLAN.md` under H4.
- **`theme.js`**: loaded synchronously in `<head>`, render-blocking on
  purpose. Stamps `data-theme` (from the OS setting, or the reader's stored
  choice) and `data-lang` on `<html>` before first paint, writes the
  per-language canonical and Russian head tags, gates the wordmark on Lora
  having loaded, and fires `vitnyr:langchange` on a language switch.
- **`main.js`**: everything else, in one IIFE. Lenis smooth scroll on
  GSAP's ticker, the IntersectionObserver reveal, the hero's line-mask
  entrance, the pointer dot (one dot that is the cursor on a fine pointer
  and eases its fill to an accent over a control; colour only, never size),
  and a magnetic pull on non-text controls only (`.tool, .view__back,
  .origin__mark, .tools__hint`), never on text links. Plus the routed
  collage view and its lightbox, the specimen reveal and permalinks, the
  method fold, "Test your ear" (English), the who-rows' Telegram
  prefills and the phone contact bar.
- **`style.css`**: one `:root` token block (colours, fonts, easing,
  spacing) feeding every rule; no other file defines a colour or a
  duration.
- **`assets/collage/`**: the photo view's photographs, two widths each,
  grayscaled at display time by `--collage-filter`. **Every image is a real
  photo of Igor**; never add stock. The deferred `<picture>`/WebP half of
  `reference/collage-plan.md` is still undone.
- **`assets/share/`**: the share cards, exported from `share-card.html`
  (`?page=`, `?lang=ru`) at 1200x630; the edge function serves the `-ru`
  twin for `?lang=ru`. **`tools/engraving/`** generates the engraved
  plates and vignettes; regenerate rather than hand-edit their paths.

### i18n: dual-language DOM, not a template system

Every translatable string exists twice in the DOM:

- Short strings: `<span data-en="..." data-ru="...">`; `theme.js`'s
  `applyLang()` copies the right one into `textContent`. Never put
  `data-en`/`data-ru` on an element that has child markup (it would be
  flattened); put them on a span inside.
- Longer blocks: twin elements marked `data-l="en"` / `data-l="ru"`, the
  inactive one hidden by CSS. The hero title uses this, which is why
  `main.js` re-measures and replays the hero on a language switch (masked
  lines in the hidden language have zero height).
- Links whose target differs by language carry `data-href-en` /
  `data-href-ru` (the Telegram prefills).

Match whichever pattern the surrounding block uses; don't invent a third.

### The reveal/motion system

One easing curve: `cubic-bezier(.16, 1, .3, 1)`, defined once as `--e` in
CSS and once as the GSAP `CustomEase` `'brand'`. One reveal rhythm
(`.reveal`: 24px rise and fade, 0.9s, 0.08s stagger, once, via
IntersectionObserver). Don't add a second curve or reveal timing; extend the
`D` duration table in `main.js` if a new animation needs a duration.

**Layout must not occupy the transform channel.** The reveal is
`transform: translateY(24px)`, so anything offset or nudged for layout uses
grid placement, margins or `inset`, never `translate`. A layout transform
fights every animation on the same element: `gsap.set('.line__inner',
{y:'110%'})` once put `NaN` in GSAP's transform cache and every later tween
rendered nothing (see `BUILD-NOTES.md`). If a composition can only be built
with `transform`, say so and stop.

Everything animated is additive: with JS absent, GSAP missing or reduced
motion, the page renders fully readable. `.reveal`'s hidden state applies
only under `html.js`, and `failsafe()` in `main.js` force-shows anything
left stuck. An author `display` value beats the UA `[hidden]` rule, so
styles on hideable elements use `:not([hidden])`.

### Colour system (do not add a third colour)

Two fixed pairs, swapped wholesale by `data-theme`:

- `--bg`/`--fg`/`--fg2`/`--rule`: the theme pair (cream, or charcoal).
- `--amber` = the specimen (the mistake under examination), `--green` = the
  target (the correct form, interaction, an outcome). Use the semantic
  names `--ink-specimen` / `--ink-target` in component CSS.

`--cursor-active-ink` (the pointer dot over a control) is amber on cream
and green on charcoal: an alias to the two inks, not a third colour.

Accents are non-text ink only (rules, underlines, glyphs, display numerals),
**never text under 24px**: amber fails 4.5:1 on cream and green on
charcoal. The one exception, `.mark--specimen` / `.mark--target`, uses the
text-safe `--amber-text` / `--green-text`.

No gradients, no shadows, no rounded corners anywhere except the cursor dot
(`border-radius: 50%` on `.cursor__dot`), a deliberate exception.

### Wordmark SVG

The masthead and footer Vitnyr mark is hand-placed SVG (paths from the brand
pack, `<text>` at Lora's own advances); never regenerate or redraw it. It is
held at `opacity: 0` until `theme.js` confirms Lora has loaded
(`lora-ready`), because the letters assume Lora's exact widths.

## Outstanding and placeholder content

Search for `PLACEHOLDER`: the chess and climbing pages have no testimonials
yet, and some note fields wait on Igor. `SITE-PLAN.md` lists what is open
and the questions for Igor. There is deliberately **no static canonical**:
`theme.js` writes a self-referencing one per language (`/` or `/?lang=ru`)
off the x-default alternate; a static `/` canonical contradicted the
`?lang=ru` alternate.

## Content and positioning decisions (already made, don't re-litigate)

These came from Igor directly, so nothing in the code says them:

- **Real material only.** No invented clients, results, testimonials or
  statistics, ever. Every claim is real or a clearly marked placeholder.
- **The confirmed facts, worded this way:** 10 years coaching, 100+
  one-on-one clients, a **2100 peak rating** in chess, never with "FIDE"
  (Igor, 2026-11-21: his live rating moves between about 1950 and 2100, so
  the site says "peak" and the number links to his Lichess profile,
  `lichess.org/@/yngvibrychenka`), **7c redpoint indoor** and a **7C Kilter
  boulder** (two grades, never merged into one "7c"). Coaching outcomes, as
  the pages word them: **C2 · IELTS 9** (Igor's own English), **3 years / 30
  students to 1800+** (chess), **2 years / 13 climbers to 7a in a year**
  (climbing), **5,000+ analysed games** (the chess pattern bank). Nothing
  beyond these is asserted about outcomes.
- **"Igor Shatsev" everywhere, including in Russian.** Vitnyr is the
  umbrella brand, Igor Shatsev is the person; both stay visible.
- **Positioning: Framing B (broad), not Framing A (IT-first).**
- **Chess and climbing are full disciplines, weighted behind English**, not
  proof that the English method transfers. English leads: first door, the
  only page with testimonials (all real, from Igor's LinkedIn
  recommendations; the two in Russian show only on the Russian page).
- **A home page that sends people to a page per discipline** (2026-10-31).
  Home: hero (all three disciplines in the headline: "Every plateau / is a
  habit." / "Каждое плато — / это привычка."), §01 the mark with three
  doors (`#origin`) and the "See me at work" photo strip, the reviews, §02
  the method's five names, §03 contact. Every sentence on a discipline page
  must make sense to someone who only wants that discipline, and the page
  ends on contact: the closing "bridge" to the other two was removed
  (2026-11-23, Igor: redundant with the masthead and home). The
  masthead's three icons always link to the discipline pages; "Photos" and
  "Notes" are text links. New blocks are unnumbered, so the 01-05 counts
  stand.
- **The photo view is a routed view inside the home page**, not a separate
  page: `#collage`, deep-linkable, with its own header and way back, Back
  closes it, focus moves to its heading. Three groups, **English, then
  chess, then climbing**, unnumbered.
- **Contact channels: Telegram, LinkedIn, Instagram, in that order.** No
  prices on the site. Every contact section says what happens next (message,
  30-minute trial, a plan).
- **The theme follows the OS** until the reader picks one with the theme
  control.
- **Motion and the pointer:** Igor likes the magnetic pull on controls and
  the ticking numbers, but the facts row they animated was removed and
  the counter code with it; don't propose re-adding it.
- **Five specialist passes** (colour, logo, copy, type, motion) were done
  once (`BUILD-NOTES.md`); reuse the pattern for a change that touches
  several disciplines, not for a narrow one.
- **Not doing** (Igor and the council threw these out): an AI chat
  assistant, a booking calendar, a general blog, an Armenian version, video
  backgrounds or more motion, invented chess or climbing reviews, a third
  colour, splitting the brand. Real `/ru/` URLs and a template build are
  deferred until Igor asks (see `SITE-PLAN.md`).
