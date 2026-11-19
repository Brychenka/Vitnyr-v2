# Site plan: step by step

**Date:** 2026-11-20. **Starts from:** `main` at `c3aee7e` (four pages, live on
vitnyrcoach.com), plus the hero-portrait branch `feature/ft2-hero-portrait`
(`88b2e40`, built and tested, not merged yet).

**What this is:** the one work order for the site from here on. It merges
`FINISHING-TOUCHES.md` (its item numbers are kept in brackets, e.g. [FT1.1],
so nothing gets lost) with the 2026-11-20 council review (developer,
designer, copywriter, marketer). Ideas the council threw out are listed at
the end so nobody proposes them again.

**Who it is for:** anyone picking up the next step, including a less
experienced developer or a smaller model. Every step says why, where, what
to do, what to leave alone, and how to know it's done. Follow the steps
literally. If a step doesn't match what you find in the code, stop and ask
instead of improvising.

**The goal, in one line:** keep everything that already makes the site
beautiful, and add only what makes it clearer, more trustworthy, or more
personal. Nothing in this plan redesigns what works.

---

## Part 0: Rules for every step (read before you start)

### 0.1 Protect what already works

These are the things people notice and like. No step in this plan may
change them, unless the step says so in words.

| What | Rule |
|---|---|
| **Colours** | Two theme colours (cream/charcoal) and two inks: amber (`--ink-specimen`, the mistake) and green (`--ink-target`, the correct form). No third colour. Accent ink is never used for text under 24px. |
| **Shapes** | No shadows, no gradients, no rounded corners (the cursor dot is the only exception). Rules are 1px hairlines in `--rule`. |
| **Type** | Lora for headings and quotes, Inter for body, JetBrains Mono for labels and specimens, Marck Script only for the handwritten notes ("message me", "Choose your discipline"). No new fonts. |
| **Drawings** | The engraved plates (chain, chess clock, fork, crux, table and chairs, rune stone, empty chair) and the wordmark are hand-placed SVG. Never redraw, regenerate or "clean up" their paths. |
| **Motion** | One easing curve (`--e` in CSS, `'brand'` in GSAP). One reveal (`.reveal`: 24px rise and fade, 0.9s, 0.08s stagger). Layout never uses `transform`. With JavaScript off or reduced motion on, every word must still be readable. |
| **Languages** | Every visible string exists in English and Russian: short strings as `data-en` / `data-ru` attributes, long blocks as twin elements with `data-l="en"` / `data-l="ru"`. Don't invent a third way. Russian copy is written for Russian readers, not machine-translated; mark any Russian draft as a draft for Igor. |
| **Content** | Real material only: no invented clients, results, reviews or numbers. If something real is missing, the step waits. |
| **Settled decisions** | All three disciplines stay in the home headline. English leads. Contact order is Telegram, LinkedIn, Instagram. No prices. "Igor Shatsev" in both languages. |
| **Signature pieces** | The "Your move." footer and its turning glyphs, the Y-mark discipline chooser, the hero portrait, the Yerevan clock, the specimen plates, the magnetic pull (only on `.tool, .view__back, .origin__mark` and the masthead "message me"). |

### 0.2 The four-page rule

The pages share no template. Anything in the masthead, footer or contact
section is changed **four times**: `index.html`, `english/index.html`,
`chess/index.html`, `climbing/index.html`. Tick all four in the commit
message. When you change `style.css`, bump its `?v=` cache key on all four
pages (same new value everywhere, e.g. `?v=20261121a`). Same for
`main.js` / `theme.js` when they change.

### 0.3 The routine for every step

1. **Branch.** One branch per stage, off an up-to-date `main`:
   `git checkout main && git pull && git checkout -b feature/<stage-name>`.
   One commit per step, so any step can be undone on its own.
2. **Run the tests before you change anything:**
   `/Users/igor/Downloads/Vitnyr/site-v2/tests/.venv/bin/pytest tests -q`
   (about 7–12 minutes; the venv lives in the main checkout, so use the full
   path when working in a worktree). Expect all green plus one known xfail
   (`specimen-register-please`). Note anything else that fails *before* your
   change, so you don't blame yourself for it later.
3. **Make the change.**
4. **Look at it.** Both themes (cream, charcoal), both languages (EN, RU),
   at 375px and 1280px wide, with and without reduced motion. No console
   errors, no sideways scroll. Use headless Playwright screenshots if the
   preview pane is hidden (it throttles animations and lies about timing).
   For phone widths, use `has_touch=True` and compare against
   `innerWidth`; `scrollWidth` misses the masthead clip.
5. **Run the tests again.** If a test fails, read why. Change a test only
   when the step deliberately changes what that test protects, and say so in
   the commit message. Never loosen a test just to make it pass.
6. **The beauty check.** Before you call it done, answer three questions:
   - Did I add a colour, a shape, a shadow, a font or a new kind of motion?
   - Is the page longer without being clearer?
   - Would this look out of place next to the engravings?

   If any answer is yes, stop and show Igor before going further.
7. **Commit, then ask Igor before merging.** Merge to `main` and push only
   when Igor says so. After any visible merge, republish the live artifact
   to the same URL: `python3 tools/artifact/build.py <repo> <out-dir>` builds
   all four pages from committed files; read the artifact before publishing
   (the tool insists).

### 0.4 Size labels

**S** = under an hour. **M** = a session. **L** = several sessions.
**Waits** = needs something only Igor can give; don't start it until the
answer is in this file.

---

## Part 1: Running order

Do the stages in this order. Inside a stage, do the steps in the order
listed. A step marked **waits** is skipped until Igor's answer arrives, then
slotted into the next stage that's open.

| Stage | Branch | Steps | Size |
|---|---|---|---|
| 1. Clean up | `feature/s1-clean-up` | A1 (Igor), C1, B1, B2, B3, B4, C2, C7 | M |
| 2. Finish the frame | `feature/s2-frame` | C3, C4, C5, E1, E2 | M |
| 3. First impression | `feature/s3-first-impression` | D1, D2, D4 | M–L |
| 4. Signature | `feature/s4-signature` | F1, F2, F4 | L |
| 5. Speed | `feature/s5-speed` | G1, G2, G3, G4, G5 | M |
| 6. Polish and jury | `feature/s6-jury` | I1, I2, I3 | S–M |
| Any time | — | H1, H2 (Igor, off the site) | — |
| When answered | — | B5, B6, C6, D3, E3–E7, F3, H3, H4 | — |

---

## Category A: Measure first

### A1. Turn on visitor stats [new] · S · Igor's click

**Why:** right now nobody can tell how many people visit, from where, or
where they stop reading. Every later step needs a before and after.

**Do (Igor, in the Cloudflare dashboard):** Workers & Pages → the site's
Pages project → Metrics → Web Analytics → Enable. It uses no cookies, so
the site needs no consent banner, and it adds nothing to the repo.

**Keep:** no other tracking, no cookies, no third-party pixels.

**Done when:** the dashboard shows visits a day later. Note the date in
`BUILD-NOTES.md` so later changes can be compared against it.

### A2. Know where each message came from [new] · no code

Each page already sends its own Telegram message ("…free trial chess
lesson", "…English lesson"; Russian on the Russian pages). When a lead
writes, Igor can see which page sent them. Optional: keep a short list
(date, page, booked or not) for a month. That's the only conversion data the
site needs.

---

## Category B: Quick fixes (copy and small markup)

### B1. Chess hero: drop "procrastination device" · S

**Why:** the line tells the reader their hobby is procrastination, right
before asking them to trust you. It also contradicts "It isn't talent."

**Where:** `chess/index.html`, the two `<p class="stand reveal">` lines
(search for `procrastination` and `прокрастинации`).

**Do:** replace the first two sentences, keep the marked phrase and the
ending exactly as they are:

- EN: `A rating plateau isn't a talent ceiling. It's <strong class="mark">the same few patterns losing you the same games</strong>, and a pattern you can name is a pattern you can train out.`
- RU: `Застой в рейтинге — не потолок таланта. <strong class="mark">Одни и те же паттерны проигрывают вам одни и те же партии</strong>, а паттерн, который можно назвать, можно и вытренировать.`

**Keep:** the headline above it, the stat row, the button.

**Done when:** both languages read cleanly at 375px and 1280px. Igor
approves the wording (it's his voice).

### B2. English: the drawing and the first mistake match · S

**Why:** the plate at the top of "Mistakes I fix" draws "I ~~am~~ agree",
but the first mistake under it is the reflexive one ("I feel good today").
The reader looks for the drawn sentence and finds a different one.

**Where:** `english/index.html`, inside `<section class="sec" id="specimen">`.

**Do:** move the whole `<article class="spec reveal" id="specimen-copula" …>
… </article>` block so it sits **above** `id="specimen-reflexive"`. Move it
as one block; don't edit inside it. The order becomes copula, reflexive,
register.

**Keep:** IDs (deep links and tests use them), the plate, the "Show the
common mistake" behaviour.

**Done when:** the first item under the drawing is "I agree with your
point." in both languages, and `#specimen-copula` links still scroll to it.

### B3. Footer lines become links (all four pages) · S

**Why:** "Your turn to speak / The board is waiting / The next grade" read
like the way into each discipline, but they're plain text.

**Where:** each page's footer, `<dl class="foot__notes">` (search for
`Your turn to speak`).

**Do:**
1. Wrap each `<dd>` text in a link to its page: `/english/`, `/chess/`,
   `/climbing/`.
2. **Move the `data-en` / `data-ru` attributes from the `<dd>` onto the new
   `<a>`.** `theme.js` replaces the whole text of any element carrying
   `data-en`/`data-ru` on every language switch; left on the `<dd>`, it would
   delete the link. In the chess line, keep the `1…` span inside the link.
3. On each discipline page, leave its own line as plain text (no link to
   the page you're already on).
4. Style: the links look exactly like the text does now. On hover and focus,
   show the same hairline underline the other text links use. No magnetic
   pull (text links never get it), but the pointer dot should change ink as
   it does over any link.

**Keep:** the "Your move." line, the turning glyphs, the chess-clock plate,
the layout of the three notes.

**Done when:** all four pages, both languages: the links work, look
unchanged at rest, and the language switch keeps them as links (switch
EN → RU → EN and click again).

### B4. Channel notes that fit the page [FT3.3] · S

**Why:** the chess and climbing pages say "I write about English here"
under LinkedIn.

**Where:** `chess/index.html` and `climbing/index.html`, the LinkedIn
`<span class="ch__hint">` in the contact section.

**Do:** change only the LinkedIn note on those two pages to
`data-en="my coaching profile" data-ru="мой профиль тренера"`. Leave the
Telegram note ("available 24/7", which Igor confirmed is true) and the
Instagram note ("climbing + tendon/nerve rehab") as they are. Home and
English keep "I write about English here".

**Keep:** channel order and handles.

### B5. "Who this is for": each page speaks its own sport · S · waits (Igor approves wording)

**Why:** all three pages use the same four-card formula, with an identical
first title ("You've plateaued and can't see a way out"). Anyone who
opens two pages sees the template.

**Where:** each page's `<section class="sec" id="who">`, the `<h3>` of each
card **and** the card's `data-prefill-en` / `data-prefill-ru` (that's the
message the visitor sends when they tap the card, so it must match the new
title).

**Do:** replace the titles with these drafts once Igor approves them.
Keep the paragraphs under them.

| Page | Card | New title (EN) | New title (RU, draft) |
|---|---|---|---|
| English | 1 | Years of lessons, and you still sound the same | Годы занятий, а звучите так же |
| English | 2 | You rehearse every sentence before the call | Вы проговариваете каждую фразу перед созвоном |
| English | 3 | You read everything and say very little | Читаете всё, а говорите мало |
| English | 4 | You switch to Russian when it gets hard | Становится трудно — и вы переходите на русский |
| Chess | 1 | Hundreds of games, and the rating won't move | Сотни партий, а рейтинг стоит |
| Chess | 2 | *(keep)* You see it in analysis, not over the board | *(keep)* |
| Chess | 3 | Your openings are ahead of your endgames | Дебюты сильнее эндшпиля |
| Chess | 4 | You trade down the moment it gets sharp | В острой позиции вы сразу идёте на размены |
| Chess | 5 | *(keep)* You're looking for a coach for your child | *(keep)* |
| Climbing | 1 | Seasons in the gym, and the same grade | Сезоны в зале, а категория та же |
| Climbing | 2 | *(keep)* You know the crux, but your body doesn't do it | *(keep)* |
| Climbing | 3 | Strong fingers, lazy feet | Сильные пальцы, ленивые ноги |
| Climbing | 4 | You grab the draw when it gets scary | Становится страшно — и вы хватаетесь за оттяжку |

### B6. "Rehab principles" on the English and chess pages · S · waits (Q4)

**Why:** "I combine neuroscience, rehab principles and the psychology of
learning" is never explained outside climbing.

**Do:** when Igor gives his story (Q4), add one sentence that explains it,
in the method intro of each page. If he'd rather not, remove "rehab
principles" from the English and chess pages only. Until then, leave it.

---

## Category C: Things that look unfinished

### C1. Merge the hero portrait [FT2, done ahead] · S · waits (Igor's go)

`feature/ft2-hero-portrait` (`88b2e40`) puts Igor's photo next to the home
headline. It's built, tested (342 passed + 1 known xfail) and shown to
Igor. Rebase on `main` if needed, run the tests, merge when Igor says so,
republish the artifact. Every later home-page step builds on it.

### C2. "See me at work" gets its photos [FT1.1] · M

**Why:** on the live home page this is a heading, an arrow and empty space.
It's the most unfinished-looking spot on the site.

**Where:** `index.html`, `<div class="proof reveal">` (search for
`See me at work`), and `.proof` in `style.css`.

**Do:**
1. Inside the existing `<a class="proof__link">`, under the text and arrow,
   add a row of five real photos from `assets/collage/`:
   `en-03-club`, `chess-02-clock`, `climb-07-coaching`,
   `chess-09-cascade`, `climb-01-board`. Use
   `srcset="…jpg 450w, …@2x.jpg 900w"`, `loading="lazy"`, `alt=""` (the link
   text already names it).
2. Same crop for all five (`aspect-ratio: 4/5; object-fit: cover`),
   grayscale through the existing `--collage-filter` token, 1px hairline gap
   or the page's gutter, no borders, no rounding.
3. At 900px and up: five in a row. Below 900px: three in a row, hide the
   last two. Never scroll sideways.
4. The whole strip stays one link to the gallery (`#collage`). Use the
   existing reveal only.

**Keep:** the gallery itself (don't touch the collage grid; its ratio rule
is a separate open question for Igor), the name story and rune stone below.

**Done when:** the band reads as a finished section at 375px and 1280px, in
both themes; clicking anywhere on it opens the gallery; tests in
`tests/test_collage*.py` still pass.

### C3. Session photo rows fill the width [FT1.2] · S

**Why:** on all three discipline pages the two photos under "How sessions
run" leave the left third empty.

**Where:** each discipline page's `<section class="sec" id="sessions">`, and
the matching rule in `style.css`.

**Do:** make the two photos split the full content width equally (two
columns, the page's gutter between). Captions stay under each photo. Same
change on all three pages.

### C4. One meaning per icon [FT1.3] · M

**Why:** the book / board / carabiner icons open photo groups on home but
discipline pages elsewhere.

**Do:** the three icons always mean the disciplines (go to `/english/`,
`/chess/`, `/climbing/`, the current one underlined). "Photos" becomes a
plain text link to the gallery. Update the caption, aria-labels (both
languages) and `tests/test_collage_nav_icons.py` deliberately. All four
pages.

### C5. Phone masthead in two rows, not three [FT1.4] · M

**Why:** at 375px the bar takes about 170px before the hero starts.

**Do:** get it to two rows **without** shrinking any touch target below
44px (the J4 rule; read the long comment about it in `style.css` first).
If it can't be done without breaking J4, stop and report; don't trade
the touch targets away. All four pages.

### C6. Six reviews, not seven [FT1.5] · S · waits (Igor picks)

The seventh card sits alone on its own row. Igor chooses which to drop
(the council's suggestion: the one ending "…has a unique teaching
approach"). Home and English pages.

### C7. Dark mode follows the phone [FT1.6] · M

**Why:** Igor decided (2026-09-29, confirmed 2026-11-20) that the site
opens in charcoal when the phone or computer is in dark mode, until the
reader picks a theme themselves.

**Where the work is:** uncommitted changes in the **main checkout**
(`/Users/igor/Downloads/Vitnyr/site-v2`), on branch
`feature/theme-follows-system`, based on an old `main` (`b0bc550`). Four
files: `theme.js`, `style.css`, `tests/conftest.py`, `tests/test_theme.py`.

**Do:**
1. Save that work without losing it: in the main checkout, run
   `git diff > <scratchpad>/theme-follows-system.patch`. Don't stash, reset
   or discard anything there.
2. In the stage branch (off current `main`), apply it:
   `git apply --3way <scratchpad>/theme-follows-system.patch`. Resolve
   conflicts by hand: `main` has gained three pages since then.
3. What it must do: with no stored choice, `theme.js` stamps
   `data-theme="dark"` when `prefers-color-scheme: dark` matches, otherwise
   `light`. It follows the OS live if it changes while the page is open. A
   choice made with the theme button is stored and always wins.
4. Check `<meta name="theme-color">` on all four pages and `404.html`.
5. Run `tests/test_theme.py` first, then the full suite.

**Keep:** the theme button, the two colour pairs exactly as they are.

**Done when:** a fresh visitor (empty storage) with a dark OS gets
charcoal, with a light OS gets cream, with no flash of the wrong theme; a
clicked choice survives reloads and page changes. Tell Igor the old branch
can be deleted; don't delete it yourself.

---

## Category D: First impression

### D1. The home headline [FT2.3] · S · waits (Igor picks A, B, C or keep)

**Drafts.** All keep the three disciplines; the third line stays the links.

| | English | Russian |
|---|---|---|
| **A** (council's pick) | Every plateau / is a habit. / *English, chess, climbing.* | Каждое плато — / это привычка. / *Английский, шахматы, скалолазание.* |
| **B** | Stuck at the / same level? / *English, chess, climbing.* | Застряли на / одном уровне? / *…* |
| **C** | Past the / plateau. / *English, chess, climbing.* | Сдвинуться / с мёртвой точки. / *…* |
| keep | Skill acquisition, / coached. / *…* | Коучинг / по навыкам. / *…* |

A says the site's whole argument in five words and matches the climbing
page. B is the safest for getting messages. C reads most like a poster. If
Igor keeps the current English, the Russian should still change: "коучинг"
reads like the online-course business in Russian, and it's the only place
the site uses it.

**Where:** `index.html`, `<h1 class="hero__title">`, the
`<span class="line"><span class="line__inner">` lines (search for
`Skill acquisition` and `Коучинг`).

**Do:** replace only the text inside the first two `line__inner` spans,
in both language blocks. One line per span: the entrance animation masks
each line, so a line that wraps gets clipped. Update the page `<title>` and
meta description only if Igor asks.

**Done when:** `tests/test_layout.py::test_hero_title_lines_fit_beside_the_portrait`
(added with C1) passes (it checks every line stays on one row at 900, 1280 and 1920 in both
languages), and the entrance looks right at 375px. If a Russian line wraps,
check the `.46em` Russian rule in `style.css` before changing any size.

### D2. The home page becomes a doorway [FT2.2] · M–L · show Igor before merging

**Why:** home is about 8,100px tall and repeats the discipline pages: the
5 principles × 3 disciplines section appears again on each discipline page.
Visitors have to scroll past it to choose a discipline. Home's job is to
show who Igor is and send each visitor to the right page.

**New order:**
1. Hero (headline + portrait) — unchanged.
2. **01 Three disciplines**: the Y-mark chooser (`#origin`), moved up,
   with "See me at work" (C2) and the name story where they are now.
3. Reviews (`#voices`), unchanged.
4. **02 The method**, shortened (below).
5. **03 How to start** (`#contact`), unchanged.

**Do:**
1. Move the whole `<section … id="origin">` so it comes straight after the
   hero. Move `#voices` after it.
2. Shorten `#method` on home only: keep the heading, the two intro
   paragraphs and the chain plate. Replace `<ol class="mechanisms">` (the five
   accordions) with a quiet numbered list of the five names (Feedback loops,
   Pattern recognition, Load management, Retrieval, Interleaving), set like
   the current row headings but not clickable, then one line: "Each
   discipline page shows all five at work: English · Chess · Climbing",
   linking to `/english/#method`, `/chess/#method`, `/climbing/#method`.
   Russian twin for everything.
3. Renumber the section labels and the masthead's section links (01 Three
   disciplines, 02 The method, 03 How to start), both languages.
4. The accordion code in `main.js` and its CSS stay: the discipline pages
   still use them.
5. Tests that check the old numbering (for example
   `tests/test_content.py` asserts `#origin .label .num` is `02`) change
   deliberately; say which in the commit message.

**Keep:** every element, just in a new order; the chain plate; all
discipline pages untouched.

**Done when:** before/after full-page screenshots (both languages, both
widths) are shown to Igor and he approves. This is the only step that
changes the home page's shape.

### D3. About block [FT2.1] · M · waits (Q4)

Three true sentences from Igor (why these three disciplines; whether rehab
is part of his own story), with the Vitnyr name story moved in next to
them. The portrait is already in the hero, so the About block has no second
photo. It sits right after the discipline chooser. Until Q4 is answered,
nothing moves.

### D4. Bigger photos on the discipline pages [FT2.4] · M

**Why:** the hero photo on each discipline page is about 330px wide; it's
the most personal thing on the page and reads as a thumbnail.

**Do:** at 900px and up, the photo takes roughly half the content width.
The "Book a free trial" button must stay above the fold at 1280×800. Keep
the grayscale filter; drop or soften the 1px frame. Same change on all
three pages. Below 900px, the current layout stays.

---

## Category E: Trust and the last step

### E1. "What happens next" strip [FT3.1] · S

In the contact section of all four pages: three steps, no prices —
**Message me → 30-minute trial → we agree on a plan.** Hairline rows in
the page's own label style (like the FORMAT / WHERE / TRIAL LESSON row on
the discipline pages). Russian twin.

### E2. Lichess link next to the rating [FT3.4] · S · check first

**Why:** 2100 is a real number; let people check it.

**First:** open `https://lichess.org/@/yngvibrychenka` and note which rating
pool shows about 2100. If none does (for example blitz says 2350 or 1950),
stop and ask Igor: a link that shows a different number raises a question
instead of answering one. The site states the rating without "FIDE"; keep it
that way.

**Do:** on `chess/index.html`, make "2100 · my rating" (hero stat) a link
to that profile, opening in a new tab, with the same hairline-underline
style as other text links. Add the profile to the `Person` JSON-LD
`sameAs` list on the chess page (create the list if it isn't there).

### E3. A first step smaller than a lesson [new] · S · waits (Igor's yes)

**Why:** "book a lesson" is a big ask from a stranger. A smaller one, done
in Telegram where this audience already lives, is also a real diagnosis.

**Do (after Igor says yes to each):** one extra line under the contact
heading on each discipline page, with its own prefilled Telegram message:
- English: "Not ready for a lesson? Send me a 60-second voice message in
  English about your work. I'll reply with the one habit I hear."
- Chess: "Or send me your Lichess username and one game you lost from a
  winning position."
- Climbing: "Or send me a clip of your project. I'll tell you the habit
  that's costing you the send."

Russian twins, written with Igor. Home keeps its single offer.

### E4. Reviews you can check [new] · S · waits (Igor's yes + links)

1. Each reviewer's name links to their LinkedIn profile (their
   recommendation is already public there). Igor supplies the URLs and
   confirms it's fine.
2. In each quote, mark the outcome phrase with the site's existing
   `<strong class="mark">` (the same marking the rest of the site uses), for
   example "a confident B2+ level", "mock interviews", "maximum practice
   without fluff". The reviewer's own words only, nothing added. No new
   component, no pull quotes.

Home and English pages.

### E5. Proof for the other numbers [new] · S · waits (Igor's material)

- **IELTS 9:** a photo of the certificate with personal details blurred,
  shown small next to "C2 · IELTS 9" on the English page.
- **7C Kilter:** a short send video or a logbook screenshot on the climbing
  page.

Only real files from Igor. Grayscale like the other photos.

### E6. FAQ per discipline [FT3.5] · M · waits (Q7)

4–5 questions each from Igor's answers, as native `<details>` rows in the
page's hairline style, plus `FAQPage` JSON-LD. Both languages.

### E7. Handles [FT3.6] · S · waits (Q6, answered "not yet")

Only if Igor moves Telegram/Instagram to `vitnyrcoach`. Then: everywhere,
JSON-LD, tests.

---

## Category F: Signature pieces (the things people remember)

All four are **new blocks added next to what exists**. None replaces a
working part. Each works in both languages, both themes, both widths, and
with reduced motion; with JavaScript off it is simply hidden (gate it under
`html.js`), so the page stays complete without it. No new colours: amber
marks the mistake, green the correct form, exactly as the specimens do.

### F1. English: "Test your ear" [new] · M · waits (Igor approves the sentences)

**Why:** the site's best idea is "a mistake you can name is a mistake you
can train". This lets the reader find their own.

**Where:** `english/index.html`, a new **unnumbered** section between
`#specimen` and `#method` (unnumbered so the 01–05 numbering and the
masthead links stay as they are). It must sit outside `#specimen`: a test
forbids digits in that section's text, and this block shows a score.

**How it works:**
1. Heading: "Which of these would a native speaker say?" (RU: "Какие из
   этих фраз сказал бы носитель?"). Eight sentences, each a button
   (`aria-pressed`) set in JetBrains Mono like the specimens. The reader taps
   the ones that sound right.
2. A "Check my ear" button. Each sentence then shows: right ones in green;
   wrong ones with the mistake struck through in amber and the correct form
   in green beside it, the same visual as the specimens.
3. Result line: "You judged 6 of 8 correctly." plus one line naming the
   habit behind the misses.
4. A Telegram link prefilled with the score: "Hi! I took the test on your
   site: 6/8. I'd like a free trial English lesson." (RU version on the RU
   page.) Nothing is stored or sent anywhere else.

**Draft sentences (Igor approves or replaces):**

| # | Sentence | Right? | Correct form | Habit |
|---|---|---|---|---|
| 1 | I am agree with you. | no | I agree with you. | adjective where English has a verb |
| 2 | I feel myself good today. | no | I feel good today. | reflexive carried across |
| 3 | I live in Yerevan since 2022. | no | I've lived in Yerevan since 2022. | tense from Russian |
| 4 | I went to the office yesterday. | yes | — | (control) |
| 5 | Can you explain me this? | no | Can you explain this to me? | word order from Russian |
| 6 | We discussed about the plan. | no | We discussed the plan. | preposition carried across |
| 7 | I've been working here for two years. | yes | — | (control) |
| 8 | She gave me a good advice. | no | She gave me some good advice. | articles |

**Tests to add:** the section exists on `/english/` only; buttons toggle
`aria-pressed`; "Check" reveals results; the Telegram link carries the
score; it works after switching to RU; hidden without JS; no sideways
scroll at 375px.

### F2. Chess: "Is your rating actually stuck?" [new] · M–L

**Why:** the chess headline says "Your rating has stalled". This shows the
visitor their own curve.

**Where:** `chess/index.html`, a new unnumbered section between
`#specimen` and `#method`.

**How it works:**
1. A text field "Your Lichess username" (`autocomplete="off"`,
   `spellcheck="false"`, letters, digits, `_` and `-`, 2–30 characters) and a
   button "Show my rating". One small line under it: "Your username goes
   from your browser straight to Lichess. Nothing is stored here."
2. On click, fetch
   `https://lichess.org/api/user/<username>/rating-history`. Lichess allows
   this from any website (checked 2026-11-20: it answers with
   `access-control-allow-origin: *`). The answer is a list of rating pools,
   each `{ name, points: [[year, month (0-based), day, rating], …] }`.
3. Pick the pool (Bullet, Blitz, Rapid or Classical) with the most points in
   the last 12 months. Draw it as an inline SVG line in the engraved style:
   1px `currentColor` line, hairline axes in `--rule`, small labels in mono.
   Mark the last 12 months' lowest-to-highest range with an amber bracket
   (ink, not text).
4. Say only what the data says: "Last 12 months, Blitz: between 1610 and
   1700." If the range is 120 points or less, add: "That's a plateau. It's
   usually the same few patterns." Otherwise: "Still moving. Let's keep it
   that way."
5. A Telegram link prefilled: "Hi! My Lichess is <username>. I'd like a
   free trial chess lesson." (RU on the RU page.)
6. Errors, in plain words: user not found (404) → "Lichess doesn't know that
   username."; too many requests (429) → "Lichess asks to wait a minute. Try
   again shortly."; no rated games in a year → say so; network failure →
   "Couldn't reach Lichess."
7. With motion allowed, the line draws in once using the brand easing
   (add the duration to the `D` table in `main.js`). With reduced motion, it
   appears at once.

**Tests to add:** use Playwright's `page.route` to fake the Lichess answer
(tests must never call the real Lichess): a flat curve, a rising curve,
404, 429. Check the text, the bracket, the prefilled link, RU, and no
sideways scroll at 375px.

### F3. Chess positions you can step through [FT4.1] · L · waits (Q8)

Each of the three chess mistakes gets a real board from Igor's games:
the position, then "what was played" (amber), then "what to play" (green),
one step per click or key. SVG in the engraved style, no chess library.
Static fallback without JS, reduced-motion support. Sits beside the current
sentence; doesn't replace the specimen until Igor sees both.

### F4. The Russian behind the mistake [FT4.2] · S–M

On the English page in English only: under each mistake, the Russian
original sits faintly ("Я согласен" under "I am agree"), so the reader sees
where the error comes from. Typography only: `--fg2`, smaller size, no new
colour. The Russian page doesn't need it. No digits (the `#specimen` test).

---

## Category G: Speed and code health (invisible to visitors)

Every step here must leave the pages **pixel-identical**. Before and after
each step, take screenshots of all four pages in both languages at 375px
and 1280px and compare them; any difference means stop.

### G1. A test that catches drift between the four pages [new] · S

**Why:** the four pages share no template; the risk is one page quietly
falling behind.

**Do:** in `tests/test_seams.py`, add a test that reads the four HTML files,
takes the footer block (`<footer` … `</footer>`), removes `href` and
`data-href-*` attribute values, collapses whitespace, and asserts the four
are identical. If the pages legitimately differ somewhere, list that
difference in the test with a comment saying why. Later, do the same for
the masthead.

### G2. Ship the code without its comments [new] · S

**Why:** about 59% of `style.css` (104 KB) and about half of `main.js` are
comments. They are valuable in the repo and useless to visitors.

**Do:** in `build.sh` (Cloudflare runs it on every deploy), after the
files are copied into `dist/`, minify the copies only:
`npx --yes esbuild@0.24.0 dist/style.css --minify --allow-overwrite --outfile=dist/style.css`,
and the same for `dist/main.js` and `dist/theme.js`. Source files keep
every comment. Pin the version.

**Done when:** a local `sh build.sh`, served from `dist/`, gives
pixel-identical screenshots to the source, with no console errors; after
deploying, the live site still passes a quick look on phone and desktop.

### G3. Host GSAP and Lenis ourselves [new] · S

Download the exact files the pages use now (GSAP 3.12.5, CustomEase
3.12.5, Lenis 1.1.14) into `assets/vendor/`, **with the version in the
filename** (e.g. `gsap-3.12.5.min.js`; `/assets/*` is cached forever, so a
new version must get a new name). Point the `<script>` tags on all four
pages at them, same order. Remove the now-unused preconnects.

### G4. Host the fonts ourselves [new] · M

Download the woff2 files Google serves now for Inter (400, 500),
Lora (the weights and italics in use), JetBrains Mono (400) and Marck
Script, **Latin and Cyrillic subsets** (Russian pages need Cyrillic), into
`assets/fonts/` with versioned names. Write `@font-face` rules with the same
`unicode-range` values and `font-display` that Google's CSS uses now.
Remove the Google Fonts `<link>`s and preconnects on all four pages and
`404.html`. The wordmark waits for Lora (`lora-ready`); check it still
appears in both languages.

**Done when:** pixel-identical screenshots, and the network panel shows no
requests to `fonts.googleapis.com` or `fonts.gstatic.com`.

### G5. Lighthouse pass [FT5.1] · M

Run Lighthouse (mobile) on all four pages; record the numbers in
`BUILD-NOTES.md`; fix what it flags. Likely: WebP/AVIF `<picture>` for the
photos (the undone half of the collage plan). Only if it flags HTML size:
try serving one engraving as a shared file (`<svg><use href="…#id">`) and
stop if any of its animation or theming breaks.

---

## Category H: Growth beyond the pages

### H1. Business profiles on maps [new] · Igor, off the site

Google Business Profile and Yandex Business for English, chess and
climbing coaching in Yerevan, linking to the matching page. Free, shows up
in map searches, and collects real reviews where people look for a coach.

### H2. Ask for chess and climbing reviews [Q9] · Igor, off the site

Ask the 30 chess students (or their parents) and the 13 climbers for one
honest sentence each, on LinkedIn or Google. When real ones come in, the
chess and climbing pages get their own review strip and the home strip
loses the "English students" label.

### H3. English club schedule [new] · S · waits (Igor)

If the English club runs on a fixed day, add one line to the English page's
"How sessions run": day, time, place, open to anyone. It's the
lowest-commitment way in, and it shows people actually come.

### H4. A library of mistakes [new] · L, ongoing · waits (Igor's texts; after G1)

**Why:** everything else converts people who already found the site. This
brings new ones: Russian speakers search for exactly these questions ("I am
agree или I agree").

**Do, once Igor approves the idea and the first text:** one short page per
mistake at `/notes/<slug>/` (e.g. `/notes/i-am-agree/`), in both languages
like the rest of the site: the mistake, why Russian speakers make it, how to
retrain it, three practice sentences, the trial offer. Same masthead and
footer as the other pages (G1's test covers them), added to `sitemap.xml`,
linked from its specimen. Igor's LinkedIn posts about English are the raw
material; nothing is published without his approval. Start with the three
specimens on the English page.

---

## Category I: Final polish

### I1. Accessibility and Safari [FT5.2] · M

Keyboard path through every new piece (footer links, photo strip, test,
rating check, boards), screen-reader names in both languages, an iOS Safari
check of the masthead, the curtain footer and the new blocks.

### I2. Jury pass [FT5.3] · S

Full-page screenshots of all four pages in both themes, both languages and
both widths. One short list of last nits, fixed in the same pass.

### I3. Docs and artifact [FT5.4] · S

Update `CLAUDE.md` (what changed in structure), `BUILD-NOTES.md` (what was
done, with dates and commits) and this file's status table. Republish the
artifact to the same URL.

---

## Questions for Igor

**Answered (2026-11-20):** Q2 finish dark mode · Q3 "available 24/7" is
true, keep it · Q5 Lichess `yngvibrychenka` · Q6 handles stay for now.

**Open:**

| # | Question | Unblocks |
|---|---|---|
| N1 | Merge the hero portrait? | C1 |
| N2 | Turn on Cloudflare Web Analytics (your click). | A1 |
| N3 | Headline: A, B, C, or keep? | D1 |
| N4 | OK with the chess hero line (B1) and the card titles (B5)? | B1, B5 |
| N5 | Which review to drop? | C6 |
| N6 | Yes or no to each smaller first step: voice message, game + username, climbing clip? | E3 |
| N7 | Link each reviewer to their LinkedIn? Send the URLs. | E4 |
| N8 | Photo of the IELTS certificate (details blurred)? Kilter send video or logbook? | E5 |
| N9 | Approve or replace the eight test sentences. | F1 |
| N10 | Does the English club run on a fixed day? | H3 |
| N11 | Start the mistake library? Which LinkedIn posts can it use? | H4 |
| Q4 | Your story: three true sentences, or skip. | B6, D3 |
| Q7 | FAQ answers per discipline. | E6 |
| Q8 | Two or three chess positions (PGN or Lichess link). | F3 |
| Q9 | Real chess and climbing reviews, whenever they come. | H2 |

---

## Not doing (the council threw these out)

- **An AI chat assistant.** The product is Igor; a bot in his place
  undercuts it.
- **A booking calendar.** It adds a step; this audience would rather just
  message.
- **A general blog.** Only the mistake library (H4), tied to real mistakes.
- **An Armenian version.** Igor coaches in English and Russian; it would
  bring leads he can't serve.
- **Video backgrounds or more motion.** They fight the quiet, engraved look.
- **A climbing self-quiz.** Self-reported answers say little; a clip (E3)
  says more.
- **Replacing the specimens' "Show the common mistake" toggle.** The test
  (F1) sits beside it instead.
- **Invented chess or climbing reviews.** Never.

## Decided later (not part of this plan)

- **A template build** (pages assembled from shared parts). It would end
  the four-page rule, but it changes how the site is previewed and tested
  and how the artifact is built. It needs its own plan and Igor's yes. G1's
  drift test covers the risk until then.
- **Real `/ru/` URLs** instead of `?lang=ru`. Better for Yandex, but it
  touches the edge rewrite, hreflang, the sitemap and every test. After the
  template build, if ever.
- **Prices, a third colour, splitting the brand:** settled with Igor; not
  reopened.

## Status

| Stage | Status |
|---|---|
| 1. Clean up | open; C1 waits for N1, A1 for N2 |
| 2. Finish the frame | open |
| 3. First impression | D1 waits for N3; D2 and D4 can start after stage 1 |
| 4. Signature | F2 and F4 can start; F1 waits for N9; F3 waits for Q8 |
| 5. Speed | open |
| 6. Polish and jury | runs last |
