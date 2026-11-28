# Site plan: what's left

**Updated:** 2026-11-21. The full plan (2026-11-20, commit `6ea7a0a`) merged
the finishing-touches list with a council review; every step that was done is
recorded in `BUILD-NOTES.md` and has been cut from here, along with the
finished work orders (Jury Pass II, Design Pass III, the Trifecta orders,
the discipline-pages and notes plans). They are all in git history.

**What this is:** the open steps, each with why, where and what to do, and
the questions only Igor can answer. Follow a step literally; if it doesn't
match what you find in the code, stop and ask instead of improvising.

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

## Open steps

### B6. "Rehab principles" on the English and chess pages · S · waits (Q4)

**Why:** "I combine neuroscience, rehab principles and the psychology of
learning" is never explained outside climbing.

**Do:** when Igor gives his story (Q4), add one sentence that explains it,
in the method intro of each page. If he'd rather not, remove "rehab
principles" from the English and chess pages only. Until then, leave it.

### D3. About block [FT2.1] · M · waits (Q4)

Three true sentences from Igor (why these three disciplines; whether rehab
is part of his own story), with the Vitnyr name story moved in next to
them. The portrait is already in the hero, so the About block has no second
photo. It sits right after the discipline chooser. Until Q4 is answered,
nothing moves.

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

**Held (2026-11-20):** needs Igor's URLs. Also, `.mark` is invisible
inside the quotes (they are already `--fg` at weight 500), so how to mark
the outcome phrase needs a decision first.

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

### F3. Chess positions you can step through [FT4.1] · L · waits (Q8)

Each of the three chess mistakes gets a real board from Igor's games:
the position, then "what was played" (amber), then "what to play" (green),
one step per click or key. SVG in the engraved style, no chess library.
Static fallback without JS, reduced-motion support. Sits beside the current
sentence; doesn't replace the specimen until Igor sees both.

### G5. Lighthouse pass [FT5.1] · M

Run Lighthouse (mobile) on all four pages; record the numbers in
`BUILD-NOTES.md`; fix what it flags. Likely: WebP/AVIF `<picture>` for the
photos (the undone half of the collage plan). Only if it flags HTML size:
try serving one engraving as a shared file (`<svg><use href="…#id">`) and
stop if any of its animation or theming breaks.

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
contact text: day, time, place, open to anyone. It's the
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

**Status (2026-11-28):** nine notes. The newest, manage
(`feature/note-manage`, waiting for Igor's review), is a vocabulary note
from his post of 1 October (manage to, not could). Before it, weigh, a
grammar note from his one English-language post. Before it: API key (pronunciation), serial
and actual (vocabulary). The eight LinkedIn posts read on 2026-11-28 are in
`reference/linkedin-posts/` with `REVIEW.md`; of those left, install is
thin (fold into a stress note), dev/deaf needs Igor's word list, redact is
thin. The open questions are NQ below.

### I1. Accessibility and Safari [FT5.2] · M

Keyboard path through every new piece (footer links, photo strip, test,
boards), screen-reader names in both languages, an iOS Safari
check of the masthead, the curtain footer and the new blocks.

### I2. Jury pass [FT5.3] · S

Full-page screenshots of all four pages in both themes, both languages and
both widths. One short list of last nits, fixed in the same pass.

#### Adding the next note (checklist)

The notes are generated; never edit `notes/**/index.html` by hand.

1. Copy a note module in `tools/notes/` (`au.py` for a word list,
   `noun_verb_stress.py` for pairs) to `tools/notes/<name>.py` and fill in
   its `NOTE` (both languages) and `body()`.
2. Add `<name>` at the front of `ORDER` in `tools/notes/build.py`.
3. `python3 tools/notes/build.py`. This writes the page, the ledger row and
   JSON-LD, every pager, the sitemap entries and the share card's text.
4. `tests/.venv/bin/python tools/notes/export_cards.py` writes the two
   share-card PNGs.
5. Run `tests/test_notes.py`, then the full suite.
6. On LinkedIn: link the note in the first comment, with `?lang=ru` for a
   Russian post.

If `english/index.html`'s masthead, contact section or footer change,
re-run step 3; `test_the_notes_are_up_to_date_with_their_generator` fails
until you do.

---

## Questions for Igor

| # | Question | For |
|---|---|---|
| N7 | Link each reviewer to their LinkedIn? Send the URLs. | E4 |
| N8 | Photo of the IELTS certificate (details blurred)? Kilter send video or logbook? | E5 |
| N10 | Does the English club run on a fixed day? | H3 |
| Q4 | Your story: three true sentences, or skip. | B6, D3 |
| Q7 | FAQ answers per discipline. | E6 |
| Q8 | Two or three chess positions (PGN or Lichess link). | F3 |
| Q9 | Real chess and climbing reviews, whenever they come. | H2 |
| NQ1 | The original carousel files (PDF or PNG), including the two slides hidden behind "+2"? Until then the "по-русски" column is left out. | H4 |
| NQ3 | Approve or replace the practice sentences written for the notes (au i–vi, feel ii–vi, could-you ii–vi; rewritten 2026-11-27 to lean less on IT, marked draft in `tools/notes/*.py`). | H4 |
| NQ11 | A plain hint for /ɔː/ on the au note, for readers who can't read IPA: anchor it to a Russian sound (a long, rounded «о») or to English words (*law*, *saw*)? Your call as the teacher. Its place is ready: the line under "Six words. One sound in every one." (`tools/notes/au.py`). | H4 |
| NQ4 | Approve the English translations of the two posts (marked draft in the source). | H4 |
| NQ5 | Links to the posts themselves? Until then "First on LinkedIn" links to your activity page (`tools/notes/lib.py`). | H4 |
| NQ6 | The exact date of the stress post (LinkedIn said "2w" on 2026-11-20)? Shown as "November 2026". | H4 |
| NQ7 | `conSOLE` as a verb means "to comfort". Keep it, or swap in a pair IT people use (`REcord / reCORD`, `UPdate / upDATE`)? | H4 |
| NQ8 | Recordings of the words and sentences (what to record: `tools/notes/RECORDINGS.md`). | H4 |
| NQ9 | The "I am agree" note is parked on `feature/notes-agree`: publish it, or leave it? | H4 |
| NQ13 | The actual note (`tools/notes/actual.py`): approve the English translation of the post, the four table rows after the carousel's four (meeting still on, offer still valid, a hot topic, the current exchange rate), the "why" lede (German *aktuell*, French *actuel*), and two test sentences (the offer, *Actually, I meant Tuesday*). All marked DRAFT. | H4 |
| NQ14 | The serial note (`tools/notes/serial.py`): approve the English translation of the post, the table rows not in the post (my favourite show, a new series on Netflix, the second season), the "why" wording, and the test sentences around the post's own phrases. All marked DRAFT. | H4 |
| NQ15 | The API key note (`tools/notes/api_key.py`): approve the English translation of the two posts, the RAM/PIN footnote, the "why" (Latin letter names from maths class; key read like hey), the stress tip (эй-пи-АЙ) and the six practice sentences. All marked DRAFT. | H4 |
| NQ16 | The weigh note (`tools/notes/weigh.py`): the post is in English, so approve the Russian translation; also the table rows beyond the post's two, the weighted-average row and footnote, the "why" (weight comes from weigh; the email/text rows) and the test sentences. All marked DRAFT. | H4 |
| NQ17 | The notes copy pass (2026-11-28, `reference/notes-copy-review.md`): approve the rewritten Russian lines (feel, could-you, api-key, weigh, stress), the new footnotes (serial in British English, feel myself, weight as a verb, au exceptions), conSOLE swapped for REcord/reCORD (closes Q7), and the eight new contact openers. The five shared footer/byline lines (section E) were fixed on `feature/shared-copy-fixes`. | H4 |
| NQ18 | The manage note (`tools/notes/manage.py`, `feature/note-manage`): approve the English translation of the post; the specimen (the post names the gap, the note names *could* as what fills it); the four table rows not in the post (еле успел, как вы справляетесь, сможете в пятницу, не удалось дозвониться); the why (мог is could, смог is managed to); and the five test sentences beyond your slide 2. Slide 2 promised answers in the first comment that were never posted; the test now carries them. All marked DRAFT. | H4 |
| NQ10 | The English page calls the Russian in "I feel myself" a "reflexive ending built into the verb", but чувствую себя uses a separate word (себя). Change it to "reflexive word", as the note says? | H4 |

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
