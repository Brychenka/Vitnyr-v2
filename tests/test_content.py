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
        {"n": "7c", "k": "redpoint, indoor"},
    ]


def test_no_unapproved_animated_statistics(open_site):
    """Every counting number is one of the three approved values. A new
    data-count would be a fabricated statistic slipping in."""
    page, _ = open_site()
    counts = page.evaluate(
        "() => [...document.querySelectorAll('[data-count]')].map(el => el.dataset.count)"
    )
    assert sorted(counts, key=int) == ["8", "100", "2100"]


def test_contact_handles_are_still_flagged_placeholders(open_site):
    """Guard rail: when the real Telegram/LinkedIn/Instagram handles land, the
    `.ch__todo` chips and the @HANDLE text go with them — and this test should
    be updated in the same commit."""
    page, _ = open_site()
    todos = page.locator(".channels .ch__todo")
    assert todos.count() == 3
    assert {t.strip().lower() for t in todos.all_text_contents()} == {"fill in"}
    hrefs = page.locator(".channels a").evaluate_all(
        "els => els.map(a => a.getAttribute('href'))"
    )
    assert hrefs == ["#", "#", "#"]


def test_contact_channel_order_is_telegram_linkedin_instagram(open_site):
    page, _ = open_site()
    order = page.locator(".channels .ch__k").all_inner_texts()
    assert [o.strip() for o in order] == ["Telegram", "LinkedIn", "Instagram"]


def test_og_url_and_image_not_yet_asserted(open_site):
    """CLAUDE.md lists og:url / og:image as real placeholders. If they get
    added, flip this test to assert their content."""
    page, _ = open_site()
    assert page.locator('meta[property="og:url"]').count() == 0
    assert page.locator('meta[property="og:image"]').count() == 0
    assert page.locator('meta[property="og:title"]').count() == 1


def test_section_numbering_is_sequential(open_site):
    page, _ = open_site()
    nums = page.locator(".sec .label .num").all_inner_texts()
    assert [n.strip() for n in nums] == ["01", "02", "03", "04", "05"]
