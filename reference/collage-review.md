# Photo collage — review gate for stages 0–2

Paste the block below into a **fresh chat** before `feature/photo-collage`
merges to `main`. The reviewer must not be the chat that built the work:
the builder has sunk cost and, worse, carries the *intent* in context —
it reads its own markup and sees what it meant.

The prompt is deliberately self-contained. It needs no context from the
conversation that produced it.

Two things it cannot do, which stay with Igor:

- **The Russian copy.** A model wrote it, Igor coaches language for a
  living, and captions fall under "real material only" — a caption
  describing a photograph that does not exist yet is a claim waiting to
  be wrong.
- **A real scroll-through in a real browser.** `BUILD-NOTES.md` still
  carries "not verified by eye: everything below the hero" as an open
  item, and this feature lands squarely down there.

`/code-review` is a weak complement here — it hunts correctness bugs, and
stages 0–2 are markup, CSS and copy with almost no logic. Worth one free
run, not worth waiting on.

---

```
VITNYR — REVIEW OF STAGES 0 THROUGH 2
Review only. Do not fix anything. Do not merge. Do not push.

═══════════════════════════════════════════════════════════════════
YOUR ROLE
═══════════════════════════════════════════════════════════════════
You did not build this. Read it cold and look for violations, not for
things to admire. A reviewer that silently fixes what it finds hides the
finding — report, and let me decide what gets changed.

Read CLAUDE.md and BUILD-NOTES.md in full FIRST. They hold decisions made
in conversation that nothing in the code will tell you about. Then read
the diff: git diff main...feature/photo-collage

Separate every finding into one of two classes and label it:
  [VIOLATION]  breaks a rule written down in CLAUDE.md or BUILD-NOTES.
               Objective. Cite the file and line of the rule.
  [JUDGMENT]   your design opinion. Legitimate, but mine to overrule.
Do not blur the two. Give file:line for every finding.

═══════════════════════════════════════════════════════════════════
GATE A — MECHANICAL. Verify each, report pass/fail with evidence.
═══════════════════════════════════════════════════════════════════
A1. i18n PARITY — the highest-risk defect in this feature, check it
    first and most carefully. Every data-en has a data-ru. Every
    data-l="en" has a data-l="ru" sibling. CSS hides the inactive
    language, so a missing twin renders NOTHING and is invisible unless
    you switch languages. Enumerate every new translatable string and
    confirm both halves exist. Do not eyeball this — count them.

A2. HEX AUDIT — every colour in the diff is one of the ten pair values
    in style.css's :root and light blocks. List any hex that isn't.

A3. BANNED PROPERTIES — no gradient, no box-shadow, no border-radius
    anywhere in the diff. The only legal border-radius on this site is
    .cursor__dot.

A4. ACCENT DISCIPLINE — amber/green appear only as ink (rules, glyphs,
    display numerals), never as text under 24px. Amber fails 4.5:1 on
    cream body text and green fails it on charcoal.

A5. TRANSFORM CHANNEL — confirm the composition achieves overlap and
    offset via grid placement, negative margins or inset, and NOT via
    transform. Stage 4's reveal is translateY and needs that channel
    free. If transform is carrying layout, this is a [VIOLATION] and it
    blocks Stage 4 — say so loudly.

A6. RESERVED BOXES — every placeholder figure has non-zero height with
    no image present. If any collapses, Stage 2's composition is built
    on sand and Stage 3 will shift.

A7. OVERFLOW SWEEP — measure document.body.scrollWidth against
    window.innerWidth at 375 / 768 / 900 / 1024 / 1100 / 1280. The
    900-1100 band is where an overlapping composition first has room to
    overlap and is the likeliest place to find overflow. Report the
    numbers, not a verdict.

A8. SECTION NUMBERING — the numbers read in sequence with no repeats
    and no gaps, in both languages.

A9. SPECIFICITY — no .collage rule fights .sec over padding or margin.
    Check for silently cancelled declarations.

A10. NEW TOKENS — any new custom property sits in the :root block under
     a --collage-* prefix, not scattered inline.

═══════════════════════════════════════════════════════════════════
GATE B — THE SEPARATE VIEW. Drive it, do not infer it.
═══════════════════════════════════════════════════════════════════
The collage is a full-screen view routed by hash, not a second file,
because the live artifact is one self-contained HTML file. Confirm:

B1. Deep link: loading #collage directly lands on the collage.
B2. Refresh while on #collage stays on the collage.
B3. Browser back returns to the main page.
B4. Theme and language persist across the transition with NO flash of
    the wrong one. theme.js stamps before first paint — confirm that
    path was not duplicated or bypassed.
B5. FOCUS MOVES to the destination view's heading on navigation, not
    just scroll position. BUILD-NOTES documents the skip-link bug where
    scroll happened and focus did not. Test with the keyboard.
B6. Scroll position resets on view change (Lenis drives scroll).
B7. The masthead wordmark SVG was reused verbatim, not regenerated or
    redrawn. index.html says never to redraw it.
B8. index.html is still a single file with no second .html and no new
    external asset the artifact rebuild could not inline.

═══════════════════════════════════════════════════════════════════
GATE C — SCOPE. Nothing from later stages may have leaked in.
═══════════════════════════════════════════════════════════════════
C1. No image files, no <picture>, no srcset. Stage 3 is blocked on a
    shoot that has not happened.
C2. No .reveal classes on the tiles, no parallax, no new entry in the D
    table in main.js. Motion is Stage 4.
C3. No data-magnetic on the tiles. That decision belongs to Stage 5 and
    the prompt requires it be argued before implemented.
C4. BUILD-NOTES.md's "no images to lazy-load" claim should still be
    UNCHANGED and still TRUE — there are no images yet. If it was
    already edited, that is a premature doc change: flag it.

═══════════════════════════════════════════════════════════════════
GATE D — DESIGN JUDGMENT. Opinions, clearly labelled as such.
═══════════════════════════════════════════════════════════════════
CLAUDE.md says the five-specialist pass is worth reusing for a feature
touching several disciplines. This one touches three. Run those three
only — skip colour (Gate A covers it), logo (untouched) and motion
(not built yet).

D1. COPY. Both languages. Does it hold to "real material only"? A
    caption describing a photograph that does not exist yet is a claim
    waiting to be wrong — flag any that overreach. Does "Igor Shatsev"
    appear in both languages? Is the register consistent with the rest
    of the page, which is dry, specific and unsold?

D2. TYPE. Mono means one thing on this site: quoted linguistic
    material. If mono is being used on the collage as texture or as a
    label, that is drift from the type pass — flag it.

D3. COMPOSITION. Screenshot the collage view at 375 and 1280 and show
    me both.

    Then the test that matters: JUDGE IT EMPTY. There are no
    photographs in it. If the composition only reads well once
    attractive images are inside, the composition is not doing the
    work — you are seeing the photos, not the layout. This question
    becomes unaskable after Stage 3, so answer it now and give me your
    honest assessment, including if the answer is that it is weak.

D4. THE ENTRY BUTTON. Is it built from vocabulary already on the page
    (.scrollcue, .tool, .channels a), or is it a new control type
    wearing the site's colours? Does it have a visible keyboard focus
    state? Is it placed where it argues for the trifecta? Would you
    know it was part of this interface if you saw it alone?

═══════════════════════════════════════════════════════════════════
OUTPUT
═══════════════════════════════════════════════════════════════════
1. Gate A, B, C as a pass/fail table with evidence — numbers, not
   assurances.
2. Findings ranked most severe first, each labelled [VIOLATION] or
   [JUDGMENT], each with file:line.
3. The two screenshots.
4. Your answer to D3, stated plainly.
5. A single closing line: is this branch fit to merge to main, yes or
   no, and if no, the shortest list of things that would change it.

Change no files. Make no commits. Do not merge.
```
