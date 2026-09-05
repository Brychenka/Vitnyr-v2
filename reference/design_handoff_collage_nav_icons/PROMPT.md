Paste this into Claude Code, run from the site-v2 folder:

---

Read design_handoff_collage_nav_icons/README.md, then read CLAUDE.md and
BUILD-NOTES.md in this repo.

Implement the three collage nav icons described in that README: chess,
climbing (screw-lock carabiner), and English (open book), added to the
masthead nav.tools after the Cream and RU switches, each jumping the collage
view to its photograph and flashing that tile's hairline in the target green.

Constraints:
- Paste the SVG path data from the README verbatim. Do not redraw or
  "optimise" the glyphs.
- No new colour values, no new dependencies, no build step. Use the existing
  custom-property tokens and the existing .tool class and its ::after
  underline.
- Reuse the existing #collage hash router to open the view; do not duplicate
  its open/close logic.
- Do not use scrollIntoView.
- Keep the icons working with JS off to the extent the rest of the nav does,
  and keep the existing keyboard and focus behaviour of the view intact.

Show me the diff before writing anything.
