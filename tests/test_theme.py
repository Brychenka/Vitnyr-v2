"""Two fixed pairs, swapped whole. System preference, explicit override,
persistence, the button label, and the theme-color meta."""

import pytest

from conftest import rule_contrast

CREAM = "#EFEBE3"
CHARCOAL = "#14181A"


def meta_theme_color(page):
    return page.locator('meta[name="theme-color"]').get_attribute("content")


def test_dark_system_pref_still_opens_cream(open_site):
    """2026-09-07 (Igor: "make cream the default one, only moving to dark one if
    the choosers chose to"): `prefers-color-scheme` was removed outright, so an
    OS-dark reader with no stored choice opens on *cream*, not charcoal. Guards
    the decision itself — a reinstated media query would fail here."""
    page, _ = open_site(color_scheme="dark")
    # no stored choice -> no data-theme attribute -> base :root -> cream
    assert page.locator("html").get_attribute("data-theme") is None
    assert meta_theme_color(page).upper() == CREAM
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == (
        "rgb(239, 235, 227)"
    )
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Charcoal"


def test_light_system_pref_uses_cream_with_no_attribute(open_site):
    page, _ = open_site(color_scheme="light")
    assert page.locator("html").get_attribute("data-theme") is None
    assert meta_theme_color(page).upper() == CREAM
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Charcoal"


def test_toggle_from_the_cream_default_sets_dark(open_site):
    """Charcoal is opt-in: it is reachable only through the control."""
    page, _ = open_site(color_scheme="dark")
    page.locator(".masthead .themeswitch").click()

    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert page.evaluate("localStorage.getItem('vitnyr-theme')") == "dark"
    assert meta_theme_color(page).upper() == CHARCOAL
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Cream"


def test_explicit_choice_overrides_system_pref(open_site):
    # OS says light, stored choice says dark -> dark wins
    page, _ = open_site(theme="dark", color_scheme="light")
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert meta_theme_color(page).upper() == CHARCOAL


def test_theme_persists_across_reload(open_site):
    page, _ = open_site()
    page.locator(".masthead .themeswitch").click()   # cream -> charcoal
    page.reload(wait_until="load")
    assert page.locator("html").get_attribute("data-theme") == "dark"


def test_background_actually_changes_between_pairs(open_site):
    page, _ = open_site()
    light_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    page.locator(".masthead .themeswitch").click()
    dark_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    assert dark_bg != light_bg
    assert light_bg == "rgb(239, 235, 227)"  # #EFEBE3
    assert dark_bg == "rgb(20, 24, 26)"      # #14181A


def test_theme_button_label_is_localised(open_site):
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()  # -> RU, still cream
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Уголь"
    page.locator(".masthead .themeswitch").click()  # -> charcoal
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Крем"


# --- P12: the hairline used to measure ~1.47:1 (charcoal) / ~1.48:1 (cream)
# against --bg — present on a good display in a dark room, gone on a dim
# laptop or in daylight. Both pairs are tuned to land near 2:1 instead. ---

def test_hairline_clears_roughly_2to1_on_charcoal(open_site):
    # theme="dark", not color_scheme: charcoal is opt-in only, so an OS-level
    # preference would have measured the cream hairline instead — which lands in
    # this same band, so the mistake passed silently.
    page, _ = open_site(theme="dark")
    ratio = rule_contrast(page)
    assert 1.85 <= ratio <= 2.3, f"--rule vs --bg on charcoal: {ratio:.2f}:1"


def test_hairline_clears_roughly_2to1_on_cream(open_site):
    page, _ = open_site()
    ratio = rule_contrast(page)
    assert 1.85 <= ratio <= 2.3, f"--rule vs --bg on cream: {ratio:.2f}:1"
