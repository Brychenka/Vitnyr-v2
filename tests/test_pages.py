"""The three discipline pages (DISCIPLINE-PAGES-PLAN.md, 2026-10-31): each one
is a real page with its own head, its own share card and its own place in the
sitemap, reached from the home page's doors and the masthead, and written so
that every sentence makes sense to a reader who only wants that discipline."""

import re
import xml.etree.ElementTree as ET
from urllib.parse import unquote

import pytest

from conftest import NARROW, horizontal_overflow

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
    expected = []
    for p in ["/", "/english/", "/chess/", "/climbing/", "/notes/", "/notes/au/", "/notes/noun-verb-stress/"]:
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
def test_only_the_bridge_names_the_other_disciplines(open_site, slug):
    """The rule: every sentence on a discipline page makes sense to someone who
    only wants that discipline. The bridge is the one sanctioned exception, and
    the contact channels' own descriptions (what each profile is about) are a
    second. Checked on rendered text, both languages."""
    for lang in ("en", "ru"):
        page, _ = open_site(path=f"{slug}/", lang=lang)
        text = page.evaluate(
            """() => {
                const main = document.querySelector('main').cloneNode(true);
                main.querySelectorAll('.bridge, .channels, .vh, [hidden]').forEach(e => e.remove());
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
def test_bridge_links_the_other_two_pages(open_site, slug):
    page, _ = open_site(path=f"{slug}/")
    hrefs = sorted(a.get_attribute("href") for a in page.locator(".bridge a").all())
    assert hrefs == sorted(f"/{s}/" for s in PAGES if s != slug)


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


# --- SITE-PLAN B3 (2026-11-20): the footer's three readings are the way into
# each discipline. Each links to its page, except the page you're already on,
# and the language switch must not flatten the link (theme.js rewrites the
# text of any element carrying data-en/data-ru, so those sit on a span inside
# the <a>, never on the <a>'s parent). ---

FOOT_TARGETS = ["/english/", "/chess/", "/climbing/"]


@pytest.mark.parametrize("path,here", [("index.html", None)] + [(f"{s}/", f"/{s}/") for s in PAGES])
def test_footer_readings_link_to_the_other_disciplines(open_site, path, here):
    page, _ = open_site(path=path)

    def hrefs():
        return page.evaluate(
            """() => [...document.querySelectorAll('.foot__notes dd')]
                   .map(dd => { const a = dd.querySelector('a');
                                return a ? a.getAttribute('href') : null; })""")

    expected = [None if t == here else t for t in FOOT_TARGETS]
    assert hrefs() == expected
    # survives a round trip through Russian
    switch = page.locator(".masthead .langswitch")
    switch.click()
    assert re.search("[а-я]", page.locator(".foot__notes dd").first.inner_text())
    assert hrefs() == expected
    switch.click()
    assert hrefs() == expected
    # at rest it reads as the plain text it used to be
    deco = page.evaluate(
        "() => getComputedStyle(document.querySelector('.foot__link .foot__text')).textDecorationLine")
    assert deco == "none"


# --- SITE-PLAN E1 (2026-11-20): every contact section says what happens after
# the message — three plain steps, no prices, in both languages. ---

@pytest.mark.parametrize("path", ["index.html"] + [f"{s}/" for s in PAGES])
def test_contact_says_what_happens_next(open_site, path):
    for lang, first, last in (("en", "You message me", "plan"), ("ru", "Вы пишете мне", "план")):
        page, _ = open_site(path=path, lang=lang)
        items = page.locator("#contact .steps li")
        assert items.count() == 3
        texts = [items.nth(i).inner_text() for i in range(3)]
        assert first in texts[0] and "30" in texts[1] and last in texts[2]
        assert not re.search(r"[$€₽֏]|AMD|USD|руб|драм", " ".join(texts), re.I), "no prices"
        assert page.locator("#steps-title").text_content().strip()


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
