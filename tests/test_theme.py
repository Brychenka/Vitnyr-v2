"""Two fixed pairs, swapped whole. System preference, explicit override,
persistence, the button label, and the theme-color meta."""

import pytest

from conftest import rule_contrast

CREAM = "#EFEBE3"
CHARCOAL = "#171310"


def meta_theme_color(page):
    return page.locator('meta[name="theme-color"]').get_attribute("content")


def test_dark_system_pref_opens_charcoal(open_site):
    """2026-09-29 (Igor: "make it follow the systems settings"), reversing the
    2026-09-07 cream-always default: an OS-dark reader with no stored choice
    opens on charcoal."""
    page, _ = open_site(color_scheme="dark")
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert meta_theme_color(page).upper() == CHARCOAL
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == (
        "rgb(23, 19, 16)"
    )
    assert page.locator(".masthead .themeswitch").get_attribute("title") == "Cream"
    # nothing is stored until the reader uses the control
    assert page.evaluate("localStorage.getItem('vitnyr-theme')") is None


def test_light_system_pref_opens_cream(open_site):
    page, _ = open_site(color_scheme="light")
    assert page.locator("html").get_attribute("data-theme") == "light"
    assert meta_theme_color(page).upper() == CREAM
    assert page.locator(".masthead .themeswitch").get_attribute("title") == "Charcoal"


def test_toggle_from_the_system_default_stores_the_other_pair(open_site):
    page, _ = open_site(color_scheme="light")
    page.locator(".masthead .themeswitch").click()

    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert page.evaluate("localStorage.getItem('vitnyr-theme')") == "dark"
    assert meta_theme_color(page).upper() == CHARCOAL
    assert page.locator(".masthead .themeswitch").get_attribute("title") == "Cream"


def test_live_os_switch_is_followed_without_a_stored_choice(open_site):
    page, _ = open_site(color_scheme="light")
    page.emulate_media(color_scheme="dark")
    page.wait_for_timeout(50)
    assert page.locator("html").get_attribute("data-theme") == "dark"


def test_live_os_switch_is_ignored_after_a_stored_choice(open_site):
    page, _ = open_site(theme="light", color_scheme="light")
    page.emulate_media(color_scheme="dark")
    page.wait_for_timeout(50)
    assert page.locator("html").get_attribute("data-theme") == "light"


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
    assert dark_bg == "rgb(23, 19, 16)"      # #171310


def test_theme_button_label_is_localised(open_site):
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()  # -> RU, still cream
    assert page.locator(".masthead .themeswitch").get_attribute("title") == "Уголь"
    page.locator(".masthead .themeswitch").click()  # -> charcoal
    assert page.locator(".masthead .themeswitch").get_attribute("title") == "Крем"


# --- P12: the hairline used to measure ~1.47:1 (charcoal) / ~1.48:1 (cream)
# against --bg — present on a good display in a dark room, gone on a dim
# laptop or in daylight. Both pairs are tuned to land near 2:1 instead. ---

def test_hairline_clears_roughly_2to1_on_charcoal(open_site):
    # theme="dark" seeds an explicit choice, so the pair doesn't hang on the
    # fixture's OS default (the cream hairline lands in this same band, so a
    # wrong pair would pass silently).
    page, _ = open_site(theme="dark")
    ratio = rule_contrast(page)
    assert 1.85 <= ratio <= 2.3, f"--rule vs --bg on charcoal: {ratio:.2f}:1"


def test_hairline_clears_roughly_2to1_on_cream(open_site):
    page, _ = open_site()
    ratio = rule_contrast(page)
    assert 1.85 <= ratio <= 2.3, f"--rule vs --bg on cream: {ratio:.2f}:1"


# --- SITE-PLAN C7 (2026-11-20): the OS decides on every page, not just home,
# and a stored choice carries across pages (the 404 included). ---

@pytest.mark.parametrize("path", ["english/", "chess/", "climbing/"])
def test_discipline_pages_follow_the_os_until_the_reader_chooses(open_site, path):
    page, _ = open_site(color_scheme="dark", path=path)
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert meta_theme_color(page).upper() == CHARCOAL
    page, _ = open_site(color_scheme="dark", theme="light", path=path)
    assert page.locator("html").get_attribute("data-theme") == "light"
    assert meta_theme_color(page).upper() == CREAM


def test_not_found_page_follows_the_os_and_a_stored_choice(open_site):
    page, _ = open_site(color_scheme="dark", path="404.html")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(23, 19, 16)"
    page, _ = open_site(color_scheme="dark", theme="light", path="404.html")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(239, 235, 227)"
    page, _ = open_site(color_scheme="light", theme="dark", path="404.html")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(23, 19, 16)"
