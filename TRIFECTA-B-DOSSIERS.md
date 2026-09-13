# Trifecta Order B — the dossier spine

**Idea 2 of the 2026-09-13 trifecta brainstorm.** Retire the three thin domain
cards and give English, chess and climbing one full section each, built from
the same five-slot template, in the same order, every time.

One of three independent orders. The other two are
`TRIFECTA-A-SPECIMENS.md` (the diagnostic format, three times) and
`TRIFECTA-C-MARK-NAV.md` (the mark as navigator). **This is the largest of
the three and the only one that changes the page's positioning.** Read Stage
B0 before anything else.

**One stage = one chat = one branch**, per `CLAUDE.md`. Before touching code,
read `CLAUDE.md`, `BUILD-NOTES.md`, `JURY-PASS-II.md` (its Standing Orders
bind here too) and this file's stage in full.

---

## Why this order exists

Measured on `main` at 1280px, 2026-09-13:

- The chess card is **227px / 42 words**. The climbing card is **227px / 45
  words**. English gets roughly 4,000px of dedicated argument across the
  hero, §01 and §02.
- §06 still asks the reader to *"Tell me what you need **English** for"* —
  so even after §05 was broadened to the full trifecta on 2026-09-12, the
  page's one conversion step accepts one discipline.
- The JSON-LD says `"jobTitle": "English coach"`; the meta description, the
  `og:` copy and `<title>` all assert a single service.

A discipline that gets 227px and no mechanism of its own is decoration, and
the page's own argument is that decoration is what it does not do.

---

## Stage B0 — the positioning decision and the material (no code)

**Output:** answers recorded in this file plus a BUILD-NOTES entry. **No
source file changes.** Every stage after this is blocked on it.

### B0.1 — the collision, stated plainly

`CLAUDE.md` records, under "Content and positioning decisions (already made —
don't re-litigate)", that chess and climbing are **proof-of-method, not
services on offer**, and that the funnel is a *credibility anchor*: the
trifecta persuades precisely because the two side disciplines are
disinterested evidence. "My method transfers, and here is proof" is a
stronger claim than "I sell three kinds of coaching", which reads generalist.

Igor's 2026-09-12 brief — *explain in detail what my English coaching offers,
chess coaching offers and climbing coaching offers* — converts proof into
product. **That is his call and it supersedes the earlier decision if he
confirms it**, but it must be confirmed explicitly and written into
`CLAUDE.md`, not assumed from this file's existence.

Two targets, and the whole order changes shape between them:

- **Weighted** *(recommended)*. Three full dossiers; English first and
  visibly largest; chess and climbing real, bookable and secondary. Keeps the
  credibility argument. Keeps C6 (§04's mark rests with English lit) and J7
  (the raised dim floor) intact, both of which are settled decisions resting
  on "English is the offer, the other two are proof it transfers".
- **Equal**. Three co-equal practices. Cleaner symmetry and the stronger
  formal move — and it forces a hero rewrite, reverses C6's rest state, and
  rewrites every piece of metadata. Note that reversing C6 is **not** a
  return to the pre-C6 neutral state, which was an accident; it would be a
  new, deliberate, equal-weight state and needs its own reasoning.

> **Decision: _pending_**

### B0.2 — the material that does not exist yet

Standing Order 8, real material only. There is **no** repo-recorded fact
about chess or climbing *coaching*. 8 years and 100+ clients are English
figures. 2100 and 7c redpoint / 7C Kilter are Igor's own results, not
coaching results. **No stage in this order may imply a chess or climbing
student exists unless Igor says one does.**

For each of the three disciplines, Igor supplies:

1. **Who it's for** — one line.
2. **What a session actually is** — the real format: length, online vs. in
   person, which gym or club in Yerevan, what happens in the first ten
   minutes. Three to four steps, his words.
3. **What you leave with** — one line.
4. **Whether it is actually sold** — is chess coaching a thing someone can
   book today, or is this a statement of what he could coach? The page must
   say the true one.
5. **The RU for all of it** (Standing Order 9).

> **Answers: _pending_**

### B0.3 — the numbering

The page's `01`–`06` count is part of its editorial identity and
`test_section_numbering_is_sequential` (`tests/test_content.py:203`) asserts
the exact list. Three dossiers make it:

```
01 The method
02 English      ← absorbs today's §02 Specimens
03 Chess
04 Climbing
05 Name & mark
06 Who this is for
07 How to start
```

Confirm the shape with Igor before B1 — in particular whether §01 "The
method" still leads, or whether the three dossiers come first and the method
reads out of them. (Recommend: method stays first. It is the argument the
dossiers are evidence for, and §01's three mechanisms — feedback loops, error
correction, load management — are the template's own spine.)

> **Decision: _pending_**

### B0.4 — what happens to the facts row and the collage door

Both live inside today's `#disciplines`, which B4 retires.

- **`.facts`** — the four measured readings (8 years, 100+, 2100, 7c/7C).
  Guarded by four tests (`test_the_three_measured_facts_are_exactly_these`,
  `test_facts_row_names_each_unit_type`,
  `test_no_unapproved_statistics_in_the_facts_row`,
  `test_reduced_motion_facts_row_shows_every_value`) and animated by
  `countUp()` (`main.js:532`) with **per-number durations, not one shared
  sweep** — Igor reversed a simplification here once already; do not
  re-simplify it. Options: (a) distribute each reading into its own dossier's
  slot 1 and retire the row, moving the counters and their tests with it, not
  deleting them; (b) keep the row intact as a summary between the hero and
  the dossiers. **Recommend (a)** — a reading beside the discipline it
  measures is worth more than a row of four unrelated instruments — but it is
  a visible change to approved content, so it is Igor's.
- **`.proof`** — the "See the work" link is the collage door, and it is not
  an ordinary anchor: it carries the shared-element View Transition into the
  `#collage` view (`openWithDoorMorph`, `main.js:1083`). Moving it means
  moving the transition's source element. **The View Transition is
  close-only by design** — `startViewTransition` defers its callback, so the
  open path must not be wrapped. Do not re-engineer it while relocating it.
  With three dossiers there is an argument for three doors, one per
  discipline, each jumping to that group in the collage view — the masthead
  icons already do exactly that via `data-collage-jump` and `jumpToGroup()`
  (`main.js:1127`). That is a genuine improvement and it is **also idea 7,
  which is parked behind the photo shoot** (Jury Pass II, J10: 15 of 18
  frames are still non-Igor stock). Decide the door's placement now; leave
  per-discipline doors until the shoot lands.

> **Decision: _pending_**

---

## Stage B1 — the template, built once, on English

**Branch:** `feature/dossier-template`. **Blocked on B0.**

Build the template and prove it with the one discipline that already has all
its material. Nothing about chess or climbing is written in this stage.

### The five slots, fixed order, every dossier

```
1  label + glyph + the one measured reading      (English: 8 / 100+)
2  who it's for                                  one line
3  what a session actually is                    3–4 steps
4  the specimen                                  named error, wrong → right
5  what you leave with                           one line
```

Slot 4 in the English dossier is today's three specimens, moved **whole**,
ids untouched. If `TRIFECTA-A-SPECIMENS.md` has already landed, slot 4 takes
that discipline's `.specs__group` and nothing else.

### Constraints that will bite

- **Section ids and specimen ids are a public contract.** `#specimen-reflexive`,
  `#specimen-copula` and `#specimen-register` are shareable permalinks that
  the whole S9A permalink feature exists to support. They survive this
  restructure unchanged. Give the new dossier sections stable, language-neutral
  ids (`#english`, `#chess`, `#climbing`) and keep `#method`, `#origin`,
  `#who`, `#contact`, `#top` working — `main.js:1062` routes in-page hashes
  around the collage router and the skip link targets `#main`.
- **The C12 rule on hairline width.** `style.css:694` bleeds
  `.mechanisms, .specs, .domains, .rows, .channels, .proof` out to the
  section's own edge and re-adds the inset as padding, so **every horizontal
  rule on the page is exactly one width**. Any new block class the dossier
  introduces joins that selector list. A block that draws its own
  `--gut`-narrower rule is the exact defect C12 removed.
- **Layout never rides the transform channel** (Standing Order 6). Grid
  placement, margins, `inset`. The `.reveal` is `translateY(24px)` and any
  element carrying a layout transform will fight every animation that later
  targets it — this is not hypothetical, see the `NaN` transform-cache bug
  in BUILD-NOTES.
- **`.past-origin` is measured off `#origin`.** `measureOrigin()`
  (`main.js:72`) reads `#origin`'s page offset and `trackProgress()` flips the
  masthead progress rule's ink from specimen to target when the reader passes
  it. If `#origin` moves from position 4-of-6 to position 5-of-7, the point
  where the page's progress hairline changes meaning moves with it. Decide
  deliberately whether that is still the right switch point and say so in the
  note; do not let it drift silently.
- `test_section_numbering_is_sequential` will fail. Update it — **and state
  in the BUILD-NOTES entry that you edited an existing test and why**
  (Standing Order 4). Prefer widening it to assert "sequential from 01 with
  no gaps" over hard-coding a new literal list.
- The `.breath` block between §02 and §03 must stay unnumbered and must not
  become viewport-height (`test_breath_block_takes_no_section_number`,
  `test_breath_block_is_not_viewport_height`).

### Craft notes

The five slots repeating unchanged across three sections **is** the design.
Resist varying the template per discipline: the variation the reader should
see is the content and the glyph, not the layout. Differentiate with the
book / checkerboard / carabiner glyphs already drawn in the masthead nav and
on the collage group labels, via the existing `.label--glyph` /
`.label__mark` idiom (`index.html:782`) — do not author a second label
pattern.

Under the **weighted** decision, English's dossier is visibly the largest:
give it the extra weight through content depth and slot 4's three specimens,
not through a bigger type scale or a different layout. One type system.

### Verify

Both themes, both languages, 375 and 1280, `prefers-reduced-motion: reduce`,
no console errors, no horizontal overflow, body-copy contrast not pushed
below 4.5:1 on cream (baseline 5.45 cream / 7.71 charcoal). Drive a real
Chromium (`tests/.venv/bin/python`, Playwright is installed) and take real
frames — the preview pane repaints on demand and one screenshot proves
nothing for anything scroll-driven.

---

## Stage B2 — the chess dossier

**Branch:** `feature/dossier-chess`. **Blocked on B0.2 and B1.**

Same five slots, checkerboard glyph, `id="chess"`. Slot 1 carries `2100` —
**stated without "FIDE"**, which is Igor's own correction and is asserted by
`test_person_json_ld_carries_only_confirmed_facts`.

Slot 4 is empty unless `TRIFECTA-A-SPECIMENS.md` Stage A3 has landed. **Do
not ship an empty slot or a "coming soon".** If A3 has not landed, the chess
dossier has four slots and the template note in the code says why — a
promise with nothing behind it is worse than a shorter section.

If Igor's answer to B0.2.4 is that chess coaching is not yet something anyone
can book, the section says what is true and slot 5 changes accordingly.
Do not soften it into an implied offer.

---

## Stage B3 — the climbing dossier

**Branch:** `feature/dossier-climbing`. **Blocked on B0.2 and B1.**

Same again, carabiner glyph, `id="climbing"`. Slot 1 carries **`7c` redpoint
indoor and a `7C` Kilter boulder as two separate readings** — they are
different grades and must never be merged into one generic "7c", and the
case difference is meaningful. `.domain__meta`'s `text-transform: uppercase`
already destroyed this distinction once; J2 fixed it on 2026-09-12 by
exempting `.domain__stat`, and there is a test reading **rendered** text
(`inner_text()`, not `text_content()`) to keep it fixed. **Any new stat
element in the dossier template needs the same exemption and the same
rendered-text assertion** — this is the single easiest regression in this
order.

---

## Stage B4 — retire §03, and fix the funnel

**Branch:** `feature/retire-domains`. **Blocked on B2 and B3.**

With three dossiers live, the three domain cards are a duplicate of them.

1. Remove `#disciplines`' `.domains` block. Relocate `.facts` and `.proof`
   per B0.4 — **relocate, never delete**; their tests and `countUp()`'s
   per-number durations move with them.
2. **Fix §06.** Its lede still reads *"Tell me what you need English for and
   where it breaks now."* Rewrite so all three disciplines can land there.
   EN drafted; **RU is Igor's**.
3. **Make the CTA discipline-aware.** `initWhoRows()` (`main.js:1186`)
   already composes a first-person clause onto the Telegram deep link from
   `data-prefill-en` / `data-prefill-ru`, and `updateCta()` rebuilds the
   `href` from `data-href-en`/`-ru`. Give each dossier a closing control that
   feeds the **same** machinery — "I'd like chess coaching." — rather than
   building a second prefill mechanism. This is the highest value-per-line
   change in the whole order: it is the difference between three sections
   that inform and three that convert.
   Do not break the deep link:
   `test_contact_cta_prefill_text_is_localized` and the S5 composition tests
   guard it, and a curly apostrophe inside a percent-encoded `data-href-*`
   breaks Telegram (J1's explicit carve-out).
4. Keep **one loudest thing** on the page. J3/J5 (landed 2026-09-12) dropped
   the three channel rows to a quieter tier and gave the travelling arrow to
   `.contact__cta` alone, so the page has a single conversion control. Three
   new per-dossier controls must sit **below** it in the hierarchy — no new
   colour, no button chrome, no rounded corners.

---

## Stage B5 — metadata catch-up

**Branch:** `feature/dossier-metadata`. **Only if B0.1 changed the
positioning.**

`<title>`, `meta[name=description]`, `og:title`, `og:description`,
`og:image:alt`, and the JSON-LD `Person` block (`jobTitle`, `description`)
all currently assert a single service. Bring them in line with whatever B0.1
decided — and no further: `test_person_json_ld_carries_only_confirmed_facts`
asserts every field is one of the site's confirmed facts and that the string
"FIDE" never appears.

`og:url`, `og:image`, `canonical` and the `hreflang` alternates stay on
`https://vitnyr.example/` — the RFC 2606 reserved placeholder, held as a
single find-and-replace point until a real domain exists. Two tests assert
it. Do not "fix" it to a guessed domain.

---

## Out of scope, deliberately

- **The hero.** It names the trifecta already. Under an "equal" decision its
  third line wants to become a typographic index of three links — that is a
  **fresh brief**, not a rider on this one. `playHero()` is the most fragile
  code in the repo (it shipped a `NaN` transform-cache bug that silently
  killed every later tween), the first viewport already carries four timed
  systems, and Spark Order S8's closure says explicitly that any hero
  revisit starts from a fresh brief.
- **The comparative instrument** (idea 3 — the three feedback loops side by
  side). It belongs *between* the dossiers and it is the thing that makes
  them one method rather than three services, but it is its own order.
- **A contents index** (idea 6). At ~8,650px with six sections the page can
  live without one; at the ~12,000px three dossiers will produce, it needs
  one. Revisit after B4, and remember the phone has no spare masthead height
  after J4.
- **Per-discipline photographs** (idea 7 / Jury Pass II J10). Parked behind
  the shoot.

## Do not

- Tabs, accordions, or any mechanism that hides a discipline's detail.
- A third colour, a per-discipline colour, gradients, shadows, rounded
  corners (the cursor dot is the one exception and not a precedent).
- A second easing curve or a second reveal rhythm — extend `D` at
  `main.js:36`.
- Horizontal scroll or parallax columns for the three dossiers: layout on the
  transform channel, and both die under reduced motion.
- Reopen J3, J6, J7 or J8 — all settled, several by Igor personally.
- **Republish the live artifact** (Jury Pass II Standing Order 2). Say in your
  BUILD-NOTES entry that you did not, and why.

---

## Stage map

| Stage | Branch | Blocked on | Status |
|---|---|---|---|
| B0 — positioning + material | none (no code) | Igor | **open** |
| B1 — the template, on English | `feature/dossier-template` | B0 | pending |
| B2 — chess dossier | `feature/dossier-chess` | B0.2, B1 | pending |
| B3 — climbing dossier | `feature/dossier-climbing` | B0.2, B1 | pending |
| B4 — retire §03, fix the funnel | `feature/retire-domains` | B2, B3 | pending |
| B5 — metadata | `feature/dossier-metadata` | B0.1 | pending (only if positioning changed) |
