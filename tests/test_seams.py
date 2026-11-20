"""Cheap guards for values that two files must keep equal by hand."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_spark_duration_in_css_matches_spark_ms_in_js():
    """--spark-d (style.css) and SPARK_MS (main.js) are the codebase's only
    CSS-to-JS coupling; a comment in each file used to be the whole guard."""
    css = (ROOT / "style.css").read_text()
    js = (ROOT / "main.js").read_text()
    css_s = float(re.search(r"--spark-d:\s*([\d.]+)s", css).group(1))
    js_ms = int(re.search(r"SPARK_MS\s*=\s*(\d+)", js).group(1))
    assert round(css_s * 1000) == js_ms


# --- SITE-PLAN G1 (2026-11-20): the four pages share no template, so the
# shared frame (footer, masthead) is kept in step by hand. These catch one
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
        # B3: a page's own reading is plain text, the other two are links
        f = re.sub(r'<a class="foot__link">(.*?)</a>', r"\1", f, flags=re.S)
        return re.sub(r"\s+", " ", f).strip()
    base = norm(PAGES[0])
    for path in PAGES[1:]:
        assert norm(path) == base, f"{path}: footer has drifted from index.html's"


def test_masthead_is_the_same_on_all_four_pages():
    def norm(path):
        h = _common(_block(path, r'<header class="masthead">.*?</header>'))
        # each page numbers its own sections (home 01-03, a discipline page 01-05)
        h = re.sub(r'<span class="tools__rule tools__rule--sections".*?</nav>', "</nav>", h, flags=re.S)
        # the current page is marked; the lockup is named for where it goes
        h = re.sub(r'\saria-current="page"', "", h)
        h = re.sub(r'\saria-label="[^"]*"', "", h)
        return re.sub(r"\s+", " ", h).strip()
    base = norm(PAGES[0])
    for path in PAGES[1:]:
        assert norm(path) == base, f"{path}: masthead has drifted from index.html's"
