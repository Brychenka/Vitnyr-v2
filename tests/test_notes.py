"""The notes (NOTES-PLAN.md, 2026-11-20): Igor's LinkedIn posts set as pages,
SITE-PLAN.md H4's library of mistakes. An index at /notes/ and one folder per
note. Most of these exist so a half-added note fails loudly: every note folder
must be in the ledger, the sitemap, the build and the share cards, with its
own head in both languages."""

import json
import re
import xml.etree.ElementTree as ET
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
    assert page.locator('.tools__group--disciplines [aria-current="page"]').count() == 0


@pytest.mark.parametrize("path", PATHS)
def test_every_section_link_has_a_target(open_site, path):
    page, _ = open_site(path=path.lstrip("/"))
    missing = page.evaluate("""() => [...document.querySelectorAll('.masthead a[href^="#"]')]
        .map(a => a.getAttribute('href').slice(1)).filter(id => !document.getElementById(id))""")
    assert missing == []


@pytest.mark.parametrize("path", PATHS)
def test_every_telegram_link_names_english(open_site, path):
    page, _ = open_site(path=path.lstrip("/"))
    links = page.locator('a[href^="https://t.me/yngvil?text="]').all()
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
