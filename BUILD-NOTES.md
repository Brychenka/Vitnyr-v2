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
   colour. The cursor is a flat dot that opens into a green ring on interactive
   elements instead.
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

## Verified

- No horizontal overflow at 1440px or 375px (`scrollWidth` equals `innerWidth`
  in both; the only element outside the viewport is the parked skip link).
- Every hex in the build is one of the ten pair values. No gradients, shadows,
  or rounded cards (the one `border-radius` is the cursor circle).
- Contrast in both pairs: all body text >= 5.45:1, all accent ink >= 3.07:1.
- Fonts resolve to Lora / Inter / JetBrains Mono, Cyrillic included.
- Cursor and magnetic effects disable themselves on coarse pointers — confirmed
  at 375px: `has-cursor` never goes on, so the native pointer is never hidden.
- Hero plays and completes in both languages, both themes, both widths, and
  releases its compositor layer when it lands.
- Counters animate from 0 through the observer with ScrollTrigger absent.
- Reveals: nothing fires off-screen, and the stagger reads top-to-bottom.
- Skip link moves focus to `#main`, not just the scroll position.
- No console errors.

Not verified by eye: everything below the hero. The preview pane repaints only
on demand, so those sections were checked by measuring the DOM rather than
looking at them. Worth a scroll-through on a real browser.
