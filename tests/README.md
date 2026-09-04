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

## Files

| file | covers |
|---|---|
| `test_smoke.py` | load, title, same-origin resources, CDN libs present |
| `test_i18n.py` | language switch, persistence, `?lang=`, both translation mechanisms |
| `test_theme.py` | system pref vs explicit choice, persistence, button label, `theme-color` |
| `test_layout.py` | no horizontal overflow (2 widths × 2 langs × 2 pairs), fixed masthead, skip link |
| `test_a11y.py` | one h1, landmarks, skip-link focus move, accessible names, reduced-motion |
| `test_motion.py` | hero plays + lands, reveal rhythm, counters reach exact values (`-m slow`) |
| `test_collage.py` | hash routing, deep link, browser back, inert background, focus, scroll restore |
| `test_content.py` | name in both languages, 2100-without-FIDE, distinct 7c/7C, placeholders flagged |

## When placeholders get filled

`test_content.py` deliberately fails-forward: `test_contact_handles_are_still_flagged_placeholders`
and `test_og_url_and_image_not_yet_asserted` assert the *current* placeholder
state. When the real handles / OG tags land, update those two tests in the
same commit.
