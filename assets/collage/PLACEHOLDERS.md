# Collage placeholder images — provenance

**These are throwaway stand-ins, NOT photographs of Igor Shatsev.** They exist
so the layout, grayscale treatment and motion stages have real pixels to run
against while the actual shoot is pending. They are replaced by real photos of
Igor — per `reference/collage-shotlist.md` — **before** the live "Vitnyr
Signature" artifact is next republished. See `BUILD-NOTES.md` →
"Collage placeholders" and `CLAUDE.md`'s note on the real-material rule.

Every file is grayscaled at display time by `--collage-filter`; none carries a
caption claim (the `<figcaption>` describes the *intended* shot, not the
stand-in) and every `<img alt>` is empty on purpose.

**Exception — the entire climbing group is real (2026-09-07).**
`climb-01-board`, `climb-02-chalk`, `climb-05-rest`, `climb-04-crimp`,
`climb-06-wide` are all photographs Igor supplied; the sixth climbing
stand-in, `climb-03-feet`, was **dropped** (the group now ships 5, which
`collage-shotlist.md` allows). Details:
- `climb-01-board` — seated at the foot of an indoor bouldering wall, first
  climbing 4:5 slot (crop-to-4:5 + gentle autocontrast, no colour). The frame
  differs from this slot's shot-list intent (a mid-move board shot).
- `climb-06-wide` — mid-move on a steep overhanging wall, shot from the floor.
  From `IMG_8681.CR2` (Canon RAW, 5472×3648), autocontrast + a small
  exposure/contrast lift (the gym frame was underexposed), no colour.
  **Right zone of the paired bottom row** (see below): centred **3:2** crop
  (near-native), delivered 1200×800 / 600×400. Caption unchanged ("The board,
  from the floor.").
- `climb-05-rest` — Igor at the foot of an **outdoor crag**, mid-gesture,
  two partners nearby (backs to camera, not identifiable). From a low-res
  phone photo (`climbingl.jpg`, 960×1280); 1:1 crop on Igor, gentle level,
  no colour. Caption changed to "At the crag, between climbs." Because this
  is the first crag frame, the climbing group's lede was softened the same
  day — it no longer says "rather than a crag … not adventure" (see
  `BUILD-NOTES.md`).

- `climb-04-crimp` — Igor on an **outdoor rock face**, on a top rope,
  mid-route, reaching for a hold. From a phone photo delivered rotated 90°
  (`l.jpg`, 1280×960, low-res); rotated upright, centred **3:2** crop on the
  figure, gentle autocontrast, no colour. Upscaled to 1200×800 for delivery
  — **soft, and Igor accepted that** (no higher-res original). Diverges from
  the slot's shot-list intent (a chalked-hand crimp close-up); slug keeps
  `-crimp`. Caption "On rock, mid-route." **Left zone of the paired bottom
  row** (see below).
- `climb-02-chalk` — a hand at the harness belay loop, threading the rope
  before a climb. From a phone photo (`climbing.jpg`, 720×1280); **not
  cropped** (Igor's call — full 9:16 frame kept), +20% brightness / small
  contrast lift (frame was underexposed) + autocontrast, no colour. Figure
  class is `--916` (`aspect-ratio: 9/16`), so this is the tallest tile in
  row 1. Diverges from the slot's intent (chalking up from a chalk bag);
  slug keeps `-chalk`. Caption "At the belay loop, before setting off."

All five carry real, claim-free `<figcaption>` / `<img alt>` text. Row 1 is
three ratio-locked tiles (`--45` / `--11` / `--916`). Row 2 is the
**`.collage__pair`**: `climb-04-crimp` and `climb-06-wide` as two equal 3:2
photos splitting the group's full width, side by side (stacked on narrow).
No overlap, no hover behaviour. `--32` / `--34` / `--span2` are retired.
See `BUILD-NOTES.md` → "Collage — first real photos", "Collage — rock-route
hero", and "Collage — paired bottom row". The climbing group is
**fully real** now.

**Exception — four chess frames are real (`chess-01`, `chess-02`, `chess-04`,
`chess-05`; 2026-09-08).** All supplied by Igor. Grade-neutral, claim-free
captions; `<img alt>` stays empty; greyed at display by `--collage-filter`.

- `chess-01-board` — Igor mid-move at an outdoor tournament (source
  `IMG_7689.JPG`, 1280×853, native 3:2). **Full frame, not cropped** — a
  first tight-4:5 crop hid the board, so Igor's call was to keep the whole
  frame even though the other players at the table stay visible. Gentle
  `autocontrast(cutoff=0.5)`, no colour; straight downscale to 900×600 /
  450×300. Slot changed `--45` → `--32`, img `width`/`height` → 900/600.
  Caption "Over the board, mid-game." unchanged.
- `chess-02-clock` — a life-size outdoor chess set on a paved board in a
  park, a game in progress, spectators at the left, trees behind (source
  `2026-09-08 16.00.54.jpg`, 960×1280 phone portrait). **Centred 1:1 crop**
  lifted 80 px to favour the pieces and onlookers over empty foreground
  paving — whole board, every standing piece, the spectators and the park
  all kept. `autocontrast(cutoff=0.5)`, no colour; 900×900 / 450×450 (`@2x`
  ~222 KB — the tiled board and foliage are high-frequency and resist JPEG,
  in line with the real climbing frames' ~220 KB). Slot unchanged (`--11`,
  900×900 already). Caption rewritten "The clock, between moves." →
  **"A life-size board, out in the park."** / «Доска в полный рост, в
  парке.» Slug keeps `-clock` (cf. `chess-04-reset`), content diverged.
- `chess-04-reset` — Igor mid-move, fingers on a pawn, clock in frame, at a
  stone-walled venue (source a 1102×1422 phone frame). Trimmed only **44 px
  of blurred wall off the top** to hit an exact 4:5 — nothing else cropped.
  `autocontrast(cutoff=0.5)`, no colour; 900×1125 / 450×563. Slot unchanged
  (`--45`, 900×1125 already). Caption rewritten "Pieces back to the starting
  rank." → **"Mid-move, on the clock."** / «Ход — под часами.» Slug keeps
  `-reset` (cf. `climb-04-crimp`), content diverged.
- `chess-05-pieces` — a hand-carved figurative set mid-position on a carved
  table (source `camphoto_684387517.jpg`, 3024×4032). Square crop on the
  board — drops only the serving-cart drawer/knob below it, keeps the whole
  board and the carved frame all round. `autocontrast(cutoff=0.5)`, no
  colour; 900×900 / 450×450 (`@2x` ~155 KB — the carved-wood texture is
  detail-dense and resists JPEG, still well under the real climbing frames'
  ~220 KB). Slot unchanged (`--11`, 900×900 already). Caption rewritten
  "Captured pieces, off to the side." → **"A hand-carved set, mid-game."** /
  «Резной комплект, партия в разгаре.» Slug keeps `-pieces`.

See `BUILD-NOTES.md` → "Collage — first real chess frame", "Collage — two
more real chess frames" and "Collage — a real park-chess frame".

**`chess-03-study` and `chess-06-notation` were pulled from the page on
2026-09-08** (Igor: "remove picture 3 and 6 for now … they are not mine").
The chess group now ships the four real frames only, two-up on desktop
(`.collage--group--pairs`; see `BUILD-NOTES.md` → "Collage — chess group
drops to four real frames"). Their `.jpg`/`@2x.jpg` files are still on disk
and their provenance stays recorded below, in case Igor wants them back.

The other 6 collage frames (all `en-*`) remain the stand-ins below, so the
artifact hold still stands.

## en-02 … en-05 — Openverse, CC0 1.0 / public-domain

| file | Openverse ID | creator | source |
|---|---|---|---|
| en-02-yerevan-table | `5e4ceb38-c8e8-49d2-8296-4edd0ab48bd2` | Kristin Hardwick | https://stocksnap.io/photo/hands-beverage-RYM2WIKREP |
| en-03-desk | `15b8aa96-d680-4c8d-bda0-9633cdbbe309` | Pixel.la Free Stock Photos | https://commons.wikimedia.org/w/index.php?curid=51439338 |
| en-04-correction | `b73d6a7e-37f4-4f5e-9468-5ac1d0ef30fe` | Helloquence | https://stocksnap.io/photo/writing-papers-Y01VDYAX63 |
| en-05-markup | `281b6a9b-acdb-48bf-9ca7-f699d191b73b` | — | https://www.rawpixel.com/image/5903740/ |

## en-06 + chess-* — LoremFlickr (Flickr Creative Commons proxy)

Openverse rate-limited the batch partway through, so the rest came from
`loremflickr.com`, which serves tag-matched images drawn from Flickr's
Creative-Commons pool. (The climbing stand-ins that were also from here are
all gone now — replaced by real photos or, for `climb-03-feet`, dropped.) LoremFlickr does not return per-image
attribution through the proxy; because these files do not ship, the collective
source note here stands in for it. If any of these somehow needs to outlive the
shoot, pull the real attribution or swap it for a CC0 image first.

| file | tags | lock | on the page? |
|---|---|---|---|
| en-01-call | office,laptop | 22 | yes |
| en-06-window | yerevan,armenia | 6 | yes |
| chess-03-study | chess,board | 9 | no — pulled 2026-09-08 |
| chess-06-notation | chess,game | 12 | no — pulled 2026-09-08 |

*(`chess-01-board`, `chess-02-clock`, `chess-04-reset` and `chess-05-pieces`
were replaced by real photos of Igor's on 2026-09-08 — see the exception
above. `chess-03-study` and `chess-06-notation` were then removed from the
page the same day; the files stay here for provenance and easy restore.)*
