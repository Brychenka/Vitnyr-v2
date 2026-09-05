"""The collage: one file, routed like its own page. Deep-linkable, own header,
browser back works, focus moves to the heading, the page behind goes inert and
stops scrolling, theme/language persist, scroll resets on the way back."""

import pytest


def _is_open(page):
    return page.evaluate(
        "() => document.documentElement.classList.contains('collage-open')"
    )


def test_opener_routes_into_the_view(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()

    assert page.evaluate("location.hash") == "#collage"
    assert _is_open(page)
    assert page.locator("#collage").is_visible()
    assert page.evaluate("document.activeElement.id") == "collage-title"


def test_page_behind_is_inert_and_locked(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(200)

    assert page.evaluate("document.getElementById('app').inert") is True
    assert page.evaluate("document.querySelector('.masthead').inert") is True
    assert page.evaluate("getComputedStyle(document.body).overflow") == "hidden"


def test_escape_closes_and_restores_focus(open_site):
    page, _ = open_site()
    opener = page.locator("[data-collage-open]")
    opener.click()
    page.wait_for_timeout(150)

    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    assert not _is_open(page)
    assert page.evaluate("location.hash") in ("", "#")
    assert page.evaluate(
        "() => document.activeElement.matches('[data-collage-open]')"
    )


def test_back_button_in_bar_closes_the_view(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(150)
    page.locator(".view__back").click()
    page.wait_for_timeout(400)
    assert not _is_open(page)


def test_browser_back_closes_the_view(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(150)
    assert _is_open(page)

    page.go_back()
    page.wait_for_timeout(400)
    assert not _is_open(page)


def test_deep_link_opens_the_view_directly(open_site):
    page, _ = open_site(hash="#collage")
    assert _is_open(page)
    assert page.locator("#collage").is_visible()
    # the head script sets .collage-open before first paint, so #app never shows
    assert page.evaluate("document.activeElement.id") == "collage-title"


def test_scroll_position_restored_on_return(open_site):
    page, _ = open_site()
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(300)
    before = page.evaluate("window.__lenis ? window.__lenis.scroll : window.scrollY")

    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(200)
    page.locator(".view__back").click()
    page.wait_for_timeout(600)

    after = page.evaluate("window.__lenis ? window.__lenis.scroll : window.scrollY")
    assert abs(after - before) < 40, f"returned to {after}, left from {before}"


def test_theme_and_language_persist_through_the_view(open_site):
    page, _ = open_site(color_scheme="dark")
    # .themeswitch now exists twice (masthead + collage view bar); the collage
    # copy is unreachable until the view opens, so drive the masthead one.
    page.locator(".masthead .themeswitch").click()  # -> light
    page.locator(".masthead .langswitch").click()   # -> ru
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(200)

    html = page.locator("html")
    assert html.get_attribute("data-theme") == "light"
    assert html.get_attribute("data-lang") == "ru"
    # no flash of the other theme: the view background is the light bg
    assert page.evaluate(
        "getComputedStyle(document.querySelector('#collage')).backgroundColor"
    ) == "rgb(239, 235, 227)"


def test_no_js_fallback_leaves_collage_as_a_plain_section(open_site):
    """With JS off, #collage is just the last block of the document and the
    opener is an ordinary in-page anchor to it — nothing hidden, no routing."""
    page, _ = open_site(java_script_enabled=False)
    collage = page.locator("#collage")
    assert collage.is_visible()
    assert "collage-open" not in (page.locator("html").get_attribute("class") or "")
    # opener still points at #collage
    assert page.locator("[data-collage-open]").get_attribute("href") == "#collage"
    # the view is a normal-flow section, not a fixed overlay
    assert collage.evaluate("el => getComputedStyle(el).position") == "static"


def test_collage_has_own_header_and_back_affordance(open_site):
    page, _ = open_site(hash="#collage")
    bar = page.locator("#collage .view__bar")
    assert bar.locator(".view__back").is_visible()
    assert bar.locator("svg[aria-label='Vitnyr']").count() == 1


# --- Stage 4: the tiles run the page's reveal rhythm, off the view's own root ---

def test_collage_tiles_are_plain_visible_before_the_view_opens(open_site):
    """Tiles ship .reveal.is-in. With the view closed they are ordinary
    visible content — never counted among 'stuck' reveals, and readable with
    JS off or under reduced motion."""
    page, _ = open_site()
    page.wait_for_timeout(300)
    assert page.evaluate(
        "() => [...document.querySelectorAll('#collage .reveal')]"
        ".every(t => parseFloat(getComputedStyle(t).opacity) > 0.95)"
    )
    # and they are excluded from the page observer's set
    assert page.evaluate(
        "() => [...document.querySelectorAll('#app .reveal')]"
        ".every(el => !el.closest('#collage'))"
    )


def test_collage_tiles_reveal_on_scroll_inside_the_view(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)

    last_tile = page.locator("#collage .view__group").last.locator(".reveal").last
    # below the first screenful of the view -> stripped back to hidden
    assert last_tile.evaluate("el => parseFloat(getComputedStyle(el).opacity)") < 0.1

    last_tile.scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    assert last_tile.evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95
    assert "is-in" in (last_tile.get_attribute("class") or "")


def test_collage_reveals_are_inert_under_reduced_motion(open_site):
    page, _ = open_site(reduced_motion=True)
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)
    assert page.evaluate(
        "() => [...document.querySelectorAll('#collage .reveal')]"
        ".every(t => parseFloat(getComputedStyle(t).opacity) > 0.95)"
    )


def test_collage_reopen_lands_on_a_settled_view(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(300)
    page.locator("#collage .view__back").click()
    page.wait_for_timeout(400)
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(300)
    assert page.evaluate(
        "() => [...document.querySelectorAll('#collage .reveal')]"
        ".every(t => parseFloat(getComputedStyle(t).opacity) > 0.95)"
    )
