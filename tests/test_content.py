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
    # \b so this doesn't trip on "confidence". The rating used to be visible
    # by default on §04's chess domain card; that card was folded into §03
    # 2026-09-18, so the figure now lives only in the origin readout's chess
    # row, which needs the chess discipline committed to become visible.
    for lang in ("en", "ru"):
        page, _ = open_site(lang=lang)
        page.locator('.origin__panel-item[data-discipline="chess"]').click()
        text = visible_text(page)
        assert "2100" in text
        assert not re.search(r"\bFIDE\b", text, re.I), "'FIDE' must not appear"


def test_climbing_grades_are_kept_distinct(open_site):
    # rendered text, not source: J2 (Jury Pass II) established that a
    # climbing grade's 7c/7C case must survive an uppercase ancestor rule.
    # §04 "Three domains" (the original home of this check, .domain__stat)
    # was folded into §03 2026-09-18; the same figures live on in the origin
    # readout's climbing row, so the check moved with them. Only the
    # committed discipline's .reading__value is visible, so commit climbing
    # first — inner_text() of a non-active value reads as empty.
    page, _ = open_site()
    page.locator('.origin__panel-item[data-discipline="climbing"]').click()
    value = page.locator('.reading__value[data-discipline="climbing"]').first
    assert value.inner_text() == "7c redpoint · 7C Kilter"


def test_reading_rows_are_coaching_achieved_mistakes(open_site):
    """Trifecta Order D / Stage D3 (2026-09-15): the readout's body is one
    spec sheet whose values change, not three panels that swap — fixed row
    order, per the plan's own table. Stage 6 (2026-09-17) cut the opening
    Measured row: it only restated the .origin__panel-item stat directly
    above it, in the same view, with no new information. Rendered text
    (inner_text), since .reading__label is text-transform:uppercase."""
    page, _ = open_site()
    labels = page.locator(".reading__label").all_inner_texts()
    # Stage 6 cut Measured; since then the readout became Credential / Years
    # coaching / Achieved / Common problems (the 4th row renamed from "mistakes").
    assert labels == ["CREDENTIAL", "YEARS COACHING", "ACHIEVED", "COMMON PROBLEMS"]


def test_reading_value_keeps_its_case_not_forced_uppercase(open_site):
    """Same regression J2 fixed for .domain__stat (test above): a value must
    not inherit any ancestor's uppercase transform. Asserts rendered text —
    text_content() would read the source and miss a CSS regression that
    brings uppercase back. Called out explicitly in TRIFECTA-D-NAVIGATOR.md's
    Stage D3 as "the single easiest regression in the order"."""
    page, _ = open_site()
    achieved = page.locator('.reading__row').nth(2).locator(
        '.reading__value[data-discipline="english"]'
    )
    assert achieved.inner_text() == "100+ one-on-one clients"


def test_reading_common_problems_row_is_terse_data(open_site):
    """Register: data, not prose (D0.7). The row is a short list of problems
    per discipline; it deliberately does not mirror §03's three specimen titles
    (Igor declined that, DESIGN-PASS-III.md DP6 — leave the readout as is)."""
    page, _ = open_site()
    problems = page.locator('.reading__row').nth(3).locator(
        '.reading__value[data-discipline="english"]'
    ).inner_text()
    assert "Carrying structure over from Russian" in problems
    assert "fear of making a mistake" in problems
    assert "." not in problems, "this row is data, not sentences"


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


# --- Trifecta D follow-up (2026-09-15): §03 (Specimens) is now discipline-
# scoped, the same way the origin readout is — English's three named
# specimens are its own .specimens-group, and chess/climbing get their own
# (currently placeholder) groups, swapped by the same commit() that drives
# updateReading(). ---

def test_english_specimens_are_the_default_before_any_commit(open_site):
    page, _ = open_site()
    groups = page.locator("#specimen .specimens-group")
    assert groups.count() == 3
    assert page.locator(
        '#specimen .specimens-group[data-discipline-group="english"]'
    ).is_visible()
    for name in ("chess", "climbing"):
        assert not page.locator(
            f'#specimen .specimens-group[data-discipline-group="{name}"]'
        ).is_visible()


@pytest.mark.parametrize("name", ["chess", "climbing"])
def test_committing_a_discipline_swaps_the_specimens_group(open_site, name):
    page, _ = open_site()
    page.locator(f'.origin__panel-item[data-discipline="{name}"]').click()
    assert page.locator(
        f'#specimen .specimens-group[data-discipline-group="{name}"]'
    ).is_visible()
    assert not page.locator(
        '#specimen .specimens-group[data-discipline-group="english"]'
    ).is_visible()


def test_committing_back_to_english_restores_its_specimens_group(open_site):
    page, _ = open_site()
    page.locator('.origin__panel-item[data-discipline="chess"]').click()
    page.locator('.origin__panel-item[data-discipline="english"]').click()
    assert page.locator(
        '#specimen .specimens-group[data-discipline-group="english"]'
    ).is_visible()
    assert not page.locator(
        '#specimen .specimens-group[data-discipline-group="chess"]'
    ).is_visible()


def test_chess_and_climbing_have_real_specimens(open_site):
    """Stage 5 (2026-09-16) replaced the Trifecta D follow-up placeholders
    with real named specimens, same format as English's three (wrong/right
    pair + why, addressable by permalink)."""
    page, _ = open_site()
    for name in ("chess", "climbing"):
        group = page.locator(f'#specimen .specimens-group[data-discipline-group="{name}"]')
        assert group.locator(".spec").count() == 3
        assert group.locator(".spec__why").count() == 6  # en + ru per specimen


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
    assert [n.strip() for n in nums] == ["01", "02", "03", "04", "05"]


def test_origin_is_the_first_section_and_carries_01(open_site):
    """Trifecta Order D / Stage D1 (2026-09-15): the mark's section moved from
    position 4 to position 1, directly after the hero, so it can act as the
    page's navigator. Cheap regression guard against a later stage silently
    moving or renumbering it back."""
    page, _ = open_site()
    first_sec = page.locator(".sec").first
    assert first_sec.get_attribute("id") == "origin"
    assert first_sec.locator(".label .num").inner_text().strip() == "01"


# --- Spark Order S9A / move 09: each specimen is addressable, and the claim it
# sits under ("Your errors are a finite list") never gets a fabricated number
# put beside it. S0 decided that line is the whole claim; no figure is invented. ---

SPECIMEN_IDS = [
    "specimen-reflexive", "specimen-copula", "specimen-register",
    "specimen-chess-calculation", "specimen-chess-memory", "specimen-chess-tilt",
    "specimen-climbing-grip", "specimen-climbing-legs", "specimen-climbing-beta",
]


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
        # a hypothetical distance in a specimen's description ("only 2 moves
        # into the attack") is not a statistic — only bare counts are barred
        prose = re.sub(r"\b\d+ (moves?|ход\w*)", "", prose)
        low = prose.lower()
        assert len(low) > 200, "reading the wrong block — specimen prose is missing"
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


_REGISTER_SPOILS_PLEASE = pytest.mark.xfail(
    reason="KNOWN REGRESSION (found in DP baseline pass): specimen-register's visible "
    "explanation names 'please' again, spoiling the reveal J6(b) was meant to protect. "
    "Fixing means rewriting Igor's copy, so it is left for him.", strict=True)


@pytest.mark.parametrize("specimen_id,word", [
    pytest.param(k, v, marks=_REGISTER_SPOILS_PLEASE) if k == "specimen-register" else (k, v)
    for k, v in SPOILED_WORDS.items()
])
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
