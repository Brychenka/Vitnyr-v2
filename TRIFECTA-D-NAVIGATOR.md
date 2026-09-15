# Trifecta Order D — the mark becomes the instrument

**Written 2026-09-15, from Igor's brief**: move the mark up so it is the
second thing a reader meets after the hero; make it plainly clickable; a
click opens that discipline's material — achievements, years coaching,
common mistakes — with **English shown by default** and the other two
revealed on demand.

Supersedes `TRIFECTA-C-MARK-NAV.md` Stage C1. Replaces `TRIFECTA-B-DOSSIERS.md`
Stages B1–B3 with a lighter form. See "What this does to Orders B and C".

**One stage = one chat = one branch**, per `CLAUDE.md`. Before touching code,
read `CLAUDE.md`, `BUILD-NOTES.md`, `JURY-PASS-II.md` (its Standing Orders
bind here too) and this file's stage in full.

> **Draft-only, standing instruction (2026-09-15).** Nothing here merges to
> `main` and nothing is pushed until Igor lifts it. Each stage commits on its
> own branch and stays there.

---

## The concept, in one line

**The page already speaks the language of instruments — it just never built
one.**

That is not a metaphor imposed from outside. It is the repo's own vocabulary,
already in the code and the notes: the facts row is *"four readings off four
unrelated instruments"*; `.fact--scale` is *"a position on a continuum"* with
a hairline gauge tick; `.fact--count` is *"a tally"*; §02 is **Specimens**;
amber is *the specimen under examination* and green is *the target*; the
masthead hairline is a **gauge** that changes ink as you pass a threshold.

The mark is a V/Y built from three strokes — left arm, right arm, stem — each
already carrying `data-discipline`. That is a **dial with three positions**.
Below and beside it sits `.origin__panel`, three name/reading pairs separated
by hairlines. That is a **readout**.

Nobody wired the dial to the readout. This order does exactly that, and
nothing more clever than that.

Why this framing matters practically: it means the whole feature is built
from vocabulary the page already owns. No new colour, no new curve, no new
rhythm, no new label pattern, no fourth glyph. Most of the work below is
**deleting the code that keeps the readout hidden**.

---

## Two moments, and then restraint

An awards-grade page has one or two moments and is otherwise disciplined.
This order proposes exactly two, and both are already half-built:

**Moment 1 — the instrument calibrates itself.** On arrival: the hero's words
land, *then* the mark draws its three strokes (S7's existing draw-in), *then*
it walks the three readings once and settles on English (the existing idle
hint). Three systems that currently race each other become one sequence. The
reader learns what the instrument does without being told.

**Moment 2 — the rule moves.** A hairline marker sits against the committed
discipline in the readout. Hover previews with ink only; **a click slides the
rule.** That single moving hairline is the entire answer to "make it clear
it's clickable" — and it is the only thing on the page that moves that is not
a reveal.

Everything else is quiet on purpose.

---

## Stage D0 — the decisions

### D0.1 — the whole of §04 moves — **answered**

The entire "Name & mark" section relocates to sit directly after the hero.
One mark on the page (plus the masthead lockup, as today). New numbering:

```
01  Name & mark      #origin       ← moved; the instrument
02  The method       #method
03  Specimens        #specimen
    (.breath, unnumbered, stays between 03 and 04)
04  Three domains    #disciplines
05  Who this is for  #who
06  How to start     #contact
```

The section's own copy already opens *"Three strokes stand for the three
disciplines I love, practice and coach"* — an invitation to choose, which is
exactly what the reader needs there. The `vit` + `nýr` etymology is the second
beat.

`test_section_numbering_is_sequential` (`tests/test_content.py:203`) reads the
`.num` spans in DOM order and asserts `01`–`06`. It does **not** break if the
relabelling is right — it is the thing that proves it was. Do not edit it.

### D0.2 — a click opens the reading in place — **answered**

No scroll, no jump. Which answers Order C's C0.1 as **buttons, not anchors**:
the three hits are a *selector*, so `<button aria-pressed>` is already the
correct semantic and the four tests C0.1 listed as casualties are safe. What
changes is what `aria-pressed` *means* — see D2.

### D0.3 — §03 and the facts row stay for now — **answered**, and see D0.7

### D0.4 — chess and climbing are bookable today — **answered**

The panels may state them as real offers. This settles the *offer*, not the
*material*: there is still no repo-recorded fact about a chess or climbing
**student**. See D0.6.

### D0.5 — the ink switch re-anchors to `#disciplines` — **decided**

`measureOrigin()` (`main.js:72`) reads `#origin`'s offset; `trackProgress()`
flips `.past-origin` there, crossfading the masthead gauge from specimen-amber
to target-green. It points at `#origin` only because `#origin` happened to sit
4-of-6 down. Move `#origin` to position 1 and the flip fires immediately,
destroying the signal.

**Re-anchor to `#disciplines`.** It inherits the exact positional role
`#origin` is vacating (4-of-6, so the timing barely moves) and it is the
better meaning: the gauge should turn from *error* to *outcome* precisely
where the page stops examining errors (§03 Specimens) and starts showing
results in three fields.

Implementation: rename `measureOrigin()` → `measureInkSwitch()`, hoist the id
to a named constant with a comment saying why that element, update
`test_progress_rule_switches_ink_at_origin` (`tests/test_motion.py:329`,
parametrised per scheme), and **state in BUILD-NOTES that an existing test was
edited and why** (Standing Order 4). Reversible in one line if Igor disagrees
once he sees it.

### D0.6 — the placeholder policy

Igor's *"put some placeholder generic information there for now, I will edit
it later"* is an explicit one-time relaxation of Standing Order 8, for **this
order's reading copy only**, with conditions that are not optional:

1. **Real numbers stay real.** Only the four confirmed readings appear as
   figures: 8 years / 100+ clients (English); **2100** (chess, **never** with
   "FIDE"); **7c redpoint indoor** and **7C Kilter** as two separate readings,
   case preserved (climbing).
2. **Every invented line carries a `<!-- PLACEHOLDER -->` comment** naming
   what Igor replaces. `CLAUDE.md`'s "search for `PLACEHOLDER`" convention is
   how these are found later; a placeholder that does not answer that search
   is a fabrication with a good excuse.
3. **No invented figure enters metadata.** `<title>`, meta description, `og:`
   copy and the JSON-LD `Person` block stay exactly as they are.
   `test_person_json_ld_carries_only_confirmed_facts` must keep passing
   unmodified.
4. **"Years coaching chess/climbing" is invented** until Igor says otherwise.
   8 and 100+ are English figures; 2100 and 7c/7C are Igor's own results, not
   coaching results. Those slots ship flagged.
5. **BUILD-NOTES lists every placeholder shipped**, so the set is countable.
6. **RU is machine-drafted and flagged** (Standing Order 9 normally puts RU
   with Igor). Igor corrects; nothing waits on it.

### D0.7 — how the top block and §03 avoid being duplicates — **design rule**

Igor chose "keep both, decide at the end" (D6). That interim state is only
survivable if the two blocks do **different jobs**, and this rule is what makes
it work — it binds from D3 onward:

| | register | content |
|---|---|---|
| **§01 readout** (new) | **data** — terse, tabular, mono figures, hairline rows | what is measured: years, results, named mistakes |
| **§03 Three domains** | **prose** — argument, full sentences | *why* chess and climbing are real disciplines, and what the method is |

Written that way they are not duplicates, they are an instrument and its
commentary. Written any other way — prose at the top, prose again at §03 —
the page repeats itself for 3,000px and D6 becomes damage control.

**The one genuine duplicate is `.facts`**, whose four readings are exactly
what the readout's first row carries. That is what D6 is really about.

---

## Stage D1 — move the section, renumber, re-anchor the gauge

**Branch:** `feature/mark-to-top`. **Blocked on nothing.**

Pure relocation. **No new behaviour, no new copy, no readout.** The riskiest
structural move in the order, proven on its own against the existing suite.

1. Move the `#origin` `<section>` — **with its preceding comment block**,
   which carries the mark's provenance and must not be orphaned — to sit
   between `</section>` of `.hero` and `<section id="method">`.
2. Relabel the `.num` spans: origin `04`→`01`, method `01`→`02`, specimen
   `02`→`03`, disciplines `03`→`04`. `#who` and `#contact` keep `05` / `06`.
3. Re-anchor the gauge per D0.5.
4. `.breath` does not move. It stays between `#specimen` and `#disciplines`;
   only the numbers either side change. `test_breath_block_takes_no_section_number`
   and `test_breath_block_is_not_viewport_height` stay green untouched.
5. **Re-point the hero's scroll cue.** `<a class="scrollcue" href="#method">`
   reads "The method" / «Метод» and now points *past* the new §01 — the first
   thing the page offers to do would be skip its own new opening. Re-point to
   `#origin`, relabel both languages.

### The one real aesthetic risk in this whole order — verify it here

Moving the mark to the top puts the **large mark, two-thirds dimmed at rest,
directly under the masthead lockup rendered at full ink**, with the sticky
masthead on screen at the same time.

**That is J7's original complaint, exactly** — J7 (2026-09-12) exists because
a two-thirds-dimmed §04 mark read as *"a bug or a loading state"* while the
same mark sat at full ink in the header above it. At 4-of-6 page depth there
was a viewport of distance between them. At position 1 there is not.

Three things make it survivable, in order of how much they carry:

- **(a) The readout is the fix.** With all three disciplines listed beside the
  mark and one visibly selected, two dim strokes obviously mean *"not
  currently selected"* rather than *"failed to load"*. This is the real reason
  D2's readout promotion is not decoration — it is what licenses the move.
  **This is why D1 ships behind D2 in the verification order below.**
- **(b) Scale and company separate them.** The masthead mark is a *wordmark
  lockup* with VITNYR set beside it; the §01 mark is a large standalone dial
  with a readout attached. Different objects, not two strengths of one.
- **(c) Do not touch either.** J7's dim floor is not re-tuned. C0.3's
  absolute rule holds: **never light or dim
  `.lockmark__part--left/--right/--stem`** — that is the header logo, and it
  would also collide with `initLockmark()`'s one-time draw-in (`main.js:860`,
  `style.css:288–292`) whose clip rects sit at `forwards`.

**Verification is not optional and not a screenshot.** Real frames, both
themes, 375 and 1280, at scroll position 0 and mid-block. Answer one question
in BUILD-NOTES in plain words: *does the dim rest state read as a choice, or
as broken?*

**Pre-agreed escape hatch:** if it reads as broken even with the readout, the
block moves to **third** — after §01 The method — instead of second. That is a
one-line change and Igor should be told it exists rather than discovering it
as a surprise. It costs the "second thing you see" brief and buys a viewport
of separation.

### What must not change, in this or any stage

- **C6 — the rest state is English lit.** `clearPaint()` (`main.js:625`)
  re-asserts `paint('english')` rather than stripping classes.
  `test_origin_mark_rests_on_english_before_any_interaction`
  (`tests/test_motion.py:133`) asserts it at load, before any scroll — and the
  section is now *at* the top, so this test gets stricter by accident, not
  looser.
- **J7 — the raised dim floor.** `--amber-dim` / `--green-dim` stay as tuned.
  `test_origin_mark_dim_strokes_use_the_raised_floor` is parametrised per
  theme.
- **The transform channel.** `.origin__mark` is both a `.reveal` target and
  `data-magnetic`; `initMagnetic()` hands the channel back from the reveal on
  first hover via `transitionProperty = 'opacity'`. Guarded by
  `test_magnetic_pull_reaches_the_origin_mark` (`tests/test_motion.py:510`)
  and `test_origin_mark_holds_still_for_the_hover_states` (`:769`).
- **Never redraw the mark.** `#glyphV` lives once in `<defs>`, referenced
  twice via `<use>`, each half clipped at `x=50` — the verified symmetry axis.
  No coordinate is touched by this order, in any stage.

### New test

The mark's section is the first `.sec` in the document and carries `01`. Cheap,
and it is the thing a later stage could silently undo.

---

## Stage D2 — wire the dial to the readout

**Branch:** `feature/mark-commits`. **Blocked on D1.**

This is the stage that makes the feature legible, and **most of it is
deleting code.**

### What already exists (read this before writing anything)

`style.css:1126–1140`. The no-JS state of `.origin__panel` is already the
target design:

```css
.origin__panel-item { display:flex; justify-content:space-between;
                      padding-block:10px; border-top:1px solid var(--rule); }
/* name uppercase sans left · reading mono right */
```

Three hairline-ruled rows, name left, reading right. Then, **only under
`html.js`**, they are stacked absolutely and all but one faded out:

```css
html.js .origin__panel      { position:relative; min-height:3em; }
html.js .origin__panel-item { position:absolute; inset:0; opacity:0; }
html.js .origin__panel-item.is-active { opacity:1; }
```

**The JS layer is hiding the better design.** Remove the overlay: the three
rows return to normal flow, permanently visible, and `.is-active` changes
meaning from *"this is the only one you can see"* to *"this is the one you
have chosen."*

`.origin__body` is likewise already `flex-direction: row` at ≥900px — mark
left, readout right. The layout this order wants is the layout that is there.

### The two feedback levels

Igor's brief separates two gestures — *"when u hover over it"* and *"when u
not hover but click (make it clear)"*. Today `setActive()` (`main.js:629`)
fires on **both** hover and focus and writes `aria-pressed` either way, so a
hover already announces a selection. Once a click has a consequence, that is
wrong.

| gesture | effect | signal |
|---|---|---|
| hover (fine pointer) | **preview** | ink only: stroke lights, row name lights |
| focus (keyboard Tab) | **preview** | ink only, plus the existing focus ring |
| click / Enter / Space / tap | **commit** | **the marker rule slides** + readout swaps + `aria-pressed` moves |
| pointer leaves without clicking | reverts to the **committed** discipline, not to English | |

**Preview is ink. Commit moves a rule.** That is the whole affordance system,
it uses nothing new, and it is self-teaching: the first hover shows you
something responds, and the difference between the two states tells you a
click does more.

The marker: a 1px rule in `--ink-target` against the inline-start edge of the
committed row, animated between rows on the one existing curve (`--e`) and the
one existing duration token. It is a new element with its own transform
channel — it does **not** touch `.origin__mark`'s.

`aria-pressed` now means *committed*, and only a commit writes it. Both
`test_origin_mark_keyboard_focus_reveals_its_panel` (`tests/test_motion.py:99`)
and `test_origin_mark_hover_switches_between_disciplines` (`:115`) encode the
old "hover == selection" model and need rewriting to the new one, **with the
reason stated in BUILD-NOTES** (Standing Order 4).

`engaged` must go permanently true on click exactly as it does on hover and
focus — checked *inside* every idle-hint timeline step rather than trusting
`.kill()`, because a step already queued on GSAP's ticker can still fire after
a kill and repaint a stale discipline over the one the reader just chose.

### The rows are clickable too

Wire the three readout rows to the same handler as the three strokes. Anyone
who does not realise the glyph is interactive gets a plainly clickable line
instead, and touch users get a target far larger than a stroke of a logo.

Bidirectional: hovering a row lights its stroke; hovering a stroke lights its
row. That link is what replaces any need to position the names under the
strokes they belong to — the lighting carries the mapping, so the settled
**English → chess → climbing** order is preserved in the list.

Focus order follows DOM order follows visual order. Do not let them diverge.

### Phone

At <900px `.origin__body` is a centred column and `.origin__mark` is
`clamp(180px, 22vw, 280px)` — 180px on a phone, with the readout under it.
Measured target: **mark + all three readout rows + the first reading visible
at 375×667 without the block running off screen.**

If it does not fit, the fix is a compact two-column band below 900px — mark
reduced to ~130px on the left, readout beside it — not a smaller type scale.
Check the hit targets survive: at 130px the stem hit (`left:20%; right:20%;
top:55%`) is ~78×59px and the arms ~65×72px, all above the 44px minimum, but
measure rather than trust the arithmetic.

### What must not change

C5 (colour is the mark's only feedback channel — the stem's scale flourish was
dropped, not extended), C6, J7, and all four `.origin__*` a11y guarantees:
all three disciplines readable with JS absent (`tests/test_a11y.py:140`),
interactive under reduced motion (`:152`), complete under reduced motion
(`:164`), visible focus ring on the figure (`:201`).

Note that the first of those gets *easier* to satisfy, not harder: removing the
JS overlay means the no-JS state and the JS state finally agree.

---

## Stage D2.5 — sequence the opening

**Branch:** `feature/mark-opening-sequence`. **Blocked on D2.** Small, and
separable — drop it without loss if it does not earn itself.

At 4-of-6 page depth, the mark's draw-in and idle hint fired long after the
hero was finished. At position 1 they fire **on top of it**. Four timed systems
in the first viewport was already the concern that parked the hero revisit
(Order B, "Out of scope").

Make it a sequence instead of a race: **hero lands → mark draws its three
strokes → mark walks the three readings once → settles on English.** That is
Moment 1, and it is three existing behaviours in a row rather than anything
new.

Implementation constraints, all of them hard:

- **Do not reach into `playHero()`.** It is the most fragile code in the repo
  — it shipped a `NaN` transform-cache bug that silently killed every later
  tween. Have it *emit* a completion signal (a `vitnyr:heroin` event on
  `document`, or resolve a promise) and have `initOrigin()` wait on **that or a
  timeout, whichever comes first.** Never couple the two timelines.
- Keep `DRAW_HOLD = 1.0s` between the draw-in and the hint so the two never
  drive the same strokes in one frame.
- Additive only. No JS, GSAP failed, or reduced motion: everything renders
  immediately, English lit, readout complete. The `failsafe()` sweep must still
  find nothing stuck.
- `test_origin_mark_draws_its_three_strokes_once` (`tests/test_motion.py:724`)
  guards the once-ness.

Judge it on real frames, not description. If the sequence reads as *slow*
rather than *composed*, cut it and let them fire independently — a race the
reader does not notice is better than a wait they do.

---

## Stage D3 — the reading, built once, on English

**Branch:** `feature/reading-english`. **Blocked on D2.**

Build the readout's body and prove it with the one discipline that already has
all its material. **Nothing about chess or climbing is written here.**

### The structure — labels persist, only values change

This is the single most important decision in the stage. The readout is **not
three panels that swap**. It is **one spec sheet whose values change**:

```
.reading
  .reading__row                       ← one per slot, hairline-ruled
    .reading__label                   ← persistent. Never changes. Never animates.
    .reading__values
      .reading__value[data-discipline="english"]
      .reading__value[data-discipline="chess"]
      .reading__value[data-discipline="climbing"]
```

Four rows, fixed order, every discipline:

```
1  Measured          the confirmed reading(s)      English: 8 years · 100+
2  Coaching since    years coaching this one
3  Achieved          what has actually been done in it
4  Common mistakes   two or three, each with a name
```

Slot 5 — the one-line offer and the way to start — sits below the sheet, not
as a row. See D4.

Why this and not three stacked panels:

- **The hairlines never move.** Only ink inside the rows changes. Switching
  discipline reads as *the same instrument reading a different subject*, which
  is the entire concept.
- **No height jump, and no dead space.** Three whole stacked panels make the
  container as tall as the tallest and leave visible slack under the short
  ones. Per-row, the slack is one line at worst.
- **The no-JS fallback becomes better than the JS state, not worse.** With
  every value visible, each row reads as a three-way comparison —
  *"Coaching since: English 8 · Chess … · Climbing …"*. That satisfies
  `test_origin_mark_shows_all_disciplines_statically_without_js` naturally
  rather than by special pleading.

### The switch

CSS owns it, JS only picks the side — same division of labour as `.past-origin`.
Inactive values are `opacity: 0` and `visibility: hidden` (**not**
`display:none` or the `hidden` attribute, which reintroduce the height jump),
plus `aria-hidden="true"` and `inert` so they leave the reading and tab orders.

Stagger the rows top to bottom with `transition-delay: calc(var(--i) * .06s)`
set from an `--i` index on each row. One curve (`--e`), one duration token, no
JS animation, and it dies correctly under the global
`transition-duration: .01ms` override at `style.css:1823`.

The row **labels** carry no transition at all. That is what sells it.

### Constraints that will bite

- **C12, the hairline-width rule.** `style.css:694` bleeds `.mechanisms,
  .specs, .domains, .rows, .channels, .proof` out to the section's own edge
  and re-adds the inset as padding, so **every horizontal rule on the page is
  exactly one width**. `.reading` joins that selector list. A block drawing its
  own `--gut`-narrower rule is the exact defect C12 removed.
- **Layout never rides the transform channel** (Standing Order 6). Grid, margin,
  `inset`. Never `translate`. The marker rule in D2 is an animation on its own
  element, which is the permitted case.
- **Glyphs come from the existing set.** Book / checkerboard / carabiner are
  drawn in the masthead nav (`index.html:155–190`) and on the collage group
  labels, via the `.label--glyph` / `.label__mark` idiom (`index.html:782`).
  No second label pattern, no fourth glyph.
- **One type system.** Under the weighted positioning (B0.1, 2026-09-13)
  English is visibly the largest offer — through content depth, never a bigger
  type scale or a different layout for its values.
- **Any new stat element needs the uppercase exemption.** `.domain__meta`'s
  `text-transform: uppercase` destroyed the meaningful `7c` / `7C` distinction
  once; J2 fixed it by exempting `.domain__stat`, with a test reading
  **rendered** text (`inner_text()`, not `text_content()`). `.reading__value`
  needs the same exemption and the same rendered-text assertion. **This is the
  single easiest regression in the order.**
- **Register: data, not prose** (D0.7). Mono figures, short noun phrases,
  named mistakes. If a value runs to a sentence, it belongs in §03.

English fills the four rows from material the page already owns — §03's
English card, the hero stand-first, the facts row — **adapted, not invented.**

---

## Stage D4 — chess and climbing

**Branch:** `feature/reading-rest`. **Blocked on D3 and D0.6.**

Same four rows, checkerboard and carabiner glyphs, `data-discipline="chess"`
and `"climbing"`. They ship together: symmetric, both placeholder-driven,
splitting them buys nothing.

- Chess row 1 carries **`2100`, without "FIDE"**.
- Climbing row 1 carries **`7c` redpoint indoor and `7C` Kilter as two
  separate readings** — different grades, never merged into one generic "7c",
  case preserved, rendered-text assertion per D3.
- Rows 2, 3 and 4 are flagged placeholders in both, per D0.6.
- The closing offer line may be real in both, per D0.4 — and must feed the
  **existing** CTA machinery, not a second one. `initWhoRows()`
  (`main.js:1186`) composes a first-person clause onto the Telegram deep link
  from `data-prefill-en` / `data-prefill-ru`; `updateCta()` rebuilds the `href`
  from `data-href-en` / `-ru`. A curly apostrophe inside a percent-encoded
  `data-href-*` breaks Telegram — J1's carve-out, guarded by
  `test_contact_cta_prefill_text_is_localized`.
- **One loudest thing.** J3/J5 gave the travelling arrow to `.contact__cta`
  alone so the page has a single conversion control. The per-discipline line
  sits **below** it in the hierarchy: no new colour, no button chrome, no
  rounded corners.

**Flag for Igor at this stage, not later:** §06's lede still reads *"Tell me
what you need **English** for and where it breaks now."* The moment chess and
climbing are bookable offers with readings of their own, that line is wrong.
It is a copy edit (Order B's B4.2); the RU is Igor's.

---

## Stage D5 — deep links, keyboard, and the no-JS floor

**Branch:** `feature/navigator-routing`. **Blocked on D4.**

The instrument is only an index if a discipline can be linked to.

- `#english`, `#chess`, `#climbing` select that discipline on cold load and
  move focus into the readout. These are the ids Order B reserved for its
  dossier sections, so nothing is renamed if B's fuller version ever lands.
- **Use `history.replaceState`, not `pushState`** — and this is a deliberate
  correction to the pattern `TRIFECTA-C-MARK-NAV.md` C1 recommends. C1 was
  describing a *jump*, where Back should undo the travel. This is a *selector*:
  if every click pushed an entry, a reader who tried all three would need three
  Backs to leave the page. That is the classic tab-history bug. `replaceState`
  keeps the URL shareable at all times and leaves Back meaning "leave the
  page".
- Either way, **never assign `location.hash` directly** — that fires
  `hashchange`, which wakes the collage router's `routeAfterHashChange()`
  (`main.js:1058`) and triggers an unrelated View Transition on every click.
  `initSpecimenPermalinks()` (`main.js:879`) is the pattern to copy.
- `tabindex="-1"` on the readout if absent, then `focus({ preventScroll: true })`
  — the reader lands *inside* it, not merely near it. Scroll alone is not
  navigation; see the skip-link bug in BUILD-NOTES.
- Wire it **before** the reduced-motion return in `main.js`: this is
  navigation, not motion. The only concession to reduced motion is that the
  switch is instant.
- No second history listener, no second in-page routing idiom.

### Tests

A click writes the right hash; a cold load of `#chess` selects chess, not
English; focus lands inside the readout; **Back leaves the page rather than
cycling disciplines**; reduced motion still switches. Regression-prove per
Standing Order 5 — and note the **worktree caveat**: the stash stack is shared,
so no bare `git stash` / `git stash pop`. Use a temporary WIP commit, or
`git stash push -u -m "<unique-tag>"` and restore with `git stash apply <sha>`.

---

## Stage D6 — resolve the duplication with §03

**Branch:** `feature/domains-after-navigator`. **Blocked on D5 and Igor.**

Per D0.3 this is decided on the live page with both blocks visible. D0.7's
register rule should already have kept §03's prose and the readout's data from
colliding — so the question narrowing to `.facts` is the expected outcome, not
a surprise.

- **(a) — recommended.** Distribute each reading into its discipline's row 1
  and retire `.facts`, **moving `countUp()` and its four tests with it, never
  deleting them.** A reading beside the discipline it measures is worth more
  than a row of four unrelated instruments — and row 1 of the readout is
  already exactly that place.
- **(b)** Keep `.facts` as a summary, retire only the three prose cards.
- **(c)** Keep both, if §03's prose ends up saying something the readout does
  not.

`countUp()` (`main.js:532`) uses **per-number durations, not one shared
sweep** — Igor reversed a simplification here once already. Do not re-simplify
while relocating.

`.proof` — "See the work" — is the collage door and carries a shared-element
View Transition (`openWithDoorMorph`, `main.js:1083`). The transition is
**close-only by design**: `startViewTransition` defers its callback, so the
open path must not be wrapped. Do not re-engineer it while relocating it.
Three per-discipline doors are a genuine improvement and are **parked behind
the photo shoot** (J10: 15 of 18 collage frames are still non-Igor stock).

---

## What this does to Orders B and C

- **Order C** — C0.1 answered (buttons: this is a selector, not navigation).
  C0.2 answered (b): §04 moves above, with the ink-switch re-anchor its own
  condition demanded (D0.5). **C1 superseded** by D2–D5, and its `pushState`
  recommendation deliberately corrected to `replaceState` (D5). C0.3 and C2
  (segmenting the masthead gauge into three) remain **open and untouched** —
  and C0.3's absolute rule stands: **never light or dim the header lockup's
  three parts.**
- **Order B** — B0.1 (Weighted) honoured: English leads, is default, is
  largest. **B1–B3 replaced** by D3–D4's lighter readout form. B0.2 answered by
  D0.4 and D0.6. B0.3's numbering superseded by D0.1. B0.4 becomes D6. **B4.2
  (§06's English-only lede) and B5 (metadata) remain open** — B4.2 is flagged
  at D4.
- **Order A** (`TRIFECTA-A-SPECIMENS.md`) untouched and still open. If it ever
  lands, its chess and climbing specimen groups are the natural occupants of
  row 4 ("Common mistakes"), replacing D0.6's placeholders. Worth knowing; not
  a dependency either way.

---

## Do not

- Add a third colour or a per-discipline colour. Two inks, both already
  semantic.
- Add a second easing curve or a second reveal rhythm — extend the `D`
  duration table (`main.js:36`).
- Add a second scroll listener, a second history listener, or a second in-page
  routing idiom.
- Put layout on the transform channel, anywhere, in any stage.
- Touch `.origin__mark`'s transform channel — `initMagnetic()` owns it.
- Light or dim `.lockmark__part--left/--right/--stem`. That is the logo.
- Rename `data-discipline` values or any existing id. `#specimen-reflexive`,
  `#specimen-copula`, `#specimen-register` are public permalinks; `#method`,
  `#origin`, `#who`, `#contact`, `#top`, `#main` all stay working.
- Redraw, regenerate or re-coordinate the mark.
- Reopen C5, C6, J3, J6, J7 or J8 — settled, several by Igor personally.
- **Republish the live artifact** (Standing Order 2; the collage still runs on
  non-Igor stock). Say in each BUILD-NOTES entry that you did not, and why.
- Merge to `main` or push, until Igor lifts the draft-only instruction.

---

## Verify (every stage)

Both themes, both languages, 375 and 1280, `prefers-reduced-motion: reduce`,
no console errors, no horizontal overflow, body-copy contrast not below 4.5:1
on cream (baseline 5.45 cream / 7.71 charcoal).

Keyboard: Tab to each stroke and each readout row; confirm preview and commit
behave differently and agree afterwards; confirm focus lands inside the
readout. Touch: tap each control with `has_touch=True` and compare against
`innerWidth`, not `scrollWidth` — `scrollWidth` cannot see a masthead clip.

Drive a real Chromium (`tests/.venv/bin/python -m pytest tests/ -q`, Playwright
installed) and take real frames — the preview pane repaints on demand and one
screenshot proves nothing for anything scroll- or time-driven. Run the full
suite and report the number.

---

## Stage map

| Stage | Branch | Blocked on | Status |
|---|---|---|---|
| D0 — decisions | none (no code) | — | **all answered 2026-09-15** |
| D1 — move, renumber, re-anchor | `feature/mark-to-top` | — | pending |
| D2 — wire dial to readout | `feature/mark-commits` | D1 | pending |
| D2.5 — sequence the opening | `feature/mark-opening-sequence` | D2 | pending (droppable) |
| D3 — the reading, on English | `feature/reading-english` | D2 | pending |
| D4 — chess + climbing | `feature/reading-rest` | D3, D0.6 | pending |
| D5 — deep links, keyboard, no-JS | `feature/navigator-routing` | D4 | pending |
| D6 — resolve §03 duplication | `feature/domains-after-navigator` | D5, Igor | pending |

**Judge the aesthetic risk (D1) only after D2 has landed** — the readout is
what licenses the move.
