# Trifecta Order A — three specimens, not one

**Idea 1 of the 2026-09-13 trifecta brainstorm.** Give chess and climbing the
page's single best device: the named error, the wrong line, the corrected
line, the proofreader's mark, the explanation beside it.

One of three independent orders. The other two are
`TRIFECTA-B-DOSSIERS.md` (the three-section spine) and
`TRIFECTA-C-MARK-NAV.md` (the mark as navigator). Read the dependency note
below before starting — **A and B overlap, and the order they run in changes
what A builds.**

**One stage = one chat = one branch**, per `CLAUDE.md`. Before touching code,
read: `CLAUDE.md`, `BUILD-NOTES.md`, `JURY-PASS-II.md` (its Standing Orders
section is binding here too — this file does not restate all of it), and this
file's stage in full.

---

## Why this order exists

Measured on `main` at 1280px, 2026-09-13 (page is 8,649px tall):

| Block | Height | Words |
|---|---|---|
| 02 Specimens | 1,342px | 279 — **English grammar only** |
| 03 Three domains → chess card | 227px | 42 |
| 03 Three domains → climbing card | 227px | 45 |

§02 is the page's most rigorous format and it exists once, for one
discipline. Chess and climbing are asserted in 87 words total and proved by
nothing the reader can inspect. Repeating one diagnostic format across three
unrelated domains **is** the argument that the method is a method — three
differently-shaped sections read as three ideas; three variations on one
template read as a system.

---

## Dependency on Order B — read before Stage A0

A needs somewhere to put six new specimens. Two modes:

- **A-standalone** (Order B has not landed): §02 becomes three labelled
  groups inside the existing section — English, then chess, then climbing,
  the same order the collage view and the masthead icons already use. The
  section keeps number `02`. This is the mode the stages below are written
  for.
- **A-into-B** (Order B has landed first): each discipline's specimen group
  moves into slot 4 of its own dossier. Stage A1 is unchanged and still
  required. Stages A2–A4 build the same markup but mount it inside the
  dossier instead of inside `#specimen`, and Stage A5 is dropped (Order B
  already rewrote the section frame).

**Check which mode you are in before Stage A2:** if `index.html` contains
`class="dossier"`, you are in A-into-B. Say which mode you ran in, in the
BUILD-NOTES entry.

If you have a free choice, **run B first.** A-standalone produces a §02 that
Order B then has to take apart again.

---

## Stage A0 — material and decisions (no code)

**Output:** edits to this file recording Igor's answers, plus a BUILD-NOTES
entry. **No source file changes.** Do not start A2 without these; do not
guess any of them.

Standing Order 8 — real material only — is the whole reason this stage
exists. There is currently **no** repo-recorded fact about chess or climbing
*coaching*. The 8 years and 100+ clients are English figures. 2100 and
7c/7C are Igor's own results, not coaching results. Nothing in A2–A4 may
imply a chess or climbing student exists unless Igor says one does.

### The six specimens — ask for these first

Three chess and three climbing. For each, Igor supplies:

1. **A name for the error** — the `.spec__label`, the thing that makes it
   stop being "I'm bad at this". English's three are "Reflexive carried
   across", "Adjective where English has a verb", "Register, not grammar".
2. **The wrong line** — what actually gets played/done.
3. **The corrected line** — the same situation, done right.
4. **The shape of the error** — 2–4 sentences for `.spec__why`.

### The rule that constrains 4 — do not lose it

`.spec__why` sits **outside** the hover reveal and is always visible. J6(b)
(Jury Pass II, landed 2026-09-12) rewrote all three English paragraphs
because they named the hidden word and spoiled the click. **New specimens
inherit that rule.** A `.spec__why` may describe the shape of an error; it
may not name or reconstruct the thing behind the reveal.
`test_specimen_why_no_longer_names_the_hidden_word` is parametrised over a
`SPOILED_WORDS` dict in `tests/test_content.py:264` — each new specimen adds
its own entry.

### The four decisions

**D1 — whose errors are these?** Errors Igor fixes *in students*, or errors
he diagnosed and fixed *in himself*? This changes the voice of all six
`.spec__why` paragraphs and it is a "real material" question, not a style
one. If he does not coach chess or climbing students yet, the specimens are
his own and must read that way.

**D2 — the glyph system.** English's three `.sig` marks are proofreading
notation (dele loop, caret, transpose hook), drawn as inline SVG in a
`0 0 10 10` box at `stroke-width="1.6"`, round caps and joins. Chess and
climbing need their own marks in **the same box, the same stroke weight,
the same caps** — the repetition is the point.
- Chess: annotation symbols (`?`, `?!`, `!`) are the native notation.
  Recommend drawing them as SVG in the shared box rather than setting them
  as type, so all nine marks stay one system. Igor confirms which symbol
  belongs to which of his three errors.
- Climbing: there is no standard notation. Proposal to put to him: a small
  circle (a hold) plus a stroke (the move into it), wrong vs. corrected. He
  may have a better one — ask; do not invent one and ship it.

**D3 — the hidden-label wording.** `.line-spec` carries a visually hidden
label so a screen reader hears which line is which
(`test_specimen_rows_have_text_equivalent_for_correctness`,
`tests/test_a11y.py:93`). English uses "Incorrect: / Correct:", except the
register specimen, which uses "Reads as: / Better as:" because calling a
grammatical sentence incorrect overstates the claim. Chess and climbing need
their own pairs — a move is not "incorrect" the way a verb is. Candidates to
put to Igor: chess "Played: / Better:", climbing "Attempted: / Corrected:".
Both languages, and the RU is his (Standing Order 9).

**D4 — mono's meaning.** The type pass (BUILD-NOTES, "The five specialist
passes") settled that `var(--mono)` means exactly one thing on this page:
**quoted linguistic material**. Chess notation and a climbing sequence are
quoted domain material but not linguistic. Two honest options:
- extend the rule to "quoted material from the discipline under
  examination", and record the amendment in BUILD-NOTES; or
- set the chess and climbing lines in `var(--sans)` and let mono stay
  English-only.

Recommend the first — the lines are artefacts of their discipline in exactly
the way a quoted sentence is, and splitting the face across three otherwise
identical blocks would break the repetition this order is built on. **But
this is an amendment to a settled pass; it is Igor's to make, not a chat's.**

### The digit trap — flag this to whoever executes A2

`test_no_invented_count_beside_the_finite_list_claim`
(`tests/test_content.py:216`) asserts that **no digit** appears anywhere in
§02's `.sec__head h2`, `.sec__lede [data-l]`, `.spec__label` or `.spec__why`,
in either language. It exists because §02 is the one place on the page built
to tempt a fabricated statistic.

Chess notation contains digits. Notation belongs in `.line-spec`, which the
test does not read, so the rule holds as written — **but a chess
`.spec__label` or `.spec__why` that mentions a rating, a move number or a
grade will fail this test, and the correct response is to change the copy,
never the test.** Say so in the stage note if it comes up.

### Answers

> Record Igor's answers here as they arrive. Until this block is filled in,
> Stages A2–A4 are blocked.

- **D1 —** _pending_
- **D2 —** _pending_
- **D3 —** _pending_
- **D4 —** _pending_
- **Chess specimens (3) —** _pending_
- **Climbing specimens (3) —** _pending_
- **RU for all of the above —** _pending_

---

## Stage A1 — generalise the machinery *(start here — needs no decisions)*

**Branch:** `feature/specimen-machinery`. **No visible change.** Runnable
today, before any of Igor's material arrives, and it de-risks every stage
after it.

Two selectors hard-code `#specimen` and would silently skip any specimen that
lives anywhere else:

1. **`main.js:1262`** — `initSpecimenReveal()` opens with
   `document.querySelectorAll('#specimen .spec')`. Change to
   `document.querySelectorAll('.specs .spec')`. `.specs` is already the
   container class and already carries the bleed rule at `style.css:694`, so
   it is the right anchor.
2. **`main.js:759`** — the pointer dot takes specimen amber from
   `hot.closest('#specimen')`. The dot's two inks are semantic (amber = the
   specimen under examination), so the ink must follow specimens wherever
   they live: `hot.closest('.specs')`.

Also update the prose that documents both, so the comments do not outlive the
code: `main.js:693` (the `initCursor` header block) and `style.css:1740`.

**Test work.** `test_cursor_takes_specimen_ink_over_a_control_inside_specimen`
(`tests/test_motion.py:391`) names `closest('#specimen')` in its docstring and
locates `#specimen .spec__prompt`. Update both, and **say in the BUILD-NOTES
entry that you edited an existing test and why** (Standing Order 4). Keep the
test asserting the same behaviour; you are re-pointing it, not widening it.

**Regression proof.** This stage changes no behaviour, so Standing Order 5's
stash-and-watch-it-fail does not apply and you must say so rather than
pretending it did. The generality test — "the reveal is built for *every*
`.specs .spec` on the page, not only those inside `#specimen`" — cannot fail
against `main` until a second group exists, so it is written in **Stage A2**,
where it can be regression-proved properly.

**Done when:** full suite green at its current baseline (232 on
2026-09-12 — confirm the number before you start; if it is not green, stop
and find out why), no console errors, and the three English specimens behave
exactly as before in both themes and both languages.

---

## Stage A2 — the group frame

**Branch:** `feature/specimen-groups`. **Blocked on A0's D2/D3 only if you
build a second group in this stage — you should not.** This stage ships one
group.

Wrap the existing three specimens in a group with its own label, so the
structure the next two stages fill already exists and already reads correctly
with one real group in it.

```
.specs
  .specs__group            ← new
    p.label.label--glyph   ← existing class, already used in the collage view
      svg.label__mark      ← the book glyph, same as the collage EN group
      span[data-en="English" data-ru="Английский"]
    article.spec × 3       ← unchanged, ids unchanged
```

**`.label--glyph` and `.label__mark` already exist** and are used by the three
collage group headings (`index.html:782`). Reuse them; do not author a second
label idiom. The book / checkerboard / carabiner glyph paths are in the
masthead nav (`index.html:150–200`) and again on the collage groups — copy
the collage instances, which are the smaller, quieter ones.

**Constraints:**
- `.specs` carries the C12 bleed (`style.css:694`): `margin-inline:
  calc(var(--gut) * -1)` plus matching padding, so its top hairline is
  exactly as wide as every other rule on the page. A new `.specs__group`
  **must not** re-introduce a second rule width. If a group needs its own
  divider, it inherits `.specs`'s inset, it does not draw its own narrower
  one.
- Grid and margins only. No `transform` for the group offsets (Standing
  Order 6).
- Specimen `id`s are a **public contract** — `#specimen-reflexive`,
  `#specimen-copula`, `#specimen-register` are shareable permalinks the S9A
  work exists to support. Never rename or renumber them, in this stage or
  any other.

**Tests to add here:**
- the generality test deferred from A1, in its A3-provable form: assert that
  the count of `.spec__prompt` buttons built at runtime equals the count of
  `.specs .spec` in the DOM. It passes trivially now and becomes real in A3.
- `.specs__group` labels appear in the settled order (English, chess,
  climbing) once more than one exists — write it now, parametrised over
  whatever groups are present.

---

## Stage A3 — the chess specimens

**Branch:** `feature/specimens-chess`. **Blocked on A0.** Do not start
without D1–D4 answered and three real chess specimens in hand.

Build a second `.specs__group`, checkerboard glyph, label "Chess / Шахматы",
three `article.spec` elements matching the English markup exactly:

- `id="specimen-chess-<slug>"` — language-neutral, stable, never renumbered.
- `.spec__label` wrapping `.spec__permalink[data-permalink]` with the `#`
  mark, the name, the visually hidden ", link to this specimen" suffix, and
  the `.spec__permalink-status` live region. Copy the English structure
  verbatim; `initSpecimenPermalinks()` (`main.js:879`) picks it up by class
  with no changes.
- `.spec__lines` holding `.line-spec.wrong` and `.line-spec.right`, each with
  its `.vh` label (D3's wording), its `.sig` glyph (D2's), and the sentence
  span **last** — `initSpecimenReveal()` reads
  `wrong.children[wrong.children.length - 1]` as the sentence, so the order
  inside the line is load-bearing.
- `<del class="mark--specimen">` / `<ins class="mark--target">` on the tokens
  that differ. These are real semantics, not colour, and the two inks are the
  page's only two.
- `data-op` — `"delete"` if the correction removes a token, otherwise
  `"restructure"`. It marks which specimens a future performance layer could
  drive; a restructure ships static.
- `.spec__why` × 2 (`data-l="en"` / `data-l="ru"`), obeying the no-spoiler
  rule above.

**Tests:**
- append the three new ids to `SPECIMEN_IDS` (`tests/test_content.py:213`) —
  `test_each_specimen_is_addressable_by_its_own_permalink` asserts the exact
  list and order.
- add three entries to `SPOILED_WORDS` (`tests/test_content.py:264`).
- `test_specimen_why_paragraphs_are_not_empty_in_either_language` picks the
  new ones up from the same dict.
- **Regression-prove the generality test from A2**: `git stash` the
  `main.js:1262` change from A1, confirm the new chess specimens get **no**
  reveal button, pop, confirm they do. This is the moment A1's refactor
  becomes provable — do it, and record it.

**Verify:** both themes, both languages, 375 and 1280,
`prefers-reduced-motion: reduce`, no console errors, no horizontal overflow.
The reveal is an affordance, not motion, so it must still work under reduced
motion (`test_specimen_reveal_works_under_reduced_motion`).

---

## Stage A4 — the climbing specimens

**Branch:** `feature/specimens-climbing`. **Blocked on A0.** Identical to A3:
carabiner glyph, label "Climbing / Скалолазание", three specimens,
`id="specimen-climb-<slug>"`, same test updates.

One extra check: climbing's "wrong line" may not be a single short sentence
the way a grammar error is. `.line-spec` is set at showpiece size
(`test_specimen_sentence_pair_reads_at_showpiece_size`,
`tests/test_layout.py:83`) and `.spec__lines` sits beside `.spec__why` in a
two-column grid at desktop (`tests/test_layout.py:64`). **If a climbing
correction cannot be said in one line, do not widen the layout to fit it —
say so and stop**, and take it back to Igor as a copy problem. The format's
whole claim is that an error can be named and shown in one line; a climbing
specimen that needs a paragraph is evidence the specimen is wrong, not that
the component is.

---

## Stage A5 — the section frame *(A-standalone mode only)*

**Branch:** `feature/specimen-section-frame`. **Skip entirely in A-into-B
mode.**

§02 currently reads, in the heading: *"Your errors are a finite list. Nobody
ever shows you the list."* and, in the lede, an argument entirely about
Russian grammar laying over English. With nine specimens across three
disciplines, both are now wrong about their own section.

- New `h2` and lede — EN may be drafted here, **RU is Igor's** (Standing
  Order 9: a chat may ship a clearly-flagged first-pass RU in an HTML
  comment; it may not ship RU voice as settled).
- The label text `Specimens / Разбор ошибок` probably survives; confirm.
- The `.breath` block directly below §02 ("Once an error has a name it stops
  being 'my English is bad'…") is now the payoff for three disciplines, not
  one. Check whether its wording still lands; it is **Igor's approved copy**
  moved here deliberately at Spark Order S3/move 08, so any change to it is
  his, and it must stay unnumbered
  (`test_breath_block_takes_no_section_number`).
- Re-check the no-digit rule after the rewrite.
- Typography: §02's copy went through J1's typographic pass on 2026-09-12 —
  new EN copy uses `’` and `“ ”`, never straight quotes, and a test asserts
  zero straight apostrophes in visible EN text.

---

## Do not

- Put the three groups behind **tabs or an accordion**. It hides content
  (Standing Order 10), fights "explain it in detail", and would be a second
  reveal mechanism on a page that already owns one.
- Give a discipline its **own colour**. Two inks exist and both are already
  spoken for: amber = the specimen under examination, green = the target.
  Differentiate by glyph, label and rhythm.
- Add a second easing curve or a second reveal timing. Extend the `D` table
  at `main.js:36` if a new duration is genuinely needed.
- Touch the hover-reveal behaviour. It is Igor's own request (2026-09-07) and
  four tests at `tests/test_a11y.py:296–375` encode it.
- Rename any `specimen-*` id.
- **Republish the live artifact.** "Vitnyr Signature" is on hold until real
  photographs of Igor replace the 15 remaining stand-ins (Jury Pass II
  Standing Order 2). Say in your BUILD-NOTES entry that you did not
  republish, and why.

---

## Stage map

Keep this table true — flip your stage in the same merge, with the date and
the merge SHA.

| Stage | Branch | Blocked on | Status |
|---|---|---|---|
| A0 — material and decisions | none (no code) | Igor | **open** |
| A1 — generalise the machinery | `feature/specimen-machinery` | nothing | **ready** |
| A2 — the group frame | `feature/specimen-groups` | A1 | pending |
| A3 — chess specimens | `feature/specimens-chess` | A0, A2 | pending |
| A4 — climbing specimens | `feature/specimens-climbing` | A0, A2 | pending |
| A5 — the section frame | `feature/specimen-section-frame` | A3, A4 | pending (A-standalone only) |
