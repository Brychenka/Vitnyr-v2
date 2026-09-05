# Collage — shot list and asset contract

For the `#collage` view on the Vitnyr site. Written before the layout so the
layout is built around real frames, not the other way round. Nothing here is
shot yet; the view ships with reserved empty boxes until it is.

**v2 — 2026-09-05.** The original contract was a single mixed grid of six
shots (two per crop ratio, domain-anchored slugs `01`–`06`). Igor asked for
the collage to become **three labelled domain groups — English, then chess,
then climbing — with a bigger set per group**. This file is rewritten to
match; the six-shot cap and the old `NN-slug` filenames are retired. If you
are picking up mid-shoot against the old list, the mapping is: `01-chess-board`
→ `chess-01-board`, `02-climb-board` → `climb-01-board`, `03-call` →
`en-01-call`, `04-table-yerevan` → `en-02-yerevan-table`, `05-yerevan-window`
→ `en-06-window`, `06-hands` → split into `chess-05-pieces` / `climb-04-crimp`.

## The one hard rule

**Real photographs of Igor Shatsev only.** No stock, no rented studio setups
dressed to look candid, no AI images, no "someone who could be a coach." This
is `CLAUDE.md`'s *real material only* rule applied to pixels. A shot that
cannot be taken for real is cut from the list, not faked.

A photo also may not imply a claim the page won't make. No invented students'
faces used as testimonial proof, no scoreboard doctored to a number, no
climbing grade written into the frame. The photographs show the work
happening; the words carry the claims.

## Subject

The three domains the site already runs on — English coaching, chess,
climbing. The site's argument is that one method transfers across all three;
the pictures should feel like the same person in the same frame of mind in
three different rooms. Each frame shows the activity *being done*, not a
portrait of Igor next to a prop.

Order on the page is **English → chess → climbing**: English is the offer,
chess and climbing are the proof it transfers (this matches the hero trifecta
and section 03).

## Shots — six per group, eighteen total

Each group runs **six frames at a fixed mix of the three crop ratios: two
`4:5`, two `3:2`, two `1:1`.** Two-of-each keeps every group reading as a
system rather than a scrapbook, and keeps the reserved-box heights balanced
before any image lands. A group may ship with as few as five if a sixth can't
be shot honestly — drop one `1:1` first.

`NN` runs `01`–`06` in on-screen reading order (top-to-bottom, the order
Stage 4 also staggers reveals in).

### English — `en-*`  (no classroom to photograph; this is the real delivery)

| # | slug | ratio | in frame |
|---|---|---|---|
| 01 | `en-01-call` | 3:2 | Igor at his desk mid-sentence on a video call — headset/earbuds, hands moving, laptop open. The other screen is not legible; no student's face identifiable. |
| 02 | `en-02-yerevan-table` | 1:1 | Igor across a small café/office table from one person, both leaning in, a notebook between them. Shot from behind/beside the student so they are not identifiable. |
| 03 | `en-03-desk` | 4:5 | The working desk itself, upright frame — laptop, notes, the tools of the lesson. Igor small in frame or just out of it. |
| 04 | `en-04-correction` | 1:1 | Close on a sentence being corrected by hand — pen on paper or stylus on screen, the edit visible as an act, not a legible claim. |
| 05 | `en-05-markup` | 3:2 | A text between two people being pulled apart — highlighting, margin notes. Hands and page, no faces needed. |
| 06 | `en-06-window` | 4:5 | The view Igor works against — a specific Yerevan street, tufa stone, Ararat behind the rooflines if it's there. Grounds "Yerevan" without a postcard. |

### Chess — `chess-*`  (the feedback loop is a rating that doesn't negotiate)

| # | slug | ratio | in frame |
|---|---|---|---|
| 01 | `chess-01-board` | 4:5 | Igor mid-game, seated, looking down into the position, hand on a piece or the clock. Opponent out of focus or cropped to a shoulder. The moment before a move is committed. |
| 02 | `chess-02-clock` | 1:1 | The clock, close, a hand near it between moves. The scoreboard as a physical object, no number doctored in. |
| 03 | `chess-03-study` | 3:2 | A position set up away from a game for study — board, a book or screen beside it, notes. |
| 04 | `chess-04-reset` | 4:5 | Hands resetting the pieces to the starting rank. The repeatable-practice point. |
| 05 | `chess-05-pieces` | 1:1 | Captured pieces off to the side of the board. Texture tile; quiet. |
| 06 | `chess-06-notation` | 3:2 | A pen and a score sheet being filled in move by move — the act of notating, not a readable result. |

### Climbing — `climb-*`  (the scoreboard is the grade; gravity keeps it honest)

| # | slug | ratio | in frame |
|---|---|---|---|
| 01 | `climb-01-board` | 4:5 | Igor on a steep indoor training board (Kilter / system board), caught mid-move — one hand reaching, body tensioned, feet placed. Chalk visible. |
| 02 | `climb-02-chalk` | 1:1 | Chalking up between attempts — hand in the bag, close. |
| 03 | `climb-03-feet` | 3:2 | Feet placed on holds before the reach — the deliberate part, lower body. |
| 04 | `climb-04-crimp` | 4:5 | A hand set on a crimp, chalked fingers, close. Connects to the chess "hands" tile as one pair of hands across two domains. |
| 05 | `climb-05-rest` | 1:1 | Resting on the wall between goes — a still moment on the board, not a summit. |
| 06 | `climb-06-wide` | 3:2 | The training board from the floor — the whole adjustable panel, Igor small on it or off it. An adjustable board, not a crag: the point is practice, not adventure. |

## Delivery contract

The later stages build against this. Numbers are fixed; if a file misses
budget it gets recompressed, not waved through.

### Crop aspect ratios — three, no more

| Ratio | Per group | Reading |
|---|---|---|
| `4 / 5` | 2 | upright figure / the board |
| `3 / 2` | 2 | wide, the context frames |
| `1 / 1` | 2 | the close / texture tiles |

A figure's ratio is fixed here and hard-coded into the markup
(`.collage__fig--45 / --32 / --11`); it must not change when the real file
lands — this is what protects the site's zero-layout-shift record.

### Resolution and delivery widths

- **Shoot** at 3000 px or more on the long edge, so crops to any of the three
  ratios still have latitude.
- **Deliver** two widths per image, `1x` and `2x`. Largest a tile ever renders
  is ~460 px CSS wide now (three columns inside `--maxw`), so:

| Ratio | `@1x` | `@2x` |
|---|---|---|
| `4 / 5` | 460 × 575 | 920 × 1150 |
| `3 / 2` | 460 × 307 | 920 × 614 |
| `1 / 1` | 460 × 460 | 920 × 920 |

### Format

- **WebP** primary, quality ~72.
- **JPEG** fallback (progressive), quality ~78, for `<picture>`'s `<img>`.
- Ship the files **as shot, in colour.** The grayscale treatment is a CSS
  `filter` custom property valued per theme — keeping the file in colour means
  one asset serves both cream and charcoal, and the decision stays reversible.

### Weight budget — enforced (revised for 18 images)

The old budget was 6 images, ≤120 KB each, ≤720 KB total. At eighteen smaller
tiles:

- **18 images maximum** (6 per group; a group may ship 5).
- **≤ 90 KB** per delivered `@2x` WebP.
- **≤ 1.6 MB** total across all `@2x` WebP → ≈ 2.1 MB once base64-inlined into
  the single-file artifact — still well under the 16 MB cap.
- JPEG fallbacks kept lean (~110 KB each) but not counted toward the inline
  budget.
- Over budget → recompress. The budget does not move.

### Filenames — under `assets/collage/`

`<domain>-NN-slug@1x.webp`, `@2x.webp`, `@1x.jpg`, `@2x.jpg` — `<domain>` is
`en`, `chess` or `climb`; `NN` is `01`–`06` in on-screen reading order.

```
assets/collage/
  en-01-call@{1x,2x}.{webp,jpg}
  en-02-yerevan-table@{1x,2x}.{webp,jpg}
  en-03-desk@{1x,2x}.{webp,jpg}
  en-04-correction@{1x,2x}.{webp,jpg}
  en-05-markup@{1x,2x}.{webp,jpg}
  en-06-window@{1x,2x}.{webp,jpg}
  chess-01-board@…   chess-02-clock@…   chess-03-study@…
  chess-04-reset@…   chess-05-pieces@…  chess-06-notation@…
  climb-01-board@…   climb-02-chalk@…   climb-03-feet@…
  climb-04-crimp@…   climb-05-rest@…    climb-06-wide@…
```

### Alt text

Real, descriptive, bilingual, added in Stage 3 via the existing
`data-en` / `data-ru` mechanism — a translatable string, not an afterthought.
Describes what is in the photograph; makes no claim.

### Still Igor's to confirm

The shot briefs above and every Russian caption in `index.html` are a
model's first pass. Igor coaches language for a living and captions fall
under "real material only" — he vets the RU and signs off the brief list
before the shoot.
