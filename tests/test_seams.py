"""Cheap guards for values that two files must keep equal by hand."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# --- The four pages share no template, so the shared frame (footer,
# masthead) is kept in step by hand. These catch one
# page quietly falling behind. Each comparison strips only what may
# legitimately differ per page, and says why. ---

PAGES = ["index.html", "english/index.html", "chess/index.html", "climbing/index.html"]


def _block(path, pattern):
    m = re.search(pattern, (ROOT / path).read_text(), re.S)
    assert m, f"{path}: block not found"
    return m.group(0)


def _common(html):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)          # notes differ, markup must not
    # link targets differ by page (/english/ vs #top, root-relative vs in-page)
    html = re.sub(r'\s(href|data-href-en|data-href-ru)="[^"]*"', "", html)
    # home opens the gallery in place; the other pages link to /#collage
    html = re.sub(r"\sdata-collage-link", "", html)
    return html


def test_footer_is_the_same_on_all_four_pages():
    def norm(path):
        f = _common(_block(path, r"<footer\b.*?</footer>"))
        return re.sub(r"\s+", " ", f).strip()
    base = norm(PAGES[0])
    for path in PAGES[1:]:
        assert norm(path) == base, f"{path}: footer has drifted from index.html's"


def test_masthead_is_the_same_on_all_four_pages():
    def norm(path):
        h = _common(_block(path, r'<header class="masthead">.*?</header>'))
        # the current page is marked; the lockup is named for where it goes
        h = re.sub(r'\saria-current="page"', "", h)
        h = re.sub(r'\saria-label="[^"]*"', "", h)
        return re.sub(r"\s+", " ", h).strip()
    base = norm(PAGES[0])
    for path in PAGES[1:]:
        assert norm(path) == base, f"{path}: masthead has drifted from index.html's"
