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
| 6 | Respect the reader | prefers-reduced-motion path, no images to lazy-load, no layout shift |
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
   Accent colour lives in ink — rules, glyphs, the display numerals.

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
- **Collage nav icons have looks but no behaviour yet.** The three
  `.tool--icon` buttons in `nav.tools` (chess / carabiner / book) render and
  are responsive, but nothing happens on click: no `data-jump`, no hook into
  the `#collage` router, no ids on the target figures. That's the design
  handoff's own "behaviour" section — see
  `reference/design_handoff_collage_nav_icons/README.md` — deliberately
  deferred to a separate pass.

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
