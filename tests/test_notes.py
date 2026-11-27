"""The notes (2026-11-20): Igor's LinkedIn posts set as pages,
SITE-PLAN.md H4's library of mistakes. An index at /notes/ and one folder per
note. Most of these exist so a half-added note fails loudly: every note folder
must be in the ledger, the sitemap, the build and the share cards, with its
own head in both languages."""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

import pytest

from conftest import NARROW, REPO_ROOT, horizontal_overflow

SITE = "https://vitnyrcoach.com"
NOTES = sorted(p.parent.name for p in (REPO_ROOT / "notes").glob("*/index.html"))
PATHS = ["/notes/"] + [f"/notes/{slug}/" for slug in NOTES]
CARD = {"/notes/": "og-notes", **{f"/notes/{s}/": f"og-note-{s}" for s in NOTES}}


def test_there_are_notes():
    assert NOTES, "no note folders under notes/"


@pytest.mark.parametrize("path", PATHS)
def test_notes_page_has_its_own_head_in_both_languages(open_site, site_url, path):
    page, _ = open_site(path=path.lstrip("/"))
    en_title = page.title()
    assert en_title.endswith("— Igor Shatsev")
    assert page.locator('link[rel="canonical"]').get_attribute("href") == SITE + path
    alternates = {a.get_attribute("hreflang"): a.get_attribute("href")
                  for a in page.locator('link[rel="alternate"][hreflang]').all()}
    assert alternates == {"en": SITE + path, "ru": SITE + path + "?lang=ru", "x-default": SITE + path}
    assert page.locator('meta[property="og:url"]').get_attribute("content") == SITE + path
    card = CARD[path]
    for sel in ('meta[property="og:image"]', 'meta[name="twitter:image"]'):
        assert page.locator(sel).get_attribute("content") == f"{SITE}/assets/share/{card}.png"
    # the edge middleware swaps .png for -ru.png on ?lang=ru, so both must exist
    for name in (f"{card}.png", f"{card}-ru.png"):
        res = page.request.get(f"{site_url}/assets/share/{name}")
        assert res.ok and res.headers["content-type"] == "image/png", name

    page, _ = open_site(path=path.lstrip("/"), query="?lang=ru")
    assert page.title() != en_title
    assert re.search("[а-я]", page.title())
    assert page.locator('link[rel="canonical"]').get_attribute("href") == SITE + path + "?lang=ru"


def test_titles_differ_across_every_page(open_site):
    titles = set()
    paths = ["index.html", "english/", "chess/", "climbing/"] + [p.lstrip("/") for p in PATHS]
    for path in paths:
        page, _ = open_site(path=path)
        titles.add(page.title())
    assert len(titles) == len(paths)


def test_every_note_is_in_the_ledger_newest_first(open_site):
    page, _ = open_site(path="notes/")
    hrefs = [a.get_attribute("href") for a in page.locator(".ledger__link").all()]
    assert sorted(hrefs) == sorted(PATHS[1:])
    graph = json.loads(page.locator('script[type="application/ld+json"]').text_content())["@graph"]
    items = next(n for n in graph if n["@type"] == "ItemList")["itemListElement"]
    assert [i["url"] for i in items] == [SITE + h for h in hrefs]


def test_every_notes_page_is_in_the_sitemap_and_the_build(site_url, open_site):
    page, _ = open_site()
    body = page.request.get(f"{site_url}/sitemap.xml").text()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {u.find("s:loc", ns).text for u in ET.fromstring(body).findall("s:url", ns)}
    for path in PATHS:
        assert SITE + path in locs and SITE + path + "?lang=ru" in locs, path
    build = (REPO_ROOT / "build.sh").read_text()
    assert re.search(r"for d in [^;]*\bnotes\b", build), "build.sh doesn't deploy notes/"


@pytest.mark.parametrize("slug", NOTES)
def test_note_json_ld_is_an_article_by_igor(open_site, slug):
    page, _ = open_site(path=f"notes/{slug}/")
    graph = json.loads(page.locator('script[type="application/ld+json"]').text_content())["@graph"]
    types = {n["@type"]: n for n in graph}
    assert set(types) == {"Article", "BreadcrumbList", "Person"}
    assert types["Article"]["author"] == {"@id": f"{SITE}/#igor"}
    assert types["Article"]["url"] == f"{SITE}/notes/{slug}/"
    assert types["Person"]["name"] == "Igor Shatsev"
    assert [i["item"] for i in types["BreadcrumbList"]["itemListElement"]] == \
        [f"{SITE}/", f"{SITE}/notes/", f"{SITE}/notes/{slug}/"]


@pytest.mark.parametrize("path", PATHS)
def test_masthead_and_footer_match_the_english_page(open_site, path):
    """The four-page rule, extended: the notes pages carry copies of the
    English page's masthead and footer, so they must not drift."""
    def parts(p):
        return p.evaluate("""() => ({
            lockup: document.querySelector('.lockup').outerHTML,
            disciplines: [...document.querySelectorAll('.tools__group--disciplines a')]
                .map(a => a.getAttribute('href')),
            util: document.querySelector('.tools__group--util').outerHTML,
            foot: document.querySelector('.foot__in').innerText,
        })""")
    english, _ = open_site(path="english/")
    page, _ = open_site(path=path.lstrip("/"))
    a, b = parts(english), parts(page)
    assert a == b
    # no discipline is current on a notes page; the Notes link is (K8)
    current = page.locator('.tools__group--disciplines [aria-current="page"]')
    assert current.count() == 1
    assert current.get_attribute("href") == "/notes/"


@pytest.mark.parametrize("path", PATHS)
def test_every_section_link_has_a_target(open_site, path):
    page, _ = open_site(path=path.lstrip("/"))
    missing = page.evaluate("""() => [...document.querySelectorAll('.masthead a[href^="#"]')]
        .map(a => a.getAttribute('href').slice(1)).filter(id => !document.getElementById(id))""")
    assert missing == []


@pytest.mark.parametrize("path", PATHS)
def test_every_telegram_link_names_english(open_site, path):
    page, _ = open_site(path=path.lstrip("/"))
    links = page.locator('a[href^="https://t.me/vitnyr?text="]').all()
    assert links
    for a in links:
        for attr in ("href", "data-href-en"):
            v = a.get_attribute(attr)
            if v:
                assert "English" in unquote(v), v
        ru = a.get_attribute("data-href-ru")
        if ru:
            assert "английскому" in unquote(ru), ru


@pytest.mark.parametrize("slug", NOTES)
def test_note_shows_the_mistake_and_the_fix(open_site, slug):
    """On a note the mistake is the subject, so the specimen reveal (which
    hides the wrong line on /english/) must leave both lines showing."""
    page, _ = open_site(path=f"notes/{slug}/")
    page.wait_for_timeout(300)
    if page.locator(".note-spec").count() == 0:
        # A note may leave out the pair when its table's first row says the
        # same (actual, 2026-11-28); its figure then carries both inks.
        fig = page.locator(".note-fig")
        assert fig.locator("del.mark--specimen").count() >= 1
        assert fig.locator("ins.mark--target").count() >= 1
        assert fig.is_visible()
        return
    for cls in ("wrong", "right"):
        line = page.locator(f".note-spec .line-spec.{cls}")
        assert line.count() == 1 and line.is_visible(), cls
    assert page.locator(".note-spec .spec__prompt").count() == 0
    assert page.locator(".note-spec del").count() == 1
    assert page.locator(".note-spec ins").count() == 1


@pytest.mark.parametrize("path", PATHS)
def test_notes_page_is_clean_at_phone_width_in_russian_dark(open_site, console_guard, path):
    page, _ = open_site(path=path.lstrip("/"), lang="ru", theme="dark", viewport=NARROW,
                        has_touch=True, reduced_motion=True)
    console_guard.watch(page)
    page.reload()
    page.wait_for_timeout(500)
    assert not horizontal_overflow(page)
    assert page.evaluate("document.documentElement.scrollWidth") == page.evaluate("innerWidth")
    hidden = page.evaluate(
        "[...document.querySelectorAll('.reveal')].filter(e => e.offsetParent"
        " && parseFloat(getComputedStyle(e).opacity) < 0.9).length")
    assert hidden == 0
    console_guard.assert_clean()


@pytest.mark.parametrize("path", PATHS)
def test_notes_page_reads_without_javascript(open_site, path):
    page, _ = open_site(path=path.lstrip("/"), java_script_enabled=False)
    h1 = page.locator("h1.hero__title [data-l='en']")
    assert h1.is_visible()
    # what JS normally un-hides: every .reveal, and the hero's masked lines
    hidden = page.evaluate(
        "[...document.querySelectorAll('main .reveal, main .line__inner')].filter(e => e.offsetParent"
        " && (parseFloat(getComputedStyle(e).opacity) < 0.9"
        "     || getComputedStyle(e).transform !== 'none')).length")
    assert hidden == 0


def test_note_links_in_the_pagers_resolve(open_site):
    for slug in NOTES:
        page, _ = open_site(path=f"notes/{slug}/")
        for href in [a.get_attribute("href") for a in page.locator(".note-pager a").all()]:
            assert href == "/notes/" or href.strip("/").split("/")[-1] in NOTES, (slug, href)


def test_english_page_links_to_the_notes(open_site):
    page, _ = open_site(path="english/")
    assert page.locator('#specimen a[href="/notes/"]').count() == 1


def test_the_notes_are_up_to_date_with_their_generator(tmp_path):
    """notes/ is generated by tools/notes/build.py from the
    note modules and english/index.html's frame. Re-run it on a copy of the
    inputs; the committed pages must come out identical, so nobody can edit
    the English page's frame (or a note) and forget to rebuild."""
    import shutil
    import subprocess
    import sys
    for rel in ("english/index.html", "sitemap.xml", "assets/share/share-card.html"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / rel, tmp_path / rel)
    shutil.copytree(REPO_ROOT / "tools" / "notes", tmp_path / "tools" / "notes",
                    ignore=shutil.ignore_patterns("__pycache__"))
    subprocess.run([sys.executable, "build.py"], cwd=tmp_path / "tools" / "notes", check=True,
                   capture_output=True)
    built = sorted(p.relative_to(tmp_path) for p in (tmp_path / "notes").rglob("index.html"))
    committed = sorted(p.relative_to(REPO_ROOT) for p in (REPO_ROOT / "notes").rglob("index.html"))
    assert built == committed, "a note page exists without its module, or the other way round"
    for rel in built + [Path("sitemap.xml"), Path("assets/share/share-card.html")]:
        assert (tmp_path / rel).read_text() == (REPO_ROOT / rel).read_text(), \
            f"{rel} is stale: run python3 tools/notes/build.py"


# ---------------------------------------------------------------------------
# The notes redesign (2026-11-27, feature/notes-redesign): the library is the
# page, the reader's own mistake leads each row, IPA is set in one face, the
# Russian title keeps its weight and a note doesn't jump while it loads.

@pytest.mark.parametrize("lang", ["en", "ru"])
@pytest.mark.parametrize("phone", [False, True])
def test_the_first_note_is_on_the_first_screen(open_site, lang, phone):
    """No booking ask or second heading above the list: the first row's
    mistake line is fully visible without scrolling, above the phone's
    fixed message bar."""
    kw = dict(viewport=NARROW, has_touch=True) if phone else dict(viewport={"width": 1280, "height": 800})
    page, _ = open_site(path="notes/", lang=lang, reduced_motion=True, **kw)
    page.wait_for_timeout(300)
    bottom = page.evaluate("document.querySelector('.ledger__spec').getBoundingClientRect().bottom")
    limit = page.evaluate("""(() => { const d = document.querySelector('.dock');
        return d && getComputedStyle(d).display !== 'none' ? d.getBoundingClientRect().top : innerHeight })()""")
    assert bottom <= limit, (bottom, limit)


def test_the_index_asks_for_nothing_above_the_notes(open_site):
    page, _ = open_site(path="notes/")
    assert page.locator('#hero a[href*="t.me"], #hero .page-cta, #hero .scrollcue').count() == 0
    assert page.locator("#notes .sec__head").count() == 0


def test_ledger_rows_lead_with_the_mistake_and_say_which_line_is_which(open_site):
    page, _ = open_site(path="notes/")
    for row in page.locator(".ledger__link").all():
        order = row.evaluate("e => [...e.querySelector('.ledger__main').children].map(c => c.className)")
        assert order == ["ledger__spec", "ledger__title"], order
        text = row.locator(".ledger__spec").inner_text()
        assert "Incorrect:" in row.locator(".ledger__spec").text_content() and \
               "Correct:" in row.locator(".ledger__spec").text_content(), text
        assert row.locator("time, .ledger__date").count() == 0


@pytest.mark.parametrize("path", ["notes/", "notes/au/"])
def test_every_transcription_renders_in_one_face(open_site, path):
    """None of the site's font files carry IPA, so a transcription left to
    per-glyph fallback mixed faces inside one word (and set the au tile's ɔː
    in Times). Each .ipa must render in a single face."""
    page, ctx = open_site(path=path)
    cdp = ctx.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    ids = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": ".ipa"})["nodeIds"]
    assert ids, "no .ipa on " + path
    rendered = 0
    for node in ids:
        fonts = {f["familyName"] for f in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]}
        assert len(fonts) <= 1, fonts     # none: the hidden language's twin
        rendered += len(fonts)
    assert rendered, "no transcription rendered on " + path


@pytest.mark.parametrize("slug", NOTES)
def test_the_russian_title_keeps_its_second_line_at_full_size(open_site, slug):
    """html[lang=ru] .hero__title em is .5em for the home page's long line;
    the notes' endings are a word or two and must match the English size."""
    sizes = {}
    for lang in ("en", "ru"):
        page, _ = open_site(path=f"notes/{slug}/", lang=lang, viewport=NARROW, has_touch=True)
        sizes[lang] = page.evaluate(
            f"parseFloat(getComputedStyle(document.querySelector('.hero__title [data-l=\"{lang}\"] em')).fontSize)")
    assert sizes["ru"] == sizes["en"], sizes


def test_note_pages_preload_inter_and_the_index_does_not():
    """A note's standfirst quotes words in mono; a late Inter swap rewrapped
    it and moved everything below (CLS up to 0.14). The index never jumped
    and its hero waits for every font, so a preload there only slowed it."""
    rx = r'<link rel="preload" href="/assets/fonts/(inter-[a-z]+-v\d+)\.woff2" as="font" type="font/woff2" crossorigin>'
    assert not re.findall(rx, (REPO_ROOT / "notes" / "index.html").read_text())
    css = (REPO_ROOT / "style.css").read_text()
    for slug in NOTES:
        found = re.findall(rx, (REPO_ROOT / "notes" / slug / "index.html").read_text())
        assert sorted(found) == ["inter-cyrillic-v20", "inter-latin-v20"], (slug, found)
        for name in found:   # the preload must be the very file the CSS asks for
            assert f"url(assets/fonts/{name}.woff2)" in css, name


# ---------------------------------------------------------------------------
# Inside a note (2026-11-27, feature/notes-inside): the ending is a reading
# page's close, not a landing page's; the hero reads top down; labels are
# wayfinding; transcriptions hold together.

@pytest.mark.parametrize("path", PATHS)
def test_a_notes_page_ends_on_a_short_contact(open_site, path):
    """The English page's contact, cut down: unnumbered (it is not chapter
    04 of the note), no engraving, the CTA smaller than the page's title,
    the three channels kept in their order."""
    page, _ = open_site(path=path.strip("/") + "/", viewport={"width": 1280, "height": 800}, reduced_motion=True)
    c = page.locator("#contact")
    assert "sec--contact-note" in c.get_attribute("class")
    assert c.locator(".vig, .label .num").count() == 0
    big, title = page.evaluate("""[parseFloat(getComputedStyle(document.querySelector('.contact__big')).fontSize),
                                   parseFloat(getComputedStyle(document.querySelector('.hero__title')).fontSize)]""")
    assert big < title, (big, title)
    assert c.evaluate("e => e.offsetHeight") < 800
    assert c.locator(".contact__portrait img").count() == 2          # one per language, as on the four pages
    names = [n.strip() for n in c.locator(".channels .ch__k").all_inner_texts()]
    assert names == ["Telegram", "LinkedIn", "Instagram"], names
    assert "t.me/vitnyr" in c.locator(".contact__cta").get_attribute("href")


@pytest.mark.parametrize("lang", ["en", "ru"])
@pytest.mark.parametrize("path", PATHS)
def test_every_notes_ending_says_what_happens_next(open_site, path, lang):
    """CLAUDE.md: every contact section says what happens next (message,
    30-minute trial, a plan). The notes' own ledes stopped at the trial."""
    page, _ = open_site(path=path.strip("/") + "/", lang=lang)
    text = page.locator("#contact .sec__lede").inner_text()
    assert "30" in text and ("plan" in text if lang == "en" else "план" in text), text


def test_the_index_says_linkedin_once():
    """The "I also write about English on LinkedIn" line sat right above the
    channels row, which says the same ("I write about English here")."""
    html = (REPO_ROOT / "notes" / "index.html").read_text()
    main = html[html.index("<main"):html.index("</main>")]
    assert "ledger__more" not in main
    assert main.count('href="https://www.linkedin.com/in/vitnyrcoach/"') == 1


@pytest.mark.parametrize("lang", ["en", "ru"])
@pytest.mark.parametrize("slug", NOTES)
def test_a_notes_figure_starts_on_the_first_phone_screen(open_site, slug, lang):
    """Phone order: standfirst, figure, then who wrote it. The figure used
    to start under the message bar, after two lines of by-line."""
    page, _ = open_site(path=f"notes/{slug}/", lang=lang, viewport=NARROW, has_touch=True, reduced_motion=True)
    page.wait_for_timeout(300)
    order = page.evaluate("[...document.querySelector('#hero .hero__foot').children].map(e => e.className.split(' ')[0])")
    assert order == ["page-hero__text", "note-fig", "note-meta"], order
    top = page.evaluate("document.querySelector('#hero .note-fig').getBoundingClientRect().top")
    limit = page.evaluate("""(() => { const d = document.querySelector('.dock');
        return d && getComputedStyle(d).display !== 'none' ? d.getBoundingClientRect().top : innerHeight })()""")
    assert top + 40 <= limit, (top, limit)


@pytest.mark.parametrize("slug", NOTES)
def test_a_notes_text_starts_level_with_its_figure(open_site, slug):
    """From 900px the standfirst sits at the top of its column, level with
    the figure; bottom alignment left a hole under the title whenever the
    figure was the taller side ("Could you")."""
    page, _ = open_site(path=f"notes/{slug}/", viewport={"width": 1280, "height": 800}, reduced_motion=True)
    page.wait_for_timeout(300)
    stand, fig = page.evaluate("""[document.querySelector('#hero .stand[data-l=en]').getBoundingClientRect().top,
                                   document.querySelector('#hero .note-fig').getBoundingClientRect().top]""")
    assert abs(stand - fig) <= 12, (stand, fig)


@pytest.mark.parametrize("slug", NOTES)
def test_section_labels_are_wayfinding_and_never_repeat_their_heading(open_site, slug):
    page, _ = open_site(path=f"notes/{slug}/")
    labels, heads = [], []
    for sid in ("words", "why", "practice"):
        sec = page.locator(f"#{sid}")
        labels.append(sec.locator(".label").inner_text().split("\n")[-1].strip().lower())
        heads.append(sec.locator('.sec__head h2[data-l="en"]').inner_text().strip().lower().rstrip("."))
    assert labels == ["the fix", "why it happens", "practice"], labels
    assert all(l != h for l, h in zip(labels, heads)), list(zip(labels, heads))


@pytest.mark.parametrize("width", [320, 375])
@pytest.mark.parametrize("lang", ["en", "ru"])
def test_a_transcription_never_breaks_across_lines(open_site, width, lang):
    """On a phone /ɔː/ broke into "/" at a line end and "ɔː/" on the next.
    Each visible .ipa is one line box, and the au table still fits 320px."""
    page, _ = open_site(path="notes/au/", lang=lang, viewport={"width": width, "height": 700},
                        has_touch=True, reduced_motion=True)
    # one rect per inline fragment (the green ɔː is its own span), so the
    # test is that every fragment sits on the same line
    broken = page.evaluate("""[...document.querySelectorAll('.ipa')].filter(e => e.offsetParent)
        .filter(e => { const t = [...e.getClientRects()].map(r => Math.round(r.top));
                       return Math.max(...t) - Math.min(...t) > 2; }).map(e => e.textContent)""")
    assert not broken, broken
    assert not horizontal_overflow(page)


def test_the_fix_in_the_au_table_is_not_the_columns_grey(open_site):
    """The green ɔː in the sound column sat on --fg2 grey and read as one
    colour in both themes; the column is set in the text ink."""
    for scheme in ("light", "dark"):
        page, _ = open_site(path="notes/au/", color_scheme=scheme)
        cell, mark = page.evaluate("""[getComputedStyle(document.querySelector('.register__ipa')).color,
            getComputedStyle(document.querySelector('.register__ipa .mark--target')).color]""")
        assert cell == page.evaluate("getComputedStyle(document.body).color"), (scheme, cell)
        assert mark != cell, scheme


def test_the_au_tiles_carry_no_scrabble_scores():
    html = (REPO_ROOT / "notes" / "au" / "index.html").read_text()
    assert "tile__v" not in html and "tile__v" not in (REPO_ROOT / "style.css").read_text()


def test_the_generator_fails_loudly_when_the_contact_changes_shape(tmp_path):
    """note_contact() cuts pieces out of the English page's contact. If one
    is gone (here: the engraving), the build must stop, not quietly ship
    the full section on every note."""
    import shutil
    import subprocess
    import sys
    for rel in ("english/index.html", "sitemap.xml", "assets/share/share-card.html"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / rel, tmp_path / rel)
    shutil.copytree(REPO_ROOT / "tools" / "notes", tmp_path / "tools" / "notes",
                    ignore=shutil.ignore_patterns("__pycache__"))
    en = tmp_path / "english" / "index.html"
    en.write_text(en.read_text().replace("vig--empty-chair", "vig--elsewhere"))
    run = subprocess.run([sys.executable, "build.py"], cwd=tmp_path / "tools" / "notes", capture_output=True, text=True)
    assert run.returncode != 0 and "note_contact" in (run.stdout + run.stderr), run


def test_a_notes_test_scores_and_names_its_note_in_the_message(open_site):
    """The actual note's practice is the English page's test (initEarTest).
    After the check, the Telegram message carries the score and the note's
    name, so Igor can tell which note a message came from."""
    page, _ = open_site(path="notes/actual/")
    picks = page.locator("#practice .ear__pick")
    assert picks.count() == 8
    assert page.locator("#practice.sec--ear").count() == 1   # hidden without JS
    right = page.locator('#practice .ear__item[data-right="true"] .ear__pick')
    for i in range(right.count()):
        right.nth(i).click()
    page.locator("#practice .ear__check").click()
    assert page.locator("#practice .ear__score").inner_text().startswith("You judged 8 of 8")
    msg = unquote(page.locator("#practice .ear__send").get_attribute("href"))
    assert "“actual”" in msg and "8/8" in msg
