"""The three discipline pages (2026-10-31): each one
is a real page with its own head, its own share card and its own place in the
sitemap, reached from the home page's doors and the masthead, and written so
that every sentence makes sense to a reader who only wants that discipline."""

import re
import xml.etree.ElementTree as ET
from urllib.parse import unquote

import pytest

from conftest import NARROW, REPO_ROOT, horizontal_overflow

SITE = "https://vitnyrcoach.com"
PAGES = ["english", "chess", "climbing"]
OTHERS = {
    "english": ("chess", "climb", "шахмат", "скалолаз"),
    "chess": ("english", "climb", "английск", "скалолаз"),
    "climbing": ("english", "chess", "английск", "шахмат"),
}


@pytest.mark.parametrize("slug", PAGES)
def test_page_has_its_own_head_in_both_languages(open_site, slug):
    page, _ = open_site(path=f"{slug}/")
    en_title = page.title()
    assert "Igor Shatsev" in en_title
    canonical = page.locator('link[rel="canonical"]').get_attribute("href")
    assert canonical == f"{SITE}/{slug}/"
    alternates = {
        a.get_attribute("hreflang"): a.get_attribute("href")
        for a in page.locator('link[rel="alternate"][hreflang]').all()
    }
    assert alternates == {"en": f"{SITE}/{slug}/", "ru": f"{SITE}/{slug}/?lang=ru",
                          "x-default": f"{SITE}/{slug}/"}
    assert page.locator('meta[property="og:url"]').get_attribute("content") == f"{SITE}/{slug}/"

    page, _ = open_site(path=f"{slug}/", query="?lang=ru")
    assert page.title() != en_title
    assert re.search("[а-я]", page.title())
    assert page.locator('link[rel="canonical"]').get_attribute("href") == f"{SITE}/{slug}/?lang=ru"


def test_titles_differ_across_all_four_pages(open_site):
    titles = set()
    for path in ["index.html"] + [f"{s}/" for s in PAGES]:
        page, _ = open_site(path=path)
        titles.add(page.title())
    assert len(titles) == 4


@pytest.mark.parametrize("slug", PAGES)
def test_page_share_card_is_its_own_and_actually_served(open_site, site_url, slug):
    page, _ = open_site(path=f"{slug}/")
    for sel in ('meta[property="og:image"]', 'meta[name="twitter:image"]'):
        assert page.locator(sel).get_attribute("content") == f"{SITE}/assets/share/og-{slug}.png"
    for name in (f"og-{slug}.png", f"og-{slug}-ru.png"):
        res = page.request.get(f"{site_url}/assets/share/{name}")
        assert res.ok and res.headers["content-type"] == "image/png", name


@pytest.mark.parametrize("slug", PAGES)
def test_page_json_ld_is_a_service_under_the_home_person(open_site, slug):
    page, _ = open_site(path=f"{slug}/")
    import json
    graph = json.loads(page.locator('script[type="application/ld+json"]').text_content())["@graph"]
    types = {n["@type"]: n for n in graph}
    assert set(types) == {"WebPage", "BreadcrumbList", "Service", "Person"}
    assert types["Service"]["@id"] == f"{SITE}/{slug}/#service"
    assert types["Service"]["provider"] == {"@id": f"{SITE}/#igor"}
    assert types["Person"]["name"] == "Igor Shatsev"
    assert [i["item"] for i in types["BreadcrumbList"]["itemListElement"]] == [f"{SITE}/", f"{SITE}/{slug}/"]
    # the home page's Person offers the same Service node
    home, _ = open_site()
    assert f'"@id": "{SITE}/{slug}/#service"' in home.content()


def test_sitemap_lists_every_page_in_two_languages(site_url, open_site):
    """Four pages, then the notes (feature/notes, 2026-11-20: the index and
    each note, newest first), each in both languages."""
    page, _ = open_site()
    body = page.request.get(f"{site_url}/sitemap.xml").text()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    root = ET.fromstring(body)
    locs = [u.find("s:loc", ns).text for u in root.findall("s:url", ns)]
    # the notes in the ledger's own order (tools/notes/build.py writes both)
    ledger = re.findall(r'class="ledger__link" href="([^"]+)"', (REPO_ROOT / "notes" / "index.html").read_text())
    assert ledger, "notes/index.html has no ledger"
    expected = []
    for p in ["/", "/english/", "/chess/", "/climbing/", "/notes/"] + ledger:
        expected += [SITE + p, SITE + p + "?lang=ru"]
    assert locs == expected
    for u in root.findall("s:url", ns):
        langs = [l.get("hreflang") for l in u.findall("x:link", ns)]
        assert langs == ["en", "ru", "x-default"]


def test_home_doors_and_mark_lead_to_the_three_pages(open_site):
    page, _ = open_site()
    for slug in PAGES:
        assert page.locator(f'#origin .door[href="/{slug}/"]').count() == 1
        assert page.locator(f'#origin .origin__hit[href="/{slug}/"]').count() == 1
        assert page.locator(f'.hero__title [data-l="en"] a.hero__door[href="/{slug}/"]').count() == 1


@pytest.mark.parametrize("slug", PAGES)
def test_masthead_links_the_pages_and_marks_the_current_one(open_site, slug):
    page, _ = open_site(path=f"{slug}/")
    # a.tool--icon: SITE-PLAN C4 put the "Photos" text link in this group too
    links = page.locator(".tools__group--disciplines a.tool--icon")
    assert links.count() == 3
    hrefs = [a.get_attribute("href") for a in links.all()]
    assert hrefs == ["/english/", "/chess/", "/climbing/"]
    current = page.locator('.tools__group--disciplines a[aria-current="page"]')
    assert current.count() == 1 and current.get_attribute("href") == f"/{slug}/"
    assert page.locator(".masthead .lockup").get_attribute("href") == "/"
    assert page.locator("a.eyebrow__home").get_attribute("href") == "/"


@pytest.mark.parametrize("slug", PAGES)
def test_page_body_never_names_the_other_disciplines(open_site, slug):
    """The rule: every sentence on a discipline page makes sense to someone who
    only wants that discipline; the masthead's icons are the way to the other
    two. The contact channels' own descriptions (what each profile is about)
    are the one exception. Checked on rendered text, both languages."""
    for lang in ("en", "ru"):
        page, _ = open_site(path=f"{slug}/", lang=lang)
        text = page.evaluate(
            """() => {
                const main = document.querySelector('main').cloneNode(true);
                main.querySelectorAll('.channels, .vh, [hidden]').forEach(e => e.remove());
                document.body.appendChild(main);
                main.style.position = 'absolute';
                const t = main.innerText;
                main.remove();
                return t.toLowerCase();
            }"""
        )
        for word in OTHERS[slug]:
            assert word not in text, (slug, lang, word)


@pytest.mark.parametrize("slug", PAGES)
def test_page_ends_on_contact_with_no_detour(open_site, slug):
    """No block between the last section and contact sends the reader to
    another discipline (the bridge was removed 2026-11-23)."""
    page, _ = open_site(path=f"{slug}/")
    assert page.locator(".bridge").count() == 0
    prev = page.evaluate("document.getElementById('contact').previousElementSibling.tagName")
    assert prev == "SECTION"
    others = [f"/{s}/" for s in PAGES if s != slug]
    hrefs = page.evaluate("[...document.querySelectorAll('main a')].map(a => a.getAttribute('href'))")
    assert not [h for h in hrefs if h in others]


@pytest.mark.parametrize("slug,word", [("english", "English"), ("chess", "chess"), ("climbing", "climbing")])
def test_every_telegram_link_names_the_discipline(open_site, slug, word):
    page, _ = open_site(path=f"{slug}/")
    hrefs = {a.get_attribute("href") for a in page.locator('a[href^="https://t.me/yngvil?text="]').all()}
    assert hrefs, "no Telegram links"
    for h in hrefs:
        assert word in unquote(h), h


@pytest.mark.parametrize("slug", PAGES)
def test_page_is_clean_at_phone_width_in_russian_dark(open_site, console_guard, slug):
    page, _ = open_site(path=f"{slug}/", lang="ru", theme="dark", viewport=NARROW,
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


@pytest.mark.parametrize("slug", PAGES)
def test_page_has_no_testimonials_it_cannot_back(open_site, slug):
    """Real material only: the nine testimonials are all from English
    students, so only /english/ carries them. Chess and climbing keep a
    PLACEHOLDER comment until real quotes exist, never an invented one."""
    page, _ = open_site(path=f"{slug}/")
    voices = page.locator(".sec--voices").count()
    if slug == "english":
        assert voices == 1
    else:
        assert voices == 0
        assert "PLACEHOLDER" in page.content()


# --- 2026-11-21: the footer's three readings (B3) are gone. What is left is
# "Your move." and the colophon, with the engraved clock standing on the
# colophon's rule at the right edge, on every page, at both widths. ---

@pytest.mark.parametrize("viewport", [NARROW, None], ids=["375", "1280"])
@pytest.mark.parametrize("path", ["index.html"] + [f"{s}/" for s in PAGES])
def test_footer_clock_stands_on_the_colophon_rule(open_site, path, viewport):
    page, _ = open_site(path=path, viewport=viewport, has_touch=viewport is NARROW)
    assert page.locator(".foot__notes, .foot__link").count() == 0
    geo = page.evaluate(
        """() => { const r = s => document.querySelector(s).getBoundingClientRect();
                   const c = r('.foot .vig--chess-clock'), b = r('.foot__base');
                   return { gap: b.top - c.bottom, right: b.right - c.right,
                            rule: getComputedStyle(document.querySelector('.foot__base')).borderTopStyle }; }""")
    assert abs(geo["gap"]) < 1 and abs(geo["right"]) < 1, geo
    assert geo["rule"] == "solid"
    assert not horizontal_overflow(page)


# --- SITE-PLAN E1 (2026-11-20): every contact section says what happens after
# the message (message, a free 30-minute trial, then a plan), no prices, in
# both languages. Since 2026-11-24 it is said once, in the contact text; the
# separate three-step strip repeated it and was cut. ---

@pytest.mark.parametrize("path", ["index.html"] + [f"{s}/" for s in PAGES])
def test_contact_says_what_happens_next(open_site, path):
    for lang, trial, plan in (("en", "30-minute trial", "agree on a plan"),
                              ("ru", "30 минут", "составляем план")):
        page, _ = open_site(path=path, lang=lang)
        text = page.locator("#contact").inner_text()
        assert trial in text and plan in text, (path, lang)
        assert page.locator("#contact .steps").count() == 0
        assert not re.search(r"[$€₽֏]|AMD|USD|руб|драм", text, re.I), "no prices"


# --- SITE-PLAN G3/G4 (2026-11-20): GSAP, Lenis and the fonts are served from
# the site; loading a page asks no third party for anything. ---

@pytest.mark.parametrize("path", ["index.html"] + [f"{s}/" for s in PAGES])
@pytest.mark.parametrize("lang", ["en", "ru"])
def test_pages_load_nothing_from_third_parties(open_site, site_url, path, lang):
    page, ctx = open_site(path=path, lang=lang)
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    page.reload(wait_until="networkidle")
    outside = sorted({u.split("/")[2] for u in seen if not u.startswith(site_url)})
    assert outside == [], outside
    assert "lora-ready" in page.locator("html").get_attribute("class")   # the wordmark's font arrived
    fonts = {u.rsplit("/", 1)[1] for u in seen if "/assets/fonts/" in u}
    assert any(f.startswith("lora-latin") for f in fonts)
    if lang == "ru":
        assert any(f.startswith("lora-cyrillic") for f in fonts)
