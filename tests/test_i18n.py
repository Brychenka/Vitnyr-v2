"""Dual-language DOM: the switch, persistence, the URL override, and the two
translation mechanisms (data-en/data-ru attributes and data-l blocks)."""

import pytest


def test_default_language_is_english(open_site):
    page, _ = open_site()
    assert page.locator("html").get_attribute("data-lang") == "en"
    assert page.locator("html").get_attribute("lang") == "en"
    assert page.locator(".masthead .langswitch").inner_text().strip() == "RU"


def test_switch_to_russian_updates_dom_and_button(open_site):
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()

    html = page.locator("html")
    assert html.get_attribute("data-lang") == "ru"
    assert html.get_attribute("lang") == "ru"
    assert page.locator(".masthead .langswitch").inner_text().strip() == "EN"
    # a data-en/data-ru node now shows its Russian text
    eyebrow_city = page.locator('.eyebrow span[data-ru="Ереван"]')
    # text_content(), not inner_text(): the eyebrow is text-transform:uppercase
    assert eyebrow_city.text_content().strip() == "Ереван"


def test_data_l_blocks_swap_visibility(open_site):
    page, _ = open_site()
    assert page.locator('.hero__title span[data-l="en"]').is_visible()
    assert page.locator('.hero__title span[data-l="ru"]').is_hidden()

    page.locator(".masthead .langswitch").click()
    assert page.locator('.hero__title span[data-l="ru"]').is_visible()
    assert page.locator('.hero__title span[data-l="en"]').is_hidden()


def test_language_choice_persists_across_reload(open_site):
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()
    assert page.evaluate("localStorage.getItem('vitnyr-lang')") == "ru"

    page.reload(wait_until="load")
    assert page.locator("html").get_attribute("data-lang") == "ru"


def test_seeded_language_applies_before_paint(open_site):
    page, _ = open_site(lang="ru")
    assert page.locator("html").get_attribute("data-lang") == "ru"


def test_lang_query_param_overrides_storage(open_site):
    # storage says RU, ?lang=en must win for this load
    page, _ = open_site(lang="ru", query="?lang=en")
    assert page.locator("html").get_attribute("data-lang") == "en"


def test_every_data_attr_node_has_both_languages(open_site):
    page, _ = open_site()
    missing = page.evaluate(
        """() => {
            const out = [];
            document.querySelectorAll('[data-en], [data-ru]').forEach(el => {
                if (el.dataset.en == null || el.dataset.ru == null)
                    out.push(el.outerHTML.slice(0, 80));
            });
            return out;
        }"""
    )
    assert missing == [], missing


def test_no_untranslated_placeholder_text_leaks(open_site):
    """After a switch, no element should still be showing its English default
    because a data-ru value was blank."""
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()
    blank = page.evaluate(
        """() => {
            const out = [];
            document.querySelectorAll('[data-en][data-ru]').forEach(el => {
                if (!el.dataset.ru.trim()) out.push(el.dataset.en);
            });
            return out;
        }"""
    )
    assert blank == [], f"data-ru empty for: {blank}"
