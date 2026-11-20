# Notes: Igor's LinkedIn posts on the site

**Date:** 2026-11-20. **Branch:** `feature/notes` (worktree
`.claude/worktrees/notes`), cut from `main` at `c3aee7e`. Built apart from
`feature/s1-clean-up` (SITE-PLAN.md, in progress in another chat) and
`feature/theme-follows-system` (uncommitted, main checkout), so neither is
touched.

**Next steps live in `NOTES-COUNCIL.md`** (2026-11-20, after SITE-PLAN
stages 1–5 reached `main`): the council review of the notes and the site,
cut down to what's worth doing, with its running order. Read it before
changing the notes.

**Igor's ask:** a page that keeps his LinkedIn posts on the website, to
bring in more readers, in the same design, vibe and aesthetics.

**Where this sits in the existing plans.** SITE-PLAN.md (unmerged) already
has this as **H4, "A library of mistakes"**: one short page per mistake at
`/notes/<slug>/`, sourced from Igor's LinkedIn posts, nothing published
without his approval. Its open question **N11** ("Start the mistake
library? Which LinkedIn posts can it use?") is answered by this request:
yes, starting with the two posts Igor sent (the `au` sound, 19 Nov; noun
and verb stress, early Nov). The council's "Not doing: a general blog"
still stands, and this plan keeps to it: every note is one real mistake.

---

## 1. The brief, restated by each seat at the table

**Marketer.** "More viewers" means two flows, and the page has to serve
both:

1. *LinkedIn → site.* The post is the trailer; the note is the full cut.
   Igor drops the note's link in the first comment (LinkedIn buries posts
   with outbound links in the body). The note has to give more than the
   post: the full word list, the reason, sentences to practise, and a
   one-tap way to book. The link preview *is* the ad, so every note needs
   its own share card.
2. *Search → site.* Russian speakers search the exact question: "как
   произносится launch", "ударение project", "PROject или proJECT". One URL
   per note, each with its own Russian title and description, is what can
   rank. An embedded LinkedIn feed ranks for nothing.

And a third, quieter one: *site visitor → trust.* Someone weighing a trial
lesson sees that this coach can name their exact mistake. The notes are
proof of method that no review can give.

**Designer.** Igor's carousels already speak the site's language: cream and
charcoal, amber for the wrong letters, green for the right sound, an
engraved "Таблица IX", the Y mark in the corner. So the page shouldn't
*show* his posts, it should *set* them, the way the site sets its
specimens: hairline rules, the serif for the idea, mono for the language
under examination, amber where it breaks, green where it's fixed. The
index reads like a page of corrected proofs: every row carries its own
tiny correction (`l~~au~~nch → lɔːntʃ`).

**Developer.** Static, hand-written, no build step, no framework, the
four-page rule (masthead and footer copied by hand). The live site deploys
through `build.sh`, which copies an explicit list of folders, and the edge
middleware already rewrites `?lang=ru` heads for any path. No new JS should
be needed: the hero line-mask, `.reveal`, the dock and the section nav all
work on any page that carries the right ids.

**Copywriter.** The posts are Russian; the Russian on the site stays
Igor's, lightly cleaned (из-за, и т. д., всё). The English is a translation
in his voice, marked as a draft for him. Titles come from his own
carousels ("Две буквы — один звук.", "О весе ударения").

---

## 2. Plan v1 (the ambitious draft)

- `/notes/` index: a featured "latest post" card with the carousel cover,
  then a card grid of every post; filter chips (Pronunciation, Stress,
  Grammar, Register) and a search box.
- Each note: the LinkedIn carousel images in a scroll-snap slider, the post
  text below, a "Hear it" button (browser text-to-speech) beside every word,
  a "tap the stressed syllable" quiz, the post's reaction count as social
  proof, a newsletter sign-up.
- A "Notes" item in the masthead on all four pages.
- Automatic import of new posts from LinkedIn.

## 3. Cold eyes on v1

| # | v1 idea | What's wrong with it | Verdict |
|---|---|---|---|
| 1 | Card grid + featured card | The brand forbids cards: "structure is whitespace and hairline rules". A card grid also reads as a generic blog, which the council threw out. | **Out.** A typeset ledger of hairline rows. |
| 2 | Filters and search | Two notes. Filters on two items are theatre and an empty-state problem. | **Later**, at eight or more notes. |
| 3 | Carousel images in a slider | We don't have the source files (only LinkedIn screenshots). Images of text can't be indexed, can't switch language or theme, and weigh more than the whole page. | **Out.** Re-set the slides as live type: the tiles and the word list become HTML. Originals can come later as a download. |
| 4 | Text-to-speech "Hear it" | A robot voice on a pronunciation coach's page undercuts him. Web Speech can't be told where the stress goes, so on some voices it would say proJECT for the noun and contradict the lesson. | **Out.** Leave room for Igor's own recordings. |
| 5 | Stress quiz | SITE-PLAN F1 already plans a test for the English page. A second, different mechanism now would fork it. | **Later**, built on F1's mechanism. |
| 6 | Reaction count | Goes stale, can't be checked live, and "9" undersells. | **Out.** One "Discuss on LinkedIn" link. |
| 7 | Newsletter | No backend, and the council rejected extra steps. | **Out.** "Follow on LinkedIn" does the job. |
| 8 | Auto-import from LinkedIn | No public API for personal posts; scraping breaks LinkedIn's terms. | **Out.** Manual, with a checklist and a test that catches a half-added note. |
| 9 | Masthead item on all four pages | The phone masthead is the site's most fragile row (the coarse-pointer clipping bug), and all four pages are being edited in another chat right now. | **Later**, once `feature/s1-clean-up` is merged. v1 links in from the English page only. |
| 10 | One long page vs one page per note | One page means one title, one description, one share card: nothing for search to rank and nothing note-specific to preview. | **One page per note**, plus an index. |
| 11 | A page per note means copying the masthead and footer into three more files | Drift risk grows with every page. | **Accept for now**, add a drift test. A generator in `tools/` once there are six notes. |
| 12 | "95% of my IT clients" | The site only states confirmed numbers. | It is Igor's own published claim, so it stays in his words, **flagged for him** (Q2). |
| 13 | Kelly & Bock (1988): 94% / 69% | A citation published under Igor's name must be right. | **Checked:** *Stress in time*, JEP: Human Perception and Performance 14(3), 389–403; 94% of ~3,000 two-syllable nouns are stressed first, 69% of ~1,000 verbs second. Cited on the page. |
| 14 | Carousel's Russian column ("по-русски") | Unreadable in the screenshot. Guessing would put words in Igor's mouth. | **Left out** until Igor sends the source slides (Q1). |
| 15 | style.css conflicts with the other chat | Both branches edit style.css. | One block **appended at the end**. Only the new pages load the new `?v=` key; the old pages use none of the new selectors, so their heads stay untouched. |
| 16 | New motion | The council: "Video backgrounds or more motion fight the quiet, engraved look." | **None.** Only the existing hero line-mask and `.reveal`. The figures are still type. |

## 4. Plan v2 (what gets built)

### URLs

| Path | Page | H1 (EN / RU) |
|---|---|---|
| `/notes/` | Index | Notes / from the lessons. · Заметки / с занятий. |
| `/notes/au/` | The `au` sound | Two letters, / one sound. · Две буквы — / один звук. |
| `/notes/noun-verb-stress/` | Noun and verb stress | The weight / of stress. · О весе / ударения. |

### The index, `/notes/`

1. Masthead (copied). Sections: 01 Notes, 02 How to start, "message me".
2. Hero, text only: eyebrow, line-mask H1, one standfirst that says where
   the notes come from (lessons) and where they appear first (LinkedIn,
   linked), the trial CTA.
3. **§01 the ledger.** One hairline row per note, newest first. Each row:
   a mono meta line in Igor's own carousel formula ("AU · 6 words · 1
   sound"), the title in the serif, the note's correction in mono (amber
   for the mistake, green for the fix, the sanctioned
   `.mark--specimen` / `.mark--target` exception), the month, an arrow. The
   whole row is one link. Under the ledger: "New notes go up on LinkedIn
   first" with a follow link. No promised cadence.
4. **§02 contact** (copied from the English page; the dock needs
   `#contact`).
5. Footer and dock (copied).

### A note, `/notes/<slug>/`

1. Masthead. Sections: 01 Words, 02 Why, 03 Say it, 04 How to start.
2. **Hero:** eyebrow (Igor Shatsev / Notes / topic), the H1, the
   standfirst (the post's opening, in Igor's words), a source line
   ("First on LinkedIn · November 2026 ↗"), and a **typeset figure** in
   the photo slot:
   - `au`: two rows of hairline tiles, `L A U N C H` with A and U in amber,
     then `L ɔː N C H` with one green tile, Scrabble values in the corners,
     as on Igor's slide. Square corners, no shadow.
   - stress: the "weights": `PRO·ject` (noun, a thing) and `pro·JECT`
     (verb, an action), the stressed syllable set large in the serif and
     the other one small in grey, so the weight of the type *is* the stress.
     Caption from his cover: "Fig. 1. PROject is a thing. The weight is on
     the first syllable."
3. **§01 Words:** the correction as a `.line-spec` pair (wrong / right),
   then the word list as a real `<table>` (accessible, indexable).
4. **§02 Why:** the Russian pull, in Igor's words. `au`: автор, август,
   аура, аудио next to their English IPA. Stress: the two Kelly & Bock
   numbers as display figures, cited.
5. **§03 Say it out loud:** practice sentences. Stress: the two slide
   lists (things, actions) transcribed. `au`: six sentences, **drafted,
   for Igor to approve** (Q3).
6. Pager: all notes, previous / next.
7. **§04 contact:** the English contact section, its Telegram message
   naming the note ("I came from your note about the au sound…").
8. Footer and dock.

### Around the pages

- **Share cards:** `share-card.html` gains `page=notes`, `page=note-au`,
  `page=note-stress`; six PNGs exported at 1200×630 (EN and RU each),
  because the edge middleware swaps `.png` for `-ru.png` on `?lang=ru`.
- **Head:** own title, description, hreflang trio, og/twitter, JSON-LD
  (`CollectionPage` + `ItemList` for the index, `Article` with
  `author → #igor` for each note, `BreadcrumbList` everywhere). No static
  canonical, the same as every page (theme.js writes it).
- **sitemap.xml:** three pages × two languages.
- **build.sh:** copy `notes/` too. Without this the pages never deploy.
- **Entry point:** one line under the English page's specimens, "More
  mistakes, one at a time: notes from the lessons →". Its own commit, so
  it can be rebased on its own if `feature/s1-clean-up` lands first.
- **Tests:** `tests/test_notes.py`: every note folder is in the index, the
  sitemap and the build; own head in both languages; share cards served;
  masthead links match the English page's; clean at 375px in RU dark with
  no console errors and no overflow; readable with JS off. The sitemap test
  that counts "four pages" is updated on purpose.

## 5. Review of v2 (second cold read)

- **Is it a blog?** No: no dates as headlines, no feed, no categories; a
  ledger of mistakes, each a lesson. Passes the council's line.
- **The beauty check** (SITE-PLAN 0.3.6): no new colour (amber/green only
  on the mistake and the fix), no new shape (square tiles are hairline
  boxes, like the rules), no new font, no new motion. Page length: a note
  is about two screens before the contact block.
- **Does it duplicate the English page?** The English page's specimens are
  grammar (reflexive, copula, register); the notes so far are sound and
  stress. No overlap. When a note covers a specimen, the specimen links to
  it (H4).
- **Cost of the next note** (Igor's real constraint): copy a note folder,
  replace the copy, add a ledger row, a sitemap pair, two share cards. The
  test fails if any of those is missed. That's tolerable up to about six
  notes; then build the generator.
- **What could go wrong:** the RU/EN head for `?lang=ru` on a new path
  (middleware is path-generic, checked); a missing `-ru.png` breaking the
  RU preview (test); the dock never showing (needs `#contact`, present);
  a masthead section link with no target (each id exists, test).

## 6. Execution, step by step

1. Worktree and branch off `main`. ✔
2. This plan. ✔
3. `notes/au/index.html`: head, masthead, hero + tiles, §01–§03, pager,
   contact, footer, dock.
4. `notes/noun-verb-stress/index.html`: same skeleton, weights figure,
   stats.
5. `notes/index.html`: hero, ledger, contact.
6. style.css: one appended "notes" block.
7. Share cards: extend `share-card.html`, export six PNGs with Playwright.
8. sitemap.xml, build.sh.
9. `tests/test_notes.py`; update the sitemap count test.
10. Look: both themes, both languages, 375px and 1280px, reduced motion,
    JS off, console, overflow.
11. Entry link on the English page (own commit).
12. BUILD-NOTES.md entry. Commit on the branch. **No merge to `main` and no
    artifact republish without Igor's yes** (SITE-PLAN 0.3.7).

## 7. Adding the next note (checklist)

1. Copy `notes/au/` to `notes/<slug>/`. Replace the head (title,
   `data-head-ru`, description, og/twitter, hreflang, JSON-LD), the hero,
   §01–§03, the pager and the Telegram prefill (both languages).
2. Add the row at the top of the ledger in `notes/index.html`, and to its
   JSON-LD `ItemList`.
3. Fix the pager on the previous newest note.
4. Add the two `<url>` blocks to `sitemap.xml`.
5. Add `page=note-<slug>` to `share-card.html`, export `og-note-<slug>.png`
   and `og-note-<slug>-ru.png`.
6. Run `tests/test_notes.py`.
7. On LinkedIn: link the note in the first comment, with `?lang=ru` for a
   Russian post.

## 8. Questions for Igor

| # | Question | Default until answered |
|---|---|---|
| Q1 | Send the original carousel files (PDF or PNG), including the two slides hidden behind "+2"? | Slides re-set as type; the "по-русски" column left out. |
| Q2 | Keep "95% of my IT clients" on the site, or soften to "almost all"? | Kept, as you wrote it. |
| Q3 | Approve or replace the six `au` practice sentences (they're mine, not from your post). | Shown, marked draft in the source. |
| Q4 | Approve the English translations of both posts. | Shown, marked draft in the source. |
| Q5 | The links to the two posts themselves? | "First on LinkedIn" links to your profile's activity page. |
| Q6 | Exact date of the stress post (LinkedIn said "2w")? | "November 2026". |
| Q7 | `conSOLE` as a verb means "to comfort", not anything to do with a console. Keep it in the list, or swap in a pair IT people actually use (e.g. `REcord / reCORD`, `UPdate / upDATE`)? | Kept, as you wrote it. |
| Q8 | Record yourself saying the words (phone voice memo is enough)? Each note has room for it. | No audio. |
| Q9 | Merge to `main` and republish the artifact once you've looked? | Not merged. |
| Q10 | Add "Notes" to the masthead on all pages after the clean-up branch lands? | English page link only. |
