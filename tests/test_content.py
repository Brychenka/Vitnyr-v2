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
    # raw DOM text: .domain__meta is text-transform:uppercase, so compare
    # case-insensitively. What matters is the two grades stay separate, not
    # merged into one generic "7c".
    text = page.evaluate("() => document.body.textContent").lower()
    assert "7c redpoint" in text
    assert "7c kilter" in text


def test_the_three_measured_facts_are_exactly_these(open_site):
    page, _ = open_site()
    facts = page.evaluate(
        """() => [...document.querySelectorAll('.facts li')].map(li => ({
            n: li.querySelector('.n').textContent.trim(),
            k: li.querySelector('.k').textContent.trim(),
        }))"""
    )
    assert facts == [
        {"n": "8", "k": "years coaching"},
        {"n": "100+", "k": "one-on-one clients"},
        {"n": "2100", "k": "chess rating"},
        {"n": "7c", "k": "redpoint, indoor · 7C Kilter"},
    ]


def test_no_unapproved_statistics_in_the_facts_row(open_site):
    """The facts row carries exactly the four confirmed figures and no more.
    Ported from test_no_unapproved_animated_statistics when Spark Order move 17
    removed the count-up: there is no [data-count] any longer, but the guard on
    "real material only" survives the change. A fifth number added to the row —
    a fabricated statistic slipping in — must fail this."""
    page, _ = open_site()
    numbers = page.evaluate(
        "() => [...document.querySelectorAll('.facts .n')].map(el => el.textContent.trim())"
    )
    assert numbers == ["8", "100+", "2100", "7c"]


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
