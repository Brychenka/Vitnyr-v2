# Design Pass III — work order

A third review of the main page, 2026-09-20, commissioned as "design, colours,
positioning, animation and message" rather than a full audit. Run in a real
browser (both themes, both languages, 1280 and 375, full scroll-through) with
layout and colour measured in the DOM, not read off screenshots.

Predecessors, and the numbering each one owns, so nothing collides:

| Order | Date | Numbers |
|---|---|---|
| Awwwards jury pass I | 2026-09-06 | `C1–C17`, `P1–P20` |
| Spark Order | 2026-09-07 | `S0–S9`, moves `1–20` |
| Jury Pass II | 2026-09-12 | `J0–J10` |
| Trifecta Orders A–D | 2026-09-13/15 | `A*`, `B0`, `C*`, `D0–D5` |
| **Design Pass III** | **2026-09-20** | **`DP0–DP7`, findings `DP1–DP13`, withdrawals `W1–W6`** |

**One stage = one chat = one branch**, per `CLAUDE.md`. Read `CLAUDE.md`,
`BUILD-NOTES.md` and `JURY-PASS-II.md`'s Standing Orders first — they bind
here too, except where the Standing Order Deltas section below corrects them.
Then read your stage in full.

This file lives in the repo on purpose, for the reason `JURY-PASS-II.md` gives:
an order kept only as an artifact drifts behind `main` because chats forget to
republish it.

---

## Read this first — six findings were withdrawn on review

The review that produced this order was written before its author re-read the
work orders and the git history. Six of its recommendations turned out to
re-open decisions that had already been made deliberately, three of them by
Igor personally. They are listed here, with their evidence, **so that a later
chat does not rediscover them and "fix" them** — the same job `J8` does in
`JURY-PASS-II.md`.

### W1 — "Invert the specimen reveal: show the mistake, hide the correction"

**Withdrawn.** Hide-until-hover is **Igor's own explicit request**, 2026-09-07:
*"make it that the mistake only shows when we hover over it, but make it
obvious it should be hovered."* It was then re-put to him at `J0`
(2026-09-12) with three options, of which **(c) reverse it and show both lines
at rest was offered and rejected** in favour of (b). Four tests encode the
current behaviour (`tests/test_a11y.py:296–375`).

The reviewer's supporting argument — that the explanation column spoils the
error anyway — was **already fixed** by Stage `J5` (`150c3a2`): the three
`.spec__why` paragraphs now describe the shape of each error without quoting
the wrong sentence. Verified against current `main`.

*Do not build it, and do not raise it a third time.* Two unrelated bugs found
inside that same module do survive, as `DP4` and `DP5` below.

### W2 — "Rewrite the three §03 headlines into one voice"

**Withdrawn.** All three were deliberately reworked in a single pass,
each on its own branch and commit:

- `e6af5c3` — "Rework §04 English headline: **name the fix, not just the problem**"
- `37fcd66` — "Rework §05 chess headline: plateau as procrastination, not names"
- `0e683e3` — "Rework §06 climbing headline: plateaus as unlearn-able habits"

The reviewer read three voices as an inconsistency. They are three deliberate
decisions, and the English one — the one the review criticised hardest for
addressing the reader directly — was reworked *specifically* to name the fix
rather than only the problem. That is the chosen framing.

What survives inside the chosen framing, because neither touches it: a
**grammar error** in the English headline (`DP1`, blocker) and a **parse
ambiguity** in the climbing one that a comma resolves (`DP13`).

### W3 — "Bring back a count-up for the readout numbers"

**Withdrawn.** `feature/stop-the-counters` is merged, and the `<ul class="facts">`
strip those counters animated was dropped outright on 2026-09-18 (`8ff0005`,
BUILD-NOTES "§04 facts row dropped") because the same four numbers were being
stated three times on one page. There is no `countUp`, no `data-count` and no
`.facts` in `main.js` or `index.html` today.

**Note for the memory index:** the stored memory `ticking-numbers-reversal`
describes the facts-row count-up as live. It is stale — the element it
describes no longer exists. Correct or delete it.

### W4 — "Put the mark in the hero"

**Withdrawn.** Trifecta Order D `D0.1` decided, from Igor's own brief, that the
mark moves to **§01, directly after the hero** — which landed 2026-09-15 and is
on `main` (`feature/mark-to-top`, merged). `TRIFECTA-D-NAVIGATOR.md`'s Stage D1
contains a written risk analysis of exactly the adjacency a hero mark would
worsen: a large two-thirds-dimmed mark sitting under the full-ink masthead
lockup is `J7`'s original "reads like a bug or a loading state" complaint, and
it survives at position 1 only because the readout beside it explains the dim
strokes. A **third** simultaneous mark instance in the hero removes that
protection and adds nothing the §01 instance doesn't already do one screen
lower.

The underlying observation — the hero's right half is empty at 1280 — is real
and survives as a question in `DP0-Q2`, to be answered by composing the hero
*with* §01, not by duplicating the mark into it.

### W5 — "'Screening' is the wrong word in the CTA"

**Withdrawn as a style note.** The §05 line is **Igor's own wording**, supplied
directly at Stage `J3` (`a21c1b2`; BUILD-NOTES 2026-09-12 "Section 05 rewritten
… and the CTA finally names the offer"). `J5` had already decided *that* the
offer gets named; Igor chose the words.

What survives is not a word choice but a **mismatch**: the English names a
screening *and* a trial lesson, the Russian names only a free lesson. Two
languages currently offer materially different things at the conversion point.
That is `DP0-Q4` — a question about the offer, not about the prose.

### W6 — "The page has no alignment rule"

**Withdrawn as stated.** The review read the centred sections as drift. Each is
a deliberate, separately-branched commit from the last week:

- `699e52d` — "Center §02's heading+lede as one column"
- `63792e0` — "Center §04 'who' heading, drop its clickable-rows lede"
- `f4f1e1c` — "Center the breath-block line and size it down"

Note that `63792e0` also **removed** the instruction line Stage `J2` had added
under the §04 heading. That was a reversal of a jury finding, made
deliberately; do not restore the line.

What survives is narrower and is a question rather than a correction: the five
section heads now split three-left / two-centre, and each decision was taken on
its own. Nobody has looked at the five together. That is `DP0-Q2`.

---

## Standing order deltas

`JURY-PASS-II.md`'s Standing Orders bind here, **with three corrections**. Its
own text is stale on these points; where they disagree, this section wins.

1. **Its Standing Order 2 — "Do not republish the live artifact" — is lifted.**
   Igor lifted the collage hold on 2026-09-17 (`CLAUDE.md`, "2026-09-17: Igor
   lifted the artifact hold"). `CLAUDE.md`'s normal rule applies again: any
   stage that changes something visible republishes "Vitnyr Signature" **to the
   same URL**, rebuilt from the current repo files (see the memory note
   `artifact-rebuild-recipe`).
2. **Its Standing Order 8 says "8 years".** The page, `CLAUDE.md` and
   `feature/ten-years-coaching` all say **10 years**. Ten is correct. The rest
   of that standing order is unchanged and absolute: 100+ one-on-one clients,
   a **2100 rating stated without FIDE**, and **7c redpoint indoor** plus a
   **7C Kilter boulder** as two separate grades.
3. **There is a test suite, and `CLAUDE.md` is wrong to say there isn't.**
   `tests/` holds 10 test files driven by Playwright; the runner is
   `tests/.venv/bin/pytest tests -q`. The last recorded full run was **281
   passed, 1 failed** (2026-09-16), the failure being
   `test_collage_icon_caption_is_back_before_scrolling_on_phone[chromium-ru-320]`,
   confirmed pre-existing on unmodified `main`. **Establish your own baseline
   before you start.** If it is not 281/1 with that same single failure, find
   out why before changing anything.

Everything else in `JURY-PASS-II.md`'s Standing Orders holds verbatim —
particularly 5 (regression-prove new tests), 6 (layout never rides the
transform channel), 7 (no third colour, one easing curve, one reveal rhythm,
extend the `D` table rather than inventing a timing), 9 (**Russian copy is
Igor's**; a chat may draft it only as a flagged HTML comment) and 10
(everything degrades).

---

## The findings

| ID | Finding | Verdict | Stage |
|---|---|---|---|
| DP1 | §03 English headline is missing the object of "teach" | **Build** | DP1 |
| DP13 | §03 climbing headline parses two ways | **Build** | DP1 |
| DP2 | "Here it's a tendon" has no antecedent | **Build** | DP1 |
| DP3 | "one-on-one" (10) vs "one-to-one" (3) | **Build** | DP1 |
| DP4 | Nine reveal buttons say "Show the common mistake", including on the one item that isn't a mistake | **Build** | DP2 |
| DP5 | Opening a reveal collapses the button's accessible name to the bare error string | **Build** | DP2 |
| DP6 | §01's "Common problems" and §03's specimen titles disagree | **Build** | DP3 |
| DP7 | `scroll-margin-top` is 0 on all five sections under a fixed masthead | **Build** | DP4 |
| DP8 | Six chess/climbing specimen permalinks are dead | **Build** | DP4 |
| DP9 | Eight live references to `https://vitnyr.example/` | **Build** | DP5 |
| DP10 | Six stale statements across `CLAUDE.md`, `JURY-PASS-II.md` and code comments | **Build** | DP6 |
| DP11 | `--spark-d` and `SPARK_MS` kept equal by hand | **Build** | DP6 |
| DP12 | Lenis `1.1` and `scrollTo` `1.2` sit outside the `D` duration table | **Build** | DP6 |
| — | Hero headline weighting | **Decision** | DP0-Q1 |
| — | Five section heads, three alignments | **Decision** | DP0-Q2 |
| — | §01's head leads with etymology | **Decision** | DP0-Q3 |
| — | EN and RU offer different things at the CTA | **Decision** | DP0-Q4 |
| — | §02's mechanisms ship collapsed | **Decision** | DP0-Q5 |
| — | The readout's column is ~260px of a 1280px viewport | **Decision** | DP0-Q6 |
| — | `--cursor-active-ink` means opposite things in the two pairs | **Decision** | DP0-Q7 |
| — | Heading typeface | **Decision** | DP0-Q8 |
| — | English collage copy claims authenticity it doesn't have | **Decision** | DP0-Q9 |
| — | Four claims absent from `BUILD-NOTES.md` | **Decision** | DP0-Q10 |
| — | 79 elements share one entrance | **Decision** | DP0-Q11 |
| — | Phone masthead height | **Re-measure first** | DP7 |

---

## DP0 — decisions (no code)

**Purpose:** get eleven answers before any chat guesses. Mirrors `S0` and `J0`.
Output is an edit to this file plus a BUILD-NOTES entry. **No source file
changes.** Put them to Igor in this order; each carries the context it needs.

### Q1 — the hero headline *(the big one)*

`.hero__title` sets **"Skill acquisition, coached."** at `clamp(52px, 8.6vw,
124px)`, full `--fg`, roman. The `<em>` beneath it — **"English, chess,
climbing."** — is `0.78em` of that, italic, and coloured `--fg2`, the
*secondary* ink. In Russian the `<em>` drops further, to `0.58em`.

So the abstract noun phrase carries the most weight on the page and the three
concrete disciplines are set smaller, italic and grey. Meanwhile the deck
beneath carries, at 17px and fourth clause in, the one sentence that explains
why these three belong together: *"Same method under three different
scoreboards."*

**Two constraints bind this question and must be stated when it is asked:**

- `CLAUDE.md` records that the 2026-09-13 **Weighted** positioning decision
  changes **nothing** about the hero "on the strength of this decision alone."
  This question therefore cannot be justified by the Weighted decision. It is a
  separate question about type hierarchy and must be answered on its own terms.
- The trifecta stays in the hero headline. Igor approved keeping all three
  there over a copywriter rewrite that led with English alone. Nothing here
  proposes removing a discipline.

**Options:** (a) leave it; (b) keep both lines, move the disciplines to full
`--fg` and raise the `<em>` scale, changing weight but no words; (c) promote
the scoreboard idea into the headline itself, which is new copy and therefore
needs Igor's English *and* his Russian.

**Recommend (b)** as the low-risk answer — it is a token and type-scale change
with no new strings, so it needs no RU pass and touches no approved copy. (c)
is the larger prize and the larger cost.

### Q2 — the five section heads

Measured at 1280: §01 left h2 with a right lede · §02 **centred** · §03 left h2
with a right lede · §04 **centred** · §05 left. Each centring is a deliberate
commit (see `W6`). The question is only whether the five, seen together, are
the intended pattern — nobody has looked at them as a set.

Related and worth deciding in the same breath: at 1280 the hero is text in the
left ~55% with roughly 500px of empty ground on the right, and §01 now sits
directly beneath it. Those two blocks are the page's opening and they were
composed separately.

**Options:** (a) confirm the current mix as intended and record it so it is
never raised again — the `J3`/`J8` treatment; (b) unify the five heads on the
left-aligned pattern §01/§03/§05 already share, leaving the breath-block coda
as the page's single centred moment; (c) unify on centred.

**Recommend (a) or (b), not (c).** Whichever is chosen, record it here.

### Q3 — what §01 leads with

`TRIFECTA-D-NAVIGATOR.md`'s `D0.1`, from Igor's own brief, reasoned that §01's
job at position 1 is an invitation to choose, and that *"the `vit` + `nýr`
etymology is the second beat."* `feature/origin-note-lead-with-disciplines`
merged and did apply that ordering — **but only inside `.origin__note`**, which
sits at `index.html:511`, below the picker and the readout.

The section *head* still runs the other way: the `h2` is "What Vitnyr stands
for." and the `.sec__lede` beside it is the full Old Norse etymology. So the
first numbered section of the page, and the destination the hero's scroll cue
names, still opens on where the brand name came from.

This is not a new opinion — it is Igor's own D0.1 reasoning, not carried all
the way up to the head. **Options:** (a) leave it; (b) swap the head's emphasis
so the invitation leads and the etymology becomes the second beat, as D0.1
described — new EN copy, RU flagged for Igor.

**Recommend (b).** Also re-point the scroll cue's label if the head changes.

### Q4 — what the CTA actually offers

EN: *"Message me for a free screening and trial lesson."*
RU: *«Пишите сюда для бесплатного занятия.»*

The English promises an assessment plus a lesson; the Russian promises a free
lesson. Both are Igor's own wording (see `W5`); this is not a prose note. The
question is which offer is real, so that one of the two can be corrected.

### Q5 — §02's mechanisms ship collapsed

All three `.mech__panel`s are closed at rest (`2edc076`, 2026-09-18, a
deliberate page-length decision). §03's nine specimens are open. So a reader
who never clicks sees the illustrations of the method in full and none of the
argument for it.

The fold itself is not in question — it solved a real length problem.
**Options:** (a) leave all three closed; (b) ship mechanism 01 open, so the
first panel teaches the interaction and one paragraph of the argument is in
front of the eye; (c) open all three, which reverses the fold.

**Recommend (b).** Note that `initMechanismFold()` is gated behind `html.js`
and the panels are already fully readable with JS absent, so (b) is a starting
attribute, not a mechanism change.

### Q6 — the readout's column

**Correcting the review on one point of fact:** it claimed the readout is
"gated behind an interaction." It is not — English is committed at rest
(`is-active` in the markup, `clearPaint()` re-asserts `paint('english')`, and
`test_origin_mark_rests_on_english_before_any_interaction` asserts it at load).
The English row is readable without touching anything.

What is true is the measurement: at 1280 the picker and readout occupy a column
roughly 260px wide, centred, with about 500px of empty ground on either side,
carrying every proof point the site has at 12–15px.

**The register is not in question.** `D0.7` fixed it deliberately: the readout
is *"data — terse, tabular, mono figures, hairline rows"*, as against §03's
prose, and that distinction is what keeps the two blocks from being duplicates.
Do not propose making it prose, and do not propose restating the numbers
elsewhere — `8ff0005` dropped the facts strip precisely to stop that.

**Options:** (a) leave it; (b) widen and re-position the block so it uses the
space §01 is currently wasting, same type, same register, same rows.

**Recommend (b)**, and note that the 2026-09-16 QA pass already had to fix
`align-items` at phone widths here — re-verify at 375 in both languages, since
Achieved and Common problems wrap to several lines in Russian.

### Q7 — the cursor's ink

`--cursor-active-ink` resolves to `--ink-specimen` (amber) on cream and
`--ink-target` (green) on charcoal. The system defines amber as *the error
under examination* and green as *the target*. The dot represents the reader;
reaching for a control is a target action in both themes.

**This contradicts Igor's own call at `C15`** (2026-09-07), made for a real
reason: green read muddy on the warm cream ground. So this is a genuine
re-opening and is marked as one.

The reviewer's counter-argument, offered once: muddiness is a *value* problem,
and this codebase already solves value problems with tuned variants rather than
hue swaps — `--green-text` exists for exactly that reason, being "the same hue
lightened to exactly 4.5:1." A cream-tuned target green would keep one meaning
across both pairs and would still be an alias to an existing ink, not a third
colour.

**Options:** (a) leave it — C15 stands, and this is struck permanently;
(b) add a cream-tuned target green and point `--cursor-active-ink` at it in
both pairs. **Igor's answer is final either way; record it so it is not asked a
fourth time.**

### Q8 — the heading typeface

Lora is a text face doing display duty at up to 124px. The brand identity pins
Lora for the **wordmark**, and that constraint is absolute for a hard technical
reason: the header/footer SVG sets `<text>` at Lora's own hardcoded advances
and would misalign in any other face. That is why the mark is held behind
`lora-ready`.

That constraint does not extend to `h1`/`h2`. Changing the heading face is
nonetheless brand-identity territory and is therefore a question, not a
finding. It would also be the largest visual change in this order.

**Recommend deferring** unless Igor wants it. If he does, it is its own order,
not a stage in this one. `reference/vitnyr-brand-identity.md` would need
updating in the same pass.

### Q9 — the English collage copy

The English group is six stock stand-ins. `assets/collage/PLACEHOLDERS.md`
protects the captions carefully — each `<figcaption>` describes the *intended*
shot — but the page-level copy around them was never covered by that policy and
makes a flat claim: *"It's me at work — English, chess, and climbing, each one
real,"* reached from a link reading *"See me at work."* Three of the six frames
do not depict English coaching under any reading.

This is the one finding in the review that can cost trust rather than polish,
and it sits directly against `CLAUDE.md`'s first content rule.

**Options:** (a) shoot the English frames, which unblocks `J10` and the deferred
`<picture>`/WebP work in the same pass; (b) until then, change the two page-level
strings so they name what is real and what is a stand-in.

**Recommend (b) now and (a) when the shoot lands.** New EN copy; RU flagged for
Igor.

### Q10 — four claims with no entry in the build log

*"patterns drawn from 5,000+ analyzed"* (§03 chess), *"C2 level · IELTS 9"* and
*"13 climbers reached 7a in a year"* (§01 readout), and *"neuroscience, rehab
principles"* (breath block). Their commit messages suggest they came from Igor,
so they are probably real — but the project's own audit trail cannot confirm
them, and `CLAUDE.md`'s first rule is that every claim is real or a marked
placeholder.

Needed: confirm each in `BUILD-NOTES.md`, or cut it. No chat should decide this.

### Q11 — one entrance, 79 times

Every `.reveal` target uses the same 24px rise and fade, 0.9s, 0.08s stagger.
There are 79 of them.

**Standing Order 7 is not in question**: one easing curve, one reveal *rhythm*,
and any new timing extends the `D` table rather than inventing a second. The
question is whether a second *kind* of entrance — a rule drawing itself
left-to-right for section heads, say — is wanted within those rules.

**Note what is already excluded:** a count-up is not available (see `W3`).

**Recommend (a) leave it** unless Igor wants the page to feel less uniform; the
discipline is currently worth more than the variety would be.

---

## The stages

Each is one chat, one branch, off an up-to-date `main`. `DP1` through `DP6` need
no decisions and can run in any order, or in parallel by different chats, since
they touch disjoint files. `DP7` is whatever `DP0` unlocks.

### DP1 — the copy corrections *(start here)*

**Branch:** `feature/copy-corrections`. **Items:** `DP1`, `DP13`, `DP2`, `DP3`.

Picked first for the same reason `J1` was: no decisions, no behaviour change, no
motion, provable by reading. All four are corrections *inside* copy Igor has
already approved — none changes a framing, and `W2` explains why that boundary
matters.

- **`DP1` (blocker).** §03's English group headline reads *"You have a list of
  errors and they are deeply rooted. I will teach how to unlearn them."*
  **"Teach" needs its object: "teach you how to."** It is set at
  `clamp(26px, 3.6vw, 36px)` Lora directly above nine specimens about errors
  that sound fine to the person making them. Check the Russian twin in the same
  edit; if the RU needs a change it is Igor's, per Standing Order 9.
- **`DP13`.** The climbing headline, *"Most plateaus are just habits that you
  can't see and unlearn,"* parses two ways: *habits you can't see and can't
  unlearn*, or *habits you can't see, and that you should unlearn*. The intended
  reading is the second. A comma after "see" resolves it without touching
  `0e683e3`'s framing. Confirm the intent before editing.
- **`DP2`.** §03's climbing session paragraph runs *"Overtraining everything
  else kills motivation. Here it's a tendon, and you…"* — nothing earlier in the
  paragraph introduces a referent for "it". Reads like an edit that lost its
  first half. Needs a clause restored, so: draft EN, flag RU.
- **`DP3`.** `index.html` carries **"one-on-one" ×10 and "one-to-one" ×3**,
  both in visible body copy, describing the same product — the hero eyebrow says
  one and §03's English session paragraph says the other. `CLAUDE.md`'s three
  confirmed facts are worded *"100+ one-on-one clients"*, so **"one-on-one" is
  the form to keep**. Sweep the three exceptions. Note the branch
  `feature/drop-one-on-one-only` is merged and may have been about a different
  string — check it before assuming intent.

**Watch for:** copy strings appear in test docstrings and assertions. Run the
full suite and read every failure rather than bulk-updating. Both languages at
both widths.

**Also republish** the live artifact afterwards (Standing Order Delta 1) — this
is visible copy.

### DP2 — the two reveal-label bugs

**Branch:** `feature/reveal-labels`. **Items:** `DP4`, `DP5`.

Both are inside `initSpecimenReveal()` (`main.js:1469–1567`). **Neither changes
the reveal behaviour**, so the four tests at `tests/test_a11y.py:296–375` are
untouched — read `W1` before you start, so you don't drift into reversing it.

- **`DP4`.** The button label is hardcoded at `main.js:1518–1520` as
  `'Show the common mistake'` / `'Показать типичную ошибку'` and applied to all
  nine specimens. One of the nine is **"Register, not grammar"**, whose own copy
  says the sentence *"is grammatically fine"* — it is explicitly not a mistake.
  The label contradicts the item. Fix by sourcing the label per specimen (a
  `data-` attribute on the specimen, consistent with how the rest of the page
  carries strings) rather than adding a special case in JS. RU flagged.
- **`DP5`.** `render()` does `label.hidden = open`, so when a reveal opens, the
  button's accessible name collapses to whatever is left inside it — the bare
  error string. A screen-reader user hears *"I feel myself good today, button,
  expanded"*: the error announced as the name of the control. Also,
  `fillReveal()` clones only `.sig` and the last child span, dropping the
  `<span class="vh">Incorrect: </span>` cue that sighted structure implies.
  Give the button a stable `aria-label` (or keep the label in the accessibility
  tree with `.vh` rather than `hidden`) so the name is constant across states.

**New tests:** assert the button's accessible name is stable across
open/closed, and that no two specimens share a label where their content
differs. Regression-prove both against unmodified `main` (Standing Order 5).

### DP3 — make the readout an index, not a second draft

**Branch:** `feature/readout-specimen-congruency`. **Item:** `DP6`.

§01's readout carries a **Common problems** row per discipline. §03 shows three
named specimens per discipline. They describe the same thing six seconds of
scrolling apart and mostly disagree:

| Discipline | Readout says | §03 shows | Overlap |
|---|---|---|---|
| Climbing | over-gripping · avoiding dynamic moves · underestimating flexibility · only training what you're good at | over-gripping · arms doing the legs' work · improvising the sequence | 1 of 3 |
| Chess | calculating only one line · hoping the opponent blunders · playing too closed · giving up too early · tilt streak · lack of versatility | calculating only as far as the shot · trusting memorised theory · damage control after one mistake | 1 of 3 |
| English | carrying structure over from Russian · fear of making a mistake · freezing up · understanding more than you can say · trouble with listening | reflexive carried across · adjective where English has a verb · register, not grammar | partial |

"Trusting memorised theory past its edge" is arguably the most recognisable
chess item on the page and is absent from the readout; "playing too closed" is
promised and never delivered.

**Shape:** make each Common problems row list its discipline's three specimen
titles verbatim, plus a phrase acknowledging there are more — §03's own intros
already say so ("There are many more", "three of many"). This also gives the
specimen permalinks somewhere to be linked *from*, which is why `DP4`'s stage
is worth running before or alongside this one.

**Constraint:** `D0.7` binds. The readout stays **data** — terse, mono, hairline
rows. Listing three titles is still data; writing sentences there is not.

New EN strings are short and derived from existing approved titles; the RU
equivalents likewise come from existing approved RU specimen titles, so this is
the rare copy change that may not need a fresh Igor pass — but say so explicitly
in the BUILD-NOTES entry and let him confirm.

### DP4 — deep links that land where they point

**Branch:** `feature/deep-link-landing`. **Items:** `DP7`, `DP8`. One branch,
because they are the same mechanism failing twice.

- **`DP7`.** `scroll-margin-top` computes to **`0px` on all five sections**
  against a `position: fixed` masthead. Measured: `#specimen-copula` lands at
  specTop −24 with mastheadBottom 110, hiding 134px — the specimen's own title
  *and* its reveal prompt. This affects the masthead's 01–05 quick-nav
  (`79caf82`), the hero scroll cue, every specimen permalink and browser
  back/forward. One rule, set from the same measurement `--head` already
  carries.
- **`DP8`.** All six chess and climbing specimen permalinks are dead. The target
  `.specimens-group` is `display: none` (`style.css:914`), so the element
  measures 0×0; the page lands at scrollY 3983, mid-English-list, with no error
  and no message. The `#` affordance and the "Link copied" toast exist
  specifically so these get shared.
  **Fix:** on load and on `hashchange`, if the hash matches a specimen in a
  non-active group, commit that discipline first — `initOrigin()` already owns
  the single `committed` value that drives `.origin__marker`, `aria-pressed`,
  `updateReading()` and `updateSpecimens()`, so this is a call into existing
  state, not new state. Then scroll. Order matters: commit, then let layout
  settle, then scroll, or you will measure a 0×0 box again.

**Verify** with a cold load of each of the nine permalinks in both languages and
both themes — `feature/collage-cold-deeplink-test` is a precedent for how this
was tested for the collage view. Add a test per discipline group.

### DP5 — the launch blockers

**Branch:** `feature/launch-blockers`. **Items:** `DP9`, plus whatever `DP0-Q9`
and `DP0-Q10` returned. **Blocked on those two answers** for its copy half; the
domain half is unblocked.

- **`DP9`.** `https://vitnyr.example/` appears **eight times**: `canonical`,
  `og:url`, `og:image`, `twitter:image`, three `hreflang` alternates,
  `sitemap.xml` and `robots.txt`. Every link pasted into Telegram, LinkedIn or
  Slack today renders with no image and a dead canonical. The share card itself
  is real and exported at `assets/share/og-share.png` — it simply cannot be
  fetched. This blocks launch, not polish. It is a single find-and-replace once
  the real domain exists; if it does not exist yet, that is the blocker to
  surface.
- **Q9's answer** — the collage copy. Two page-level strings, plus the link
  label reading "See me at work."
- **Q10's answer** — confirm the four claims in `BUILD-NOTES.md`, or cut them.

### DP6 — the record and the seams

**Branch:** `chore/record-and-seams`. **Items:** `DP10`, `DP11`, `DP12`.
Documentation and invariants; no visible change, so no republish.

- **`DP10`.** Six stale statements, each of which could mislead a future chat:
  1. `CLAUDE.md` says "no linter and no test suite." There are 10 test files and
     a Playwright venv. **Highest-value fix in this stage** — a chat that
     believes it has no tests will not run them.
  2. `CLAUDE.md` describes Trifecta Order D as a parked draft on an unmerged
     branch. **All stages merged to `main` on 2026-09-15** (BUILD-NOTES,
     "Trifecta Order D (all stages) merged to main"). `feature/navigator-order`
     is the superseded earlier draft.
  3. `CLAUDE.md` lists the Telegram / LinkedIn / Instagram handles as
     outstanding placeholders. All three are live in `index.html`.
  4. `JURY-PASS-II.md` Standing Order 2 forbids republishing. Lifted 2026-09-17.
  5. `JURY-PASS-II.md` Standing Order 8 says "8 years". The page says 10.
  6. `style.css` annotates the shipped charcoal `--bg: #171310` as
     *"EXPERIMENT (feature/dark-theme-color-exploration, **not merged**)"*. It
     is merged and it is the right call — a warm near-black puts both pairs in
     one warmth family. The risk is a later chat reverting it as leftover.
     Also: an `index.html` comment still reads "50 students to 1800+" where the
     value five lines below reads **30** (`ae40b76` corrected the value, not the
     comment).
- **`DP11`.** `--spark-d: .5s` in CSS and `SPARK_MS = 500` in `main.js:680` are
  kept equal by a comment in both files. It is the only CSS-to-JS coupling in
  the codebase. Do **not** add a read-back mechanism for one value — add a test
  that asserts the two agree, which is cheaper and cannot itself drift.
- **`DP12`.** The comment above `D` in `main.js:27–37` states *"Six durations,
  and nothing between them."* Lenis is constructed with `duration: 1.1`
  (`main.js:53`) and both `scrollTo` calls pass `duration: 1.2`
  (`main.js:116`, `:1114`) — three timings outside the table, none equal to
  `D.hero` (1.05). Either fold them into `D` as named scroll durations or amend
  the comment to say the table governs animation and scroll is separate. The
  rule is only worth having if it is true.

### DP7 — the phone, and whatever DP0 unlocks

**Branch:** per item. **Blocked on `DP0`** except the re-measurement.

**Re-measure the masthead before proposing anything.** This review measured
**187px expanded / 120px collapsed** at 375×812 — against `J9`'s pre-fix
**127.6px**, which Stage `J4` (`01679d3`) then reduced. Those numbers do not
reconcile, so one of them is measured wrong or something regressed after `J4`;
`79caf82` added the section quick-nav as desktop-only and should not have
touched phone. **Establish the real number first**, with `has_touch=True`
against `innerWidth` — `scrollWidth` cannot see a masthead clip (memory:
`coarse-pointer-clipping-check`).

**Hard constraint, carried from `J4`:** the 2026-09-10 masthead fix must
survive. `flex-wrap: nowrap` below the breakpoint and the `overflow` clip are
deliberate. Any height reduction comes from row structure or a scroll-collapse,
never from letting the nav wrap or overflow again.

The related question — that the phone has no section nav at all, on a page
nearly nine screens long — only becomes answerable once the height is known.

---

## Stage map

| Stage | Items | Status |
|---|---|---|
| DP0 — decisions | Q1–Q11 | **open** — nothing below its dependents starts until answered |
| DP1 — copy corrections | DP1, DP13, DP2, DP3 | open, unblocked |
| DP2 — reveal labels | DP4, DP5 | open, unblocked |
| DP3 — readout as index | DP6 | open, unblocked |
| DP4 — deep-link landing | DP7, DP8 | open, unblocked |
| DP5 — launch blockers | DP9, Q9, Q10 | domain half unblocked; copy half blocked on DP0 |
| DP6 — record and seams | DP10, DP11, DP12 | open, unblocked |
| DP7 — the phone + DP0's outcomes | — | blocked on DP0 and on re-measurement |

Withdrawn: **W1–W6**. Do not build them and do not raise them again.

---

## One open question this order did not create

`reference/collage-shotlist.md` on disk is still v2 — *"six frames at a fixed
mix of the three crop ratios: two 4:5, two 3:2, two 1:1"* — and the rendered
page matches it, measured in-browser. But a decision of 2026-09-06 replaced
that with **one crop ratio per domain group** (English 3:2, chess 1:1, climbing
4:5), planned as Stage 1.4 of that work order and never executed. `main` also
ships a **9:16** frame (`climb-02-chalk`) and a `collage__pair` construct that
appear in no spec at all.

Two states disagree and neither can be assumed. **Ask Igor which holds before
anyone touches the collage grid**; the 9:16 outlier needs its own answer either
way. See the memory note `collage-ratio-contract-pending`.
