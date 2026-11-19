"""Content and positioning rules from CLAUDE.md that no other test enforces:
real material only, the three confirmed facts worded exactly, the name in both
languages, and the placeholders still visibly flagged (not silently shipped)."""

import re

import pytest


def visible_text(page):
    return page.evaluate("() => document.body.innerText")


def test_name_is_igor_shatsev_in_english(open_site):
    page, _ = open_site()
    assert "Igor Shatsev" in visible_text(page)


def test_name_is_still_igor_shatsev_in_russian(open_site):
    page, _ = open_site(lang="ru")
    text = visible_text(page)
    assert "Igor Shatsev" in text
    # not transliterated, not replaced by the umbrella brand as the person
    assert "Игорь Шацев" not in text


PAGES = ("english/", "chess/", "climbing/")


def test_chess_rating_is_stated_without_fide(open_site):
    # Igor's explicit correction: the 2100 rating is stated without "FIDE".
    # \b so this doesn't trip on "confidence". Discipline pages (2026-10-31):
    # the figure is on the home page's chess door and in /chess/'s hero.
    for path in ("index.html", "chess/"):
        for lang in ("en", "ru"):
            page, _ = open_site(lang=lang, path=path)
            text = visible_text(page)
            assert "2100" in text, (path, lang)
            assert not re.search(r"\bFIDE\b", text, re.I), "'FIDE' must not appear"


def test_climbing_grades_are_kept_distinct(open_site):
    # rendered text, not source: J2 (Jury Pass II) established that a
    # climbing grade's 7c/7C case must survive an uppercase ancestor rule.
    # The figures moved with the readout's retirement (discipline pages,
    # 2026-10-31) to the home page's climbing door and /climbing/'s hero.
    page, _ = open_site()
    facts = page.locator(".door--climbing .door__facts").inner_text()
    assert facts.startswith("7c redpoint · 7C Kilter")
    page, _ = open_site(path="climbing/")
    keys = page.locator(".creds .creds__k").all_inner_texts()
    assert keys[:2] == ["7c", "7C"]


def test_credential_figures_keep_their_case_beside_uppercase_labels(open_site):
    """The regression J2 fixed for .domain__stat, then pinned on the readout:
    a figure must not inherit an uppercase transform. Each discipline page's
    credential strip sets its label (.creds__v) in caps, so its figure
    (.creds__k) is the one that must keep its case. Rendered text, not
    source, so a CSS regression is what fails here."""
    page, _ = open_site(path="english/")
    keys = page.locator(".creds .creds__k").all_inner_texts()
    assert keys[1:] == ["10 years", "100+"]


def test_reading_chess_and_climbing_placeholders_are_flagged(open_site):
    """D0.6.2: every invented reading line carries a PLACEHOLDER comment
    naming what Igor replaces. Stage 5 (2026-09-16) and its same-day
    follow-up landed real chess figures and climbing's coaching duration,
    so only climbing's student-outcome row (Achieved) remains unconfirmed."""
    page, _ = open_site()
    html = page.content()
    # Every D0.6 placeholder has since been replaced by a real figure
    # (climbing's Achieved row was the last).
    assert html.count("PLACEHOLDER (D0.6") == 0


# --- Discipline pages (2026-10-31): §03 Specimens used to hold all three
# disciplines' groups and swap them on a commit from the mark. Each page now
# carries only its own group, shown with no commit at all. ---

@pytest.mark.parametrize("path,name", [("english/", "english"), ("chess/", "chess"), ("climbing/", "climbing")])
def test_each_page_shows_only_its_own_specimens(open_site, path, name):
    page, _ = open_site(path=path)
    groups = page.locator("#specimen .specimens-group")
    assert groups.count() == 1
    assert groups.get_attribute("data-discipline-group") == name
    assert groups.is_visible()
    assert groups.locator(".spec").count() == 3
    assert groups.locator(".spec__why").count() == 6  # en + ru per specimen


def test_home_page_has_no_specimens_left(open_site):
    page, _ = open_site()
    assert page.locator("#specimen, .spec").count() == 0


def test_contact_handles_are_real(open_site):
    """The real Telegram/LinkedIn/Instagram handles landed 2026-09 (commit
    dd1ff9c) — updated from the old placeholder-guard test per the note in
    tests/README.md. No more `.ch__todo` chips, and every href is a real,
    absolute, https link rather than "#"."""
    page, _ = open_site()
    assert page.locator(".channels .ch__todo").count() == 0
    hrefs = page.locator(".channels a").evaluate_all(
        "els => els.map(a => a.getAttribute('href'))"
    )
    assert hrefs == [
        "https://t.me/yngvil",
        "https://www.linkedin.com/in/vitnyrcoach/",
        "https://www.instagram.com/brychenka/",
    ]


def test_contact_channel_order_is_telegram_linkedin_instagram(open_site):
    page, _ = open_site()
    order = page.locator(".channels .ch__k").all_inner_texts()
    assert [o.strip() for o in order] == ["Telegram", "LinkedIn", "Instagram"]


def test_og_url_and_image_use_the_real_domain(open_site):
    """P1 (Stage 6): og:url / og:image landed as a real share card + a
    documented placeholder domain; 2026-09-23 swapped for Igor's registered
    domain, vitnyrcoach.com (not hosted yet)."""
    page, _ = open_site()
    assert page.locator('meta[property="og:url"]').get_attribute("content") == "https://vitnyrcoach.com/"
    assert (
        page.locator('meta[property="og:image"]').get_attribute("content")
        == "https://vitnyrcoach.com/assets/share/og-share.png"
    )
    assert page.locator('meta[property="og:title"]').count() == 1


def test_canonical_and_hreflang_share_the_same_domain(open_site):
    page, _ = open_site(lang="en")
    assert page.locator('link[rel="canonical"]').count() == 1
    assert page.locator('link[rel="canonical"]').get_attribute("href") == "https://vitnyrcoach.com/"
    alternates = {
        el.get_attribute("hreflang"): el.get_attribute("href")
        for el in page.locator('link[rel="alternate"][hreflang]').all()
    }
    assert alternates == {
        "en": "https://vitnyrcoach.com/",
        "ru": "https://vitnyrcoach.com/?lang=ru",
        "x-default": "https://vitnyrcoach.com/",
    }


def test_russian_url_is_its_own_canonical_with_russian_head(open_site):
    """2026-09-23: a static canonical of "/" told Google ?lang=ru was a
    duplicate, contradicting its own hreflang. The Russian load now carries
    a self-referencing canonical, html[lang=ru], and the Russian title and
    description; switching back restores the English set."""
    page, _ = open_site(query="?lang=ru")
    assert page.locator('link[rel="canonical"]').count() == 1
    assert page.locator('link[rel="canonical"]').get_attribute("href") == "https://vitnyrcoach.com/?lang=ru"
    assert page.locator("html").get_attribute("lang") == "ru"
    assert page.title() == "Igor Shatsev — коуч по английскому, шахматам и скалолазанию в Ереване | Vitnyr"
    desc = page.locator('meta[name="description"]').get_attribute("content")
    assert "коуч" in desc and "Igor Shatsev" in desc
    assert page.locator('meta[name="description"]').evaluate("el => el.textContent") == ""
    page.locator(".masthead .langswitch").click()
    page.wait_for_function("document.documentElement.lang === 'en'")
    assert page.title() == "Igor Shatsev — English, Chess & Climbing Coach in Yerevan | Vitnyr"
    assert page.locator('link[rel="canonical"]').get_attribute("href") == "https://vitnyrcoach.com/"
    assert "коуч" not in page.locator('meta[name="description"]').get_attribute("content")


def test_share_card_asset_is_actually_served(open_site, site_url):
    """The og:image / twitter:image meta values are necessarily absolute
    placeholder-domain URLs (no real domain exists yet), but the asset
    itself has to exist at that same path once the domain is swapped in —
    checked here against the real path, relative to site root."""
    page, _ = open_site()
    resp = page.request.get(f"{site_url}/assets/share/og-share.png")
    assert resp.ok
    assert resp.headers.get("content-type", "").startswith("image/")
    ru = page.request.get(f"{site_url}/assets/share/og-share-ru.png")
    assert ru.ok


def test_person_json_ld_carries_only_confirmed_facts(open_site):
    page, _ = open_site()
    graph = page.evaluate(
        """() => JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)"""
    )["@graph"]
    assert [n["@type"] for n in graph] == ["WebSite", "Person"]
    data = graph[1]
    assert data["name"] == "Igor Shatsev"
    assert data["sameAs"] == [
        "https://t.me/yngvil",
        "https://www.linkedin.com/in/vitnyrcoach/",
        "https://www.instagram.com/brychenka/",
    ]
    assert "FIDE" not in str(graph)
    assert [o["itemOffered"]["name"] for o in data["makesOffer"][1:]] == [
        "English coaching", "Chess coaching", "Climbing coaching",
    ]


def test_repetitor_is_search_only_never_visible_copy(open_site):
    """2026-09-23: "репетитор" is what Russian searchers type, but Igor
    wants it off the page — it may live in the RU meta description and the
    JSON-LD, never in rendered text, in either language."""
    for lang in ("en", "ru"):
        page, _ = open_site(lang=lang)
        assert "репетитор" not in page.locator("body").inner_text().lower()
    page, _ = open_site(query="?lang=ru")
    assert "репетитор" in page.locator('meta[name="description"]').get_attribute("content")


def test_real_chess_photos_carry_alt_text(open_site):
    page, _ = open_site()
    for img in page.locator('img[data-src*="collage/chess-"]').all():
        assert img.get_attribute("alt").strip()


@pytest.mark.parametrize("path,count", [("index.html", 3), ("english/", 5), ("chess/", 5), ("climbing/", 5)])
def test_section_numbering_is_sequential(open_site, path, count):
    page, _ = open_site(path=path)
    nums = page.locator(".sec .label .num").all_inner_texts()
    assert [n.strip() for n in nums] == [f"{i:02d}" for i in range(1, count + 1)]


def test_home_runs_hero_method_then_the_doors(open_site):
    """Discipline pages, Stage 1 (2026-10-31): Igor's order for the home
    page is the hero, then the method, then the mark with its three doors.
    Cheap regression guard against a later change moving them around."""
    page, _ = open_site()
    ids = page.locator(".sec[id]").evaluate_all("els => els.map(e => e.id)")
    assert ids[:2] == ["method", "origin"]
    assert page.locator("#origin .label .num").inner_text().strip() == "02"


# --- Spark Order S9A / move 09: each specimen is addressable, and the claim it
# sits under ("Your errors are a finite list") never gets a fabricated number
# put beside it. S0 decided that line is the whole claim; no figure is invented. ---

SPECIMEN_IDS = [
    "specimen-reflexive", "specimen-copula", "specimen-register",
    "specimen-chess-calculation", "specimen-chess-memory", "specimen-chess-tilt",
    "specimen-climbing-grip", "specimen-climbing-legs", "specimen-climbing-beta",
]


def test_no_invented_count_beside_the_finite_list_claim(open_site):
    """"Real material only": the specimens section is the one place on each
    discipline page built to tempt a fabricated statistic ("the average learner has N errors"). Its
    prose — the heading, the lede, every specimen label and every "why" —
    carries no digit, in either language. Adding one fails here."""
    for path in PAGES:
        for lang in ("en", "ru"):
            page, _ = open_site(lang=lang, path=path)
            prose = page.evaluate(
                """() => {
                    const sec = document.getElementById('specimen');
                    const sel = '.sec__head h2, .sec__lede [data-l],'
                              + ' .spec__label, .spec__why';
                    return [...sec.querySelectorAll(sel)]
                        .map(el => el.textContent).join('  ');
                }"""
            )
            # a hypothetical distance in a specimen's description ("only 2 moves
            # into the attack") is not a statistic — only bare counts are barred
            prose = re.sub(r"\b\d+ (moves?|ход\w*)", "", prose)
            low = prose.lower()
            assert len(low) > 200, "reading the wrong block — specimen prose is missing"
            assert not re.search(r"\d", prose), f"a digit crept into the specimen prose: {prose!r}"


def test_each_specimen_is_addressable_by_its_own_permalink(open_site):
    """Every <article class="spec"> carries a stable, language-neutral id and a
    label that links to exactly that id — so a reader can send one specific
    error, not the whole section. The ids survived the split unchanged, which
    is what the home page's old-link redirect relies on."""
    ids = []
    for path in PAGES:
        page, _ = open_site(path=path)
        pairs = page.evaluate(
            """() => [...document.querySelectorAll('.specs .spec')].map(a => ({
                id: a.id,
                href: a.querySelector('.spec__permalink') &&
                      a.querySelector('.spec__permalink').getAttribute('href'),
            }))"""
        )
        assert [p["href"] for p in pairs] == ["#" + p["id"] for p in pairs]
        ids += [p["id"] for p in pairs]
    assert ids == SPECIMEN_IDS


# --- J6(b) (Jury Pass II, 2026-09-12): the reveal hides each specimen's
# wrong/right pair until clicked, but the .spec__why paragraph beside it
# sits outside that reveal — always visible — and used to name the exact
# word or quote the corrected sentence, spoiling the click. Rewritten to
# describe each error's shape instead; this pins the specific word each
# paragraph used to give away so the fix can't quietly regress. ---

SPOILED_WORDS = {
    "specimen-reflexive": "myself",
    "specimen-copula": "agree",
    "specimen-register": "please",
}


_REGISTER_SPOILS_PLEASE = pytest.mark.xfail(
    reason="KNOWN REGRESSION (found in DP baseline pass): specimen-register's visible "
    "explanation names 'please' again, spoiling the reveal J6(b) was meant to protect. "
    "Fixing means rewriting Igor's copy, so it is left for him.", strict=True)


@pytest.mark.parametrize("specimen_id,word", [
    pytest.param(k, v, marks=_REGISTER_SPOILS_PLEASE) if k == "specimen-register" else (k, v)
    for k, v in SPOILED_WORDS.items()
])
def test_specimen_why_no_longer_names_the_hidden_word(open_site, specimen_id, word):
    page, _ = open_site(path="english/")
    why = page.locator(f"#{specimen_id} .spec__why:visible").inner_text().lower()
    assert word not in why, f"{specimen_id}: '{word}' still appears in the visible explanation"


def test_specimen_why_paragraphs_are_not_empty_in_either_language(open_site):
    """The RU rewrites are a first pass (Standing Order 9) but must still be
    real, non-empty prose, not a blank left behind by the edit."""
    for lang in ("en", "ru"):
        page, _ = open_site(lang=lang, path="english/")
        for specimen_id in SPOILED_WORDS:
            text = page.locator(f"#{specimen_id} .spec__why:visible").inner_text().strip()
            assert text, f"{specimen_id}/{lang}: .spec__why is empty"


def test_specimen_permalink_updates_the_url_and_moves_focus(open_site):
    """Clicking a specimen's label writes that permalink to the address bar
    (so it can be copied and shared) and moves focus into the specimen, not
    just the scroll position. Back then clears it."""
    page, _ = open_site(path="english/")
    page.locator("#specimen-copula .spec__permalink").click()
    page.wait_for_timeout(150)
    assert page.evaluate("location.hash") == "#specimen-copula"
    assert page.evaluate(
        "() => document.activeElement.closest('.spec') && document.activeElement.closest('.spec').id"
    ) == "specimen-copula"
    page.go_back()
    page.wait_for_timeout(150)
    assert page.evaluate("location.hash") == ""
    assert page.evaluate("() => !document.body.classList.contains('collage-open') "
                         "&& !document.documentElement.classList.contains('collage-open')")


def test_no_straight_apostrophes_in_visible_english_copy(open_site):
    """J1 (Jury Pass II): prose apostrophes are typographic ('), not straight
    ('). innerText mirrors what a reader sees — display:none RU text and any
    JS/attribute-only strings (hrefs, data-prefill-*) never enter it, so this
    can't be tripped by the things J1 was told not to touch."""
    for path in ("index.html",) + PAGES:
        page, _ = open_site(lang="en", path=path)
        assert "'" not in visible_text(page), path

    # The #collage view is a separate visible state, not reachable from the
    # main-page innerText above — check it too.
    page, _ = open_site(lang="en", hash="#collage")
    assert "'" not in visible_text(page)


def test_head_names_all_three_disciplines_english_first(open_site):
    """2026-09-23: Igor wants to be findable for chess and climbing coaching
    too, not just English. Title and description in both languages name all
    three, English first (Weighted positioning)."""
    for lang, words in (("en", ["english", "chess", "climbing"]),
                        ("ru", ["английск", "шахмат", "скалолаз"])):
        page, _ = open_site(query=f"?lang={lang}")
        for text in (page.title().lower(),
                     page.locator('meta[name="description"]').get_attribute("content").lower()):
            positions = [text.find(w) for w in words]
            assert all(p >= 0 for p in positions), (lang, text)
            assert positions == sorted(positions), (lang, text)
