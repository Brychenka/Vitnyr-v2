# Discipline pages — plan

Branch: `feature/discipline-pages` (worktree `.claude/worktrees/discipline-pages`), cut from
`origin/main` at 3110e7b on 2026-10-31. Igor's brief, in his words: the home page is the hero,
then the method, then the interactive logo, centred, leading people to a page per
discipline; the words are re-cut as a native writer would, in English and Russian, so each
page carries the weight the old single page did.

This file is the work order. Each stage ends in a state that can be reviewed in a browser,
and Igor sees it before the next one starts.

---

## The rule that decides where every sentence goes

The old page wrote most blocks as one sentence per discipline, packed together (method
cards, "Which of these is you?", the §01 readout). The split:

| Layer | What it is | Where it lives |
|---|---|---|
| **Core** | The idea with no discipline in it ("A mistake is easiest to fix the second you make it.") | Home, and the top of the matching block on every discipline page |
| **Discipline** | The example, the specimen, the number, the format | Only on its own page |
| **Bridge** | One line, near the end of a discipline page, saying the same method runs in the other two | Each discipline page, once |

**The test for a discipline page:** every sentence on `/chess/` must make sense to someone who
only cares about chess. A "shared" sentence that names the board, the wall *and* the language
fails it and gets a per-page variant.

**Home keeps the whole picture, sorted rather than mixed:** each method principle shows its
core, then one line per discipline under a label that links to that page.

---

## Architecture decisions (taken in Stage 1, revisit in Stage 5)

1. **Real URLs:** `/` · `/english/` · `/chess/` · `/climbing/`. Each is `<folder>/index.html`.
2. **Language stays as it is:** the same dual-language DOM (`data-en`/`data-ru`, `data-l`), and
   `?lang=ru` per page, with `theme.js` unchanged. No third i18n mechanism, no build step, and
   the instant language switch survives. Real `/ru/…` paths are a possible later stage, not
   assumed.
3. **Shared files:** `style.css`, `theme.js`, `main.js` and `assets/` are referenced by absolute
   path (`/style.css`) from the sub-pages. `main.js` already returns early when a section is
   missing, and every new behaviour keeps that contract.
4. **The masthead and footer are copied into each page**, at four pages. If they drift, a
   small include step in `build.sh` is the fix (Stage 6 decides).
5. **The edge function** (`functions/_middleware.js`) currently hardcodes `/?lang=ru`. Stage 5
   generalises it to any path, so `/chess/?lang=ru` gets its Russian `<head>` for crawlers and
   link previews.

---

## Stage 1 — Home: hero → method → the mark  ✅ built on this branch

**1.1 Hero** (kept, as Igor asked)
- Unchanged in look and copy.
- New: the italic line *English, chess, climbing.* is three real links to the three pages. This
  is the fastest choice on the site, it's on the first screen, and it gives Google an internal
  link per page. Hover underlines the word in its stroke's ink (amber, amber, green). An
  underline is a rule, not text, so the "no accent text under 24px" rule holds.
- The scroll cue now reads *Choose a discipline ↓* and jumps past the method straight to the
  mark. People who already know what they want don't have to read theory. People who scroll
  get the method first, as ordered.

**1.2 §01 The method** (moved up from §02, re-cut)
- Heading kept: *Deliberate practice, pointed at the weakest link.* The RU heading no longer
  has English in it: *Осознанная практика, нацеленная на самое слабое звено.*
- The lede is kept. The RU lede gains the closing sentence the EN had and the RU had lost.
- Each of the five principles opens to: the core paragraph, then three labelled lines
  (English · Chess · Climbing), each label linking to that page's method block.
- Copy changes, all in the commit:
  - Feedback loops: the unsourced "Tutoring software found the same thing" sentence was
    removed. Put it back with a named study if there is one.
  - Load management: "chilling" became "coasting", which keeps the register.
  - Feedback loops and Retrieval each got a new English line. They had no English example,
    because English was the default. **Igor to confirm these two lines describe how he
    actually teaches.**
  - RU names: *Интерливинг* → *Чередование*, *Распознавание закономерностей* →
    *Поиск закономерностей*, *Циклы обратной связи* → *Обратная связь в моменте*.
  - RU climbing: *из одних зацепок* lost the point; it is now *из одних мизеров*.

**1.3 §02 Three disciplines: the mark** (was §01, now centred)
- The mark sits in the centre, large. Each stroke has its door in its own corner: English at the
  top-left arm, chess at the top-right arm, climbing under the stem. Every door is a link with
  the discipline's name in display type, one line on who it's for, and its credentials in
  mono.
- Hovering or focusing a stroke or a door lights that stroke, dims the other two, and shows the
  stroke's sigil, using the paint logic the mark already had. A click goes to the page. There is
  no more "commit" state on the home page.
- The draw-in on first view and the idle hint (the strokes light in turn until someone engages)
  are kept.
- The readout table (credential / years / achieved / common problems) leaves the home page.
  Each line moves to its own discipline page's hero (Stages 2–4).
- The handwritten *Choose your discipline* stays, centred above the mark.
- The Vitnyr etymology stays under the mark, because that is where it explains the mark. RU
  grammar fixed (*напутствует поиску* → *призыв искать*).
- Phones: the mark on top, then the three doors as a big-type index list.

**1.4 What follows the mark**
- *In their words* (testimonials) and *How to start* (now §03) are unchanged, and so are the
  footer and the phone dock.
- §03 Specimens and §04 Who this is for **leave the home page**. Their content moves, split by
  discipline, to Stages 2–4. Until then it lives on `main` and in git history.
- Masthead section links: 01 Method · 02 Disciplines · 03 How to start.
- The progress hairline's ink switch now flips at the mark (it used to flip at §04, which is
  gone from home).

**1.5 Known gaps at the end of Stage 1**
- `/english/`, `/chess/` and `/climbing/` don't exist yet, so the doors and the hero links 404
  locally until Stages 2–4.
- The Playwright suite still describes the old page. Specimen and who-row tests will fail on
  home. They move with their content (Stage 6).

---

## Stage 2 — `/english/` (EN + RU)  ✅ built on this branch

**As built (2026-10-31)**, where it differs from or adds to the order below:

- **Order:** hero → 01 Mistakes I fix (`#specimen`) → 02 How I coach English (`#method`) →
  03 Who this is for (`#who`) → 04 How sessions run (`#sessions`) → testimonials (unnumbered,
  as on home) → bridge → 05 How to start (`#contact`). Mistakes come first: they are the
  page's proof, and the method reads better once you've seen what it fixes.
- **Masthead:** on a discipline page the three photo shortcuts become links to the three
  pages (label *Coaching* / *Направления*), and the current one carries the underline a
  section link gets when it's in view. The lockup goes home (`/`). The section numerals are
  this page's own five.
- **Hero:** the H1 is the line-mask title at a smaller size, and the hero sizes to its
  content, so the CTA is on the first screen at 1280×800. *Igor Shatsev* in the eyebrow
  links home: a visible breadcrumb to match the JSON-LD one. The photo is
  `en-01-anywhere` (*I can teach anywhere*), not the portrait: the portrait stays in
  contact, so no image appears twice on one page. The club and article frames sit under
  *How sessions run*, so the English photo group is all here, inline.
- **Hero CTA** goes straight to Telegram with the English opener. A who-row pick composes
  onto it too (`updateCta()` targets `.page-cta`).
- **Method:** each panel is the core sentence plus the English line only (`.mech__here`).
  The lede is re-cut for English: *If it did, years of films, podcasts and apps would
  already have done the job.*
- **Mistakes:** the three specimens and the *I am agree* engraving come across verbatim.
  New H2: *Your mistakes have deep roots. I'll teach you to unlearn them.* RU fix: *please
  недостаточно* (one word).
- **Sessions:** the old §03 closing paragraph, with RU moved from *ты* to *вы* to match the
  rest of the site, plus three facts (format, where, first lesson).
- **Contact:** *Message me for a free trial English lesson.* The lede now says *the first
  lesson is free* instead of *We start with a call*, which matches the dock and the Q4
  answer (trial lesson only). Igor should confirm this.
- **Head:** own title and description (RU description carries *репетитор*), og/twitter,
  hreflang `/english/` + `/english/?lang=ru`, and a JSON-LD WebPage + BreadcrumbList +
  Service (with the free-trial Offer) pointing at the home page's `#igor` Person. The share
  image is still the generic card; per-page cards are Stage 5.
- **Shell:** the masthead, footer, dock and contact are generated from the home page's
  markup (comments stripped) by a scratch script, then committed as plain HTML.
  `english/index.html` is the source of truth from here on; a home-page shell edit has to be
  copied across by hand until Stage 6 decides on an include step.
- **Pulled forward from Stage 5**, because shipping this page without them would break it:
  `build.sh` copies `english/` (and `chess/`, `climbing/` once they exist), and the
  middleware's Russian canonical/og:url now uses the request's own path. Before, it said
  `/?lang=ru` on every page, so `/english/?lang=ru` would have called itself the home page.
  The title and description were already read from each page's own `data-head-ru`.

Original order, for reference:


Order on the page. Source → treatment:

1. **Hero.**
   - Eyebrow: *Igor Shatsev / English / Yerevan & online*.
   - H1: the English specimen heading, re-cut: EN *You know English far better than you speak
     it.* / RU *Вы знаете английский гораздо лучше, чем на нём говорите.* This comes from the
     JSON-LD's own description, which until now was the only place it existed.
   - Stand-first: the §03 English intro ("Russian speakers don't make random mistakes…").
   - Credential strip (moved from the §01 readout): *C2 · IELTS 9 · 10 years · 100+ one-on-one
     clients*.
   - CTA, *Book a free trial lesson*, plus the portrait.
2. **Mistakes I fix** (eyebrow *Specimens*). The three English specimens, verbatim, with their
   reveal, plus the common-problems line as a short list under them.
3. **How I coach English.** The five principles: core sentence plus the English line only. One
   anchor, `#method`, so the home page's labels land here.
4. **Is this you?** The four who-rows, cut to their English clause, and re-phrased where the
   clause was a list:
   - Plateau → *Years of grammar drills and the English still freezes under pressure.*
   - Stress → *You understand the conversation, but the words don't come when it counts.*
   - One skill carrying the rest → *Your reading is far ahead of your listening and speaking.*
   - Backing off → *The conversation gets hard and you switch back to Russian.*

   Each row's Telegram prefill names English.
5. **How sessions run.** The §03 English session paragraph (one-on-one or groups, built around
   you, online or Yerevan). The free trial gets one name used everywhere (**Igor decides:
   lesson or call, and how long**).
6. **In their words.** All nine testimonials. They are all English learners, so this is where
   they belong.
7. **Bridge.** *I coach chess and climbing the same way: find the habit, fix it in the moment,
   bring it back cold a week later.* → links.
8. **CTA + footer.** The Telegram opener names English: *Hi! I'd like a free trial English
   lesson.*
9. **Photos.** The English collage group, inline (three frames).

Head: title *Spoken English coaching for Russian speakers in Yerevan and online — Igor
Shatsev*, its own description (RU twin with *репетитор*, per Igor's rule that the word lives
only in snippets and JSON-LD), its own share card, a Service JSON-LD node and breadcrumbs.

## Stage 3 — `/chess/`  ✅ built on this branch

**As built (2026-10-31)**, where it differs from or adds to the order below:

- **Order:** the same as `/english/`: hero → 01 Patterns I fix → 02 How I coach chess →
  03 Who this is for → 04 How sessions run → bridge → 05 How to start. There is no
  testimonials block: none from chess students exist, and the plan's `.ch__todo` class no
  longer exists in the CSS, so instead of a visible placeholder the page carries an HTML
  `PLACEHOLDER` comment where the quotes go. A visitor never sees an empty slot.
- **Hero:** EN H1 as planned. RU H1 re-cut to *Рейтинг встал. / А то, что его держит, /
  никуда не делось.*: the planned *А паттерн… — нет* read as a calque. Stand-first carries
  the softened procrastination line (*can turn from learning into a way of putting it off*).
  **The sharper original is still Igor's call.** Credentials: 2100 · 30 students brought to
  1800+ · 3 years · 5,000+ analysed games. Photo: `chess-01-board`.
- **Patterns I fix:** H2 *The same three mistakes, at every rating.* / *Одни и те же три
  ошибки — на любом рейтинге.* The lede now names the three specimens that are actually on
  the page (the old lede described an earlier set). Specimens verbatim from `origin/main`
  with two fixes: RU *насмотрености* → *насмотренности*, and the tilt specimen's
  explanation re-cut in both languages (*A pawn down, a quiet game drifts into a lost
  endgame…*), because the old sentence said losing the pawn itself put you in a lost
  endgame. Permalink ids are unchanged, so Stage 5's redirect map still holds.
- **Method:** core sentence plus the chess line only; lede re-cut for chess (*More games
  don't build skill. If they did, a few thousand blitz games would already have got you
  there.*). The home page's method labels link to `/chess/#method`, which now resolves.
- **Who:** the four planned chess clauses, each with its own Telegram prefill.
- **Sessions:** H2 *Your games, read against five thousand others.* Lede is the old §03
  chess paragraph re-cut; facts are 60 minutes / Lichess or Chess.com plus a call, or in
  Yerevan / first lesson free. Photos: `chess-04-reset`, `chess-09-cascade`.
- **Telegram opener:** *Hi! I'd like to book a free trial chess lesson.* The username ask
  moved into the contact lede (*Send me your Lichess or Chess.com username…*): `updateCta()`
  appends a who-row pick after the opener with ` — `, so an opener ending in *username:*
  would have read *username: — My rating has been flat…*.
- **Head:** own title, description (RU twin), og/twitter, hreflang, and WebPage +
  BreadcrumbList + Service JSON-LD, as on `/english/`.

Original order, for reference:

Same skeleton.
- **H1:** EN *Your rating has stalled. The pattern behind it hasn't.* / RU *Рейтинг встал. А
  паттерн, который его держит, — нет.* The §03 chess heading ("procrastination device") moves
  into the stand-first, softened to *can turn into*. **Igor decides whether he wants the sharper
  original.**
- **Credential strip:** *Rated 2100 · 3 years coaching · 30 students to 1800+ · 5,000+ analysed
  games*.
- **Specimens:** the three chess specimens. Fix: *Calculating only 2 moves* → *two moves*. RU
  common-problems list moved to second person, and *враг* → *соперник*.
- **Format:** 60 minutes, Lichess or Chess.com plus a call, reviewing 2–3 recent games against
  the pattern bank.
- **Who-rows (chess clause):** *Years of rated games and the rating's flat.* · *You see the move
  in analysis, not over the board.* · *Your openings are far ahead of your endgames.* · *The
  position gets sharp and you head for a safe trade.*
- **Proof:** no chess testimonials exist yet. The section ships as a marked placeholder
  (`.ch__todo`), never an invented quote. Igor to collect 2–3.
- **Telegram opener:** *Hi! I'd like a free trial chess lesson. My Lichess/Chess.com
  username:*
- **Igor decides:** adults only? (Most chess search in Yerevan is parents.)

## Stage 4 — `/climbing/`  ✅ built on this branch

**As built (2026-10-31):**

- **Order:** the same as `/chess/`, with no testimonials block (an HTML `PLACEHOLDER`
  comment marks the spot until real climbing quotes exist).
- **Hero:** H1 as planned (EN *Most plateaus / are habits you / can't see yet.*, RU
  *Большинство плато — / это привычки, которых / вы пока не видите.*). Stand-first re-cut
  from the old lede: fear, old injuries and undertraining each leave a habit behind. The
  eyebrow says *Yerevan & over video*, not *online*, because that is how climbing sessions
  run. Credentials: 7c redpoint, indoor · 7C on the Kilter Board · 13 climbers to 7a in a
  year · 2 years. Photo: `climb-07-coaching` (Igor coaching at the wall).
- **Habits I fix:** H2 *Three habits, and none of them is weak fingers.* / *Три привычки — и
  ни одна не про слабые пальцы.* Specimens verbatim from `origin/main` with these fixes:
  RU label *Перехват из страха* → *Пережим из страха* (перехват is a re-grip); RU label
  *Импровизирует…* → *Импровизируешь связку на трассе* (the only third-person label among
  nine); two RU correct-lines smoothed (*ровно с той силой, которая нужна…*, *руки прямые и
  нужны только для баланса*); the beta explanation re-cut in both languages.
- **Method:** chess-style re-cut lede (*Mileage doesn't build skill. If it did, years in the
  gym would already have got you there.*), core plus climbing line per principle.
- **Who:** the four planned climbing clauses; RU uses *ключ* and *нижняя страховка*.
- **Sessions:** H2 *Technique, route-reading, and your head on lead.* The tendon sentence is
  re-cut as planned. Facts: one-on-one or group / gym in Yerevan or over video / first
  session free. Photos: `climb-04-crimp`, `climb-06-wide`.
- **Wording:** climbing says *session* where English and chess say *lesson* (CTA, facts,
  Telegram opener, JSON-LD offer).

Original order, for reference:

Same skeleton.
- **H1:** EN *Most plateaus are habits you can't see yet.* / RU *Большинство плато — это
  привычки, которых вы пока не видите.* This fixes the old heading, which in both languages said
  the habits *couldn't* be unlearned.
- **Credential strip:** *7c redpoint · 7C Kilter · 2 years coaching · 13 climbers to 7a in a
  year*.
- **Format paragraph re-cut.** The "overtraining everything else…" sentence becomes *In most
  hobbies, overtraining costs you motivation. In climbing it costs you a tendon, and you find
  out when it's already too late.*
- **Who-rows (climbing clause):** *Years of gym sessions and the grade hasn't moved.* · *You know
  the crux, but your body doesn't do it on the lead.* · *Your grip strength is far ahead of your
  footwork.* · *The move gets scary and you climb down.* RU uses *ключ* to match *crux*
  (the old RU said *бета*).
- **Proof:** placeholder until real quotes exist.
- **Telegram opener:** *Hi! I'd like a free trial climbing session. I climb around…*

## Stage 5 — Google and old links  ✅ built on this branch

**As built (2026-10-31):**

- **Sitemap:** eight URLs (four pages × EN/RU), each listing en, ru and x-default.
  `robots.txt`'s comment updated to match.
- **Old links:** a render-blocking script in the home page's `<head>` (beside the
  `#collage` one) sends `/#english`, `/#chess`, `/#climbing` to the page, and every
  specimen permalink (`#specimen-copula`, `#specimen-chess-tilt`, …) to its page with the
  hash kept, using `location.replace` so the dead URL doesn't sit in history. `?lang` is
  carried across. `/#specimen` and `/#who` are rewritten in place to `/#origin` (the
  doors). Verified: all nine specimen targets land clear of the masthead.
- **Share cards:** `assets/share/share-card.html` takes `?page=english|chess|climbing`
  and renders that page's H1, credentials and a discipline tag (amber, green for
  climbing). Six new exports: `og-english(-ru).png`, `og-chess(-ru).png`,
  `og-climbing(-ru).png`. The home cards are untouched.
- **Edge function:** the Russian share image is now the page's own `og:image` with
  `-ru` added, so every page gets its own Russian card. (Path-based canonical and og:url
  landed in Stage 2.)
- **Home head:** title leads with the name (*Igor Shatsev — English, Chess & Climbing
  Coach in Yerevan | Vitnyr*, RU twin to match). The JSON-LD's three Services carry the
  `@id` and `url` of their page's Service node, so the Person on `/` and the Service on
  each page are one entity to Google.
- **`build.sh`** already copies the three folders (Stage 2).

Still Igor's, after deploy: resubmit the sitemap in Search Console and Yandex
Webmaster, request indexing for the three new URLs, and point profiles at the matching
page (Lichess → `/chess/`, Instagram → `/climbing/`, LinkedIn → `/english/`).

Original plan, for reference:

- **Sitemap:** 2 URLs → 8 (four pages × EN/RU), each pair with hreflang.
- **`_middleware.js`:** RU `<head>` rewrite for any path; canonical and og:url built from the
  request path; a per-page RU share card.
- **Old hash links redirect** (a small script at the top of `/`):
  - `/#english`, `/#chess`, `/#climbing` → the page.
  - `/#specimen-chess-tilt` → `/chess/#specimen-chess-tilt`, and the same for every specimen.
  - `/#who`, `/#specimen` → the home doors.
- **Home head:** title *Igor Shatsev — English, chess and climbing coach in Yerevan | Vitnyr*
  (brand query). The disciplines' own queries move to their pages.
- **`build.sh`** copies the three new folders into `dist/`.
- **After deploy (Igor):** resubmit the sitemap in Search Console and Yandex Webmaster,
  request indexing for the three new URLs, and point profiles at the specific page (Lichess →
  `/chess/`, Instagram → `/climbing/`, LinkedIn → `/english/`).

## Stage 6 — Polish, tests, docs  ✅ built on this branch

**As built (2026-10-31):**

- **View Transitions:** cross-document, `@view-transition { navigation: auto }` under
  `prefers-reduced-motion: no-preference`, typed `page` so the masthead's own
  `view-transition-name` applies only to page-to-page moves and never to the photos
  view's same-document transitions. Root and masthead both run on `--t`/`--e`. The
  result is a crossfade with the masthead holding still. **Not built:** the planned
  morph of the clicked stroke into the next page's header. It needs a matching
  named element on both sides and was more risk than this stage should carry; it's a
  self-contained follow-up if Igor wants it.
- **Photos view:** kept as the home page's routed `#collage` view (the default while
  Igor decides). Its "See me at work" door is back on home, under the three doors:
  Stage 1 had dropped it with §03, which left the view reachable only from the
  masthead icons. Each discipline page also shows its own photos inline.
- **Landing on a specimen:** a cold-loaded permalink on a discipline page (a shared
  link, or the old-link redirect) now lands the specimen exactly under the masthead
  and focuses it (`initSpecimenPermalinks`). It waits for `load` so the browser's own
  fragment jump can't race it, measures from `offsetTop` so the reveal's rise can't
  skew it, measures twice because the masthead is shorter at rest than once
  scrolled, and holds the phone masthead so it doesn't slide away mid-jump.
- **Tests:** `open_site(path=…)` opens any page. Specimen and who-row tests moved to
  the pages; the readout/commit tests (retired with the readout) became door,
  redirect and landing tests; the home title tests follow Stage 5's new title.
  `tests/test_pages.py` covers each page's head, canonical, hreflang, share card,
  JSON-LD, the sitemap, the masthead's page links, the bridge, the Telegram
  openers, "the rule" (no other discipline named outside the bridge), and the
  testimonial rule.
- **Docs:** CLAUDE.md (four pages, live hosting, the superseded one-file rule, the
  mark's new rest state) and a BUILD-NOTES entry.
- **Asset URLs** bumped to `?v=20261031a` on all four pages.
- **Artifact:** untouched. It's a single-file snapshot of the old one-page site and
  can't hold four pages. **Igor decides:** retire it, or keep it as a home-only
  snapshot.

Original plan, for reference:

- **Cross-document View Transitions** (`@view-transition { navigation: auto }`): the stroke
  you click grows into the top of the discipline page. Chrome and Safari animate; others just
  navigate. Motion stays additive.
- **The photos view:** retire the global `#collage` overlay in favour of each page's own
  group, or keep it as `/photos/` (**Igor decides**).
- **Tests:** split `tests/` per page, move the specimen and who-row tests to their pages, and
  add tests for door links, hreflang and the redirect map.
- **Docs:** CLAUDE.md's "one file" rule, the §-numbering and the stale "no hosting yet"
  line get updated. BUILD-NOTES entry.
- **The claude.ai artifact can't hold four pages.** Retire it, or keep it as a home-only
  snapshot (**Igor decides**).

## Things Igor hasn't been asked yet (collected)

1. Is the free trial a lesson or a call, and how long? One name everywhere.
2. Show prices, or a "from"?
3. Chess: adults only?
4. Sharp chess heading ("procrastination device"), or softened?
5. The two new English method lines (Feedback loops, Retrieval): true to how you teach?
6. "available 24/7" on Telegram: keep, or say what's true?
7. Photos: one global view, or each page's own?
8. Artifact: retire, or keep as a snapshot?

### Igor's answers (2026-10-31)

1. **Trial: 30 minutes.** Named "trial lesson" everywhere ("trial session" on `/climbing/`);
   the sessions facts row reads *Trial lesson: 30 minutes, free, no strings attached*, the
   contact ledes and meta descriptions say the same, and home's "We start with a call" became
   "We start with a 30-minute trial lesson". Regular sessions stay 60 minutes.
2. **No prices.** Nothing added.
3. **Chess: kids and adults.** The sessions lede, meta description and Service JSON-LD say
   *kids and adults under 1800*, and a fifth who-row speaks to parents (*You're looking for a
   coach for your child*, own Telegram prefill).
4. **Sharp chess line.** The stand-first opens with the original §03 sentence verbatim, EN
   and RU (*A rating plateau is when chess stops being about learning and becomes a
   procrastination device.*). The H1 is unchanged.
5. **Chess/climbing testimonials:** Igor asked for a stand-in quote until real ones arrive.
   Not done: an invented review on a live page would be the first fabricated claim on the
   site (Real material only, CLAUDE.md) and reads to a visitor as a real student's words.
   The PLACEHOLDER comments stay; the slot is filled the day real quotes come in.
6. Still open (not asked this round).
7. **Photos view:** Igor asked for a recommendation; keep the home gallery as it is.
8. **Artifact:** the artifact host now serves extra pages, so the four-page site can be
   published to the same URL with root-relative links rewritten. Done at merge time.
