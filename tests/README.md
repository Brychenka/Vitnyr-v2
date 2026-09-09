# QA suite — Vitnyr site-v2

End-to-end tests that automate the manual verification checklist in
`../CLAUDE.md` and `../BUILD-NOTES.md`: both themes, both languages, ~375 and
~1280, `prefers-reduced-motion`, no console errors, no horizontal overflow,
focus management, the hash-routed collage view, the count-up numbers, and the
content/positioning rules that have no other guardrail.

Stack: **pytest + Playwright (Python)**. Self-contained in this folder — the
site itself stays a no-build, no-`package.json` static site. A throwaway
`python -m http.server` on a free port serves the repo root for the run.

## Run

```bash
# one-time: create the venv and download Chromium
python3 -m venv tests/.venv
tests/.venv/bin/pip install -r tests/requirements.txt
tests/.venv/bin/python -m playwright install chromium

# every run (from the repo root)
tests/.venv/bin/pytest tests -q
```

Useful flags:

```bash
tests/.venv/bin/pytest tests -q -m "not slow"   # skip animation-timing tests
tests/.venv/bin/pytest tests/test_collage.py -q  # one file
tests/.venv/bin/pytest tests -q --headed --slowmo 250   # watch it drive
```

## Choosing the pair

`color_scheme=` sets only the OS preference, which the page has ignored since
2026-09-07 (cream is the default; charcoal is opt-in). **A test that needs the
charcoal pair must pass `theme="dark"`** — `color_scheme="dark"` silently
measures cream, and assertions that happen to hold in both pairs pass while
testing nothing.

## Files

| file | covers |
|---|---|
| `test_smoke.py` | load, title, same-origin resources, CDN libs present |
| `test_i18n.py` | language switch, persistence, `?lang=`, both translation mechanisms |
| `test_theme.py` | cream default (OS pref ignored), charcoal opt-in, persistence, button label, `theme-color` |
| `test_layout.py` | no horizontal overflow (2 widths × 2 langs × 2 pairs), fixed masthead, skip link |
| `test_a11y.py` | one h1, landmarks, skip-link focus move, accessible names, reduced-motion |
| `test_collage_nav_icons.py` | chess/carabiner/book icons: structure, glyph fidelity, ink tokens, lockup's 176px floor, the 600px wrap, 44px touch targets, no click wiring yet |
| `test_motion.py` | hero plays + lands, reveal rhythm, facts row counts its numbers up as separate instruments (`-m slow`) |
| `test_collage.py` | hash routing, deep link, browser back, inert background, focus, scroll restore |
| `test_content.py` | name in both languages, 2100-without-FIDE, distinct 7c/7C, contact handles real, OG tags flagged |

## When placeholders get filled

`test_content.py` deliberately fails-forward on what's still outstanding.
Contact handles landed 2026-09 (commit `dd1ff9c`); `test_contact_handles_are_real`
was updated to match. `test_og_url_and_image_not_yet_asserted` still asserts
the *current* placeholder state — update it in the same commit that adds
`og:url` / `og:image`.
