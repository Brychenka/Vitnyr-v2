"""No horizontal overflow in either pair, either language, at ~375 and ~1280.
The masthead stays fixed; the skip link stays parked until focused."""

import itertools

import pytest

from conftest import NARROW, WIDE, horizontal_overflow

VIEWPORTS = [("narrow", NARROW), ("wide", WIDE)]
LANGS = ["en", "ru"]
SCHEMES = ["dark", "light"]


@pytest.mark.parametrize(
    "vp_name,lang,scheme",
    [
        (v[0], l, s)
        for v, l, s in itertools.product(VIEWPORTS, LANGS, SCHEMES)
    ],
)
def test_no_horizontal_overflow(open_site, vp_name, lang, scheme):
    vp = dict(VIEWPORTS)[vp_name]
    page, _ = open_site(lang=lang, color_scheme=scheme, viewport=vp)
    page.wait_for_timeout(400)
    assert not horizontal_overflow(page), f"{vp_name}/{lang}/{scheme} overflows"

    # and again after opening the collage view, which is its own scroll container
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)
    assert not horizontal_overflow(page), f"{vp_name}/{lang}/{scheme} collage overflows"


def test_masthead_is_fixed_and_spans_width(open_site):
    page, _ = open_site()
    box = page.locator(".masthead")
    assert box.evaluate("el => getComputedStyle(el).position") == "fixed"
    rect = box.bounding_box()
    assert rect["x"] <= 1 and rect["width"] >= page.viewport_size["width"] - 2


def test_skip_link_hidden_until_focus(open_site):
    page, _ = open_site()
    skip = page.locator(".skip")
    off = skip.bounding_box()
    assert off["x"] < 0  # parked at left:-9999px

    skip.focus()
    on = skip.bounding_box()
    assert on["x"] >= 0 and on["y"] >= 0  # pulled into the viewport


def test_masthead_ground_turns_opaque_after_scroll(open_site):
    page, _ = open_site()
    assert "is-scrolled" not in (page.locator("html").get_attribute("class") or "")
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(300)
    assert "is-scrolled" in page.locator("html").get_attribute("class")
