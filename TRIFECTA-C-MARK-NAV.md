# Trifecta Order C — the mark as navigator

**Idea 4 of the 2026-09-13 trifecta brainstorm.** §04's mark already maps
stroke → discipline on hover. Promote it from an explainer to an instrument:
each stroke becomes a real jump, and the reader's position in the argument is
readable from the masthead.

One of three independent orders. The other two are
`TRIFECTA-A-SPECIMENS.md` and `TRIFECTA-B-DOSSIERS.md`. **C runs standalone** —
it needs neither, though its jump targets get better when B has landed.

**One stage = one chat = one branch**, per `CLAUDE.md`. Before touching code,
read `CLAUDE.md`, `BUILD-NOTES.md`, `JURY-PASS-II.md` (its Standing Orders
bind here too) and this file's stage in full.

---

## Correction to the original pitch — read this first

The brainstorm proposed "each stroke lights as you scroll through its
section." **That half does not work as pitched**, and the reason matters:

§04 sits at page depth ~6,100 of 8,650px. Every discipline section is
*above* it. By the time the mark is on screen the reader has already passed
everything it would be indicating, so a scroll-linked light on §04's own mark
would fire where nobody can see it. The scroll indicator has to live in
something that is always visible — the masthead — which raises its own
problem (see C0.3). Stage C2 is written against the corrected shape, not the
pitch.

The navigation half (C1) is sound as pitched.

---

## Stage C0 — three decisions (no code)

**Output:** answers recorded here plus a BUILD-NOTES entry. **No source file
changes.**

### C0.1 — buttons or anchors?

Today the three hit regions are real `<button aria-pressed>` elements
(`index.html:511–521`) — a selection semantic, deliberately chosen so
keyboard Tab and touch tap both work natively, with mouse hover layered on
for fine pointers only. Navigation is a different semantic.

- **(i) Cheap.** Keep the three buttons as the preview control and make the
  **panel item** the link — `.origin__panel-item` already shows the active
  discipline's name and stat, so it becomes
  `<a href="#chess">Chess · 2100 →</a>`. Nothing about `aria-pressed`
  changes; no existing test breaks. Costs one extra click for a mouse user.
- **(ii) Stronger.** Convert the three hits to `<a href="#…">`. One gesture
  does both: hover previews, click goes. This is the better instrument and
  the honest cost is four tests plus an aria model change —
  `aria-pressed` disappears (an anchor is not a toggle), and
  `setActive()` (`main.js:629`) currently writes `aria-pressed` on all three
  hits and `aria-hidden` on the panel items. Affected:
  `test_origin_mark_keyboard_focus_reveals_its_panel`
  (`tests/test_motion.py:99`),
  `test_origin_mark_hover_switches_between_disciplines` (`:115`),
  `test_origin_mark_rests_on_english_before_any_interaction` (`:133`), and
  `test_origin_mark_shows_a_focus_ring_on_the_visible_figure`
  (`tests/test_a11y.py:201`).

**Recommend (ii).** But whichever is chosen, the four `.origin__*` a11y
guarantees survive unchanged: all three disciplines readable with JS absent
(`test_origin_mark_shows_all_disciplines_statically_without_js`), interactive
under reduced motion, complete under reduced motion, and a visible focus ring
on the figure.

> **Decision: _pending_**

### C0.2 — the mark points backwards

§04 sits *after* §03 today, and after all three dossiers if Order B lands.
So every jump from the mark scrolls the reader **up**, to something already
read. That is not automatically wrong — a recap index is a legitimate device,
and "here are the three again, go back to any of them" is honest — but the
copy around the mark has to say so, or the jumps read as a lost scroll
position.

Three options for Igor:

- **(a) Frame it as a recap.** Keep §04 where it is; the panel gains a
  "back to" sense. Cheapest, no structural change.
- **(b) Move §04 above the disciplines.** The mark then introduces the three
  and the jumps go forward. Costs: the section renumbering, and
  `measureOrigin()` / `.past-origin` (`main.js:72`) uses `#origin`'s offset as
  the point where the masthead progress rule flips its ink from specimen to
  target — move `#origin` to near the top of the page and that flip happens
  almost immediately, which destroys the signal. If (b) is chosen, the ink
  switch must be re-pointed at a deliberately chosen new element and that
  choice recorded, not left to follow `#origin` by accident.
- **(c) Two instances.** A small index near the top, the full explainer at
  §04. Rejected in advance unless Igor asks for it: two strengths of one mark
  on one page is exactly the "faded logo" reading J7 was raised about.

> **Decision: _pending_**

### C0.3 — the masthead indicator must not dim the logo

The obvious home for a scroll indicator is the masthead lockup: its mark is
the same geometry, split into the same three parts
(`.lockmark__part--left/--right/--stem`, `index.html:112–114`), already
individually addressable.

**Do not light and dim those three parts.** That is the header logo. J7
(Jury Pass II, 2026-09-12) exists because §04's mark resting two-thirds
dimmed read as "a bug or a loading state" *while the same mark rendered at
full ink in the header above it* — dimming the header copy itself makes the
page's logo flicker between three strengths as the reader scrolls. It would
also collide with `initLockmark()`'s one-time draw-in (`main.js:860`,
`style.css:288–292`), whose clip rects sit at `forwards` so the finished mark
holds for good.

The indicator therefore needs a device that is not the logo. Recommended, and
cheapest by a distance: **segment the progress hairline.** `.progress`
already lives on the masthead's bottom edge, already scales with scroll depth
and already crossfades between the two inks (`index.html:204–207`,
`trackProgress()` at `main.js:75`). Three segments, one per discipline, the
active one at full ink — same hairline vocabulary the whole page speaks, no
new element, no new colour, and it is driven from the scroll handler that
already exists.

Alternatives if Igor dislikes it: a three-tick rule beside the `.tools`
group; or no masthead indicator at all, in which case C2 is dropped and C1
alone is the order.

> **Decision: _pending_**

---

## Stage C1 — the strokes navigate

**Branch:** `feature/mark-navigates`. **Blocked on C0.1 and C0.2 only.**

### Targets

- If Order B has landed: `#english`, `#chess`, `#climbing`.
- If not: the three `.domain` cards in `#disciplines` need stable ids —
  `id="domain-english"`, `domain-chess`, `domain-climbing`. Add them in this
  stage; they are language-neutral, harmless, and Order B can re-point the
  mark later.

Either way, `data-discipline` on the three glyph parts and the three hits is
already `english` / `chess` / `climbing` and is the natural key. Do not
introduce a second naming scheme.

### Reuse the routing that already exists

`initSpecimenPermalinks()` (`main.js:879`) is the pattern, and it is correct
in four ways worth copying exactly:

1. `history.pushState` rather than assigning `location.hash` — Back keeps
   working **and** no `hashchange` fires, so the collage router's
   `routeAfterHashChange()` (`main.js:1058`) stays out of it. Assigning the
   hash directly would fire an unrelated View Transition on every stroke
   click.
2. `lenis.scrollTo(target, { duration: 1.2 })` when Lenis is present, falling
   back to `target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' })`.
3. `tabindex="-1"` set on the target if absent, then `focus({ preventScroll:
   true })` — the reader lands *inside* the destination, not merely near it.
   This is the skip-link bug documented in BUILD-NOTES; scroll alone is not
   navigation.
4. Wired **before** the reduced-motion return in `main.js`, because it is
   navigation, not motion. The only concession to reduced motion is an
   instant scroll.

Put the new code in `initOrigin()` or a sibling called from the same place;
do not add a second scroll or history listener.

### What must not change

- **C6 — the rest state is English lit.** `clearPaint()` (`main.js:625`)
  re-asserts `paint('english')` rather than stripping classes, deliberately:
  English is the offer, chess and climbing are proof it transfers, not
  equal-weight alternatives. `test_origin_mark_rests_on_english_before_any_interaction`
  asserts it at load, before any scroll, so it cannot pass by coincidence.
- **J7 — the raised dim floor.** `--amber-dim` / `--green-dim` were re-tuned
  on 2026-09-12 so the two unlit strokes read quiet, not washed out.
  `test_origin_mark_dim_strokes_use_the_raised_floor` is parametrised per
  theme. Adding navigation must not re-tune them.
- **The one-shot idle hint.** It previews all three pairs twice when §04
  first scrolls into view, then settles back, and it holds for `DRAW_HOLD =
  1.0s` so it never drives the same strokes as S7's draw-in in one frame. Its
  `engaged` flag goes permanently true on the first real interaction —
  deliberately checked inside every timeline step rather than trusting
  `.kill()`, because a step already queued on GSAP's ticker can still fire
  after kill. A click handler must set `engaged` the same way hover and focus
  do, or a queued idle step can repaint a stale discipline over the one the
  reader just chose.
- **The transform channel.** `.origin__mark` is both a `.reveal` target and
  `data-magnetic`; `initMagnetic()` hands the transform channel back from the
  reveal on first hover by setting `transitionProperty = 'opacity'`. Do not
  add a transform anywhere in this path.
  `test_magnetic_pull_reaches_the_origin_mark` (`tests/test_motion.py:510`)
  and `test_origin_mark_holds_still_for_the_hover_states` (`:769`) both
  guard this — the second one exists because the hover states are colour
  only, by C5.
- **Never redraw the mark.** The V path lives once in `<defs>` as `#glyphV`
  and is referenced twice via `<use>`, each half clipped at `x=50`, the
  shape's verified symmetry axis. No coordinate is touched by this order.

### Tests

Add: a stroke click writes the right hash, moves focus into the destination,
and Back returns — the shape of
`test_specimen_permalink_updates_the_url_and_moves_focus`
(`tests/test_content.py:286`). Add the reduced-motion case: navigation still
works, scroll is instant.

Regression-prove per Standing Order 5: stash, watch the new test fail against
unmodified `main`, pop, watch it pass.

---

## Stage C2 — the indicator

**Branch:** `feature/discipline-progress`. **Blocked on C0.3. Drop this stage
entirely if C0.3 chose "no masthead indicator".**

Written against the recommended option — segmenting `.progress`.

- Add `trackDiscipline(y)` beside `trackProgress(y)` and call it from the
  **existing** `onScroll(y)` (`main.js:82`). The file's comment there is
  explicit that the progress hairline rides the same scroll source and there
  is no second listener; keep it that way.
- Measure the three section offsets the way `measureOrigin()` does: once at
  init, again on `resize`, again on the `vitnyr:langchange` event — never per
  scroll frame. Russian copy changes section heights, so the langchange
  re-measure is not optional.
- Express the active segment with a class on `<html>` or on `.progress`, and
  let **CSS own the crossfade**, exactly as `.past-origin` does today. The JS
  picks the side; it does not animate anything.
- Reduced motion: the indicator is state, not motion, so it still updates —
  but it must not introduce a transition that survives the global
  `transition-duration: .01ms` override at `style.css:1823`.
- With JS absent, `.progress` sits at `scaleX(0)` and is invisible; it
  carries nothing a reader needs. Keep that true.

**Do not** dim `.lockmark__part--left/--right/--stem`. See C0.3.

### Tests

`test_progress_rule_tracks_scroll` (`tests/test_motion.py:302`) and
`test_progress_rule_switches_ink_at_origin` (`:329`, parametrised per scheme)
already cover the hairline. Extend rather than replace them, and add: the
active segment matches the section actually on screen at three measured
scroll depths, in both languages.

---

## Do not

- Give a discipline its own colour. Two inks, both already semantic.
- Add a second easing curve or reveal rhythm — extend `D` (`main.js:36`).
- Add a second scroll listener, a second history listener, or a second
  in-page routing idiom.
- Reopen C5 (colour is the mark's only feedback channel — the stem's scale
  flourish was dropped, not extended to the arms), C6, or J7.
- Rename `data-discipline` values or any existing id.
- **Republish the live artifact** (Jury Pass II Standing Order 2). Say in your
  BUILD-NOTES entry that you did not, and why.

---

## Verify (every stage)

Both themes, both languages, 375 and 1280, `prefers-reduced-motion: reduce`,
no console errors, no horizontal overflow. Keyboard: Tab to each stroke,
Enter, confirm focus lands in the destination. Touch: tap each stroke with
`has_touch=True` and compare against `innerWidth`, not `scrollWidth` —
`scrollWidth` cannot see a masthead clip. Drive a real Chromium
(`tests/.venv/bin/python`, Playwright installed) and take real frames; the
preview pane repaints on demand and one screenshot proves nothing for
anything scroll-driven. Run the full suite and report the number.

---

## Stage map

| Stage | Branch | Blocked on | Status |
|---|---|---|---|
| C0 — three decisions | none (no code) | Igor | **open** |
| C1 — the strokes navigate | `feature/mark-navigates` | C0.1, C0.2 | pending |
| C2 — the indicator | `feature/discipline-progress` | C0.3 | pending (dropped if C0.3 says no) |
