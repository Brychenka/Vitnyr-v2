# Photo collage — build plan

Written 2026-09-04, before any collage code existed. Stages 0–2 are built and
merged to `main` (`72d1da5`, 2026-09-05) — `#collage` was rebuilt as a routed
view partway through, during the review gate below; read "Notes for the next
chat" before touching this feature. Stages 3–6 are not started; stage 3 is
blocked until real photographs exist.

The stage prompts below are the operational part of this file. Paste one
into a fresh chat, one stage at a time. `collage-review.md` next to this
file is the review gate that ran before stages 0–2 merged.

## Notes for the next chat

Four things a chat starting fresh on this feature would otherwise have to
rediscover the hard way or guess at — none of them are written down anywhere
else:

- **Moderate, not wild.** Igor's own words, choosing between options mid-build:
  *"you dont have to go that wild. you can make it moderat."* The references
  below (xxix.co especially) are read for technique — hard edges, pure CSS, no
  library — not for how aggressively they overlap. The shipped composition has
  exactly one deliberate overlap (tile 4 over tile 3); that was a deliberate
  dial-down from a denser first draft, not a limitation of the approach. Don't
  push it toward xxix.co's own density without asking first.
- **Preview stand-ins are throwaway, always.** When Igor needs to judge a
  composition before real photographs exist, grayscale placeholders (Lorem
  Picsum was used here) are fine to pull into a *preview artifact* — never
  into the repo, never into `assets/collage/`, never into anything that ships.
  Delete them once he's looked.
- **Don't republish the live "Vitnyr Signature" artifact for this feature
  yet.** That's the public link Igor already shares. Republishing it while
  `#collage` still holds empty placeholder boxes puts unfinished work on a
  link other people may open. Stage 6's prompt already says this — repeating
  it here because a chat skimming past Stage 6 could otherwise republish
  early "just to check."
- **Update, same day:** a Playwright suite landed in `tests/` (65 tests, see
  `tests/test_collage.py`) and fixed a real bug this note was circling — deep-
  link focus landed on the `<section>` wrapper instead of the heading, because
  the browser's own scroll-to-fragment step ran after `applyOpen()` and won.
  `test_scroll_position_restored_on_return` covers the warm path (open from
  the link, close, land where you were) and passes. What's still *not*
  asserted anywhere: opening via a cold deep link (`#collage` in a fresh tab)
  and then closing — does that land at the top of the page, or wherever the
  browser's fragment jump put it? Add that one case to `test_collage.py`
  before trusting it either way.

## References

Four sites, inspected by reading their DOM rather than trusting
screenshots. The finding is consistent and useful: **award-winning photo
collages are not doing anything exotic.** They are careful CSS layout,
disciplined image delivery, and restraint about how many photos ship.

**dennissnellenberg.com** — GSAP 3.9.1 + ScrollTrigger, Locomotive Scroll,
Barba.js, vanilla-lazyload, jQuery. But the entire home page ships *one*
image — a single 3000×3141 portrait — carrying a page that otherwise runs
on type and motion. The lesson is rationing, not technique. Take: fewer,
larger, better photos beat a wall of thumbnails. Leave: the whole stack —
we dropped ScrollTrigger deliberately and don't need Barba on one page.

**xxix.co** — Awwwards' own "overlapping image gallery" exemplar and the
closest aesthetic match to Vitnyr: brutalist, hard-edged, editorial. Every
image computes `border-radius: 0px`. There is **no GSAP, no Lenis, no
WebGL, no canvas** — the overlapping collage is plain CSS layout. Delivery
is `loading="lazy"` + `decoding="async"` + `srcset` on every image through
an optimiser proxy. This is the reference to build against.

**seanhalpin.design** — fourteen images, zero layout shift, no animation
library. Every image resolves an intrinsic aspect ratio from its own
`width`/`height` attributes, so the box is reserved before a byte of image
data arrives. This is the single technique that protects our zero-CLS
record.

**bryce-jones.com** — cited on Awwwards for sticky-column scrolling: one
column pinned while an adjacent column of images scrolls past. Held as the
*fallback* composition if the asymmetric overlap doesn't survive contact
with only three usable photographs. Pattern noted from Awwwards; site not
inspected directly.

## Two decisions, made in advance

**Treatment: monochrome, mapped to the theme's own ink.** Climbing holds
are saturated by design and a chess board is high-contrast black and
white. Dropping either into a page with ten permitted hex values, a ban on
a third colour, and two accents carrying *semantic* meaning (amber =
specimen, green = target) puts uncontrolled colour into the largest
elements on the page. Grayscale keeps photos inside the pair system, works
from one asset in both themes, and leaves amber and green doing their job.
Implement as one custom property, valued per theme, on `.collage img`.

Honest argument against: grayscale is the safe answer and every second
portfolio does it. Colour is a legitimate call — but it is a deliberate,
documented exception to the colour rule and belongs in `BUILD-NOTES.md` as
a fourth deviation, not slipped in. What is *not* on the table is
amber-tinted duotone: that floods a large area with a colour meaning "the
thing being examined," and the photographs are not specimens.

**Delivery: repo files, inlined as data URIs at republish.** External
hosting adds a 404 surface to a project whose source has vanished from
disk twice. Keep real files in `assets/collage/` and base64-inline them
when rebuilding the single-file artifact — the same step that already
inlines the CSS and JS. Budget is part of the decision: **at most 6
images, WebP, ≤120 KB each, ≤720 KB total** — roughly 960 KB base64,
comfortably under the 16 MB artifact cap.

## Architecture: separate view, not separate file

Recorded in `CLAUDE.md` under the content decisions. Summary: the live
artifact is one self-contained HTML file, so a second `.html` would be
unreachable from it and the collage would silently vanish from the
published link. The collage is a full-screen view inside `index.html`,
routed by URL hash, that behaves like a page — deep-linkable, own header,
own way back, browser back works, theme and language persist with no
flash, focus moves on navigation, scroll resets.

## The stage ladder

Numbered because the order carries information: each stage leaves the site
shippable, and each can only break what it just added. Structure before
pixels, pixels before motion, motion before polish — so when something
looks wrong you already know which stage owns it.

| Stage | Scope | State |
|---|---|---|
| 0 | Shot list and asset contract, no code | done |
| 1 | View skeleton, copy, entry button | done |
| 2 | Composition (CSS only, empty boxes) | done |
| 3 | Real images and delivery | blocked on the shoot |
| 4 | Motion, inside the existing system | not started |
| 5 | Signature move and polish | not started |
| 6 | Verify, document, merge, republish | not started |

### Stage 3 — images and delivery

```
Read CLAUDE.md and reference/collage-shotlist.md. Continue on
feature/photo-collage. Photos are in assets/collage/.

Each <figure> gets a <picture> with a WebP source and a JPEG fallback,
srcset at 1x and 2x, explicit width and height attributes matching the
reserved aspect ratio, loading="lazy", decoding="async", and real alt
text in both languages via the existing i18n mechanism — alt is a
translatable string, not an afterthought.

Treatment: grayscale, mapped to the theme's own ink. Define the filter
once as a custom property in :root and give it a different value per
theme, so one asset reads correctly on both cream and charcoal. Do not
tint toward amber or green — those two colours carry meaning on this
page and photographs are not specimens.

Delete the placeholder hairline boxes and the PLACEHOLDER comment.

Budget, enforced: 6 images maximum, 120KB each, 720KB total. If a photo
misses budget, recompress it — do not raise the budget.

IMPORTANT: BUILD-NOTES.md currently lists "no images to lazy-load" as a
verified property. That statement becomes false in this stage. Correct
it in the same commit rather than leaving a verified claim that no
longer holds.

Verify: measure each figure's box before and after image load and confirm
it is unchanged — zero layout shift is an existing verified property and
this stage is the one that can break it. Confirm nothing above the fold
fetches an image it does not need. Both themes, both languages, 375 and
1280.

Commit. Stop and report.
```

### Stage 4 — motion

```
Read CLAUDE.md's motion section and BUILD-NOTES.md's "Motion" pass.
Continue on feature/photo-collage. Motion only.

Do not add a library. ScrollTrigger is deliberately absent — see
BUILD-NOTES deviation 2 — and must not come back.

Add .reveal to the tiles so they use the single existing reveal rhythm:
24px rise plus fade, 0.9s, 0.08s stagger, once, via the
IntersectionObserver in buildReveals(). That stagger chain is capped at 4
beats; six tiles must not extend the cap. Order them by screen position,
the way the existing code already does.

If you add parallax, it must: ride the existing Lenis/GSAP ticker, use
the single --e curve / 'brand' CustomEase, take its duration from the D
table in main.js rather than inventing a number, and stay under 40px of
displacement. If it cannot be done inside those constraints, do not do it
and say why.

Reduced motion: under prefers-reduced-motion: reduce every tile sits at
rest, fully visible, no transform. Confirm the failsafe() sweep reaches
the new tiles.

Verify by driving real frames, not one screenshot. The preview pane
repaints on demand, and BUILD-NOTES documents several real bugs that a
single screenshot hid. Confirm: nothing fires off-screen, nothing is
stuck at opacity 0 with JS disabled, the stagger reads top to bottom.

Commit. Stop and report.
```

### Stage 5 — signature move and polish

```
Read CLAUDE.md and BUILD-NOTES.md's motion pass. Continue on
feature/photo-collage.

Integrate the collage with the existing signature move. The tiles are not
links, so decide deliberately whether they take data-magnetic: the
magnetic field is normalised to element size and capped at 12px, and a
large image tile drifting under the cursor may read as a rendering bug
rather than an affordance. Recommend and justify BEFORE implementing —
do not just wire it up. "We added nothing" is an acceptable outcome.

Hover and focus states are built from the vocabulary already on the page:
the hairline, the scaleX underline, the cursor's green ring. Do not
introduce a new interaction language for one section. If tiles become
focusable, keyboard focus must be visibly distinct.

will-change is requested on hover only — never permanently, never under
reduced motion. This was a real finding in the motion audit.

Verify on a coarse pointer at 375px that has-cursor never goes on and the
native pointer is never hidden. Both themes, both languages.

Commit. Stop and report.
```

### Stage 6 — verify, document, ship

```
Read CLAUDE.md. Continue on feature/photo-collage. Final pass — add no
new features.

Run the full checklist from CLAUDE.md step 3: both themes, both
languages, 375px and 1280px, prefers-reduced-motion, no console errors,
no horizontal overflow (scrollWidth === innerWidth).

Audit the whole diff: confirm every hex is one of the ten pair values,
and that no gradient, shadow, or border-radius was introduced anywhere
except the existing cursor dot.

Update BUILD-NOTES.md — add a collage section, record any deviation from
the guide, and confirm the "no images to lazy-load" correction from
Stage 3 landed. Update CLAUDE.md's architecture section for the new
assets/collage/ directory.

Merge feature/photo-collage into main and push.

Republish the live artifact to the SAME URL:
https://claude.ai/code/artifact/f516ba87-7ade-47a6-b65c-c5944147006c
Rebuild the inlined single-file HTML from the current repo files — read
the artifact before publishing so a concurrent chat's work is not
clobbered. Inline the collage images as data URIs. Report the rebuilt
file's size and confirm it is under the 16MB cap.

Report what shipped.
```

## Why the prompts read like this

Habits that keep staged work cheap and predictable, worth reusing on the
next feature:

- **One stage, one chat.** The repo is the handoff, not the conversation.
  A chat carrying three commits of context pays for it on every turn.
- **A scope fence, always.** "Layout only." "No JS." "index.html only."
  Most cross-stage bugs are one stage quietly editing another's file.
- **Forbid-lists over explanations.** "Do not reintroduce ScrollTrigger"
  costs four words; re-deriving why it was dropped costs a page of
  reading and sometimes gets it wrong anyway.
- **Acceptance checks, not vibes.** Every stage ends in something
  falsifiable — a measurement, a number, a screenshot at a named width.
- **An explicit stop.** Without "stop and report," a capable model
  helpfully runs three stages and the resulting commit is unreviewable.
