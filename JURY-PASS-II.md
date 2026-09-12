# Jury Pass II — work order

A second Awwwards-jury-style review of the main page, 2026-09-12, run in a
real browser (both themes, 1280 and 375, full scroll-through) rather than by
reading code. The first jury pass was `BUILD-NOTES.md` →
"Awwwards-jury review, Stages 1–6" (2026-09-06, the C/P numbering); the Spark
Order (S0–S9) followed it. This order uses **J-numbers** for findings and
**J0–J6** for stages so nothing collides with either.

**One stage = one chat = one branch**, per `CLAUDE.md`. Read that file and
`BUILD-NOTES.md` first; read this file's Standing Orders section before
touching code; read the stage you are on in full.

This file lives in the repo on purpose. The Spark Order lived only as an
artifact and drifted several stages behind `main` because chats forgot to
republish it (see the memory note `spark-order-artifact-republish`). A repo
file is read automatically from `main` by the next chat and cannot drift.

---

## Baseline as of this order (2026-09-12)

- Branch `main` at `9ebfab8`.
- Full suite: **232 passed, 0 failed** (`tests/.venv/bin/pytest tests -q`,
  ~5 min). There are **no known-failing tests** — the three
  `test_collage_nav_icons.py` failures mentioned in older BUILD-NOTES entries
  are fixed. If your run is not 232-green *before* you start, stop and find
  out why.
- No console errors, no page errors, no horizontal overflow at 375 or 1280,
  either theme.
- Body-copy contrast: **5.45:1** on cream, **7.71:1** on charcoal. Both pass
  AA. Do not let a stage push cream below 4.5.
- The live artifact "Vitnyr Signature" is **on hold** (collage placeholders).
  See Standing Orders.

---

## The findings

Each has an ID, a verdict, and a stage. **Verdict matters more than severity**
— four of these collide with decisions that were already made deliberately,
and three of those were made by Igor personally.

| ID | Finding | Verdict | Stage |
|---|---|---|---|
| J1 | English copy uses 91 straight apostrophes/quotes; Russian copy is set properly | **Build** — landed 2026-09-12, `6c58df6` | J1 |
| J2 | `text-transform: uppercase` destroys the 7c / 7C grade distinction on screen | **Build** — landed 2026-09-12, `6c58df6` | J1 |
| J3 | Facts-row labels are half lowercase, half uppercase | **Decided 2026-09-12: keep as is** — no code | — |
| J4 | §05 rows are clickable with no resting affordance and no instruction | **Build** — landed 2026-09-12 | J2 |
| J5 | The one conversion link doesn't name the offer and looks like the three below it | Hierarchy half **landed** 2026-09-12; copy half **decided: name the offer** — wording pending from Igor | J3 |
| J6 | §02 specimens hide the mistake at rest | **Decided 2026-09-12: keep the reveal, fix the spoiler (b)** | J5 |
| J7 | The origin mark rests two-thirds dimmed | **Decided 2026-09-12: raise the dim floor** | J5 |
| J8 | The three §01 mechanism rows have ragged left edges | **Withdrawn** | — |
| J9 | Phone: headline scales down hard; sticky masthead eats 128px of 780px | **Build** — landed 2026-09-12 | J4 |
| J10 | The photographs are the least-surfaced asset on the page | **Parked** | J6 |

### J1 — straight quotes (Build)

`index.html` carries **91** `'` characters and zero `’`. Visible English copy
uses typewriter apostrophes and straight double quotes throughout — "that's",
"can't", `"my English is bad"` at 110px Lora in §02's breath block,
`"I blundered"` in the chess domain card. The Russian copy, by contrast, is
set correctly: « » guillemets and real em dashes.

The page's own argument is that precision is the product. A type-literate
jury reads mixed-quality punctuation as the author not noticing.

Not a wording change — `'` → `’` and `"…"` → `“…”` changes no approved
string's words. But it *is* a change to approved strings' bytes, so it needs
the care in Standing Orders.

### J2 — the 7c / 7C distinction is destroyed on screen (Build)

`style.css` `.domain__meta { text-transform: uppercase }` renders
`7c redpoint · 7C Kilter` as **`7C REDPOINT · 7C KILTER`**. Both grades
become 7C. `CLAUDE.md` states the two are different climbing grades and "not
to be merged into one generic 7c".

The rule is currently enforced in the DOM and broken on the screen:
`tests/test_content.py:39–44` deliberately lowercases the DOM text before
asserting, with a comment acknowledging the uppercase. So the guard passes
while the reader sees the wrong thing.

Fix is narrow: exempt the stat (or just its grade reading) from the
uppercase, without disturbing the ENGLISH / CHESS / CLIMBING labels beside
it, which are correct as caps. Then add a test that reads **rendered** text,
not source text.

### J3 — facts-row label case (Decided 2026-09-12: keep as is)

Row reads: `years coaching` / `one-on-one clients` (lowercase) then
`CHESS RATING` / `REDPOINT, INDOOR` (uppercase). This is deliberate — Spark
Order S2 move 18 made a tally, a scale and a grade look like three different
instruments on purpose, and that reasoning is sound. But no reader decodes
it; on screen it reads as an oversight.

**Igor's answer at J0: keep the current mixed styling.** The
tally-vs-grade distinction stands. No code change. Struck — do not raise
this a third time.

### J4 — §05's selectable rows are invisible (Build)

Spark Order S5 move 19 made each "Which of these is you?" row selectable; the
selection composes a first-person clause onto the §06 Telegram message. Good
feature. But the **only** visual state is the *selected* one (a 2px
`--ink-target` rule at `left: -14px`). At rest there is nothing at all: no
marker, no hint, no sentence telling the reader the rows do anything.

An affordance nobody can see does not exist. The feature is currently
undiscoverable by anyone who doesn't mouse over a row and notice the cursor
dot change colour.

This is a **gap, not a reversal** — S5 never decided against a resting
affordance, it simply only built the selected state.

Shape (not yet decided, propose it in the stage): a resting marker in the
same `-14px` gutter the selected rule already owns — the hairline vocabulary
the page already speaks, at rest weight, going to full `--ink-target` on
selection. Plus one line under the §05 `h2` saying what picking does. That
line is new copy, so: EN drafted, **RU flagged for Igor**.

### J5 — the CTA doesn't name the offer (Decided 2026-09-12: name it — wording pending)

§06's `.contact__cta` reads "Message me." It is a text link with an underline
and a travelling arrow — and immediately below it sit Telegram, LinkedIn and
Instagram in the same face, at a similar size, with the *same* travelling
arrow. Four things that look alike, one of which is the page's entire
conversion goal.

The actual offer — a free 30-minute call, nothing owed afterwards, and the
reader leaves with at least one named error (Spark Order S0 decisions 6 and
7) — is in grey body copy underneath.

Two separable changes, and Igor should rule on the first:

1. **Copy.** Put the offer in the big type. "Book the free intro call." is
   the obvious candidate but it is his voice, not a chat's — and the RU must
   be his. **Igor's answer at J0: yes, name the offer** — he has not yet
   supplied the exact English or Russian wording. Stage J3 needs both before
   it can implement the copy half; the hierarchy half does not wait on it.
2. **Hierarchy.** Regardless of the wording, separate the CTA from the three
   channel rows so the page has one loudest thing. No new colour, no button
   chrome, no rounded corners — use space, rule weight, or dropping the three
   channels to a quieter tier.

### J6 — §02 hides the mistake (Decided 2026-09-12: keep the reveal, fix the spoiler)

**Read this before proposing it.** The hide-until-hover behaviour is
**Igor's own explicit request**, 2026-09-07, in his words: *"make it that the
mistake only shows when we hover over it, but make it obvious it should be
hovered."* It retired the S6 performed correction to get there.

The jury observation still stands and is worth him hearing once: §02's
headline promises "Nobody ever shows you the list", and the rest state is
three identical grey "Show the common mistake" buttons. Worse, the
explanation column beside each one already spoils the error before you click
— specimen 1's paragraph says "the **myself** comes along for the ride… **feel
myself** now means something else entirely". So the reveal is hiding
something the page has already told you.

**That spoiler is the part worth fixing even if the reveal stays** — and
fixing it needs no reversal at all. Offer that as the cheap option.

Four tests encode the current behaviour and would have to be inverted or
deleted if it were reversed:
`test_specimen_reveal_is_an_accessible_disclosure`,
`test_specimen_reveal_works_under_reduced_motion`,
`test_specimen_mistake_is_hidden_until_hover_or_tap`, and the no-JS case
above them (`tests/test_a11y.py:296–375`).

**Igor's answer at J0: option (b)** — keep the reveal, rewrite the three
`.spec__why` explanation paragraphs so they describe the shape of each
error without quoting the wrong sentence verbatim. Those four tests are
untouched: the reveal behaviour they guard doesn't change, only the prose
beside it. Lands in Stage J5.

### J7 — the mark rests dimmed (Decided 2026-09-12: raise the dim floor)

§04's mark rests with the English arm lit and the other two at
`--amber-dim`/`--green-dim`. The jury reading: the brand mark appears at a
third strength on the one section devoted to explaining it, while the same
mark renders at full ink in the header 400px above — two strengths of one
logo on one page reads as a bug or a loading state.

But this is **C6**, a deliberate fix from the first jury pass: the rest state
used to be neutral (all three equal, panel blank) and was changed *because*
neutral was an accident rather than a choice — "English is the offer; chess
and climbing are proof it transfers, not equal-weight alternatives." A test
asserts the state at load, before any scroll, so it cannot pass by
coincidence.

Middle option worth putting to Igor instead of a straight reversal: keep
English as the resting emphasis but **raise the dim floor**, so the other two
strokes read as present-but-quiet rather than washed out. That keeps C6's
argument and removes the "faded logo" reading. It is a token change
(`--amber-dim` / `--green-dim`), not a behaviour change, and C5's "solid
token, never opacity" rule still holds.

**Igor's answer at J0: this middle option** — raise the dim floor, keep
English as the lit stroke. C6 stands; no return to a neutral rest state.
Lands in Stage J5.

### J8 — mechanism rows (Withdrawn)

I flagged the three §01 rows starting their paragraph at three different left
edges (403px / 507px / a third). That is **P14**, a deliberate first-jury-pass
fix — `grid-template-columns: 80px fit-content(260px) 1fr` sizes each row's
middle track to its *own* heading, because the previous shared track gave
"Load management" the same ~470px as the longest heading on the page and left
it sitting in a pool of empty space. A test asserts the three rows get three
*different* widths.

My finding would re-introduce the exact defect P14 removed. **Withdrawn. Do
not build it, and do not raise it again** — this entry exists so a future
chat doesn't rediscover the ragged edges and "fix" them.

### J9 — the phone (Build)

Measured at 375×780:

- Hero headline: **42px** on phone vs **110px** at 1280. A steeper drop than
  the width difference justifies; the phone hero reads as a modest blog
  header where the desktop one reads as a statement.
- `.masthead` is **127.6px tall** and sticky, because the lockup and the
  tools row stack into two rows below the breakpoint. That is **16% of the
  viewport permanently occupied**, and the second row is a theme switch, a
  language switch and three collage icons — none of which is why anyone came.
- The `Photos` caption disappears on phone, so the three collage icons are
  unlabelled there — which is the exact problem P10 (2026-09-06) fixed on
  desktop, still live on mobile.

Juries score mobile equally. Constraints: the masthead is `overflow`-clipped
and `flex-wrap: nowrap` below the breakpoint **by design** (see the
2026-09-10 "phone masthead was clipping its own nav" entry) — that fix must
not be undone. Coarse-pointer touch padding adds ~36px to the true row width
and is invisible to a mouse-based measurement; verify with `has_touch=True`
against `innerWidth`, never `scrollWidth`.

### J10 — the photographs (Parked)

The collage is a genuinely strong asset — chess, climbing, teaching, as
evidence the method transfers. It is reachable only via three small icons in
the masthead corner and one link two-thirds down the page. Nothing above the
fold suggests photographs exist. The page argues the method transfers
entirely in words, about a person the reader cannot see.

**Parked, not rejected.** 15 of 18 collage frames are still non-Igor stock
placeholders and the artifact is on hold because of it. Surfacing the photos
harder while they are stand-ins makes the placeholder problem worse, not
better. This stage starts when the real shoot lands, in the same pass as the
deferred `<picture>`/WebP work.

---

## Standing orders — every stage, no exceptions

1. **Branch off an up-to-date `main`**: `git checkout -b <name>`. Never commit
   to `main` directly. Commit on the branch, merge to `main`, push, so the
   next chat starts from a `main` that has your stage in it.
2. **Do not republish the live artifact.** "Vitnyr Signature" is held at its
   pre-placeholder version until real photographs of Igor replace the 15
   remaining stand-ins. This overrides `CLAUDE.md`'s normal
   republish-after-any-visible-change rule. Say in your BUILD-NOTES entry
   that you did not republish and why.
3. **Verify before calling it done**: both themes, both languages, 375 and
   1280, `prefers-reduced-motion: reduce`, no console errors, no horizontal
   overflow. The preview pane repaints on demand — do not trust one
   screenshot for anything scroll- or time-driven. A real Chromium is already
   available at `tests/.venv/bin/python` with Playwright; drive it and take
   real frames.
4. **Run the full suite and report the number.** `tests/.venv/bin/pytest tests
   -q`. Baseline is 232. Never edit an existing test to make your change pass
   without saying so, in the note, with the reason. Prefer adding a test to
   widening one.
5. **Regression-prove new tests**: `git stash` your source changes, confirm the
   new test *fails* against unmodified `main`, pop, confirm it passes. A test
   that has never been seen failing proves nothing.
6. **Layout never rides the transform channel.** Grid, margins, `inset` — not
   `translate`. If a composition can only be built with a transform, say so
   and stop.
7. **No third colour, no gradients, no shadows, no rounded corners.** One
   easing curve (`--e` / the `brand` CustomEase). One reveal rhythm. Extend
   the `D` table in `main.js` rather than inventing a second timing.
8. **Real material only.** No invented clients, results, testimonials or
   numbers. The three confirmed facts are worded exactly as `CLAUDE.md` has
   them — 8 years, 100+ one-on-one clients, a 2100 rating **without** FIDE,
   7c redpoint indoor and a 7C Kilter boulder.
9. **Russian copy is Igor's.** A chat may draft EN and may draft RU as a
   clearly-flagged first pass, in an HTML comment, the way
   `reference/collage-shotlist.md` and the §05 `h2` do. It may not quietly
   ship RU voice as settled.
10. **Everything degrades.** No JS, GSAP failed to load, or reduced motion
    must leave the page fully readable with nothing hidden.
11. **Write the BUILD-NOTES entry in the same commit**, in the house style:
    what changed, why, what you decided *not* to do, what you did not verify
    by eye, the suite number.
12. **Flip your stage's row in this file to landed** — date and merge SHA — in
    the same merge. This file is the tracker; keep it true.

---

## The stages

### J0 — decisions (no code) — landed 2026-09-12

**Purpose:** get four answers from Igor before any chat guesses, so nothing
is re-litigated later. Mirrors Spark Order Stage 0. Output is an edit to this
file plus a BUILD-NOTES entry. **No source files change.**

**All four answered 2026-09-12** (full detail under each finding's own
write-up above):

1. **J6 — specimens:** option **(b)**, keep the hover reveal, fix the
   spoiler paragraphs. Lands in Stage J5.
2. **J5 — CTA copy:** yes, name the offer. **Exact English and Russian
   wording still needed from Igor** before Stage J3's copy half can run;
   the hierarchy half doesn't wait on it.
3. **J7 — mark's rest state:** raise the dim floor; C6 stands. Lands in
   Stage J5.
4. **J3 — facts-row case:** keep the current mixed styling. No code —
   struck, closed.

Put these to him, in this order, with the context each one carries:

1. **J6 — the specimens.** State plainly that hide-until-hover was his own
   request on 7 Sep and that the default is to keep it. Then give him the
   observation (rest state is three identical buttons; the explanation column
   already spoils the error) and offer three options: **(a)** leave it alone;
   **(b)** keep the reveal, fix the spoiler — rewrite the three explanation
   paragraphs so they describe the *shape* of the error without quoting the
   wrong sentence, which is copy-only and cheap; **(c)** reverse it and show
   both lines at rest, which costs four tests and undoes his own call.
   Recommend **(b)**.
2. **J5 — the CTA copy.** Does the big line stay "Message me.", or does it
   name the offer ("Book the free intro call." or his own wording)? If it
   changes, he supplies the RU. The hierarchy half of J5 proceeds either way.
3. **J7 — the mark's rest state.** Offer: leave as-is (C6 stands); or keep
   English lit but raise the dim floor so the other two strokes read quiet
   rather than faded. Recommend the latter. Do **not** offer a return to
   neutral — that is the accident C6 fixed.
4. **J3 — facts-row label case.** Unify all four, or keep the
   tally/scale/grade distinction S2 built? Either answer is fine; record it
   so it is never asked again.

Do not start J1 waiting on these — J1's own two items need no decision. J3
folds into J1 only if the answer arrives first; otherwise it moves to
whichever stage is open when it does.

### J1 — the typographic pass *(start here)*

**Branch:** `feature/typographic-pass`. **Items:** J1, J2, and J3 if answered.

Picked first because it needs no decisions, changes no behaviour, touches no
motion, and is provable by measurement — the same reason Spark Order S1 went
first. It proves the pipeline end to end with almost nothing that can break.

- **J1.** Replace straight punctuation with typographic punctuation in all
  visible **English** copy: `'` → `’`, `"…"` → `“…”`. Prose only.
  - **Do not touch**: `href`s, `data-href-*` URLs (percent-encoded — a curly
    apostrophe there breaks the Telegram deep link), `data-prefill-*` values
    that feed those URLs, JS string literals, CSS, JSON-LD, meta tags,
    `alt`/`aria-label`, code comments, or the mono specimen lines if changing
    them would alter what the specimen demonstrates.
  - Russian copy already uses « » and em dashes — leave it alone. Check
    nothing regressed it.
  - Sweep `main.js` too: `initSpecimenReveal()` sets `'Show the common
    mistake'` and its RU twin from JS, and the permalink status strings live
    in the DOM. Anything the reader sees, wherever it is authored.
  - Add a test that asserts **zero** straight apostrophes in visible EN text
    nodes, so this cannot silently rot back.
- **J2.** Stop `text-transform: uppercase` from flattening `7c` → `7C` in
  `.domain__meta`. Keep ENGLISH / CHESS / CLIMBING in caps. Add a test that
  reads `inner_text()` (rendered), not `text_content()` (source) — the
  existing `test_content.py:39–44` sidesteps the uppercase by lowercasing,
  and that workaround should be replaced, not kept alongside.
- **J3** if answered: apply and record.

**Watch for:** copy strings appear in test docstrings and occasionally in
assertions; run the full suite and read every failure rather than
bulk-updating. Both languages at both widths — a curly apostrophe is wider
than a straight one and §02's breath block is already near its wrap point.

### J2 — make the answer visible

**Branch:** `feature/who-rows-affordance`. **Item:** J4.

Give §05's rows a resting affordance in the `-14px` gutter the selected rule
already owns, and one line of instruction under the `h2`. Reuse the hairline
vocabulary; do not introduce a card, a fill, a hover lift, or a second
interaction idiom. `initWhoRows()` builds the overlay `<button>` at runtime,
so the resting mark must also degrade: a no-JS reader sees four plain rows
and must not see a marker promising an interaction that isn't there.

New EN copy drafted; **RU flagged in an HTML comment for Igor**, per Standing
Order 9. Selecting a row must still not nudge the grid (S5's reason for the
detached `::before`). Verify under reduced motion — this is interaction, not
motion, so it is wired before the reduced-motion return.

### J3 — one loudest thing

**Branch:** `feature/cta-hierarchy`. **Item:** J5.

Copy half only if J0 answered it; hierarchy half proceeds regardless.
Separate `.contact__cta` from the three `.channels` rows so the page has a
single loudest element. Constraints: no new colour, no button chrome, no
rounded corners. Space, rule weight, and type scale are the available tools.
The travelling-arrow device appears three times on the page (`.proof__link`,
`.contact__cta`, `.channels`) — consider whether the CTA keeping it while the
channels lose it does the separation on its own.

Do not break the deep link: the `href` is rebuilt at runtime by
`updateCta()` from `data-href-en`/`-ru` composed with any §05 selection, and
`test_contact_cta_prefill_text_is_localized` plus the S5 composition tests
guard it.

### J4 — the phone

**Branch:** `feature/phone-pass`. **Item:** J9.

Three parts, in this order of confidence: bring the collage icons' caption
back at phone widths (P10's fix, currently desktop-only); reduce the sticky
masthead's permanent height; raise the hero's phone type scale.

**Hard constraint:** the 2026-09-10 masthead fix must survive. `flex-wrap:
nowrap` below the breakpoint and the `overflow` clip are deliberate. Any
height reduction has to come from the row structure or a scroll-collapse, not
from letting the nav wrap or overflow again. Verify at 320, 360, 375 and 390
with `has_touch=True`, comparing against `innerWidth` — `scrollWidth` cannot
see a masthead clip (memory: `coarse-pointer-clipping-check`).

### J5 — the spoiler and the dim floor

**Branch:** `feature/spoiler-and-mark-dim`. **Items:** J6(b), J7.

Resolved by J0 (2026-09-12) — both items are confirmed, so this stage is no
longer contingent. Two independent, unrelated fixes bundled because both are
small copy/token edits with no shared code path:

- **J6(b).** Rewrite the three `.spec__why` paragraphs (reflexive carried
  across, adjective-for-verb, register) so each describes the *shape* of its
  error without quoting the wrong sentence verbatim. The four hover-reveal
  tests (`tests/test_a11y.py:296–375`) are not touched — the reveal
  mechanism doesn't change, only the prose next to it. EN only; RU is
  Igor's per Standing Order 9, so the RU `.spec__why` twins need his pass
  too if the EN rewrite changes their meaning.
- **J7.** Raise `--amber-dim` / `--green-dim` so the mark's two unlit
  strokes read as quiet, not washed out, while English stays the lit
  stroke. Token-only — C5's "solid token, never opacity" rule holds, C6's
  rest-state test still describes the same *state*, just re-tuned values.
  Check contrast doesn't newly clear 4.5:1 in a way that would make the dim
  strokes look intentionally readable as text (they aren't text, but verify
  the visual read stays "quiet accent," not "equal to English").

### J6 — parked behind the photo shoot

**Item:** J10. Blocked. Starts when real photographs of Igor replace the 15
remaining stand-ins, in the same pass as the deferred `<picture>`/WebP and
bilingual `alt` work. Unblocks the artifact republish at the same time.

---

## Stage map

| Stage | Items | Status |
|---|---|---|
| J0 — decisions | J3, J5, J6, J7 | **landed** 2026-09-12, `9cc6ac6` — all four answered, no code |
| J1 — typographic pass | J1, J2, (J3) | **landed** 2026-09-12, `6c58df6` — J3 resolved as "keep as is," no code needed |
| J2 — make the answer visible | J4 | **landed** 2026-09-12, `0ba4f27` |
| J3 — one loudest thing | J5 | hierarchy half **landed** 2026-09-12, `49426cd` — copy half still needs Igor's exact EN/RU CTA wording |
| J4 — the phone | J9 | **landed** 2026-09-12, merge SHA pending |
| J5 — the spoiler and the dim floor | J6(b), J7 | not started — no longer gated, both confirmed at J0 |
| J6 — photographs | J10 | parked |

Withdrawn: **J8**.
