# Collage — shot list and asset contract

For the `#collage` section on the Vitnyr site (`feature/photo-collage`).
Written before the layout so the layout is built around real frames, not the
other way round. Nothing here is shot yet; the section ships with reserved
empty boxes until it is.

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

Three domains the site already runs on — English coaching, chess, climbing —
plus Yerevan as the place. Each frame should show the activity *being done*,
not a portrait of Igor next to a prop. The site's argument is that one method
transfers across all three; the pictures should feel like the same person in
the same frame of mind in three different rooms.

## Shots

Six proposed. The three marked **[core]** are the ones to get if only three
are ever taken — one per domain, each showing the activity rather than a pose.

### 01 — Over the board  **[core]**
- **In frame:** Igor mid-game, seated, looking down into the position. Hand on
  a piece or on the clock. Opponent out of focus or cropped to a shoulder.
- **Orientation:** portrait (4:5).
- **Evidences:** chess. The site's line is *the feedback loop is a
  scoreboard* — this is the moment before a move is committed, which is where
  that pressure actually lives.
- **Earns its place over:** a posed shot of Igor beside a board. A hand
  already on a piece reads as a real game; a tidy starting position reads as a
  photo shoot.

### 02 — On the system board  **[core]**
- **In frame:** Igor on a steep indoor training board (Kilter / system
  board), caught mid-move — one hand reaching, body tensioned, feet placed.
  Chalk visible.
- **Orientation:** portrait (4:5).
- **Evidences:** climbing, and specifically the *7C Kilter boulder* the site
  cites. The board is adjustable and repeatable, which is the deliberate-
  practice point — an outdoor crag would say "adventure," not "training."
- **Earns its place over:** a summit or scenic outdoor shot. Pretty, off-
  message: the site frames climbing as load management under a scoreboard
  (the grade), not as travel.

### 03 — A lesson on a call  **[core]**
- **In frame:** Igor at his desk mid-sentence on a video call — headset or
  earbuds, hands moving, laptop open. The other person's screen is not
  legible (blur or angle); no student's face is identifiable.
- **Orientation:** landscape (3:2).
- **Evidences:** the coaching itself, as it actually happens — one-on-one,
  online. There is no classroom to photograph; this is the real delivery.
- **Earns its place over:** a whiteboard / classroom setup. That's a teaching
  aesthetic the practice doesn't use, and it would be staged.

### 04 — In person, Yerevan
- **In frame:** Igor across a small café or office table from one person, both
  leaning in, a notebook or phone between them. Read from behind or beside the
  student so they are not identifiable.
- **Orientation:** square (1:1).
- **Evidences:** *online or in Yerevan* — the in-person half of the offer, and
  a second human presence so the section isn't six frames of one man alone.
- **Earns its place over:** another solo shot. The section needs one frame
  with a student in it, kept anonymous.

### 05 — Yerevan, from the desk
- **In frame:** the view Igor actually works against — a window onto a
  specific Yerevan street, tufa stone, Ararat behind the rooflines if it's
  there. Igor small in the frame or just out of it.
- **Orientation:** landscape (3:2).
- **Evidences:** place, without a postcard. Grounds "Yerevan" as a real desk
  in a real city rather than a location tag.
- **Earns its place over:** a landmark shot (Cascade, Republic Square). Those
  say "tourism"; a working window says "this is where the calls happen."

### 06 — The same hands
- **In frame:** hands only, close. Chalked fingers on a crimp, or fingers
  resetting chess pieces to the starting rank. Macro, shallow depth.
- **Orientation:** square (1:1).
- **Evidences:** connects the two proof domains through one pair of hands, and
  gives the composition one quiet close-up for rhythm against the wider
  frames.
- **Earns its place over:** a fourth full-body shot. The grid needs a texture
  tile, not more scale.

## Delivery contract

The later stages build against this. Numbers are fixed; if a file misses
budget it gets recompressed, not waved through.

### Crop aspect ratios — three, no more

| Ratio | Used by | Reading |
|---|---|---|
| `4 / 5` | 01 chess, 02 climb | upright figure, the two proof domains |
| `3 / 2` | 03 call, 05 Yerevan | wide, the context frames |
| `1 / 1` | 04 table, 06 hands | the close / human tiles |

Two portraits, two landscapes, two squares — a set that reads as a system,
not a scrapbook. A figure's ratio is fixed here and hard-coded into the
markup; it must not change when the real file lands (this is what protects
the site's zero-layout-shift record).

### Resolution and delivery widths

- **Shoot** at 3000 px or more on the long edge, so crops to any of the three
  ratios still have latitude.
- **Deliver** two widths per image, `1x` and `2x`. Largest a tile ever renders
  is ~720 px CSS wide, so:

| Ratio | `@1x` | `@2x` |
|---|---|---|
| `4 / 5` | 720 × 900 | 1440 × 1800 |
| `3 / 2` | 720 × 480 | 1440 × 960 |
| `1 / 1` | 640 × 640 | 1280 × 1280 |

### Format

- **WebP** primary, quality ~72.
- **JPEG** fallback (progressive), quality ~78, for `<picture>`'s `<img>`.
- Ship the files **as shot, in colour.** The grayscale treatment is a CSS
  `filter` custom property valued per theme (plan decision 1) — keeping the
  file in colour means one asset serves both cream and charcoal, and the
  decision stays reversible.

### Weight budget — enforced

- **6 images maximum.**
- **≤ 120 KB** per delivered `@2x` WebP.
- **≤ 720 KB** total across all six `@2x` WebP (≈ 960 KB once base64-inlined
  into the single-file artifact — well under the 16 MB cap).
- JPEG fallbacks kept lean too (~140 KB each) but are not counted toward the
  inline budget.
- Over budget → recompress. The budget does not move.

### Filenames — under `assets/collage/`

`NN-slug@1x.webp`, `NN-slug@2x.webp`, `NN-slug@1x.jpg`, `NN-slug@2x.jpg`

`NN` is `01`–`06` in composition reading order (top-to-bottom on screen — the
order Stage 4 also staggers reveals in). `slug` is domain-anchored:

```
assets/collage/
  01-chess-board@1x.webp   01-chess-board@2x.webp   01-chess-board@1x.jpg   01-chess-board@2x.jpg
  02-climb-board@1x.webp    02-climb-board@2x.webp   02-climb-board@1x.jpg   02-climb-board@2x.jpg
  03-call@1x.webp           03-call@2x.webp          03-call@1x.jpg          03-call@2x.jpg
  04-table-yerevan@1x.webp  04-table-yerevan@2x.webp 04-table-yerevan@1x.jpg 04-table-yerevan@2x.jpg
  05-yerevan-window@1x.webp 05-yerevan-window@2x.webp 05-yerevan-window@1x.jpg 05-yerevan-window@2x.jpg
  06-hands@1x.webp          06-hands@2x.webp         06-hands@1x.jpg         06-hands@2x.jpg
```

### Alt text

Real, descriptive, bilingual, added in Stage 3 via the existing
`data-en` / `data-ru` mechanism — a translatable string, not an afterthought.
Describes what is in the photograph; makes no claim.
