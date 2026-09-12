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


def test_chess_rating_is_stated_without_fide(open_site):
    # Igor's explicit correction: the 2100 rating is stated without "FIDE".
    # \b so this doesn't trip on "confidence".
    for lang in ("en", "ru"):
        page, _ = open_site(lang=lang)
        text = visible_text(page)
        assert "2100" in text
        assert not re.search(r"\bFIDE\b", text, re.I), "'FIDE' must not appear"


def test_climbing_grades_are_kept_distinct(open_site):
    page, _ = open_site()
    # rendered text, not source: .domain__meta is text-transform:uppercase,
    # and J2 (Jury Pass II) stopped that rule from flattening the domain
    # stat's 7c/7C case. inner_text() reflects what the reader actually sees;
    # text_content() would read the un-transformed source and miss a
    # regression that brings the uppercase back.
    stat = page.locator("article.domain").nth(2).locator(".domain__stat")
    assert stat.inner_text() == "7c redpoint · 7C Kilter"
    # Spark Order S2 / move 18: in the facts row the two readings are two
    # separate elements now, not one run-on text node joined by a middle dot —
    # so a non-climber can see they are two different achievements.
    readings = page.evaluate(
        "() => [...document.querySelectorAll('.fact--grade .fact__reading')]"
        ".map(el => el.textContent.trim())"
    )
    assert readings == ["redpoint, indoor", "7C Kilter"]


def test_domain_labels_stay_uppercase_while_stats_keep_their_case(open_site):
    # The other half of J2: .domain__meta's uppercase must still apply to the
    # ENGLISH/CHESS/CLIMBING label — only the stat span opts out.
    page, _ = open_site()
    labels = page.locator(".domain__meta > span:first-child")
    assert [labels.nth(i).inner_text() for i in range(labels.count())] == [
        "ENGLISH",
        "CHESS",
        "CLIMBING",
    ]


def test_the_three_measured_facts_are_exactly_these(open_site):
    page, _ = open_site()
    # S2 / move 18 split the climbing fact into two stacked .fact__reading
    # elements; every asserted string is still present verbatim, including the
    # meaningful 7c / 7C case difference. The three animated numbers are read
    # from data-count(+suffix) so this stays stable whether or not the count-up
    # (restored as "separate instruments") is mid-flight when the test runs.
    facts = page.evaluate(
        """() => [...document.querySelectorAll('.facts li')].map(li => {
            const n = li.querySelector('.n');
            return {
                n: n.dataset.count ? n.dataset.count + (n.dataset.suffix || '')
                                   : n.textContent.trim(),
                unit: li.classList.contains('fact--grade')
                    ? [...li.querySelectorAll('.fact__reading')].map(r => r.textContent.trim())
                    : li.querySelector('.k').textContent.trim(),
            };
        })"""
    )
    assert facts == [
        {"n": "8", "unit": "years coaching"},
        {"n": "100+", "unit": "one-on-one clients"},
        {"n": "2100", "unit": "chess rating"},
        {"n": "7c", "unit": ["redpoint, indoor", "7C Kilter"]},
    ]


def test_facts_row_names_each_unit_type(open_site):
    """Spark Order S2 / move 18: the four facts are readings off four unrelated
    instruments and the row now says so structurally — each li carries a
    modifier naming its unit type, which the typographic treatment hangs on. A
    later change that flattens them back to one identical style fails here."""
    page, _ = open_site()
    kinds = page.evaluate(
        """() => [...document.querySelectorAll('.facts li')].map(li =>
            [...li.classList].find(c => c.startsWith('fact--')) || null)"""
    )
    assert kinds == ["fact--count", "fact--count", "fact--scale", "fact--grade"]


def test_no_unapproved_statistics_in_the_facts_row(open_site):
    """The facts row carries exactly the four confirmed figures and no more.
    Guards "real material only": a fifth number — a fabricated statistic
    slipping in — must fail this, whether it animates (a new data-count) or
    sits static. The count-up was removed by move 17 and later restored as
    "separate instruments"; this guard is indifferent to that."""
    page, _ = open_site()
    animated = page.evaluate(
        "() => [...document.querySelectorAll('.facts .n[data-count]')].map(el => el.dataset.count)"
    )
    assert sorted(animated, key=int) == ["8", "100", "2100"]
    labels = page.evaluate(
        """() => [...document.querySelectorAll('.facts .n')].map(el =>
            el.dataset.count ? el.dataset.count + (el.dataset.suffix || '')
                             : el.textContent.trim())"""
    )
    assert labels == ["8", "100+", "2100", "7c"]


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


def test_og_url_and_image_use_the_placeholder_domain(open_site):
    """P1 (Stage 6): og:url / og:image landed as a real share card + a
    documented https://vitnyr.example/ placeholder domain (RFC 2606) rather
    than a guessed real-looking one — a real domain still doesn't exist."""
    page, _ = open_site()
    assert page.locator('meta[property="og:url"]').get_attribute("content") == "https://vitnyr.example/"
    assert (
        page.locator('meta[property="og:image"]').get_attribute("content")
        == "https://vitnyr.example/assets/share/og-share.png"
    )
    assert page.locator('meta[property="og:title"]').count() == 1


def test_canonical_and_hreflang_share_the_same_placeholder_domain(open_site):
    page, _ = open_site()
    assert page.locator('link[rel="canonical"]').get_attribute("href") == "https://vitnyr.example/"
    alternates = {
        el.get_attribute("hreflang"): el.get_attribute("href")
        for el in page.locator('link[rel="alternate"][hreflang]').all()
    }
    assert alternates == {
        "en": "https://vitnyr.example/?lang=en",
        "ru": "https://vitnyr.example/?lang=ru",
        "x-default": "https://vitnyr.example/",
    }


def test_share_card_asset_is_actually_served(open_site, site_url):
    """The og:image / twitter:image meta values are necessarily absolute
    placeholder-domain URLs (no real domain exists yet), but the asset
    itself has to exist at that same path once the domain is swapped in —
    checked here against the real path, relative to site root."""
    page, _ = open_site()
    resp = page.request.get(f"{site_url}/assets/share/og-share.png")
    assert resp.ok
    assert resp.headers.get("content-type", "").startswith("image/")


def test_person_json_ld_carries_only_confirmed_facts(open_site):
    page, _ = open_site()
    data = page.evaluate(
        """() => JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)"""
    )
    assert data["@type"] == "Person"
    assert data["name"] == "Igor Shatsev"
    assert data["sameAs"] == [
        "https://t.me/yngvil",
        "https://www.linkedin.com/in/vitnyrcoach/",
        "https://www.instagram.com/brychenka/",
    ]
    assert "FIDE" not in str(data)


def test_section_numbering_is_sequential(open_site):
    page, _ = open_site()
    nums = page.locator(".sec .label .num").all_inner_texts()
    assert [n.strip() for n in nums] == ["01", "02", "03", "04", "05", "06"]


# --- Spark Order S9A / move 09: each specimen is addressable, and the claim it
# sits under ("Your errors are a finite list") never gets a fabricated number
# put beside it. S0 decided that line is the whole claim; no figure is invented. ---

SPECIMEN_IDS = ["specimen-reflexive", "specimen-copula", "specimen-register"]


def test_no_invented_count_beside_the_finite_list_claim(open_site):
    """"Real material only": section 02 is the one place on the page built to
    tempt a fabricated statistic ("the average learner has N errors"). Its
    prose — the heading, the lede, every specimen label and every "why" —
    carries no digit, in either language. Adding one fails here."""
    for lang in ("en", "ru"):
        page, _ = open_site(lang=lang)
        prose = page.evaluate(
            """() => {
                const sec = document.getElementById('specimen');
                const sel = '.sec__head h2, .sec__lede [data-l],'
                          + ' .spec__label, .spec__why';
                return [...sec.querySelectorAll(sel)]
                    .map(el => el.textContent).join('  ');
            }"""
        )
        low = prose.lower()
        assert "finite list" in low and "конечный список" in low, (
            "reading the wrong block — the finite-list claim is not in it"
        )
        assert not re.search(r"\d", prose), f"a digit crept into the specimen prose: {prose!r}"


def test_each_specimen_is_addressable_by_its_own_permalink(open_site):
    """Every <article class="spec"> carries a stable, language-neutral id and a
    label that links to exactly that id — so a reader can send one specific
    error, not the whole section."""
    page, _ = open_site()
    pairs = page.evaluate(
        """() => [...document.querySelectorAll('.specs .spec')].map(a => ({
            id: a.id,
            href: a.querySelector('.spec__permalink') &&
                  a.querySelector('.spec__permalink').getAttribute('href'),
        }))"""
    )
    assert [p["id"] for p in pairs] == SPECIMEN_IDS
    assert [p["href"] for p in pairs] == ["#" + i for i in SPECIMEN_IDS]


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


@pytest.mark.parametrize("specimen_id,word", list(SPOILED_WORDS.items()))
def test_specimen_why_no_longer_names_the_hidden_word(open_site, specimen_id, word):
    page, _ = open_site()
    why = page.locator(f"#{specimen_id} .spec__why:visible").inner_text().lower()
    assert word not in why, f"{specimen_id}: '{word}' still appears in the visible explanation"


def test_specimen_why_paragraphs_are_not_empty_in_either_language(open_site):
    """The RU rewrites are a first pass (Standing Order 9) but must still be
    real, non-empty prose, not a blank left behind by the edit."""
    for lang in ("en", "ru"):
        page, _ = open_site(lang=lang)
        for specimen_id in SPOILED_WORDS:
            text = page.locator(f"#{specimen_id} .spec__why:visible").inner_text().strip()
            assert text, f"{specimen_id}/{lang}: .spec__why is empty"


def test_specimen_permalink_updates_the_url_and_moves_focus(open_site):
    """Clicking a specimen's label writes that permalink to the address bar
    (so it can be copied and shared) and moves focus into the specimen, not
    just the scroll position. Back then clears it."""
    page, _ = open_site()
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
    page, _ = open_site(lang="en")
    assert "'" not in visible_text(page)

    # The #collage view is a separate visible state, not reachable from the
    # main-page innerText above — check it too.
    page, _ = open_site(lang="en", hash="#collage")
    assert "'" not in visible_text(page)
