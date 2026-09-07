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
  **Now the right half of the paired bottom row** (see below): re-cropped to
  **3:2**, figure biased right so the climber sits toward the outer edge and
  reads at rest under the 60% clip. Delivered 1200×800 / 600×400. Caption
  unchanged ("The board, from the floor.").
- `climb-05-rest` — Igor at the foot of an **outdoor crag**, mid-gesture,
  two partners nearby (backs to camera, not identifiable). From a low-res
  phone photo (`climbingl.jpg`, 960×1280); 1:1 crop on Igor, gentle level,
  no colour. Caption changed to "At the crag, between climbs." Because this
  is the first crag frame, the climbing group's lede was softened the same
  day — it no longer says "rather than a crag … not adventure" (see
  `BUILD-NOTES.md`).

- `climb-04-crimp` — Igor on an **outdoor rock face**, on a top rope,
  mid-route, reaching for a hold. From a phone photo delivered rotated 90°
  (`l.jpg`, 1280×960, low-res); rotated upright, cropped to **3:2** (window
  shifted right so the climber sits toward the left/outer edge), gentle
  autocontrast, no colour. Upscaled to 1200×800 for delivery — **soft, and
  Igor accepted that** (no higher-res original). Diverges from the slot's
  shot-list intent (a chalked-hand crimp close-up); slug keeps `-crimp`.
  Caption "On rock, mid-route." **Left half of the paired bottom row** (see
  below).
- `climb-02-chalk` — a hand at the harness belay loop, threading the rope
  before a climb. From a phone photo (`climbing.jpg`, 720×1280); **not
  cropped** (Igor's call — full 9:16 frame kept), +20% brightness / small
  contrast lift (frame was underexposed) + autocontrast, no colour. Figure
  class is `--916` (`aspect-ratio: 9/16`), so this is the tallest tile in
  row 1. Diverges from the slot's intent (chalking up from a chalk bag);
  slug keeps `-chalk`. Caption "At the belay loop, before setting off."

All five carry real, claim-free `<figcaption>` / `<img alt>` text. Row 1 is
three ratio-locked tiles (`--45` / `--11` / `--916`). Row 2 is the
**`.collage__pair`**: `climb-04-crimp` and `climb-06-wide` as two 3:2 photos
filling the group's full width — stacked on narrow / touch / reduced-motion,
and side-by-side on desktop where hovering (or keyboard-focusing) one opens
its `clip-path` to full width so it flows over the other. `--32` / `--34` /
`--span2` are retired.
See `BUILD-NOTES.md` → "Collage — first real photos", "Collage — rock-route
hero", and "Collage — paired flow-over bottom row". The climbing group is
**fully real** now; the other 12 collage frames
(all `en-*`, all `chess-*`) remain the stand-ins below, so the artifact hold
still stands.

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

| file | tags | lock |
|---|---|---|
| en-01-call | office,laptop | 22 |
| en-06-window | yerevan,armenia | 6 |
| chess-01-board | chess,player | 7 |
| chess-02-clock | chess,clock | 302 |
| chess-03-study | chess,board | 9 |
| chess-04-reset | chess,pieces | 304 |
| chess-05-pieces | chess,knight | 305 |
| chess-06-notation | chess,game | 12 |
