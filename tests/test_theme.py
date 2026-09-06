"""Two fixed pairs, swapped whole. System preference, explicit override,
persistence, the button label, and the theme-color meta."""

import pytest

CREAM = "#EFEBE3"
CHARCOAL = "#14181A"


def meta_theme_color(page):
    return page.locator('meta[name="theme-color"]').get_attribute("content")


def test_dark_system_pref_uses_charcoal_with_no_attribute(open_site):
    page, _ = open_site(color_scheme="dark")
    # no stored choice -> no data-theme attribute, effective theme is charcoal
    assert page.locator("html").get_attribute("data-theme") is None
    assert meta_theme_color(page).upper() == CHARCOAL
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Cream"


def test_light_system_pref_uses_cream_with_no_attribute(open_site):
    page, _ = open_site(color_scheme="light")
    assert page.locator("html").get_attribute("data-theme") is None
    assert meta_theme_color(page).upper() == CREAM
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Charcoal"


def test_toggle_from_dark_sets_light(open_site):
    page, _ = open_site(color_scheme="dark")
    page.locator(".masthead .themeswitch").click()

    assert page.locator("html").get_attribute("data-theme") == "light"
    assert page.evaluate("localStorage.getItem('vitnyr-theme')") == "light"
    assert meta_theme_color(page).upper() == CREAM
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Charcoal"


def test_explicit_choice_overrides_system_pref(open_site):
    # OS says light, stored choice says dark -> dark wins
    page, _ = open_site(theme="dark", color_scheme="light")
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert meta_theme_color(page).upper() == CHARCOAL


def test_theme_persists_across_reload(open_site):
    page, _ = open_site(color_scheme="dark")
    page.locator(".masthead .themeswitch").click()
    page.reload(wait_until="load")
    assert page.locator("html").get_attribute("data-theme") == "light"


def test_background_actually_changes_between_pairs(open_site):
    page, _ = open_site(color_scheme="dark")
    dark_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    page.locator(".masthead .themeswitch").click()
    light_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    assert dark_bg != light_bg
    assert dark_bg == "rgb(20, 24, 26)"      # #14181A
    assert light_bg == "rgb(239, 235, 227)"  # #EFEBE3


def test_theme_button_label_is_localised(open_site):
    page, _ = open_site(color_scheme="dark")
    page.locator(".masthead .langswitch").click()  # -> RU
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Крем"
    page.locator(".masthead .themeswitch").click()  # -> light
    assert page.locator(".masthead .themeswitch").text_content().strip() == "Уголь"
