# Finishing touches — work order

**Date:** 2026-11-20. **Starts from:** `main` at `c3aee7e`, the four-page site
(home + `/english/` `/chess/` `/climbing/`), live on vitnyrcoach.com and on the
claude.ai artifact the same day.

**Goal:** take the site from "well built" to "polished, award-level, and
converting": a stranger lands, sees a real person, picks a discipline in
seconds, trusts what they read, and messages Igor.

**Where this came from:** the 2026-11-03 review (four lenses: design-award
judge, marketer, copywriter, brand strategist). Its five small fixes already
shipped (`e8844b5`). Everything below is what's left from that review, put in
order.

## Standing orders

1. One stage per branch (`feature/ft<N>-<name>`), off an up-to-date `main`.
   Merge and push only when Igor says so. Republish the artifact with
   `tools/artifact/build.py` after every visible merge.
2. **Real material only** (CLAUDE.md). Any item that needs Igor's words,
   photos, reviews or links waits for them. It never gets a stand-in that
   looks real.
3. Settled decisions stay settled: all three disciplines in the home
   headline, English leads (Weighted), Telegram → LinkedIn → Instagram, no
   prices, no third colour, no shadows or rounded corners, one easing curve,
   layout never takes the transform channel.
4. Verify every stage: both themes, both languages, ~375px and ~1280px,
   reduced motion, no console errors, no horizontal overflow, and the full
   test suite.
5. **Every masthead, footer or contact change is made four times**, once per
   page (the pages share no template). Checklist per item: home, english,
   chess, climbing.

---

## FT0: Igor's answers (no code)

Each FT stage says which of these it needs. Ask them in one message.

| # | Question | Needed by |
|---|---|---|
| Q1 | **Home headline.** Pick one of three plateau-language options (drafted in FT2 before asking), or keep "Skill acquisition, coached." | FT2 |
| Q2 | **Dark mode.** On 2026-09-29 you reversed the 2026-09-07 rule (cream always) so the site follows the phone's setting. That work is half-done and uncommitted on `feature/theme-follows-system`. Finish it, or drop it? | FT1 |
| Q3 | **Reply time.** Is "available 24/7" true? If not, what is: "usually within a few hours"? "by the next morning"? | FT3 |
| Q4 | **Your story.** Three true sentences: why these three disciplines, and is rehab part of your own story (Instagram suggests so)? Or skip the About block's story line. | FT2 |
| Q5 | **Proof links.** Lichess and/or Chess.com username (public, shows the 2100)? Any climbing video you'd show? | FT3 |
| Q6 | **Handles.** Can Telegram / Instagram move to `vitnyrcoach` (LinkedIn already is)? If not, they stay as they are. | FT3 |
| Q7 | **FAQ answers**, per discipline, 4–5 each: beginners? kids' ages (chess)? non-Russian speakers (English)? group size? how many sessions until results? | FT3 |
| Q8 | **Chess positions.** 2–3 positions from your own games (or students', with their permission) that show each of the three chess mistakes. A PGN or a Lichess link is enough. | FT4 |
| Q9 | **Reviews.** Real chess / climbing quotes, whenever they come in. Until then, the home strip stays labelled "English students". | any |

**Igor's answers (2026-11-20):** Q1 draft the options · Q2 **finish** dark
mode · Q3 **"available 24/7" is true, keep it** (so 3.2 is dropped) · Q4
later · Q5 Lichess **`yngvibrychenka`** · Q6 not yet (handles stay) · Q7
later · Q8 later.

**Done ahead of order (2026-11-20, `feature/ft2-hero-portrait`, 88b2e40,
not merged):** Igor asked to "pull the picture to the top". The portrait
moved from the contact section into the home hero (two columns at >=900px,
between title and stand on phones); the hero's still-life vignette gave up
its place, and the empty chair took the portrait's column in contact. This
covers the portrait half of 2.1 and part of 2.4's intent on home; the About
block's story lines still wait for Q4.

---

## FT1: Fix what looks unfinished

*Small items, mostly CSS and markup. Needs: Q2 only. About 1–2 sessions.*

| # | Item | Where | What "done" looks like |
|---|---|---|---|
| 1.1 | **"See me at work" photo strip** | home | The empty band becomes a row of 4–5 real photos (from the gallery's existing files) with the heading over it; the whole strip opens the gallery. Uses the existing reveal, with no new motion. |
| 1.2 | **Session photo rows** | english, chess, climbing | The left third stops being empty: either the two photos span the full width, or a short line sits there (the trial-lesson line, or the page's one quote). Pick one pattern and use it on all three pages. |
| 1.3 | **One meaning per icon** | all four mastheads | The book / board / carabiner icons always mean the disciplines (go to `/english/` etc., current one underlined). "Photos" becomes a plain text link to the gallery. Update the caption, the aria-labels and the tests. |
| 1.4 | **Phone masthead height** | all four | At 375px the bar takes 3 rows (~170px) before the hero. Get it to 2 rows without shrinking any 44px touch target (J4's constraint, see the long comment in style.css). If it can't be done without breaking J4, say so and stop. |
| 1.5 | **Six reviews, not seven** | home + english | The seventh card sits alone on its own row in the static (reduced-motion) grid. Drop the weakest ("…has a unique teaching approach"). Check with Igor first; it's his material. |
| 1.6 | **Dark mode** | theme.js | Per Q2: finish and merge `feature/theme-follows-system` (rebase it onto the new `main` first), or close it. |

---

## FT2: A face and a first impression

*The biggest lever for getting messages. Needs: Q1, Q4. About 2 sessions.*

| # | Item | Where | What "done" looks like |
|---|---|---|---|
| 2.1 | **About block** | home | Igor's portrait (the graded colour file already in `assets/portrait/`), three lines from Q4, and the Vitnyr name story moved here from where it floats now. Sits right after the discipline choice, before the method. The contact section keeps its own small portrait. |
| 2.2 | **Home order** | home | Hero → choose a discipline → about → method (compressed: the chain drawing plus the five principle names, each linking to the matching section on the discipline pages) → reviews → contact. The full 5×3 method stays on the discipline pages, where it already is. |
| 2.3 | **Home headline** | home | Per Q1. Draft three options in plateau language; all three disciplines stay in the headline. Line-mask entrance and RU sizing re-checked (the `.5em` RU rule in style.css exists for a reason). |
| 2.4 | **Bigger hero photos** | english, chess, climbing | The top-of-page photo goes from ~330px to roughly half the content width at ≥900px, without pushing the "Book a free trial" button below the fold at 1280×800. Keep the grayscale filter, drop or soften the 1px frame. |

---

## FT3: Trust and the last step

*Copy and small components. Needs: Q3, Q5, Q6, Q7. About 2 sessions.*

| # | Item | Where | What "done" looks like |
|---|---|---|---|
| 3.1 | **"What happens next" strip** | contact, all four | Three steps, no prices: *Message me → 30-minute trial → we agree on a plan.* Hairline rows, the page's own label style. |
| 3.2 | ~~**Reply time instead of 24/7**~~ dropped: Q3 says 24/7 is true | contact + footer, all four | Per Q3. If it fits, tie it to the footer's Yerevan clock ("It's 23:23 in Yerevan, so expect a reply by morning"). Uses data that's already on the page; no new tracking. |
| 3.3 | **Channel notes per page** | contact, three discipline pages | Each page's notes about the three channels speak to that discipline (chess no longer says "I write about English here"). Order unchanged. |
| 3.4 | **Proof links** | chess (+ climbing if Q5) | Lichess/Chess.com profile link next to "2100 · my rating". A real, checkable number. |
| 3.5 | **FAQ** | three discipline pages | 4–5 questions each from Q7, as a native `<details>` list in the page's hairline style, plus `FAQPage` JSON-LD. Both languages. |
| 3.6 | **Handles** | everywhere + JSON-LD + tests | Only if Q6 says yes. |

---

## FT4: The signature moment

*The thing people remember and share. Needs: Q8. About 2–3 sessions; the
largest stage.*

| # | Item | Where | What "done" looks like |
|---|---|---|---|
| 4.1 | **Chess positions you can step through** | chess | Each of the three chess mistakes gets a real board: the position, then "what was played" (amber), then "what to play" (green), one step per click or key. Drawn as SVG in the engraved-plate style (no chess library), with a static fallback when JS is off and reduced-motion support. It replaces or sits beside the current code-font sentence. |
| 4.2 | **The Russian behind the mistake** | english | Under each English mistake, the Russian original sits faintly ("Я согласен" under "I am agree"), so the reader sees where the error comes from. EN page only; the RU page already speaks Russian. Typography only, no new colour. |

---

## FT5: Launch polish and the jury pass

*About 1 session, then whenever something lands.*

| # | Item | What "done" looks like |
|---|---|---|
| 5.1 | **Speed** | Lighthouse (mobile) on all four pages; fix what it finds. Likely: WebP/AVIF `<picture>` for the photos (the undone half of the collage plan), font subsetting, and checking the plates' SVG weight. Record the before/after numbers in BUILD-NOTES. |
| 5.2 | **Accessibility + Safari** | Keyboard path through every new component, screen-reader names in both languages, iOS Safari check of the dock, the curtain footer and the chess boards. |
| 5.3 | **Jury pass** | Full-page screenshots of all four pages in both themes, both languages and both widths, judged against this order's goal. One short list of last nits, fixed in the same pass. |
| 5.4 | **Docs** | CLAUDE.md, BUILD-NOTES.md, memory. Republish the artifact. |

---

## Stage map

| Stage | Needs from Igor | Size | Status |
|---|---|---|---|
| FT0: answers | n/a | one message | **open** |
| FT1: unfinished bits | Q2 (answered: finish) | small | **open**, all of it can start now |
| FT2: face + first impression | Q1 (draft), Q4 (later) | medium | **open**; hero portrait built (88b2e40), headline drafts next |
| FT3: trust + last step | Q5 answered; Q6, Q7 later | medium | **open**, 3.1, 3.3 and 3.4 can start now |
| FT4: signature moment | Q8 | large | **open**, blocked on Q8 |
| FT5: polish + jury | n/a | small | **open**, runs last |

Already done from the 2026-11-03 review: the climbing contradiction, the home
intro numbers, chess wording, search titles/snippets, and the home review
label (`e8844b5`). The four-page site was merged and published on 2026-11-20
(`c3aee7e`).
