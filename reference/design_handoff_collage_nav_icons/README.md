# Handoff: collage nav icons (chess / climbing / English)

## Overview
Three icon buttons added to the masthead `nav.tools`, next to the existing
Cream and RU switches. Each one jumps the collage view to the photograph for
that discipline and briefly flashes that tile's hairline in the target green.

## About the design files
`Vitnyr Collage Nav Icons.dc.html` in this bundle is a **design reference**
built as standalone HTML — a prototype of the intended look and behaviour, not
production code to copy. Recreate it in `site-v2` using that project's own
patterns: plain HTML in `index.html`, CSS in `style.css` on the existing
custom-property tokens, vanilla JS in `main.js`. No build step, no
dependencies, no framework. Read `site-v2/CLAUDE.md` and `BUILD-NOTES.md`
first and follow them where they conflict with anything here.

## Fidelity
**High-fidelity.** The SVG path data below is final — paste it verbatim.
Sizes, weights, and states are specified exactly.

## The three glyphs
All three: `viewBox="0 0 24 24"`, rendered at 17×17 in the nav,
`fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
stroke-linejoin="round"` (the chess glyph is the exception — see below), and
`aria-hidden="true"` because the button carries the label.

### 1. Chess — filled checkerboard corner
```html
<svg viewBox="0 0 24 24" aria-hidden="true">
  <rect x="1" y="1" width="10" height="10" fill="currentColor"/>
  <rect x="13" y="1" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <rect x="1" y="13" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <rect x="13" y="13" width="10" height="10" fill="currentColor"/>
</svg>
```

### 2. Climbing — screw-lock carabiner (offset-D)
Frame is an open C-loop; the gate is a short straight bar broken either side of
the locking barrel, which is a hairline quad with mitred joins.
```html
<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor"
     stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
  <path d="M16.9 8.4C17.7 5.7 16.1 3.6 13.3 3 10.7 2.4 7.7 3.2 6.3 5.4 5 7.5 4.8 10.4 5 13.2 5.2 16.4 6.1 19 7.9 20.5 9.4 21.8 11.5 21.6 12.7 20.1 13.3 19.4 13.6 18.9 13.9 18.4"/><path d="M16.9 8.4 16.42 10"/><path d="M14.74 15.6 13.9 18.4"/><path d="M14.95 10.21 17.53 10.99 16.21 15.39 13.63 14.61Z" stroke-linejoin="miter"/>
</svg>
```

### 3. English — open book
```html
<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor"
     stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4.5 5.5c2-1 4.5-1 6.8 0v13.2c-2.3-1-4.8-1-6.8 0z"/>
  <path d="M19.5 5.5c-2-1-4.5-1-6.8 0v13.2c2.3-1 4.8-1 6.8 0z"/>
</svg>
```

## Markup — masthead
Append inside the existing `nav.tools` in `index.html`, after the two
switches, preceded by a hairline divider:

```html
<span class="tools__rule" aria-hidden="true"></span>
<button class="tool tool--icon" type="button" data-jump="fig-chess"
        aria-label="Chess photograph" title="Chess" data-magnetic>…svg…</button>
<button class="tool tool--icon" type="button" data-jump="fig-climb"
        aria-label="Climbing photograph" title="Climbing" data-magnetic>…svg…</button>
<button class="tool tool--icon" type="button" data-jump="fig-english"
        aria-label="English coaching photograph" title="English" data-magnetic>…svg…</button>
```

Add matching ids to the first three collage figures in `#collage`:
`id="fig-chess"` on the `01-chess-board` figure, `id="fig-climb"` on
`02-climb-board`, `id="fig-english"` on `03-call`.

## CSS
Reuse `.tool` as-is — its `::after` underline, `--fg2` → `--fg` hover
and `--ink-target` rule already match the design. Add only:

```css
.tools__rule { width: 1px; height: 14px; background: var(--rule); }
.tool--icon { display: inline-flex; padding: 4px; }
.tool--icon svg { display: block; width: 17px; height: 17px; }
@media (pointer: coarse) { .tool--icon { padding: 13px 10px; } }  /* 44px target */
```
Use whatever the project's existing hairline token is called in place of
`--rule` (the collage slots' border colour). No new colour values —
`--fg2` default ink, `--fg` on hover/focus, `--ink-target` underline.

## Behaviour
On click, in `main.js`, alongside `initCollageView()`:
1. If the collage view is closed, open it through the existing router (push
   `#collage`, the same path `[data-collage-open]` takes) — do not duplicate
   the open logic.
2. Scroll the target figure into view **inside the view's own scroll
   container** — the design uses `container.scrollTo({top: fig.offsetTop - 14,
   behavior: 'smooth'})`. Do not use `scrollIntoView`.
3. Flash that figure's `.collage__slot`: set `border-color` and
   `inset 0 0 0 1px` box-shadow to `--ink-target`, revert after 1300ms;
   clear any pending timer first so repeat clicks behave.
4. Under `prefers-reduced-motion: reduce`, jump instead of smooth-scrolling
   and keep the flash (it is a colour change, not motion) or drop it — match
   whatever the project already does for the collage router.

Focus behaviour should follow the existing view: the icons are buttons in the
masthead, so keyboard order is Cream → RU → chess → climbing → English.

## Design tokens used
Ink `--fg2` (rest) / `--fg` (hover, focus-visible), underline and flash
`--ink-target`, divider = existing hairline rule token. Stroke 1.6 at a 24
viewBox, rendered 17px. Transition: the project's `var(--t) var(--e)`.
No radius, no shadow, no gradient.

## Assets
None — all three icons are inline SVG path data, given in full above.

## Files
- `Vitnyr Collage Nav Icons.dc.html` — the design reference (turn 4 at the top
  is the final set; earlier turns are rejected explorations, ignore them)
- Target: `site-v2/index.html`, `site-v2/style.css`, `site-v2/main.js`
