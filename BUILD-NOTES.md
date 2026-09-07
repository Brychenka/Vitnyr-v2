# Vitnyr v2 — "One Signature Move" build

Built against `onesignaturemove.pdf`. Phase mapping below, then what still
needs you. v1 (four static pages) is untouched in `../site/`.

    index.html   style.css   theme.js   main.js   assets/   favicon.ico

Run it: `python3 -m http.server` in this folder, then open localhost:8000.

## Guide phases

| Phase | Guide asks for | Built |
|---|---|---|
| 0 | Static HTML/CSS/JS, GSAP + ScrollTrigger + Lenis via CDN | done, versions pinned — ScrollTrigger since dropped, see deviation 2 |
| 1 | Real content before design | reused the voice-checked v1 copy, RU + EN |
| 2 | Two typefaces, type scale, judged at rest | Lora display / Inter body / JetBrains Mono for labels and specimens |
| 3 | Smooth scroll + one reveal rhythm | Lenis; 24px rise + fade, 0.9s, 0.08s stagger, once, at 20% into view |
| 4 | Pick ONE signature move | custom cursor + magnetic targets — the guide's own recommendation for limited content |
| 5 | Polish pass | hover / focus-visible / active on every control, scaleX underlines, one curve everywhere |
| 6 | Respect the reader | prefers-reduced-motion path, no layout shift (18 collage images added Stage 3, all `loading="lazy"` + ratio-boxed) |
| 7 | Ship | not deployed — see below |

`cubic-bezier(.16, 1, .3, 1)` is the only easing on the page, as `--e` in CSS
and a matching GSAP CustomEase in JS, so the two never drift apart.

## Three deliberate deviations from the guide

1. **No `mix-blend-mode: difference` on the cursor.** A difference blend over
   charcoal invents colours the brand doesn't own, and the brand forbids a third
   colour. The cursor is a flat dot that eases its fill to the accent ink over
   interactive elements instead (green, or amber inside `#specimen`) — colour
   only, no size change (reworked at C14; was a green ring). The active ink is
   `--cursor-active-ink`: target green on charcoal, specimen amber on cream
   (C15); `.is-specimen` inside `#specimen` stays amber in both.
2. **ScrollTrigger is not loaded at all.** Reveals were always on an
   IntersectionObserver — a scroll-position tween sits at opacity 0 if its rAF
   loop never runs, and an observer is the right shape for "has this entered
   view once". That left ScrollTrigger driving three counters and nothing else,
   so the counters moved onto the same observer and the plugin came out: 40KB
   less, one scroll mechanism instead of two. Lenis still drives the scroll.
3. **Two accents kept off small text.** The section numbers and the eyebrow
   separators started amber/green and were moved to neutral: amber is 3.07:1 on
   cream and green 3.58:1 on charcoal, both below the 4.5:1 floor at 12px.
   Accent colour lives in ink — rules, glyphs, the display numerals. (One
   narrow, later exception: see "Accent-as-text exception" below.)

## What still needs you

- **Contact handles.** Telegram, LinkedIn, Instagram are `@TELEGRAM_HANDLE`-style
  placeholders with a "fill in" chip. Replace the `href` and the visible text
  together; delete the `.ch__todo` span.
- **Domain + share card.** `og:url` and `og:image` are marked PLACEHOLDER in the head.
- **A portrait, if you want one.** The build is typography-led because the brand
  bans stock photography and no real photo was supplied.
- **Client stories.** None invented. Nothing in the page claims anything beyond
  8 years, 100+ clients, a 2100 chess rating (stated without FIDE, as you asked),
  and 7c — redpoint indoor, and a 7C Kilter boulder.
- **Positioning.** Still Framing B. The hero and the "who this is for" block are
  marked `SWAPPABLE BLOCK`; Framing A is a copy edit, not a rebuild.
- **The `#origin` ("Name & mark") section's etymology needs your sign-off.**
  `reference/vitnyr-brand-identity.md` defines the mark's geometry and colours
  but never states what "Vitnyr" means or where it comes from. The section
  currently reads it as Old Norse `vit` (sense, understanding) + `nýr` (new) —
  a proposed compound, not a sourced one. Confirm, correct, or replace before
  this ships; "real material only" applies to etymology the same as to client
  claims. The mark's "V and Y fused" reading stays the *official* one per the
  brand file; the "three strokes = three disciplines" reading is Igor's own
  addition on top of it, not a replacement, per his 2026-09-05 direction.
## The five specialist passes

**Colour.** Accent is semantic, not decorative: **amber marks the specimen** —
the thing being examined — and **green marks the target**: an interaction, a
progression, an outcome reached. Nothing else gets colour. Five shipping
contrast failures were found and fixed by moving accent out of text and into
ink. Cream was judged not too bright: the hex is right, the hairlines were
under-weighted. At `.16` the cream rules read ~7% weaker than charcoal's `.14`;
`.20` matches on both contrast (1.482 vs 1.466) and lightness step (ΔL* 14.36
vs 14.45).

**Logo.** The lockup is `clamp(176px, 13vw, 208px)`, and the masthead's height
is derived from it rather than guessed. The mark's ink is only **67% of its SVG
box** — the remaining 33% *is* the brand's required quarter-height clear space,
so the box must never be trimmed to the ink. Conversion, if you need it:
mark ink height = 0.18416 x lockup CSS width.

**Copy.** Run through the humanizer pass: less pitch, fewer stock constructions,
no claim the page can't stand behind. The hero headline is the one rewrite
rejected — the trifecta stays, by your call.

**Type.** Inter / Lora / JetBrains Mono confirmed as the right three, but the
roles were tightened: the eight 12px labels moved from mono to sans (mono at
label size was texture, not meaning), and mono now means one thing only —
**quoted linguistic material**. `font-synthesis: none` so no weight or slope is
ever faked. The wordmark is held at opacity 0 until `document.fonts.load` says
Lora is real, because it is live SVG text sitting at Lora's own advances and
would otherwise paint a redrawn wordmark in a fallback face.

**Motion.** Audited and rebuilt where it was wrong:

- The hero `<h1>` could stay invisible forever on a background-tab load. Every
  timed thing now waits behind a first-frame gate, and a re-armed guard shows
  the headline outright if it is ever still masked 2.5s after a play.
- `playHero()` ran twice on a cold load, the second call snapping mid-flight
  lines back. Guarded on language, and the initial language stamp is no longer
  treated as a change.
- Reveals were observed **per section**, so items up to 1059px below the fold
  had already finished animating before they were scrolled to. Now observed per
  element, ordered by screen position, with the stagger chain capped at 4 beats.
- `has-cursor` was applied before a cursor existed, hiding the native pointer
  with nothing in its place. It now goes on with the first real pointer move.
- Magnetic pull was a hard snap: `.channels a` sat pinned at maximum across
  97.3% of its width with a 24px sign flip across the centre, while
  `.langswitch` barely moved, and a diagonal reached 17px on a 12px setting.
  The field is now normalised to each element's own size and the **vector** is
  scaled rather than each axis clamped, so 12px is a real ceiling. Measured
  after: pinned across 24.9% instead of 97.3%, no sign flip, `.langswitch` moves
  7.9px, nothing exceeds 12px, and displacement returns to 0 continuously at the
  field edge instead of dropping off a cliff.
- `getBoundingClientRect()` ran on every mousemove, forcing a reflow and feeding
  the element's own displacement back into its next reading. Measured once on
  enter, with the current translate subtracted.
- The reset `gsap.to` fought the live `quickTo`. It is now the same tween,
  retargeted to zero.
- The skip link scrolled but never moved focus, which is the entire point of a
  skip link. Fixed for every in-page link.
- The cursor's `quickTo` double-smoothed an already-lerped value; it is a
  `quickSetter` now. Its rAF loop parks itself when the dot has caught up
  instead of running forever.
- `will-change` was permanent on 12 elements, including under reduced motion.
  Asked for on hover, and on the hero lines only while they are moving.
- Five duration tiers, and nothing between them.
- One genuine easing exception, marked in the stylesheet: the scroll cue's
  `nudge` loop. `--e` is an ease-out, and an ease-out on a keyframe loop that
  returns to its start snaps at the midpoint. A symmetric hint needs a
  symmetric curve, so that one is `ease-in-out`.

One bug surfaced that predates the audit: `gsap.set('.line__inner', {y:'110%'})`
was hitting the hidden-language twins, and a percentage of a zero-height box
leaves `NaN` in GSAP's transform cache — after which every later tween on those
elements renders nothing. The Russian headline would have stayed masked after a
language switch. Only the lines actually on screen are tweened now.

## Copy/colour re-audit (2026-09-05)

The copy and colour passes above predate the collage view (built 2026-09-04/05),
so its text had never been through either. Re-ran both against the whole page
as a check, not a rebuild:

- **Colour.** Clean. Every accent use still traces to the specimen/target rule:
  the four `.facts .n` numerals and the wordmark are the only places colour
  sits directly on text, and both clear the WCAG large-text 3:1 floor at their
  30px/56px sizes. Everywhere else — the `.mark` phrases, the wrong/right rows
  — colour stays in non-text ink (underline, border, glyph), per the 24px rule
  already documented above. No new colour was introduced.
- **Copy.** The collage lede (`#collage .view__lede`, EN+RU) had a run-on: "What
  goes here is how Igor Shatsev actually works: ... — and the two places the
  same method gets tested" mixes a manner-clause with a place-list off one
  "and", which the rest of the page's shorter sentences don't do. Tightened to
  "What's here is Igor Shatsev at work: ... — the two places the same method
  gets tested" in both languages. Also added the view's first `.mark`
  (`a rating and gravity` / `рейтингом и гравитацией`) so it echoes the same
  motif the Disciplines section states ("two things that don't negotiate: a
  rating, and gravity") — six marks on the page now, still exactly one
  coloured. See the `.mark` comment in `style.css`. No other section needed a
  copy change; the original humanizer pass already holds up.

## Accent-as-text exception (2026-09-05)

The line above ("still exactly one coloured [mark]") no longer holds — this
same day, later, added a second, narrower exception to deviation 3 above
("Two accents kept off small text"). Recorded here rather than editing that
entry, so the reasoning survives instead of just the outcome.

**What changed.** Two places now put accent colour directly on text under
24px, where it had never been used as text before:

- The Method section's one target phrase (`.mark--target`) lost its
  underline and is now green text outright.
- Inside each Specimens wrong/right pair, the exact word responsible for
  the error is amber, and the exact word that fixes it is green
  (`.mark--specimen` / `.mark--target` on a bare `<span>`, no `.mark`).

**Why these and nothing else.** An earlier draft the same day coloured
several more "key" words — the hero's "grammar drills", a list/sentence
contrast in Feedback Loops — and both were cut. Neither is a specimen under
examination or a target reached; colouring them was decoration borrowing
the specimen/target costume without the meaning, and it diluted the two
places where colour is actually load-bearing. The bar that survived: colour
only the word that *is* the specimen or *is* the target, never a word that
merely feels important.

**Contrast, done properly.** Deviation 3's numbers are correct but
incomplete — they only checked the ink hex reused as-is, which fails 4.5:1
in exactly one theme per colour (green 3.58:1 on charcoal, amber 3.07:1 on
cream). The fix isn't picking a theme to leave broken: `--amber-text` /
`--green-text` (top of `style.css`, one definition per theme) are the same
hue tuned to clear 4.5:1 specifically in the theme where the ink hex
doesn't — amber darkened for light, green lightened for dark — while the
ink hex itself keeps carrying every non-text use (rules, glyphs, the
wordmark) completely unchanged. Verified: 7.41:1 (amber/dark), 4.50:1
(amber/light, tuned), 4.50:1 (green/dark, tuned), 5.62:1 (green/light).

**Honest argument against.** The blanket rule was simpler and already
verified once; this trades it for two more custom hex values a future
palette change has to remember to re-tune, and for a naming split
(`.mark--target` now means two different things depending on whether it's
paired with `.mark`). Worth it here because the specimen/target section is
the page's actual teaching mechanism and scans measurably faster in colour
— but this is not a licence to colour more words elsewhere on the same
reasoning; re-read the "why these and nothing else" note above first.

**Superseded the same day.** The tuned `--amber-text` numbers above assumed
amber still swapped per theme (`#D99B3F` dark / `#B07C24` light). The
"single darker amber" fix later that day (see below) fixed `--amber` at
`#B07C24` everywhere, which changes what `--amber-text: var(--amber)`
resolves to in the dark pair — it now resolves to `#B07C24` there too,
still clearing 4.5:1 (4.9:1, down from 7.41:1, still comfortably over the
floor) so no further change was needed, but the "7.41:1 (amber/dark)"
figure above is stale. `--green-text` is untouched by that fix.

## Collage nav icons (2026-09-05)

Design handoff (chess checkerboard-corner / screw-lock carabiner / open book,
final set chosen in that file's turn 4) copied into
`reference/design_handoff_collage_nav_icons/` — it lived only in `~/Downloads`
as a loose zip first, same failure mode `reference/`'s other two files were
copied in to avoid. Implemented the "looks" half only, per Igor's request:
SVG paths pasted verbatim into `nav.tools`, `.tool` class and its existing
underline/hover reused as specified, no new colour values.

Testing this at 375px surfaced a real bug, not a hypothetical one: flexbox
was shrinking the wordmark `.lockup` below its brand-mandated 176px floor to
make room for the new icons, rather than letting `.tools` overflow. Fixed
with `flex: none` on `.lockup` (`style.css`) — the mark holds its width now,
`.tools` gives way instead. Once protected, Cream/RU plus three icons at the
handoff's own coarse-pointer touch-target padding (44px targets) don't fit
in one row below ~600px no matter how tight the gaps get, so below that width
`.tools` wraps onto its own right-aligned line and `--head` grows to match
(same media query, `style.css`). Verified no horizontal overflow at 320 /
375 / 600 / 601 / 1280px, both themes.

**Behaviour half (2026-09-05).** The "behaviour" section of the handoff is
now done — Igor: *"take the nav bar icons and attach them to the respective
place on the collage … make transition smooth."* Each button gained
`data-collage-jump="chess|climb|en"`; `main.js` `initCollageView()` wires
them to open `#collage` (via the same `pushState` + `sync(false)` the
`data-collage-open` link uses) and then `view.scrollTo({ top, behavior })`
to that group — `behavior: 'smooth'` normally, `'auto'` under
`prefers-reduced-motion`. The scroll runs synchronously in the click
handler, not inside a `requestAnimationFrame`: `applyOpen` has already
flipped `.collage-open` (visibility/opacity only, so geometry is live) and a
deferred frame can be suspended in a background tab. The scroll target is the
group's **`.label`** (not the group's edge) minus the sticky `.view__bar`
height minus a 16px gap, clamped at 0 — the label carries the clicked glyph,
so it's what should arrive at the top; anchoring to the group edge instead
parks the label below its 44–88px `padding-top`, which only reads right when
you scroll in. Focus then moves to the group's `<h3>`, which gained
`tabindex="-1"` and the same `:focus` / `:focus-visible` outline pair as
`#collage-title`. The click handler also `focus()`es the button before
opening, so `applyOpen` captures it as `returnFocus` and Back returns to the
icon in every browser (a plain mouse click doesn't focus a `<button>` in
Safari). Each group's `.label` gained the matching glyph (`.label--glyph`
wrapper + `.label__mark`, path data echoing the masthead but not locked to
it — the label copy is the smaller, quieter instance — sized `1.15em` off
the 12px label, inked `--fg2`). The buttons' `aria-label` / `title` stay
English-only, matching the doc's other structural labels (`nav aria-label
="Site"`, the lockup) — `theme.js` localises visible text, not `aria-label`.
Verified: jump + focus for all three from cold and warm state, both themes,
EN/RU (glyphs persist across the language switch), 375 / 1280, deep-link
still lands focus on `#collage-title`, Back / Esc / browser-back unaffected,
no horizontal overflow.

`test_collage_nav_icons.py` updated in the same change: the accessible-name
list now expects the action phrasings ("Jump to the chess photographs" …),
and `test_icon_buttons_have_no_click_wiring_yet` is replaced by
`test_icon_buttons_jump_to_their_collage_group` (parametrized per domain)
plus `test_icons_do_not_open_the_view_on_load`. (The `…_17px` size test was
renamed to `…_19px` on `main` in a separate commit before this landed.)

## Collage → three domain groups (2026-09-05)

Igor asked the collage view to stop being one mixed grid and become three
labelled sections — **English, then chess, then climbing** (the site's order:
English is the offer, the other two prove the method transfers). Each group
carries ~6 placeholder figures, so the view goes from 6 reserved boxes to 18.

- **Composition retired.** Stage 2's asymmetric 12-column grid with one
  deliberate overlap is gone. Each group is now a plain repeating grid —
  1 column, then 2 at ~600px, then 3 at ~900px — no offsets, no negative
  margins, nothing in the transform channel. `--collage-drop-a/b/d` and
  `--collage-overlap` deleted; `--collage-gap-x/y` added. Base
  `.collage__fig / __slot / __wait / figcaption` and the three ratio
  modifiers were reused unchanged.
- **Structure.** Three `<section class="view__group">` inside `.view__body`,
  each with an unnumbered `.label` domain word, an `<h3>` (`id` =
  `collage-en / -chess / -climb`, `aria-labelledby` target), a one-line
  `.view__group-lede`, and a `.collage.collage--group` grid. The router's
  focus target (`#collage-title`, the `<h2>`) is untouched, so `main.js`
  needed no change.
- **No `.reveal` added.** The collage view has never used the reveal system
  (it is display-toggled, not scrolled into); all motion stays Stage 4. This
  keeps `test_a11y`'s "no hidden reveals" invariant clean.
- **Copy.** The `.view__lede` was reworded from "two places" to "the three
  places the same method gets tested: an English lesson, a rated game, a
  graded climb" (its one `.mark`). New h3s + per-group ledes carry the
  confirmed facts in their own words — 2100 rating without "FIDE", "7c
  redpoint" and "7C Kilter" kept distinct. Every RU string is a model draft,
  flagged for Igor in `collage-shotlist.md`.
- **Shot list rewritten** to v2: `reference/collage-shotlist.md` now lists 6
  shots per domain at a fixed 2×`4:5` / 2×`3:2` / 2×`1:1` mix, new filenames
  (`en-* / chess-* / climb-*`), and a revised weight budget (≤90 KB per `@2x`
  WebP, ≤1.6 MB total). `collage-plan.md` gained a Stage-2-reopened note.
- Tests: no changes needed. `test_collage.py` is behavioural (routing, focus,
  inert, no-JS fallback); `test_i18n`'s parity sweep and `test_layout`'s
  collage-overflow check cover the new nodes automatically.

## Collage Stage 3 — placeholder images (2026-09-06)

Igor: real photos are weeks out, *"use stock photos and move on with the
stages … we'll replace them later."* So Stage 3 shipped against **temporary
stand-ins, not photographs of Igor** — a documented, bounded exception to the
"real photographs of Igor Shatsev only" rule in `collage-shotlist.md` and
`CLAUDE.md`'s real-material rule. The exception is scoped:

- **Repo + local preview only.** The live "Vitnyr Signature" artifact is
  **not** republished off this — a link other people open must not show
  stand-in people under Igor's first-person captions. Artifact republish
  waits for the real shoot (`collage-plan.md` Stage 6 already says so).
- Sources: `en-02`–`en-05` from Openverse (CC0 1.0); the other 13 from
  `loremflickr.com` (Flickr-CC proxy) after Openverse rate-limited the batch.
  Full provenance + the swap contract in `assets/collage/PLACEHOLDERS.md`.
- Every `<img alt>` is empty and no `<figcaption>` names the stand-in — the
  captions describe the *intended* shot and come true when the real files land.

What actually changed in the build (this part is real and stays):

- 18 `.collage__wait` hairline boxes → `<img>` with `srcset` (`450w`/`900w`),
  `sizes`, explicit `width`/`height` per ratio, `loading="lazy"`,
  `decoding="async"`. The `<picture>`/WebP half of the Stage 3 spec is deferred
  to the real-photo swap (no WebP encoder on the build box; JPEG-only stand-ins
  aren't worth a `<source>` that gets rewritten anyway).
- `en-01` stand-in retired: the figure goes back to the shot list's `--32`
  and the slug becomes `en-01-call`, restoring English to the 2/2/2 ratio mix.
- Ratio classes untouched, so the box is reserved before decode — **zero CLS
  holds**: measured 238×159 / 238×238 / 238×298 boxes identical before and
  after the images loaded.
- Grayscale is the existing per-theme `--collage-filter` token; `.collage
  __slot:has(img)` drops the chip padding. Both already in CSS from Stage 2 —
  no CSS change this stage.
- Weight: 1.52 MB across the 18 `@2x` JPEGs (budget ≤1.6 MB). Four detailed
  `1:1`/`4:5` tiles sit at 100–137 KB, over the ≤90 KB per-image line — fine
  for throwaways, to be met by real optimised WebP at swap time.
- Verified: `#collage` open, all 18 resolve (200 from the static server; the
  preview pane doesn't fire `loading="lazy"` without compositing, so they were
  force-loaded for the check), no console errors, no horizontal overflow at
  375 / 1280, grayscale filter live in both themes, RU captions render.
- Tests: still behavioural, no change. `test_layout`'s collage-overflow check
  and `test_i18n` parity cover the new `<img>` nodes.

**Note for the swap:** the view's own intro still reads *"Ни стоков, ни
постановки"* / "No stock, no staging" — true again only once the real photos
are in. Don't republish the artifact before then.

## Collage Stage 4 — motion (2026-09-06)

The 18 tiles now run the page's one reveal rhythm — 24px rise + fade, 0.9s,
the `brand` curve, 0.08s stagger, capped at 4 beats, fired once — off the
**collage view's own `overflow:auto` root**, not the document viewport.

Why a second observer instead of just adding `.reveal`: `#collage` is
`position: fixed; visibility: hidden` until it opens, so the page's
viewport-rooted observer would report all 18 as "in view" at load and burn
the whole entrance while nobody is looking (this is the exact reason Stage 2
recorded *not* adding `.reveal`). So:

- `buildReveals()` now excludes `#collage` (`!el.closest('#collage')`), and
  the batch→stagger step is factored into a shared `fireReveals()` so both
  observers run the identical rhythm.
- `armCollageReveals(view)` — called once from `applyOpen()` on first open —
  strips the shipped `.is-in`, then observes the tiles with an observer whose
  `root` is the view (`rootMargin: '0px 0px -10% 0px'`). It also calls
  `armFailsafe()` so a missed tile is still force-shown.
- Tiles **ship `class="… reveal is-in"`** in the markup: visible with JS
  absent, under `prefers-reduced-motion` (the existing `@media reduce`
  neutraliser already covers `.reveal`), and while the view is closed — so
  they never count as a "stuck" reveal in `test_a11y` / `test_motion`.
  `armCollageReveals` early-returns under reduced motion, leaving `.is-in` on.
- `applyClose()` puts `.is-in` back on every tile, so a reopen lands on a
  settled view rather than a half-run stagger; tiles the observer hasn't
  reached yet stay observed and still catch up on scroll.

No parallax (Stage 4's optional half): nothing here needs it, and it would be
the first thing on the page to put layout in the transform channel of a
grid. No CSS change — `.collage__fig` takes the existing `.reveal` rules as
is; `transform: translateY(24px)` on a grid item is paint-only, so **zero CLS
still holds**. GSAP/ScrollTrigger untouched (ScrollTrigger stays out).

Tests: four added to `test_collage.py` — tiles visible before open + excluded
from the page set, reveal-on-scroll inside the view, inert under reduced
motion, settled on reopen. Full suite green.

## Collage Stage 5 — signature move / polish: nothing added to the tiles

Stage 5's brief was to decide *whether* the tiles join the signature move
(custom cursor + magnetic targets), recommend before wiring, and accept "we
added nothing" as an outcome. They get nothing, on purpose:

- **The tiles aren't interactive.** They're supporting imagery in a captioned
  `<figure>` — no link, no click target, `alt=""` with the `<figcaption>`
  carrying the words. A hover or magnetic affordance would advertise a
  behaviour that isn't there.
- **`data-magnetic` on an image tile reads as a bug**, not an affordance —
  the plan's own caution. The magnetic vector is normalised to element size
  and capped at 12px; on a ~460px tile that is a small, unexplained drift.
- **No focusability.** Adding `tabindex` would plant empty keyboard stops
  with nothing to do at them.
- **No grayscale→colour on hover.** The obvious portfolio move, but colour is
  a governed resource here (`--collage-filter` is the deliberate constraint,
  amber/green carry meaning) — reversing it on hover breaks that on the
  page's largest elements.

The signature move is already present in the view where it belongs: the
custom cursor renders above it (`z-index 90` vs the view's `60`), and
`.view__back` + the view-bar `.themeswitch` already carry `data-magnetic`.
No code change this stage; nothing to re-verify beyond the coarse-pointer
floor the suite already holds (`has-cursor` never applies, native pointer
never hidden at 375px).

## Collage Stage 6 — verify + document (2026-09-06)

Ran CLAUDE.md's step-3 checklist over Stages 3–5:

- Playwright suite **90 passed** (4 new collage-reveal specs; 10 pre-existing
  `.themeswitch` strict-mode failures on `main`, from the collage-view theme
  switch, fixed in the same series).
- Both themes: grayscale `--collage-filter` resolves in Cream and Charcoal.
- Both languages: RU captions + ledes render; `test_i18n` parity green.
- 375 and 1280: no horizontal overflow (`scrollWidth === clientWidth` on the
  view and the document at both); grid collapses 3→1 column cleanly.
- `prefers-reduced-motion`: tiles sit at rest, `armCollageReveals` early-
  returns (`test_collage_reveals_are_inert_under_reduced_motion`).
- No console errors. Zero CLS (ratio boxes measured identical before/after
  decode).
- Diff audit (`0604b8c..HEAD`, code files): no new hex, gradient, shadow, or
  `border-radius`. `style.css` untouched since Stage 2.

**Not done, on purpose:** the live "Vitnyr Signature" artifact is **not**
republished — it stays on the pre-placeholder version until real photos of
Igor land. Merge of `feature/photo-collage` to `main` + push is left for
Igor's go-ahead (the branch also carries `584a167`, the `Claude outputs/`
edit intermediates he asked to keep on a branch).

**Cosmetic, placeholder-only:** a few LoremFlickr stand-ins carry a small
baked-in `cc` badge / attribution strip in the corner. Gone when the real
files replace them; not worth re-fetching a throwaway over.

## Collage view theme switch (2026-09-06)

Igor: *"Make a collage page also have a cream/charcoal switch."* The open
collage view is `position: fixed; z-index: 60`; the masthead (which carries
the only Cream/Charcoal control) is `z-index: 40`, so once the view was open
the theme couldn't be changed. Fix: a second `.themeswitch` button in the
`.view__bar`, grouped with Back inside a new `.view__tools` flex cluster
(`gap: clamp(16px, 3vw, 30px)`) that mirrors the masthead's `.tools` row —
footmark holds the left, tools sit at the right. Reuses the `.tool` class
(same 12px uppercase, `--fg2`, green `::after` underline) and `data-magnetic`,
so it's the masthead button in a second place, not a new style.

`theme.js` changed from `querySelector('.themeswitch')` to `querySelectorAll`
in both `labelTheme()` and the DOMContentLoaded click wiring, so every
`.themeswitch` is labelled and wired and the two stay in lockstep. No new
storage, no new state — both buttons call the same `save(THEME_KEY, …)` +
`applyTheme()`. The RU label path (`Крем` / `Уголь`) already came from
`labelTheme()`, so the collage button localises for free. `langswitch`
stays masthead-only (out of scope; Igor asked for theme only).

Verified: switch from inside the open view flips both button labels and the
`data-theme` attribute, persists across navigation (localStorage), both
languages, 375 / 1280, no console errors, bar doesn't overflow at 375px.
Live artifact "Vitnyr Signature" rebuilt from current repo files and
republished to the same URL.

## Awwwards-jury review, Stage 2 — reveal + payload fixes (2026-09-06)

A jury-style pass over the finished build ("Vitnyr Jury Sheet", 33 findings)
was turned into a staged plan ("Vitnyr Work Order"), both published as
artifacts outside this repo. Stage 1 (pull the placeholder photos, restore
the shot list's own documented empty-box state) is **deliberately skipped for
now** — the work is a draft nobody has asked to publish yet, so there is no
artifact hold to lift. Stage 2 is the two blockers that don't touch the
collage photos at all:

**B3 — the scroll cue was invisible until you'd already started scrolling.**
`.hero` is `min-height: 100svh`, so `.hero__foot` (the `.stand` paragraph and
`.scrollcue` link) sits near the bottom of the viewport at rest. `buildReveals()`
ran every `.reveal` off one `IntersectionObserver` with `rootMargin: '0px 0px
-20% 0px'` — correct for content below the fold the reader hasn't reached,
but it cuts a dead zone across the bottom 20% of the viewport, and the hero
foot sat inside it. Proved at 800/900/1080px viewport heights before touching
code: `.scrollcue` measured `opacity: 0` at rest at all three. Fix: the hero's
`.reveal` elements (`el.closest('.hero')`) are handed to a second observer
with `rootMargin: '0px'` — the true viewport — while everything else keeps
the `-20%` margin. `main.js`'s `fireReveals()` is unchanged and shared by
both observers, so the stagger rhythm is identical either way.

**B4 — the 18 collage figures downloaded on every visit, never displayed.**
The `#collage` view is `opacity: 0; visibility: hidden`, not `display: none`
(needed so the fade-in transition has something to animate), and the
browser's native `loading="lazy"` schedules by distance from the viewport —
a `position: fixed; inset: 0` panel over the same viewport reads as "close
enough," so all 18 images fetched on ordinary page load regardless of the
`lazy` hint. Measured: 1,231 KB of images on a visit that never opens the
collage. Fix: the figures ship as `data-src`/`data-srcset` (inert to the
browser's own loader) with a `<noscript>` sibling carrying the real
attributes for the no-JS path; `main.js`'s `applyOpen()` now calls
`promoteCollageImages(view)` on first open, copying `data-src`/`data-srcset`
onto `src`/`srcset` so the fetch only happens once someone actually looks.
Built now rather than deferred to the real-photo swap — the same bug returns
the moment the placeholders are replaced with heavier real photographs, and
the `<img>` markup shape (data-src, noscript twin) doesn't change either way.

Both bugs were reproduced as failing tests against pre-fix `main` before the
fix landed (`git stash` the two source files, run the new specs, confirm red,
restore, confirm green) rather than asserted from reading the code:
- `test_motion.py::test_hero_foot_is_visible_at_rest_without_scrolling` (800 /
  900 / 1080) — failed at 800 and 900 pre-fix (`.scrollcue` opacity 0), passed
  at all three post-fix.
- `test_collage.py::test_collage_images_are_not_fetched_before_the_view_opens`,
  `test_collage_images_promote_and_fetch_on_first_open`,
  `test_collage_images_have_noscript_fallback_in_markup` — 15 of 18 images
  fetched on load pre-fix (LoremFlickr URLs vary, so the exact count isn't
  stable — the `0` assertion is what matters), 0 noscript fallbacks in the
  markup; 0 on load / 18 on open / 18 fallbacks post-fix.

Full suite: **96 passed** (90 + 6 new). No `<picture>`/WebP/AVIF work here —
that's still the real-photo swap's job (`collage-shotlist.md`), and nothing
in this stage's markup shape needs to change when it happens.

**Not done:** the live "Vitnyr Signature" artifact is not republished — the
placeholder-photo hold from Collage Stage 3 stands regardless of Stage 2's
own changes, and this stage's work is a draft, not something Igor has asked
to ship yet.

## Awwwards-jury review, Stage 3 — accessibility pass (2026-09-06)

Seven findings (C1–C4, C7, P5, P11), branch `feature/a11y-pass`. Same hold as
Stage 2: not republished, draft only.

- **C1 — language switch missing from the collage bar.** The open view sits
  above the masthead (z-index), so its `.themeswitch` copy (added earlier)
  was the only Cream/Charcoal control reachable while it's open — but there
  was no `.langswitch` there at all, so a Russian-reading visitor stuck in
  English inside the view had no way back without leaving it. Added a second
  `.langswitch` to `.view__tools`; `theme.js`'s `applyLang()` and its click
  wiring changed from `querySelector('.langswitch')` to a `querySelectorAll`
  loop, the same pattern `labelTheme()` already used for `.themeswitch`, so
  every copy stays labelled and wired. Six existing tests drove the single
  masthead button with a bare `.langswitch` selector, which now matches two
  elements and throws in Playwright's strict mode — rescoped to
  `.masthead .langswitch`; added a test that actually clicks the in-view
  copy and confirms the language, the masthead's own copy, and the group
  heading underneath all follow.
- **C2 — text touch targets under the 24px WCAG 2.2 minimum.** Measured
  `.themeswitch`/`.langswitch` at 76×23 / 19×23 and `.view__back` at 70×31
  on a coarse pointer, beside icons calculated to exactly 44×44. Extended
  the icons' existing `@media (pointer: coarse)` block: `padding-block` for
  height (keeps the flex row's baseline from moving — no `height` property
  involved) plus a small `padding-inline` on `.tool`, since two letters at
  12px can't reach 24px width through vertical padding alone. Order in the
  stylesheet matters — `.tool--icon`'s own coarse rule has to come after
  `.tool`'s or its uniform 12.5px would be overwritten. New tests hold both
  axes to ≥24px for all three controls on a `has_touch` context.
- **C3 — heading levels skip and duplicate.** `#collage-title` was an `h2`
  and its three group headings were `h3`s, both one level under where they'd
  sit if `#collage` were a real page — which the routing already treats it
  as (CLAUDE.md's "behaves like its own page" note). Promoted title to `h1`,
  groups to `h2`, and wrapped `.view__body` in `<main id="collage-main">`
  (the site's own `<main id="main">` keeps its id — the two are never both
  exposed, since `#app` goes `inert` while the view is open and the view
  itself is `visibility:hidden` while closed). `test_single_h1_and_main_landmark`
  asserted a raw DOM count of 1, which the new architecture makes 2 by
  design; rewrote it to check what's actually reachable (no `inert`
  ancestor, not `visibility:hidden`) rather than raw count, and added the
  mirror case for the view open.
- **C4 — §05 "Who this is for" skips straight to four `h3` rows with
  nothing governing them.** Every other section pairs its `.label` with a
  `.sec__head` `h2`; this one didn't, leaving four answers with no question
  a heading-level screen-reader pass would land on first. Added
  "Which of these is you?" / "Какой из этих случаев — про вас?" as a new
  `h2`, following the section's existing dual-`data-l` pattern. New copy,
  not yet Igor-reviewed — flagged the same way the shot list flags its own
  draft copy.
- **C7 — the origin mark's focus ring was suppressed outright.** The three
  `.origin__hit` buttons are invisible, oversized rectangles laid over the
  glyph so touch and keyboard both have a real target; a ring drawn on one
  of them wouldn't trace anything visible, so `:focus-visible { outline:
  none }` was the whole answer, relying on the dim/active glyph contrast
  alone to mark focus — which isn't a focus indicator. Moved the ring to
  `.origin__mark` (the `<figure>` a reader can see) via
  `:has(.origin__hit:focus-visible)`, already an established pattern in this
  file (`.collage__slot:has(img)`). New test confirms the ring appears on
  the figure and stays off the hit rectangle itself.
- **P5 — the register specimen's hidden labels overstated the claim.** The
  third specimen ("Register, not grammar") is grammatically fine on its
  "wrong" line — the fault is pragmatic, not a grammar error like the other
  two — so labelling it "Incorrect:" alongside them was inaccurate. Gave it
  its own visually-hidden pair, "Reads as:" / "Better as:"; the other two
  specimens keep "Incorrect:"/"Correct:" since those are real grammar
  errors. Updated `test_specimen_rows_have_text_equivalent_for_correctness`
  to expect both pairs and to check the register specimen specifically.
- **P11 — alt text was deferred wholesale to the real-photo swap.** Wrote a
  bilingual draft (EN/RU) for all 18 frames directly into
  `collage-shotlist.md`, beside each shot's brief, so alt text lands with
  the file instead of being drafted after the fact under time pressure. Flagged
  alongside the shot briefs as a model's first pass — Igor's to confirm, not
  yet wired into `index.html` (there's nothing to wire it to until the real
  files replace the placeholders).

The findings with real logic behind them (the h1/main landmark split, the
origin-mark focus ring, the specimen labels, the touch-target sizes) were
confirmed failing against pre-fix `main` before the fix landed, not just
asserted from reading the code. Full suite: **101 passed** (96 at the end of
Stage 2 + 5 new).

## Awwwards-jury review, Stage 4 — commit to the three ideas (2026-09-06)

The one stage that changes the ceiling rather than the floor: C10, C11, C5,
C6, C13, branch `feature/signature-moments`. Two decisions were put to Igor
before building — the specimen redesign's size (there wasn't really a
choice on the table, more a go/no-go on the largest single visual change in
the plan) and the cursor fix's shape (two real alternatives) — both
confirmed before writing any code.

- **C10 — the specimens, the page's own "showpiece," ran at 14px mono in a
  cramped third of a 1320px page.** Rebuilt `.specs` as full-width rows —
  same shape as `.rows` in section 05 (hairline stack, one column of
  content beside another rather than stacked) — with the wrong/right
  sentence pair in its own `.spec__lines` wrapper at `clamp(17px, 1.7vw,
  20px)` and the explanation beside it instead of below. The ✕/✓ glyph
  moved to `em` sizing so it scales with the pair instead of sitting
  fixed-small next to now-larger text. New tests hold the pair to ≥17px and
  check the two columns actually sit side by side at ≥900px, stacked at
  375px.
- **C11 — the specimen's wrong/right lines had no gap between them.**
  `.wrong` and `.right` are adjacent `.line-spec` boxes with padding but no
  margin, so a 2px amber rule ran straight into a 2px green one with zero
  space between — one stroke changing colour halfway down, right where the
  error/fix distinction is the entire point of the device. Fixed with
  `.line-spec + .line-spec { margin-top: 12px }` — margin between the two
  boxes, not padding inside either. New test measures the gap.

  **Correction, caught before shipping this note:** the first pass of this
  stage misread C11 as being about the origin mark instead — its amber V and
  green stem *do* meet at a shared vertex and read as one two-tone shape
  where overlapping fills touch, but that's a different defect this sheet
  never separately numbered. The keyline described below was built and
  tested under the wrong label; it stays, because it's real and the tests
  for it are real, but it's C5's fix extended, not C11. This entry and the
  code comments were relabelled once the mistake surfaced.
- **C5 — two defects in the same mechanism, plus one extra fix alongside
  them.** Dimming was `opacity: .32`, which blends with whatever renders
  behind a shape — including the *other* glyph part it overlaps at the
  mark's shared vertex. Replaced with explicit solid
  `--amber-dim`/`--green-dim` tokens per theme (full opacity, a real colour
  that can't bleed into a neighbour), landing close to the old opacity look
  by design. Separately, the stem carried a `scale(1.1)` on activation that
  the two arms structurally can't get (they're clipped halves of one shared
  path; scaling would tear the clip from the mark underneath) — dropped
  instead of extended, so colour is the one feedback channel all three hit
  regions share. Alongside both: a thin `--bg`-coloured `stroke: 1.25px` on
  every `.glyph__part`, painted last in DOM order (the stem sits after both
  arms), cuts a clean edge at that same overlapping vertex without moving a
  single path coordinate — the "never redraw this mark" rule holds, since
  it's the interactive `.origin__mark` instance carrying the class, not the
  wordmark. New tests check the dimmed fill is solid (`opacity: 1`, an exact
  token colour), that the stem's `transform` no longer changes on
  activation, and that the keyline's `stroke` resolves to `--bg`.
- **C6 — the mark's resting state was neutral, not a choice.** `clearPaint()`
  stripped every class, so before any hover/focus (and permanently, under
  reduced motion, where the idle hint never runs) the glyph sat at equal
  weight and the stat panel was blank. English is the offer; chess and
  climbing are proof it transfers, not equal-weight alternatives.
  `clearPaint()` now calls `paint('english')`, and is itself called once at
  `initOrigin()` init so the default is established from the first frame,
  not just after the idle hint's own cycle ends. New test checks the state
  immediately at load, before any scroll or interaction, so it can't pass by
  coincidence with the hint's own preview (which also opens on English, but
  only once the mark is scrolled into view).
- **C13 — `cursor: none` applied to every element, so hovering plain body
  copy showed no cursor at all: no native I-beam, no signal that text is
  selectable.** Two options were put to Igor: scope the suppression to
  interactive surfaces, or keep it universal and give the dot a text state.
  Chose the former (recommended): `cursor: none` now applies only to
  `html.has-cursor a, button, [data-magnetic]` — the same `HOT` selector
  `initMagnetic()`/`initCursor()` already used for the ring effect — so the
  native cursor, I-beam included, returns everywhere else. The dot's own
  visibility moved from a JS-tweened opacity gated on any mouse movement to
  a CSS rule gated on `cursor-active` (`html.has-cursor.cursor-active
  .cursor { opacity: 1 }`), so it now only ever appears near a real control
  instead of trailing the pointer for the whole session. Two new tests:
  plain text keeps a real cursor, and the dot's opacity follows hot/not-hot
  hover state precisely.

All ten new tests with real logic behind them were confirmed failing against
pre-fix `main` before landing the fix — including the real C11 gap, re-run
against the version of `main` this stage had already merged, to confirm the
mislabelling had actually left it unfixed. Full suite: **111 passed**
(101 + 10 new).

**Not republished:** same hold as Stages 2 and 3 — the placeholder-photo
freeze from Collage Stage 3 is unrelated to this stage's changes but still
stands, and this remains a draft.

## Awwwards-jury review, Stage 5 — composition & rhythm (2026-09-06)

Nine places where a grid meets uneven content and loses, or a rule and a
weight don't say what they mean: C8, C9, C12, P9, P10, P12, P13, P14, P15,
branch `feature/composition-pass`. Re-read the actual work-order text for
every item before touching code, not just the paraphrase from earlier in
this project — the C11 mislabelling in Stage 4 was exactly the failure mode
of trusting a reconstruction over the source.

- **C8 — nothing to do.** The one-ratio-per-group decision (Collage Stage 1)
  already gives `.collage--group` a plain repeating grid that aligns evenly
  at one/two/three-up with six identical crops per group. Kept on the sheet
  as a pointer, not a task.
- **C9 — the contact handle was the smallest, furthest thing in its own
  row.** "Telegram" sat at 44px Lora against the left margin; "@yngvil" sat
  13px mono up to ~950px away at the right — three rows that read as a
  table missing its middle column, with the one piece a reader actually
  needs both the faintest and the most distant. Rebuilt `.channels a` from
  a two-column grid to a flex row: the handle (`.ch__v`, bumped to
  `clamp(14px, 1.5vw, 17px)`) now sits directly behind the platform name in
  one `.ch__text` unit, and the right edge it gave up carries `.ch__arrow`
  — the same two-copy travelling-arrow device `.proof__arrow` already uses,
  reused rather than reinvented. New tests check the gap between name and
  handle, and that the arrow sits at the row's right edge.
- **C12 — two rule widths with no stated relationship.** `.sec`'s own
  top border spans its full 1320px box; `.mechanisms`/`.specs`/`.domains`/
  `.rows`/`.channels`/`.proof` sit inside that box's own `--gut` padding, so
  their dividers drew `--gut` narrower on each side — not a deliberate
  second tier, just where `.sec`'s padding happened to land. Bled all six
  back out with `margin-inline: calc(var(--gut) * -1)` and re-added the
  same amount as `padding-inline`, so the text inside still lines up with
  the `.sec__head` heading above it, but every horizontal rule on the page
  is now exactly one width. New tests check the six containers are flush
  with their own section's box, and that the content inset didn't move.
- **P14 — the mechanisms grid gave every row the same fixed heading
  column** (`minmax(0, 1fr)`, sized against the row's *paragraph*, not its
  own heading), so "Load management" got the same ~470px as the longest
  heading on the page and sat in a pool of empty track before its
  paragraph started. `min(max-content, 260px)` looked like the fix but
  Chromium rejects `max-content` inside a `min()`/`max()` math function in
  track-sizing position — the whole declaration drops silently and the
  column falls back to one implicit full-width track. Caught by the
  regression test itself (it failed with the "fixed" CSS in place, not
  just against pre-fix `main`). `fit-content(260px)` is the actual
  built-in for this — sizes to the row's own content, capped so a long
  heading wraps instead of pushing the paragraph column aside. New test
  checks the three rows now get three different column widths, each within
  a small gap of its own paragraph.
- **P13 — the mobile header was quietly spending ~32% of a 390×844
  viewport before the first line of real copy.** The header itself (mark's
  clear-space floor + a genuine two-line, 44px-touch-target row) already
  can't give anything back. What could: `.hero`'s own
  `justify-content: center` was splitting the *remaining* vertical slack
  top-and-bottom on a short viewport, so the header's own height got
  doubled before real content appeared. A `max-width: 600px` override
  anchors `.hero` to `flex-start` and trims its own breathing room from
  `clamp(32px, 7vh, 90px)` to `clamp(20px, 3vh, 40px)` — first line moved
  from y≈305–326px up to y≈226px in testing, with the desktop rule
  untouched (placed *after* the base `.hero` rule on purpose: same
  specificity, so source order is what makes the override win — it was
  written before the base rule at first and silently lost every time).
- **P12 — the hairline measured ~1.47:1 (charcoal) / ~1.48:1 (cream)
  against `--bg`.** "Structure is whitespace and hairline rules" only
  holds if the hairline survives a real screen; the old alpha only did on
  a good display in a dark room. `--rule`'s alpha moved from `.14`/`.20` to
  `.235`/`.33` (tuned separately per pair — they don't share one alpha
  that lands the same ratio on both bases), landing both at ~2:1. Not
  verified on Igor's own laptop, per the sheet's own instruction to do so
  before committing to a number — flagged for him. New helper in
  `conftest.py` (`rule_contrast`) flattens `--rule` over `--bg` from actual
  computed styles (normalised through a probe element's `color`, since the
  two tokens are authored in different formats — hex vs `rgba()` — across
  the stylesheet) and checks both pairs land in 1.85–2.3:1.
- **P10 — the three masthead photo-jump icons had no *visible* label.**
  `aria-label` and a `title` tooltip, neither of which a touch reader ever
  sees, pointing at a view the reader hasn't been told exists yet.
  Considered gating the icons behind scroll position (hidden until the
  reader passes "See the work") and rejected it — that would be a second
  reveal mechanism the existing `.reveal`/`IntersectionObserver` system
  doesn't need a competitor for. One shared `.tools__label` caption
  ("Photos"/"Фото") instead, in the exact type `.tools` already uses.
  Adding it to the row broke two *existing* tests (`.tools` overflowed its
  335px mobile budget by a few px, and flexbox proportionally shrank every
  child — including the 44px icons Stage 3 had just fixed — down to
  ~36–43px). Fixed with `flex-shrink: 0` on `.tool`, `.tool--icon` and
  `.tools__rule`: a touch target is a floor, not something flexbox gets to
  negotiate down when a new sibling arrives.
- **P9 — "See the work" rested at `--fg2` with its underline drawn in only
  on hover** — the most recessive large element on the page guarding the
  one visible door into the collage view. `.proof__text` now sits at full
  `--fg`, and `.proof__link::after` starts at `scaleX(1)` in a quiet
  `--rule`-coloured hairline, brightening to `--ink-target` green on
  hover/focus — findable at rest, with hover still adding emphasis rather
  than being the only thing that reveals the link exists.
- **P15 — the footer was the mark and one 12px line**, a dead stop after
  ~7,500px of scroll with no way back up. Added `.foot__top`, an `<a
  href="#top">` that reuses `.tool` wholesale (no new control style) routed
  through the same in-page Lenis link wiring every other `#`-href on the
  page already uses, plus a year appended to the existing identity line
  (`· © 2026`). Left the three contact channels unrepeated on purpose —
  they're in the section directly above with nothing between, so
  duplicating them here would be the redundant kind of ending, not the
  conclusive kind.

Thirteen new test functions (eighteen collected cases — one is parametrized
across the six C12 containers) were confirmed failing against pre-fix
`main` before landing each fix. Two caught real mistakes mid-stage rather
than just proving the fix afterward: P14's first CSS draft (`min(max-content,
260px)`) failed its own new test, which is what surfaced that Chromium
silently drops that declaration in track-sizing position; and P10's new
`.tools__label` broke two *existing* tests by pushing the icon row's
content past its available width, which is what caught flexbox
proportionally shrinking the 44px touch targets Stage 3 had fixed. Full
suite: **129 passed** (111 + 18 new).

**Not republished:** same hold as Stages 2–4 — the placeholder-photo freeze
from Collage Stage 3 still stands, and this remains a draft.

## Awwwards-jury review, Stage 6 — ship readiness (2026-09-06)

Six items that only matter once a domain exists, plus three loose copy ends:
P1, P2, P3, P4/P7, P6, P8, branch `feature/ship-readiness`. Two of these
(P6, P8) were real decisions, not implementation calls, and were put to
Igor before any code changed rather than assumed from the work-order text
alone.

- **P1 — the share card was still the documented placeholder,** so every
  link shared a blank grey box, on Telegram (the first contact channel,
  and the one that renders previews most aggressively) above all. Built
  the actual 1200×630 asset — `assets/share/share-card.html` is the source
  (every color, the mark's path data and the wordmark's per-letter colors
  copied verbatim from `index.html`/`style.css`, never its own palette),
  rendered once via the test venv's own Playwright at exactly 1200×630
  device pixels and exported to `assets/share/og-share.png` (48KB). `og:url`
  / `og:image` (plus width/height/alt, and `twitter:card`) now point at
  `https://vitnyr.example/` — the IANA-reserved placeholder TLD (RFC 2606),
  not a guessed real-looking domain — as the one thing left to swap once a
  real domain exists.
- **P2 — the language lived only in `localStorage`.** `theme.js` read
  `?lang=` on load and never wrote it back, so a reader who switched to
  Russian and sent the URL handed everyone else an English page. Added
  `syncLangUrl()`, called only from the switch handler (not from the
  initial `applyLang()` call, so an ordinary first visit never rewrites a
  clean address bar on its own) — wrapped in `try/catch` like every other
  storage/history call here, because the live artifact runs this page
  inside a cross-origin iframe where `history.replaceState` can throw.
- **P3 — no canonical, no `hreflang`, no `robots.txt`/`sitemap.xml`, no
  structured data**, for a bilingual single page selling a named person's
  services in a named city — the cheapest search work available, and none
  of it existed. Added a `Person` JSON-LD block (`sameAs` is exactly the
  three settled channels, in the settled order; every field is one of the
  site's own confirmed facts, nothing invented for search's sake), a
  canonical link, `en`/`ru`/`x-default` `hreflang` alternates pointing at
  the `?lang=` URLs P2 now actually writes, and `robots.txt` + `sitemap.xml`
  at the site root. All four share the one `vitnyr.example` placeholder, so
  the eventual domain purchase is a single find-and-replace.
- **P8 — a positioning call, put to Igor rather than assumed:** the free
  intro call is the page's actual conversion goal, but nothing on the page
  read as "press this." Decision: add a real door now, as a Telegram deep
  link (Igor's choice over Calendly or a placeholder href), reusing the
  existing `@yngvil` handle. "Message me." — the page's single biggest
  line of text — is now `<a class="contact__cta">`, pre-filled with a
  message about the free call and localized via a new
  `data-href-en`/`data-href-ru` pair (the same generic-attribute-copy idea
  `applyLang()` already used for text, extended to `href`). Styled with the
  same drawn-underline / travelling-arrow language as `.proof__link` and
  `.channels a`, scaled up, rather than introducing a filled-button style
  the rest of the page doesn't use anywhere.
- **P6 — the etymology sign-off, resolved rather than deferred again.**
  The `vit` + `nýr` Old Norse reading had an HTML comment above `#origin`
  flagging it as unconfirmed. Checked both roots against the
  Cleasby–Vigfusson Old Norse dictionary before touching anything: `vit` =
  "consciousness, sense" / "wit, understanding, reason"; `nýr` = "new,
  fresh, recent" — both match the copy as written. Confirmed; the
  flag comment is gone, replaced with a note of what was checked and
  against what.
- **P4/P7 — two copy ends that disagreed with themselves.** The four-across
  facts row said only "redpoint, indoor" for the climbing fact, dropping
  the harder 7C Kilter number from the row most likely to actually be
  read, while the domain card and the origin mark's panel both carry both
  grades — `.k`'s label now reads "redpoint, indoor · 7C Kilter" to match.
  And the collage's English group heading carried a colon in `data-en` but
  an em dash in the markup's own text and in the Russian version — every
  visit that ever ran `applyLang()` silently overwrote the em dash with a
  colon. Matched to the em dash both other copies already used.

Regression-proved the two behavioural changes (P2's URL mirroring, P8's
localized CTA link) the same way as prior stages: `git stash` the source
files, confirm all five new tests fail against pre-fix `main`, pop, confirm
all five pass. The rest (P1/P3/P4/P7/P6) are static content and metadata
checked directly against the new tests with no separate proof needed. Nine
new test functions: three in `test_i18n.py` (URL mirroring), two in
`test_layout.py` (the CTA link), three in `test_content.py` (canonical/
hreflang, the JSON-LD block, the share-card asset actually resolving — plus
one existing test updated for `og:url`/`og:image` and one for the facts
row), one in `test_smoke.py` (`robots.txt`/`sitemap.xml`). Full suite:
**138 passed** (129 + 9 new).

**Not republished:** same hold as Stages 2–5 — the placeholder-photo freeze
from Collage Stage 3 still stands, and this remains a draft. This closes
the work order's six planned stages; the one item left on the sheet
(the photo shoot itself) is parked on the shoot, not on any of this work.

## Spark Order, Stage 0 — decisions (2026-09-06)

Seven questions put to Igor before any of the Spark Order's code stages
start, so a later chat never has to guess and never re-litigates these.
The order itself lives at
`https://claude.ai/code/artifact/240b79ff-9a8f-4098-8667-825ac1355fe5`
("Vitnyr Spark Order"); its reasoning is in the companion Crit Sheet at
`https://claude.ai/code/artifact/d4ce3a94-907e-40e4-b16a-473a50e65dfa`.

**Decided (Igor, 6 Sep):**

1. **Move 01 — the transform bend: approved, with a guard.** The performed
   correction may use a transient FLIP, which borrows the transform channel
   for the length of one tween. It is only acceptable because it clears
   itself: S6 must ship `test_correction_leaves_no_residual_transform`,
   asserting no animated node holds a non-identity transform once the tween
   settles. That test is the condition of the bend and must never be
   deleted. The standing rule in CLAUDE.md is otherwise unchanged: layout
   still never rides the transform channel.

2. **Move 07 — the hero: deferred, not cancelled.** S8 does not start until
   S6 has landed and been looked at. The reasoning is that the performed
   correction may already give the page the spark the hero rework was meant
   to supply — and `playHero()` is the most fragile code in the repo, so it
   should only be touched if something is still missing afterwards. Revisit
   after S6; do not treat the deferral as a no.

3. **Move 11 — Russian register: yes, but Igor writes it.** The RU specimens
   may diverge in voice from the EN ones (blunter, funnier about
   «чувствовать себя»), without diverging in substance. A chat marks the
   three or four places where the copy could loosen and states what each
   needs to do; **Igor supplies the actual wording.** Do not draft Russian
   voice on his behalf — the loanword-keeping register already on the page
   is his, and it should stay his.

4. **Move 15 — voice: yes, starting with one specimen.** Igor records the
   register specimen only to begin with: "Send me the report today, please."
   against "Could you send me the report today?" — two takes, ~15 seconds.
   That is the specimen that genuinely cannot be read, only heard, so it
   carries the most proof for the least effort. If it lands, the other two
   specimens follow. **His real voice, never TTS, never a stand-in** — if
   the recording doesn't happen, S9C is struck rather than synthesised.

5. **Move 09 — specimen count: finite, no figure.** Each specimen gets its
   own anchor and share entry point, but the page does not claim a number.
   The existing copy already says truthfully that the list is finite ("Your
   errors are a finite list"); that stands, and no count is asserted that
   Igor would have to stand behind. This is the "real material only" rule
   applied to a number that would have been easy to invent.

6. **Move 10 — the free call: 30 minutes.** Now a real, publishable fact
   rather than a gap.

7. **Move 10 — what the reader leaves with: at least one named error.**
   Igor hears them speak and names something specific they do wrong, in the
   call. This is the method performed on the reader rather than described
   to them, which is why it belongs on the page: it makes section 06 the
   payoff of section 02 instead of an unrelated ask.

**Consequences for the order:** S6 is unblocked. S8 is parked behind S6's
result. S9A's move 09 shrinks to anchors and share entries only. S9A's
move 10 has its material. S9C narrows to a single specimen. S1–S5 and S7
were never gated on any of this and remain free to start.

## Spark Order, Stage 1 — subtraction (2026-09-06)

Branch `feature/stop-the-counters`. Moves 17 and 16 — the first is a net
deletion, the second is a line in this file. Picked first in the order
because it removes a rhythm every later stage would otherwise have had to
compose against, and it proves the pipeline end to end with almost nothing
that can break.

- **Move 17 — the count-up is gone.** The facts row's four numbers (8 years,
  100+ clients, a 2100 chess rating, a 7c grade) used to run up from zero on
  an IntersectionObserver, sharing one 1.6s tween. They are four readings off
  four unrelated instruments and a shared count animation made them read as
  one instrument — so the animation went, not the numbers. Deleted `countUp()`
  from `main.js` whole, both call sites (`countUp(true)` in the reduced-motion
  early return, `countUp(false)` in the go block), and `count: 1.6` from the
  `D` duration table. The comment above `D` enumerated five durations by name
  and now describes four. In `index.html` the three `.facts .n` spans that
  carried `data-count` / `data-suffix` lost those attributes; their text
  already read `8`, `100+`, `2100` and is untouched. The fourth fact (`7c`)
  never had a counter. All four `.facts li` keep `.reveal`, so the row still
  arrives on the ordinary rhythm with everything else.
  - **Did not** take the optional `--d` stagger offset on `.k`. The stage is
    meant to be a clean subtraction; adding a CSS beat back in the same pass
    works against that, and the labels landing with their numerals is fine.
- **Move 16 — no interaction sound, ever.** Recording the decision so a
  future chat does not add a tasteful hover tick and call it an improvement:
  audio on this site means "this is Igor speaking" and nothing else. No hover
  ticks, no ambient bed, no UI sounds, no click feedback — not now and not
  later. The only sound the site will ever carry is Igor's recorded voice on
  a specimen line (Spark Order S9C), and that is the whole of it.

**Tests.** The count-up had three tests across two files; each was ported,
not dropped, because a counter test that now passes vacuously is worse than
none:

- `test_content.py::test_no_unapproved_animated_statistics` →
  **`test_no_unapproved_statistics_in_the_facts_row`**. Its job was to stop a
  fabricated statistic being added to the row, and that job outlives the
  count-up. Rewritten to read the text of every `.facts .n` and assert
  exactly `["8", "100+", "2100", "7c"]`; a fifth number added to the row
  fails it.
- `test_motion.py::test_counters_count_up_to_exact_values` and
  `test_counter_starts_below_its_target` → one new
  **`test_numbers_do_not_animate`**: scroll the facts row into view, sample
  `.facts .n` immediately and again 600ms later (the window the old tween
  lived in), assert both reads are the final four values and identical. The
  second old test asserted the value was *below* target mid-count — the exact
  opposite of the new behaviour — and referenced a `[data-count]` selector
  that no longer resolves, so it went.
- `test_a11y.py::test_reduced_motion_counters_show_final_value_without_animating`
  → **`test_reduced_motion_facts_row_shows_every_value`**: same assertion,
  renamed and re-commented so it reads as a guard on the reduced-motion
  early-return path rather than implying a counter still exists.
- `tests/README.md`'s one-line summary of `test_motion.py` updated.

Regression-proved `test_numbers_do_not_animate` per the standing protocol:
`git stash push -- main.js index.html`, ran the new test against pre-change
source — it failed with the numbers caught mid-count (`['7', '92+', '1924',
'7c']`) — popped, ran again, passed.

`grep -rn "data-count\|countUp\|D.count" index.html main.js` returns nothing.
Full suite: **137 passed** (was 138). The count drops by one on purpose:
three counter tests were replaced by two — `test_counters_count_up_to_exact_values`
and `test_counter_starts_below_its_target` both folded into the single
`test_numbers_do_not_animate`, since with no animation there is no separate
"starts below target" state to assert. The other two counter tests were
ported 1:1. No test was deleted without its guard being carried forward.

**Not republished:** the Collage Stage 3 placeholder-photo hold still stands
and this remains a draft. Landing on `main` only.

## Spark Order, Stage 2 — reading the numbers (2026-09-06)

Branch `feature/facts-units`. Move 18 only. The facts row's four figures —
`8` years, `100+` clients, a `2100` chess position, `7c` — sat in one
identical treatment as if they were four readings of the same instrument.
They are readings off four unrelated instruments, and the mismatch is the
argument (three incommensurable domains, one method), so it is now visible
rather than flattened. **Typographic treatment only** — no colour beyond the
ink tokens already in use, no new component, and not one approved fact string
changed.

- **Each `.facts li` gains a unit-type modifier.** `fact--count` (`8`, `100+`),
  `fact--scale` (`2100`), `fact--grade` (`7c`), on a `fact` base class. New
  `test_facts_row_names_each_unit_type` asserts the four in order, so a later
  change that flattens them back to one style fails.
- **count — the label drops the caption voice.** `.fact--count .k` is set in
  `--mono`, `text-transform: none`, 13px, so `8 · years coaching` reads as a
  number and its unit rather than a number and a heading. The strings
  (`years coaching`, `one-on-one clients`) are untouched — only their type
  changed. This was Igor's call on move 18's "unit as a mono suffix": restyle
  the label, do not split or reorder the approved string.
- **scale — a position on a continuum.** `.fact--scale .n` restates
  `font-variant-numeric: tabular-nums` (already the row default) as intent and
  gets a short 1px tick beneath the numeral — a gauge mark, drawn in `--rule`,
  the sanctioned hairline ink, so it stays a rule and not a third colour.
- **grade — two readings, not one.** `7c redpoint, indoor · 7C Kilter` read as
  a single fact to anyone who does not climb — two scales joined by a middle
  dot. It is now two stacked, separately-labelled `.fact__reading` elements
  under the one `7c` numeral. Both strings survive verbatim, **including the
  `7c` / `7C` case difference**, which is a real grade distinction and is not
  normalised. In `index.html` the old combined `.k` (which carried
  `data-en`/`data-ru`) becomes a wrapper holding one translated
  `.fact__reading` (`redpoint, indoor` / `редпоинт, зал`) and one static one
  (`7C Kilter`); `theme.js`'s `applyLang()` walks `[data-en][data-ru]` nodes,
  so moving the attributes onto the child just works.

**Tests.** Two existing, one new:

- `test_content.py::test_the_three_measured_facts_are_exactly_these` — updated
  for the split: the grade row's unit is now read as a list of `.fact__reading`
  texts. Every asserted string is preserved (`8`, `years coaching`, `100+`,
  `one-on-one clients`, `2100`, `chess rating`, `7c`, `redpoint, indoor`,
  `7C Kilter`).
- `test_content.py::test_climbing_grades_are_kept_distinct` — extended per the
  order: still asserts both grades appear in body text (via the domain card),
  now also asserts the facts row holds them in **separate elements**
  (`['redpoint, indoor', '7C Kilter']`), not one text node.
- `test_content.py::test_facts_row_names_each_unit_type` — **new.** The
  unit-type modifiers are present and in order.

`test_no_unapproved_statistics_in_the_facts_row` (the "real material only"
guard) still reads `.facts .n` as `["8", "100+", "2100", "7c"]` and still
fails if a fifth number is added — untouched. `test_a11y.py`'s and
`test_motion.py`'s facts-row checks read `.facts .n` too and are unaffected.

Regression-proved per the standing protocol: `git stash push -- index.html
style.css`, ran the two changed tests plus the new one against reverted
source — all three failed (`.fact__reading` absent, unit still the run-on
string, no `fact--` modifiers) — popped, ran again, all passed.

Verified headless (Trap 2: the preview pane reported `clientWidth: 0`, so a
real Playwright pass through `tests/.venv/bin/python` did the looking): facts
row at 375 and 1280, EN and RU, both themes — no horizontal overflow
(`scrollWidth - clientWidth == 0` in every case), no console or page errors,
numerals top-aligned across the row, the `2100` tick visible on both grounds.
Full suite: **138 passed** (was 137) — the one added test is
`test_facts_row_names_each_unit_type`; the two edited tests kept their count.

## Spark Order, Stage 3 — pace and progress (2026-09-06)

Branch `feature/pace-and-progress`. Moves 08 and 20. Two additions that give
the long scroll a beat and a sense of position, both on the existing rhythm —
no new easing, no new reveal timing, no second scroll listener.

**Move 08 — the breath.** A new full-width block between `#specimen` and
`#disciplines` carrying one sentence, `<div class="breath reveal">` with a
`data-l="en"`/`data-l="ru"` pair (the longer-block i18n pattern the hero
already uses). The line is not new: it closed mechanism 02 of section 01 —
*"Once an error has a name it stops being 'my English is bad' and becomes one
specific thing you can train."* Igor's call was **move, not echo**, so
mechanism 02 now ends on its previous sentence (*"...and every one of them has
a name."*) in both languages, and the sentence appears once on the page.

- It is **not a section**: no `.label`, no `01–06` numeral, class `breath` not
  `sec`. `test_section_numbering_is_sequential` still counts exactly six, and
  `test_breath_block_takes_no_section_number` guards the absence.
- Sized by **content + padding**, never `100vh`: `padding-block: clamp(100px,
  18vh, 210px)` on the block, `font-size: clamp(28px, 5.2vw, 60px)` on the
  line (larger than the 17px body, smaller than the hero at every width).
  Measured heights: 447px (375/EN), 513px (375/RU), 608px (1280/EN), 679px
  (1280/RU) — all well inside the viewport. `test_breath_block_is_not_viewport_height`
  asserts `< 780` at 375×780 in both languages.
- Same `.reveal` rhythm as everything else; `border-top: 1px var(--rule)` so it
  divides `#specimen` from `#disciplines` the way every section divides.

**Move 20 — the progress hairline.** A 1px `aria-hidden` rule on the
masthead's bottom edge: `<div class="progress">` with two stacked
`.progress__fill` spans, `left/right: 0` so it is exactly as wide as the
masthead border-bottom it sits on (one hairline width — C12).

- **Driven from the one existing scroll source.** `main.js`'s `setStuck`
  wiring (`lenis.on('scroll')`, or the `window` listener when Lenis is off)
  now calls `onScroll(y)` → `setStuck(y)` + `trackProgress(y)`. No second
  listener. `trackProgress` sets `--progress` (0–1, document depth) on
  `.progress`; both fills are `transform: scaleX(var(--progress))`,
  `transform-origin: left` — animation using the transform channel
  legitimately, on an element that carries no layout (Trap 4 clear).
- **The colour switches, it does not blend.** `.progress__fill--specimen`
  (`--ink-specimen`) sits underneath; `.progress__fill--target`
  (`--ink-target`) is `opacity: 0` and fades to `1` over `--t` when
  `html.past-origin` is set. Two fills each keeping their own token — never an
  amber→green interpolation across hues, which would be a third colour by the
  back door. `past-origin` flips when the reader's viewport-midpoint passes
  `#origin` (its page offset measured once, re-measured on resize and
  `vitnyr:langchange`, not read per frame).
- **Reduced motion:** the block runs before `main.js`'s reduced-motion return,
  so the bar still tracks position; the `@media (prefers-reduced-motion)`
  rule collapses the crossfade to an instant switch. Verified: `past-origin`
  and target opacity still resolve correctly with `reduced_motion` on.
- With JS off, `--progress` is unset, `scaleX(0)` — the bar is invisible and
  carries nothing a reader needs.

**Tests.** Three names, six cases, all new:

- `test_motion.py::test_progress_rule_tracks_scroll` — `scaleX` sampled at
  top / mid / end of the document: `< 0.05`, strictly increasing, `> 0.95`.
- `test_motion.py::test_progress_rule_switches_ink_at_origin` (×dark, ×light)
  — each fill's `background-color` equals its resolved token; above `#origin`
  the target fill is `opacity ~0` and `html` lacks `past-origin`; scrolled to
  `#origin` both flip.
- `test_layout.py::test_breath_block_is_not_viewport_height` (×en, ×ru) —
  `120 < height < 780` at 375×780.
- `test_layout.py::test_breath_block_takes_no_section_number` — no `.label` /
  `.num` inside `.breath`; section numbering still `01…06`.

Regression-proved per the standing protocol: `git stash push -- index.html
main.js style.css`, ran all six new cases against reverted source — every one
failed (`.breath` / `.progress__fill--specimen` absent) — popped, ran again,
all six passed.

Verified headless (Trap 2: the preview pane reported `clientWidth: 0`): the
full matrix — 375 and 1280, EN and RU, both themes, plus reduced-motion — no
horizontal overflow (`scrollWidth - clientWidth == 0` in every case), no
console or page errors, `.progress` bounds equal `.masthead` bounds at 375 /
1280 / 1600, `scaleX` 0→1 across the scroll, `past-origin` off at the top and
on at `#origin`.

Full suite: **144 passed** (was 138, +6 new cases). Nothing edited in the
existing tests; the earlier `test_scroll_position_restored_on_return` blip was
a contaminated background run (Trap 1), green on a clean pass.

## Spark Order, Stage 4 — switch and pointer (2026-09-06)

Branch `feature/switch-and-pointer`. Moves 05 and 20's sibling 02 — the
language swap gets a transition, and the custom dot borrows the page's two
accents. `theme.js` stays render-blocking and works alone.

**Move 05 — the language crossfade.** `theme.js`'s `.langswitch` handler now
builds the swap (`applyLang` + `syncLangUrl`) as a callback and, *if*
`window.__vitnyrLangFade` is a function, hands it over; otherwise it calls it
straight, exactly as before. `main.js` installs `__vitnyrLangFade` past its
reduced-motion return, so it exists only under GSAP + motion-allowed. It runs
the swap, then `gsap.fromTo`s `#app` from `opacity: 0` back to `1` over
`D.state` on the brand ease — a page-wide fade rather than a hard text swap.
`#app` only: `.masthead` is its sibling, so the switch the reader just pressed
stays solid and visibly answers.

- **Deviation from the sheet's literal "fade out over `D.micro`, invoke the
  callback, then fade back in":** the callback is *not* deferred to the bottom
  of a fade-out, and there is no explicit out phase. Two reasons. (1) There is
  no second, old-language layer to fade out — holding one needs S6's
  clone/FLIP machinery, which isn't built. (2) Deferring the swap by ~`D.micro`
  desyncs every existing i18n test that asserts on the same tick as the click
  (`data-lang`, the `?lang=` mirror, `data-l` visibility), and S4 requires
  those green. Running the swap synchronously satisfies both, and the "callback
  must always run, even if a second click interrupts" guard becomes trivial:
  it always runs, first thing, on every call.
- **Double-click safety.** Each call re-runs its own swap and `kill()`s the
  running opacity tween before starting a fresh `fromTo`. The last call's tween
  is never killed by anyone, so `#app` always lands at `opacity: 1` on the
  final language — three fast clicks end fully visible on RU, never dark on the
  first.
- **Degradation.** With `main.js` blocked (no GSAP) `__vitnyrLangFade` is never
  installed and `theme.js` swaps instantly, `js` class dropped, page fully
  readable — `test_language_swap_degrades_to_instant_without_gsap` blocks the
  `gsap|lenis|customease` requests and proves it. Reduced motion: same instant
  path, `#app` untouched at `opacity: 1`.

**Move 02 — the dot learns the two accents.** `initCursor()`'s delegated
`mouseover`/`mouseout` pair now also toggles `.is-specimen` / `.is-target` on
`.cursor`: `is-specimen` when the hot target is inside `#specimen`,
`is-target` when it is (or is inside) `.contact__cta`. The fill comes from CSS
— `--ink-specimen` / `--ink-target`, the same tokens every other accent uses;
no hex entered `main.js`. The dot is a shape, so the sub-24px accent-on-text
rule doesn't apply. `#specimen` has no interactive control yet (S6 adds them),
so that branch is wired ahead and tested against an injected `[data-magnetic]`
probe. Coarse pointers still return early from `initCursor()` — the dot never
appears on touch (`test_cursor_absent_on_touch_devices`).

**Comment.** `main.js`'s header and the cursor section no longer call the
cursor "the signature move" — from S6's correction on, the performed edit is
the page's one move; the cursor is pointer feedback. Guide-phase-4 reference
kept. `style.css` still says "phase 4" (a build-guide phase label, accurate).

**Tests.** Seven new cases, four files' worth of behaviour in two:
- `test_i18n.py`: `test_language_swap_fades_app_but_not_the_masthead`,
  `test_rapid_repeated_clicks_never_strand_the_app_faded`,
  `test_language_swap_is_instant_under_reduced_motion`,
  `test_language_swap_degrades_to_instant_without_gsap`.
- `test_motion.py`: `test_cursor_takes_target_ink_over_the_contact_cta`,
  `test_cursor_takes_specimen_ink_over_a_control_inside_specimen`,
  `test_cursor_absent_on_touch_devices`.

Regression-proved per the standing protocol: `git stash push -- main.js
theme.js style.css`, ran the new cases against reverted source — the three
that assert the *new* behaviour failed (`__vitnyrLangFade` undefined, no
`is-target`/`is-specimen` class); the four degradation/guard cases pass either
way by design (they assert the fallback path, which already worked). Popped,
all seven green. Every pre-existing i18n test passed untouched — the
synchronous-swap decision is what keeps that true.

Verified headless (Trap 2: the preview pane reports `clientWidth: 0`): 375 and
1280, EN and RU, both themes — clicking `.langswitch` dips `#app` below 0.9
and restores it above 0.98 while `.masthead` holds at 1, the swap lands
synchronously, no horizontal overflow in either language, no console or page
errors. Cursor: target-green fill over the CTA, specimen-amber over an
injected `#specimen` control, both clearing on mouse-out. Reduced motion: no
hook, instant swap, `#app` at 1.

Full suite: **151 passed** (was 144, +7 new cases). No existing test edited
for behaviour; the two specimen/target cursor cases gained a 700ms settle wait
because `.cursor__dot`'s `background` is a `--t` transition.

## Spark Order, Stage 5 — answer the question (2026-09-06)

Branch `feature/answer-the-question`. Move 19 — section 05 asked "which of
these is you?" and gave no way to say. The four self-recognition rows and the
section 06 Telegram deep link were two halves of one feature; this joins them.

- **Each `.rows > li` is selectable** via an invisible overlay `<button
  class="row__pick">` that `initWhoRows()` builds at runtime — so a no-JS
  reader still sees four plain rows and the CTA keeps its static `href`
  (`test_who_rows_are_plain_and_cta_static_without_js`). The button follows the
  origin mark's hit-region precedent exactly: a real `<button>` (native
  keyboard + touch), named by a visually-hidden `<span class="vh">` that
  carries the heading's own `data-en`/`data-ru` so `applyLang()` localises it
  for free. Not `aria-labelledby` — the existing
  `test_every_link_and_button_has_an_accessible_name` reads `textContent` /
  `aria-label` only, and the `.vh` span is the house answer anyway.
- **Single-choice, toggleable.** Clicking the picked row clears it. State is
  `aria-pressed` on the button plus `.is-picked` on the `li`; the visual mark
  is the page's hairline vocabulary — a 2px `--ink-target` rule down the row's
  leading edge, drawn as a detached `::before` at `left: -14px` (in the
  gutter, `opacity` crossfaded over `--t`) so selecting a row never nudges its
  grid. No fill, no card. `test_picking_a_second_row_replaces_the_first`.
- **One writer for the href.** `updateCta()` reads the current language *and*
  the current selection every call — from the row handler and from a
  `vitnyr:langchange` listener — so the two compose and the href is never
  built in two places. No selection: it hands the CTA back to `applyLang()`'s
  plain per-language default. A selection:
  `BASE + encodeURIComponent(decodedBase(l) + " — " + clause)`, where `BASE`
  and `decodedBase` are both derived from the CTA's own `data-href-en`/`-ru`
  (one source for the handle and the base message). Reuses Stage 6's
  `data-href-*` mechanism, now per-answer as well as per-language.
- **Copy.** Each row gets `data-prefill-en` / `data-prefill-ru` in
  `index.html` — a short first-person clause restating that row's own approved
  heading. A model's first pass, flagged in an HTML comment for Igor to
  confirm, the same way `reference/collage-shotlist.md` and the §05 `h2` (C4)
  flag their draft copy. No approved string changed; FIDE still appears
  nowhere; `test_contact_heading_is_a_real_telegram_link` and
  `test_contact_cta_prefill_text_is_localized` pass untouched.
- Wired before `main.js`'s reduced-motion return (it is interaction, not
  decoration) — verified selectable under `prefers-reduced-motion`.

**Tests.** Six new cases: five in `test_layout.py`
(`test_selecting_a_row_rewrites_the_cta_prefill`,
`test_deselecting_restores_the_default_prefill`,
`test_picking_a_second_row_replaces_the_first`, `test_rows_are_keyboard_operable`,
`test_who_rows_are_plain_and_cta_static_without_js`), one in `test_i18n.py`
(`test_row_selection_and_language_compose`). Regression-proved per the standing
protocol: `git stash push -- index.html main.js style.css`, the five that need
`.row__pick` failed against reverted source, the no-JS guard passed either way;
popped, all six green.

An early cut used `aria-labelledby` on the pick button; the full suite caught
`test_every_link_and_button_has_an_accessible_name` (which resolves
`textContent`/`aria-label`, not `aria-labelledby`) and the button switched to
the `.vh`-span pattern — the house precedent — rather than the test being
widened. No existing test was edited.

Verified headless (Trap 2): 375 and 1280, both themes — pick composes the
prefill onto the base message, the picked hairline shows at `opacity 1`, a
second pick replaces the first, toggling off restores the default `href`, a
language switch recomposes the clause in Russian (`созвон`, not `intro call`),
Enter/Space toggle, no-JS gives plain rows + static CTA, no horizontal overflow
in either language with the `-14px` rule visible, no console or page errors.

Full suite: **157 passed** (was 151, +6 new cases). No existing test edited.

## Spark Order, Stage 6 — the correction (2026-09-06)

Branch `feature/perform-the-correction`. Moves 06 + 01 — the centrepiece:
the page's one *performed* edit. A specimen sentence corrects itself in front
of the reader; the deleted word lifts out and the surviving text reflows
closed over the gap. Joined because both moves rebuild `.spec`'s markup.

- **Move 06 — proofreader's notation.** The ✕/✓ glyph pair in `.line-spec .sig`
  is replaced by real marks drawn in the same 1.6-stroke `currentColor` style:
  the **dele loop** on a deletion, the **caret** on the insertion, the
  **transpose hook** on specimen three (the register example, which is *not* a
  grammar error — a ✕ overstated it). Ink stays ink: amber on the deletion,
  green on the insertion, both as strokes.
- **Semantic diff.** The faulty token is now `<del class="mark--specimen">`
  and the corrected token `<ins class="mark--target">`, replacing the
  colour-only `<span>`s. Real HTML meaning, and machine-readable anchors for
  the performance. `.line-spec del, .line-spec ins { text-decoration: none }`
  keeps the sighted appearance identical to before (the ink is the signal).
- **Move 01 — the FLIP.** `initCorrections()` (past the reduced-motion return)
  runs only for `data-op="delete"` specimens. On the page's existing reveal
  observer — same `rootMargin: '0px 0px -20% 0px'`, no ScrollTrigger — it
  builds one `aria-hidden="true"` `.spec__perform` clone of the wrong line,
  drops the static pair to `opacity: 0` (**never** `display:none` — assistive
  tech and every layout test keep the real paragraphs and their boxes), and
  overlays the clone absolutely. The beat: the `<del>` lifts and fades
  (`yPercent`, `D.correct * 0.42`), then a FLIP — measure the surviving
  `.spec__tail`'s left edge, set `display:none` on the `<del>`, measure again,
  `gsap.set({x: before - after})` then tween `x: 0` on the brand ease at a new
  named `D.correct` (0.8), `clearProps: 'transform'` on complete. The clone
  fades (`D.micro`) and the untouched static pair comes back. Fires once per
  specimen.
- **The S0 bend, and why it's allowed.** The FLIP puts layout in the transform
  channel — the one thing `CLAUDE.md` forbids — but only on a throwaway node
  that clears every transform and is removed on completion. Nothing static is
  ever transformed. `test_correction_leaves_no_residual_transform` is the
  guard and must never be deleted.
- **Restructure ships static.** Specimen three (`data-op="restructure"`,
  "Send me the report today, please." → "Could you send me the report
  today?") is a word reorder, not a deletion; a convincing FLIP for it was
  out of reach, so it renders as the static `<del>`/`<ins>` pair with the
  transpose hook. Two performed corrections beat three where one is awkward
  (spec, move 01).
- **Language switch.** The specimen sentences carry no `data-l` twin — they
  are English error examples, identical in both languages — so there is
  nothing to rebuild (Trap 3 is moot: no zero-height twin to measure). The
  `vitnyr:langchange` handler only has to not strand a beat behind `#app`'s
  S4 crossfade: it kills any running timeline, removes the clone, and hands
  the static pair back. A specimen not yet scrolled to stays armed.
- **Degrades to today's page.** No JS, no GSAP, or reduced motion: the
  static `<del>`/`<ins>` pair with the new marks, nothing hidden, no clone
  built. `build()` is wrapped in try/catch — a throw leaves the static pair
  visible, never an empty box.

**Tests.** Six new cases: four in `test_a11y.py`
(`test_specimen_static_pair_survives_without_js`,
`test_specimen_static_pair_survives_reduced_motion`,
`test_correction_performance_is_hidden_from_assistive_tech`,
`test_specimen_marks_are_proofreading_notation`), two in `test_motion.py`
(`test_correction_leaves_no_residual_transform`,
`test_correction_replays_after_language_switch`). Regression-proved per the
standing protocol: `git stash push -- index.html main.js style.css`; the four
behaviour tests failed against reverted source, the two degradation guards
passed either way; popped, all six green. The existing specimen layout tests
(`test_specimen_pair_sits_beside_its_explanation_at_desktop_width`,
`test_wrong_and_right_lines_have_a_visible_gap`, …) were re-examined and pass
**untouched**: they measure boxes, and `opacity: 0` leaves the box — the
performance layer shares no class with `.line-spec` / `.wrong` / `.right` /
`.vh`, so the static DOM stays the sole match for their selectors.

Verified headless (Trap 2): 375 and 1280, both themes, both languages, motion
and reduced — the clone appears `aria-hidden`, the word lifts, the tail FLIPs
and clears, the static pair returns at `opacity 1`, no residual transform, no
`NaN` geometry, no horizontal overflow, no console or page errors. Screenshots
of the mid-beat, the settled pair and the reduced-motion reference in the
Stage 6 chat.

Full suite: **163 passed** (was 157, +6 new cases). No existing test edited.

## Reversal — ticking numbers restored, as separate instruments (2026-09-06)

Branch `feature/restore-ticking-numbers`. Igor asked to undo Spark Order move
17 (the facts-row count-up removal) — "I like ticking numbers." Move 16 (the
"no interaction sound, ever" note) is untouched; it was never about the
numbers.

Move 17's objection was real, so this is not a straight `git revert` (S2–S6
rebuilt that row anyway). The count-up comes back **without** the thing that
got it cut: three numbers sweeping up on one shared 1.6s duration read as a
single gauge. Now each counts on its **own** length.

- **`countUp()` back in `main.js`**, past the same IntersectionObserver the
  reveals use (`rootMargin: '0px 0px -12% 0px'`). Two call sites restored:
  `countUp(true)` in the reduced-motion early return (settles every number to
  its final text, no tween), `countUp(false)` in the go block.
- **Per-number duration.** `D.count` is back in the table as the *reference*
  length (1.2s), and each number's actual tween is
  `D.count * (0.6 + log10(value + 1) / 4)` — counting rate is roughly fixed,
  so a bigger number takes longer to arrive, log-compressed so 2100 isn't
  ~260× slower than 8. Measured: 8 lands ≈1.0s, 100+ ≈1.4s, 2100 ≈1.9s. Each
  also starts `i * STAGGER` (0.08s) after the previous. The `D` comment now
  names six durations; `count`'s line says "scaled per number so each reads
  as its own instrument".
- **No flash of the final value.** The observer zeroes a number
  (`textContent = '0' + suffix`) the instant it's committed to counting, so
  the literal markup value never shows for a frame before the first tween
  update. `onComplete` calls the same `settle()` the reduced-motion path uses,
  so a cut tween still lands exact.
- **`index.html`:** `data-count` / `data-suffix` restored on the three `.n`
  spans (`8`, `100` + `+`, `2100`). `7c` is not a number, has no `data-count`,
  and never counts — same as before move 17. Literal text in every span is
  unchanged, so no-JS still reads `8 / 100+ / 2100 / 7c`. S2's `fact--count`
  / `fact--scale` / `fact--grade` treatments and the `2100` gauge tick are
  untouched; `tabular-nums` (already on `.facts .n`) keeps digit width steady
  through the count.

**Tests.** Net +1 (163 → 164).
- `test_motion.py::test_numbers_do_not_animate` → **`test_numbers_count_up_to_their_values`**
  (end state exact, `7c` never touched) + **`test_numbers_finish_at_different_times`**
  (polls each number to completion, ignoring the pre-tween literal match;
  asserts the last number lands >250ms after the first — fails against the old
  shared-duration countUp, where all three finished within a frame). Module
  docstring updated.
- `test_content.py::test_no_unapproved_statistics_in_the_facts_row` — now
  reads `.n[data-count]` again (the real-material guard: a fifth `data-count`
  = a fabricated statistic) plus the rendered-label set. `test_the_three_measured_facts_are_exactly_these`
  reads the three numbers from `data-count` so it's stable mid-count.
- `test_a11y.py::test_reduced_motion_facts_row_shows_every_value` — assertion
  unchanged; comment corrected (the branch calls `countUp(true)` again).
- `tests/README.md` line for `test_motion.py` updated.

Regression-proved per protocol: `git stash push -- index.html main.js`, ran
the new cases against reverted source — `test_numbers_finish_at_different_times`
and `test_no_unapproved_statistics_in_the_facts_row` both fail (no
`.n[data-count]`); popped, both green.

Verified headless (Trap 2): 375 and 1280, both themes, both languages — the
numbers zero on scroll-in and count up in a visible cascade (8 first, 2100
last, spread ~0.9s), settle exact at `8 / 100+ / 2100 / 7c`, no horizontal
overflow, no console or page errors. Reduced motion: final values immediately,
no count. No-JS: literal values. Language switch mid-page leaves settled
numbers alone. Mid-cascade and settled screenshots in this chat.

Full suite: **164 passed** (was 163; −1 test removed, +2 added).

## Spark Order, Stage 7 — the mark and the door (2026-09-06)

Branch `feature/mark-and-door`. Moves 03 and 04 — the wordmark draws its
three strokes on first reveal, and leaving the collage view cross-fades.

**Move 03 — the mark assembles from three strokes.** Section 04's copy says
*"It's still three strokes: two for the V, one for the stem."* On the mark's
`.is-in` (the same reveal observer everything else uses) each stroke now
draws in, in that order: left arm top→vertex, right arm vertex→tip, then the
stem down from the vertex.

- **Geometry untouched.** `#glyphV` and the stem `d=` are never animated or
  redrawn (CLAUDE.md forbids it, and the path is shared verbatim with
  `.lockup` / `.footmark`). The draw grows each part's **clip rect**:
  `#glyphClipLeft` / `#glyphClipRight` (already there for the half-clip) get
  their `height` — and the right one its `y` — animated from zero; a new
  `#glyphClipStem` clips the stem the same way. Pure CSS, keyframed on the
  one `--e` curve, `.45s` per stroke, `.22s` apart, each offset by the
  figure's own `var(--d)` so it starts with the reveal fade rather than
  ahead of it. The brand ease is very front-loaded, so it reads as a brisk
  assemble (~0.6s visually) inside the 0.9s fade.
- **Additive.** No `html.js` (no JS / GSAP failed) → the base collapse rule
  never applies and the rects sit at their full-size attributes → finished
  mark. Reduced motion → an explicit-px reset in the existing
  `@media (prefers-reduced-motion: reduce)` block (a clip rect's
  `height: auto` computes to **0** here, which would clip the stroke away —
  so the reset is `100px` / `44px`, not `auto`), plus the block's global
  `.01ms` rule. `test_origin_mark_is_complete_under_reduced_motion` guards it.
- **Sequenced against the idle hint.** `initOrigin()`'s idle preview
  (`threshold: 0.4`, previews all three disciplines) now starts on a 1.0s
  `delay` so the draw finishes before the hint drives the same strokes.
  `is-active` / `is-dim` are fill changes, orthogonal to the clip geometry,
  and `test_origin_mark_holds_still_for_the_hover_states` confirms a focus
  after the draw doesn't disturb the rects.

**Move 04 — View Transition on the collage route, close direction only.**
`location.hash` stays the single source of truth. `routeAfterHashChange()`
wraps the same `sync()` the router already calls in
`document.startViewTransition()` — but only when the hash resolves to a
**close**, and only when the API exists, motion is allowed, and the tab is
visible; otherwise it's the direct call, unchanged.

- **Why close only.** `startViewTransition` defers its update callback ~1
  frame (measured). `applyOpen` and the masthead jump focus a heading
  synchronously and `test_opener_routes_into_the_view` /
  `test_deep_link_opens_the_view_directly` assert that with no wait — a
  deferred focus there would strand it (this view shipped that bug once).
  So the open paths (opener click, glyph jumps, deep-link init) stay direct;
  closing returns focus to the opener button and every close test settles
  first, so it takes the transition. The optional glyph→label morph
  (`view-transition-name`) is on the jump path, which stays synchronous, so
  it's not taken.
- **Reduced motion** skips `startViewTransition` via the explicit `!reduce`
  gate rather than relying on the API's own PRM handling.
- Back, forward, Escape, the bar's back button, deep links and all three
  glyph jumps behave exactly as before; every test in `test_collage.py`
  passes **unchanged**.

**Tests.** +5 (164 → 169).
- `test_motion.py`: `test_origin_mark_draws_its_three_strokes_once` (real
  draw — a partial state is seen; arms fill before the stem; one-shot, still
  full ~1s later) and `test_origin_mark_holds_still_for_the_hover_states`.
  Both read the clip rects via `getBBox().height` (`getComputedStyle` reports
  `auto` for a zero/`auto` CSS height).
- `test_a11y.py`: `test_origin_mark_is_complete_under_reduced_motion`.
- `test_collage.py`: `test_view_transition_does_not_delay_focus` (open focus
  is synchronous, not behind the transition callback; close still restores
  focus to the opener) and `test_view_transition_falls_back_cleanly_under_reduced_motion`
  (`startViewTransition` is never called under reduced motion). Both are
  guards on the direct/fallback path and pass either way, like the S4/S6
  degradation guards.

Regression-proved per protocol: `git stash push -- index.html style.css
main.js`; the three origin-mark cases fail against reverted source
(`#glyphClipStem` absent); popped, all green.

Verified headless (Trap 2): 375 and 1280, both themes, both languages — the
three strokes draw in order (left arm before the stem in every config), a
partial state is caught mid-draw, the mark holds full afterward, no
horizontal overflow, no console or page errors. Reduced motion: the mark is
whole from the first frame, no draw. No-JS: whole. Collage close cross-fades
via `startViewTransition`; open, deep-link and glyph-jump stay synchronous
with focus intact; reduced motion takes neither transition. Mid-draw,
settled and reduced-motion screenshots in this chat.

Full suite: **169 passed** (was 164, +5 new cases). No existing test edited.

## Spark Order, Stage 8 — subsumed into S6, not built (2026-09-06)

S8 ("The hero — three beats, carried by the rules", move 07) was parked at S0
pending S6's result, with an explicit note: *"the correction may already
supply what this was for. Ask again once S6 has been seen; do not start on
your own judgement."* Asked. Igor's call: **do not build it — mark it
subsumed.**

The reasoning, recorded so a later chat doesn't reopen it:

- **The payoff now overlaps the centrepiece.** S8 was written to *pre-state*
  section 04's argument in a form the reader only understands later. S6 now
  *enacts* that argument — it corrects `vit → nýr`, a broken pattern replaced
  by one that holds, as motion. Foreshadowing an effect 200px above the place
  you then fully deliver it is a weaker page, not a richer one.
- **Risk/reward is upside-down.** The hero is the only thing above the fold,
  `playHero()` is the most fragile code in the repo, and it has already
  shipped a `NaN`-cache bug that silently killed every later tween. The
  reward for re-entering that code was three 1px resting hairlines under
  three words — an accent most visitors never consciously register.
- **The ink mapping was imposed, not real.** "amber, amber, green = left arm,
  right arm, stem" requires climbing to be the *correct outcome* of English
  and chess. It isn't. A colour pass would read that as a back-door third
  meaning for the two accents.
- **Composition budget.** The first viewport already carries the masked-line
  entrance, the wordmark font-gate, the progress hairline and the restored
  counters. A fourth timed system is where a page like this stops feeling
  composed.

No code changed for this decision. `feature/hero-trifecta` was never cut.
The Spark Order tracking artifact marks S8 subsumed; the Crit Sheet's move 07
is closed the same way. If the hero is ever revisited, it starts from a fresh
brief, not this one.

## Spark Order, Stage 9A — specimen permalinks (move 09) (2026-09-06)

Branch `feature/specimen-series`. Files: `index.html`, `style.css`,
`main.js`, `tests/test_content.py`, `tests/test_a11y.py`. Suite 169 → 174
(five new cases; one existing a11y test had its `.vh` selector tightened,
no assertion changed).

Move 09's brief was two lines: *give each specimen an anchor id and a share
entry point; assert no count.*

**Addressable.** The three `<article class="spec">` now carry stable,
language-neutral ids — `specimen-reflexive`, `specimen-copula`,
`specimen-register`. Each specimen's label became a permalink to its own id:
a quiet mono `#` (theme ink `--fg2`, never accent), the label text, and a
`.vh` suffix — *", link to this specimen" / ", ссылка на этот разбор"* — so
the link's accessible name says why a section label is a link. The label
underlines only on hover/focus; the shared `:focus-visible` rule is the ring.

**Share entry point.** `initSpecimenPermalinks()` (wired before the
reduced-motion return — navigation, not motion) intercepts the click:
`history.pushState` writes the permalink to the address bar (so it can be
copied and shared, and Back still works), the target scrolls in on the one
shared easing, focus lands *inside* the specimen, and `navigator.clipboard`
gets the full URL. On a successful copy a `role="status"` line shows *"Link
copied" / "Ссылка скопирована"* for 1.8s — its two languages are DOM
`data-l` spans, no strings in `main.js`. Everything degrades: with the file
absent the label is still `<a href="#specimen-…">`, the browser jumps, and
the status line stays `hidden`. The confirmation's visible-state CSS is
scoped `:not([hidden])` so a bare `display` can't out-specify the UA
`[hidden]` rule and leak the text on load (caught in regression-proving).

**`pushState` not `location.hash`** on purpose: a raw hash assignment fires
`hashchange`, and the collage router's `routeAfterHashChange()` would then
wrap a no-op `sync()` in `startViewTransition` for a hash that has nothing
to do with the collage. That handler also gained an `applied &&` guard — the
close transition only makes sense when the view is actually open — so Back
out of a specimen permalink (which *does* fire `hashchange`) and the
existing `#top` / `#method` anchors no longer trigger an invisible
page-wide cross-fade either. The S7 collage View-Transition tests pass
unchanged.

**Assert no count.** `test_no_invented_count_beside_the_finite_list_claim`
reads the whole specimen section's prose — heading, lede, every label, every
"why", both languages — and fails on any digit. S0 decided *"Your errors are
a finite list"* is the entire claim and no figure gets invented to sit
beside it; section 02 is the one place on the page built to tempt a
fabricated statistic. This is a standing guard (it passes against reverted
source too), same category as the S4/S6/S7 degradation guards.

Regression-proved per protocol: `git stash push -- index.html style.css
main.js`; the four behavioural cases fail against reverted source
(`.spec__permalink` absent), the no-count guard passes; popped, all five
green. Verified headless (Trap 2) across 16 configs — both themes, both
languages, 375 and 1280, motion and reduced — plus no-JS: the address bar
updates, focus lands in the specimen, no View Transition fires for a
specimen hash, no horizontal overflow (RU confirmation wraps as a unit,
never mid-phrase), clean console. Light/EN and dark/RU screenshots in this
chat.

Full suite: **174 passed** (was 169, +5). One existing test's selector
tightened (`.vh` → `.line-spec .vh`, its own earlier scope), no assertion
touched.

## C14 — the dot is the pointer; magnetic pull retired (2026-09-07)

Branch `feature/cursor-colour-signal`. Files: `main.js`, `style.css`,
`index.html` (one comment), `tests/test_a11y.py`, plus this note and
`CLAUDE.md`. Igor: *"i don't like the way cursor gets when u move it to
letters."* Over a link the old behaviour did three things at once on top of
the words — killed the native cursor, ballooned the dot 3×, and (on every
`data-magnetic` element, which is most links) dragged the text itself up to
12px toward the pointer. He chose: **the dot everywhere, one size, colour as
the only signal.**

- **Present always.** `.cursor` is `opacity: 1` under `html.has-cursor` (armed
  on the first `mousemove`), not gated on `cursor-active` any more. It fades
  out only while the pointer is off the window — `main.js` sets `.cursor-out`
  on `mouseleave` of the root, clears it on `mouseenter` and the next
  `mousemove`.
- **`cursor: none` is page-wide now** (`html.has-cursor, html.has-cursor *`),
  reversing C13's scoping — the dot *is* the pointer, so there is no native
  cursor to fall back to over body copy. Cost, accepted: no I-beam over text.
  Text stays selectable; only the visual cue is gone. A dot text-state was
  offered as a later refinement if it's missed.
- **Colour is the whole effect.** No `scale` tween — the `gsap.quickTo` for it
  is deleted. Over a `HOT` target (`a, button, [data-magnetic]`) the dot's
  fill crossfades `--fg` → `--ink-target` green over `--t` on the brand curve;
  over a control inside `#specimen` it goes `--ink-specimen` amber; over the
  contact CTA, target green. Same `.is-specimen` / `.is-target` classes and
  the same S4/move-02 meaning, just no ring/transparent-bg styling wrapped
  around it. `.cursor__dot` lost its `border` (the ring lived there); it is a
  solid 14px fill at rest and active.
- **`initMagnetic()` is gone** — function and call both removed, along with the
  `[data-magnetic]:hover { will-change: transform }` rule and the attribute
  from the reduced-motion `will-change` reset. The `data-magnetic` attributes
  stay in the markup as the interactive-hint hook the dot's `HOT` selector
  reads; only the movement is retired. If a pull ever returns it belongs on
  the icon buttons / switches, never on running copy.

Tests: the two C13 a11y cases encoded the old rule and were rewritten to the
new spec — `test_dot_is_the_pointer_page_wide` (dot visible over plain text,
native cursor suppressed page-wide) and
`test_dot_stays_one_size_and_only_recolours_over_hot_targets` (rendered size
unchanged over a link; `cursor-active` toggles; fill settles to `--ink-target`).
The two `test_motion.py` specimen/target ink cases pass unchanged (treatment
keeps `.cursor__dot`'s background as the assertion target).

Deviation 1 in this file ("flat dot that opens into a green ring") updated to
"eases its fill to the accent ink."

**Live artifact not republished** — still on hold behind the collage
placeholder photos (`assets/collage/PLACEHOLDERS.md`). This change folds into
the inline rebuild whenever that hold lifts.

## C15 — the dot's active ink goes amber on cream (2026-09-07)

Branch `feature/cursor-cream-amber`. Files: `style.css`, `tests/test_motion.py`,
plus this note. Igor: *"can we make cursor on cream theme to be ember not green
when it hovers over clickable stuff."* Green (`--ink-target`, `#3D6543` on the
light pair) sat muddy against the warm cream ground; amber has more presence
there.

- New token **`--cursor-active-ink`**, defined once in `:root` as
  `var(--ink-target)` and pair-swapped to `var(--ink-specimen)` in both light
  blocks (the `prefers-color-scheme: light` one and `:root[data-theme="light"]`),
  exactly like every other themed token. `--amber` is fixed, so cream resolves
  to `#B07C24`; charcoal is unchanged green.
- Both cursor rules that used to read `--ink-target` — the generic
  `.cursor-active .cursor__dot` and `.is-target` (the contact CTA) — now read
  `--cursor-active-ink`. So on cream the dot is amber over *every* control,
  contact CTA included; the specimen/target split still holds on charcoal.
- `.is-specimen` (a control inside `#specimen`) stays wired straight to
  `--ink-specimen` — amber in both pairs. "The error under examination" is not
  a per-theme idea.
- No JS change. `main.js` still only toggles `.is-specimen` / `.is-target`.
- Test: `test_cursor_active_ink_follows_the_theme` (parametrised dark/light) —
  the generic hover and the contact CTA both settle to `--cursor-active-ink`,
  and on light that value is `--ink-specimen` and *not* `--ink-target`. The
  three existing cursor cases run on the charcoal default and are unaffected.

**Live artifact not republished** — same collage hold as C14.

## P17 — masthead tools grouped: toggles | collage-nav (2026-09-07)

Branch `feature/nav-photo-cluster`. Files: `index.html`, `style.css`, this
note. Igor, looking at the header: *"the words photo and 3 icons next to it
are not exactly connected… theme language are separate buttons and photo
should stand separately with icons to show that they are together."* Right
read — `.tools` was one flex row at a single `clamp(14–26px)` gap, so the
theme switch, the language switch, the "Photos" caption and the three
collage-jump icons all sat the same distance apart. Nothing said the caption
+ icons are one group, or that they differ in kind from the two toggles (jump
into `#collage` vs. mutate the page you're on).

- **Two clusters, divider at the seam.** `.tools` now holds
  `.tools__group--util` (theme + language) then `.tools__rule` then
  `.tools__group--nav` (caption + icons). The rule moved *out* from between
  the caption and its own icons — where it had been splitting the group it
  should bind — to the real boundary between the two kinds of control.
- **Proximity does the grouping.** Within-cluster gap `10px`; between-cluster
  gap `clamp(18px, 2.6vw, 30px)`, ~2–3× looser by width. No box, no fill, no
  bracket — just the ratio.
- **A hairline binds the caption to its glyphs.** `.tools__group--nav::after`,
  a resting 1px rule the full width of the cluster in `--rule`, lifting to
  `--ink-target` on `:hover` / `:focus-within`. Same 1px-hairline vocabulary
  as `.tool::after`, and deliberately the same ink as it — C15 sent the
  *cursor dot* amber on cream but left `.tool::after` green, so the cluster
  hairline matches the sibling rule, not the dot. Pseudo-element only, so no
  layout rides the transform channel (the `.line__inner` lesson). Checked in
  both pairs: rest = each theme's `--rule`, active = each theme's target ink.
- **Order is util-first, on purpose.** Nav-first (icons nearest the wordmark)
  was tried and reverted: S16/`switch-no-shift` left `.themeswitch`
  width-unpinned, and its "Charcoal"/"Уголь" ~30px swing only cancels for
  controls *downstream* of it in the right-anchored row. Nav-first put the
  icons upstream — they rode the full 30px on every language toggle, the jump
  switch-no-shift had just killed for RU/EN. Util-first keeps them downstream;
  measured drift back to 0, both directions. The `.tools__label::before`
  width-pin from that stage now sits inside `.tools__group--nav` and still
  holds the caption at a constant 57px.
- **Wrap.** `.tools` gained `flex-wrap: wrap` so the two clusters drop as
  whole units in the ~600–900px band instead of the row clipping; re-joined
  to one line under 600px (`flex-wrap: nowrap` in that query), where the
  header already goes two-row and `--head` already budgets for it.

Verified in-browser: structure/order, gap ratio, hairline in both themes,
language-toggle drift = 0 on the icons and on RU/EN both directions, label
pinned 57px EN/RU, no console errors, no horizontal overflow at 1280 or 375,
mobile one-line header below the lockup with 44px icon targets, and
`data-collage-jump` still routes into `#collage`.

**Live artifact not republished** — same collage-placeholder hold. Folds into
the inline rebuild when that lifts.

## C16 — magnetic pull back, controls only (2026-09-07)

Branch `feature/magnetic-controls`. Files: `main.js`, `style.css`, this note,
`CLAUDE.md`, `tests/test_motion.py`. Igor: *"it used to be that when i hover
over interactable things they would slightly move… why u removed it?"* — then
*"can we bring this movement back?"*, and chose **controls only** when asked
the scope (the option C14's own note had pre-approved: *"belongs on non-text
controls only… never on running copy"*).

- **`initMagnetic()` restored verbatim** from `1a94b4c^` — same field maths
  (60px halo, `PULL` 12, per-axis normalise against the element's half-size,
  vector scaled not axis-clamped so a diagonal can't exceed `PULL`, peaks
  halfway out, zero at the rim), same `gsap.quickTo` on `x`/`y` over `D.state`
  retargeted on leave so one tween never fights itself, same measure-once-on-
  enter with the element's own translate subtracted. Called after `initCursor()`
  in the go block — **past the reduced-motion return**, so a `reduce` reader
  never gets it.
- **Scope is the only change from the retired version.** It now queries
  `.tool, .view__back` — the Cream/RU switches (masthead + collage bar), the
  three collage icon-nav buttons, the footer "Back to top", the collage
  "Back" — **not** `[data-magnetic]`. That attribute stays exactly as C14 left
  it: the broad interactive hint the dot's `HOT` colour selector reads, still
  on the text links (`.scrollcue`, `.proof__link`, contact CTA, footer
  handles, `.origin__mark`) which get colour but no movement.
- **`will-change`** is granted only on `:hover` of those controls
  (`.tool:hover, .view__back:hover { will-change: transform }`), same
  standing-layer discipline as the hero lines. The reduced-motion block drops
  that hint and pins `.tool, .view__back` to `transform: none !important` as
  belt-and-braces (the JS already never runs there). `.tool::after`'s hover
  hairline is a pseudo-element and untouched.
- **Transform channel is clear on these elements** — none are `.reveal`
  targets, nothing else tweens them, theme.js only rewrites their text. So the
  pull owns the channel with nothing to compose against (the hazard CLAUDE.md's
  motion section flags).
- Test: `test_magnetic_pull_moves_a_control_but_not_a_text_link` in
  `test_motion.py` — hovering the masthead `.langswitch` shifts its computed
  `transform` off `none` toward the pointer and it eases back to `none` on
  leave; hovering the `.scrollcue` text link (also `data-magnetic`) never
  moves it. Runs on the fine-pointer default; skipped shape matches the other
  cursor cases.

Verified in-browser: pull on all four control types in both themes and both
languages, drift back to exactly `none` on leave (both axes), nothing on the
text links, `data-collage-jump` still routes, no console errors, no horizontal
overflow at 1280 or 375, and `prefers-reduced-motion: reduce` leaves every
control flat.

**Live artifact not republished** — same collage-placeholder hold. Folds into
the inline rebuild when that lifts.

## C17 — magnetic pull reaches the §04 origin mark (2026-09-07)

Branch `feature/magnetic-origin-mark`. Files: `main.js`, `style.css`, this
note, `CLAUDE.md`, `tests/test_motion.py`. Straight after C16 Igor pointed at
the "What Vitnyr stands for" section — *"the history block with 3 lines
showing what they stand for, can u bring it back too?"* — and, asked to pick
how, said: *"i want you to just make it magnetic. don't change the way lines
light up or anything like that."* So this is C16's pull extended to one more
target and **nothing else** — `initOrigin()` (stroke lighting, the panel
reveal, the idle hint) is untouched.

- **`.origin__mark` added to the pull selector** — now
  `.tool, .view__back, .origin__mark`. The mark is a fair target by C14's own
  rule: it is an interactive control (three real `<button>` hit-regions,
  focusable, already answers hover), not running copy. It already carried
  `data-magnetic` for the dot's colour cue; now it moves too.
- **It is also a `.reveal` target — the one real complication.** `.reveal`
  uses the transform channel for its 24px rise (`transition: … transform .9s`
  under `.is-in`). Left alone, every magnetic nudge would be double-eased
  (GSAP `D.state` 0.6s + that CSS 0.9s). CLAUDE.md's motion note allows a
  *transient* transform to hand the channel back once it's done: the rise is
  one-shot and settles at `none`, and §04 is deep enough that the first hover
  is always long after it. So `initMagnetic`'s `capture()` does, once, on the
  first `mouseenter` of a `.reveal` target: `el.style.transitionProperty =
  'opacity'`. The rise still plays for the normal first view; from then on
  GSAP owns the channel unopposed. No DOM change, no second reveal timing.
- **`will-change`** hint extended to `.origin__mark:hover`; the
  reduced-motion block adds it to the `will-change: auto` reset (the existing
  `html.js .reveal { transform: none !important }` already pins the mark flat
  there, and `initMagnetic` never runs under `reduce` anyway).
- Test: `test_magnetic_pull_reaches_the_origin_mark` in `test_motion.py` —
  the mark sits at rest `(0,0)` after its reveal, eases toward the pointer on
  hover (`tx > 1.5`), its `transitionProperty` is `opacity` after the
  handoff, hovering the chess stroke still lights that panel line, and it
  returns to rest on leave.

Verified: pull on the mark in both themes, reveal rise still plays on first
scroll-in, stroke lighting + panel reveal unchanged, settles to exactly
`(0,0)` on leave, `prefers-reduced-motion: reduce` leaves it flat, no console
errors, no overflow at 1280 or 375.

**Live artifact not republished** — same collage-placeholder hold.

## F1 — the footer mark turns once on hover (2026-09-07)

Branch `feature/footer-mark-spin`. Files: `style.css`, this note. Igor: *"there
is vitnyr logo [in the footer] … rotate it 360 degrees when u hover over it.
rotate just once."*

- **CSS only, no `main.js`.** The spin is pure decoration, so it degrades to a
  static mark with JS or GSAP absent — nothing in `main.js` knows about it.
- **Scoped to `.foot`** — `.foot .footmark` base gets `transform: rotate(0deg)`,
  `.foot .footmark:hover` gets `rotate(360deg)` + `transition: transform
  var(--t-turn) var(--e)`. The same `.footmark` in the `#collage` view bar is
  left alone. A full turn lands the mark back on its own geometry exactly, so
  it is never left off-register — the reason a full 360 and not, say, a wobble.
- **`--t-turn: 1.2s`**, new token beside `--t`. Started at .8s (`D.correct`);
  Igor asked for it 30–50% slower so the whole rotation reads — bumped to
  `D.count`'s 1.2s, the "measured, counting" register, a turn you watch finish.
- **`--e` is allowed here.** The scrollcue note bans the ease-out on a loop
  that returns to its start value (it snaps mid-way). This doesn't loop: 0 ->
  360 once, accelerate out of rest, settle soft into the finish.
- **"Just once" = `transition` on `:hover` only.** Pointer-leave has no
  transition, so the mark jumps 360 -> 0 with no visible motion (360deg ==
  0deg) and no reverse spin. Each new hover re-arms one clean turn. Cost:
  leaving mid-spin cuts straight back to rest — accepted for a flourish.
- **No `:focus-visible` / no tab stop.** The mark is `role="img"`, not a
  control; making it focusable would plant a keyboard stop on decoration.
- **`will-change: transform`** on `:hover` only; reduced-motion block resets it
  to `auto` and adds `.footmark:hover { transform: none !important }` — without
  that, the global `transition-duration: .01ms` override just turns the hover
  into an instant flip.

Verified: one clockwise turn on hover in both themes (amber/green land back in
place), instant silent reset on leave, re-hover turns again cleanly, EN + RU,
1280 + 375, no horizontal scrollbar during the turn (checked across real
animation frames), `prefers-reduced-motion: reduce` leaves it flat, no console
errors.

**Live artifact not republished** — same collage-placeholder hold.

## Verified

- No horizontal overflow at 1440px or 375px (`scrollWidth` equals `innerWidth`
  in both; the only element outside the viewport is the parked skip link).
- Every hex in the build is one of the ten pair values. No gradients, shadows,
  or rounded cards (the one `border-radius` is the cursor circle).
- Contrast in both pairs: all body text >= 5.45:1, all accent ink >= 3.07:1.
- Fonts resolve to Lora / Inter / JetBrains Mono, Cyrillic included.
- The dot disables itself on coarse pointers — confirmed at 375px: `has-cursor`
  never goes on, so the native pointer is never hidden. The magnetic pull
  (`initMagnetic`, back at C16 on controls only) is behind the same
  `finePointer` gate, so it is off there too.
- Hero plays and completes in both languages, both themes, both widths, and
  releases its compositor layer when it lands.
- Counters animate from 0 through the observer with ScrollTrigger absent —
  each on its own duration so the four figures don't read as one gauge.
- Reveals: nothing fires off-screen, and the stagger reads top-to-bottom.
- Skip link moves focus to `#main`, not just the scroll position.
- No console errors.

Not verified by eye: everything below the hero. The preview pane repaints only
on demand, so those sections were checked by measuring the DOM rather than
looking at them. Worth a scroll-through on a real browser.
