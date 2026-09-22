"""In-view domain switcher in #collage's own .view__bar.

Once a masthead icon jumps a reader into #collage, the masthead — those same
three icons included — goes `inert` (setBehindInert in main.js), so there was
no way to move between English/chess/climbing except manual scrolling. These
three buttons live inside the view's own sticky .view__bar instead, so they
stay reachable the whole time the view is open. They reuse the masthead's
exact data-collage-jump wiring (main.js's jumpers query picks up any matching
element) rather than adding new JS. See BUILD-NOTES.md's entry for this
stage.
"""

import pytest

from conftest import horizontal_overflow

JUMP_TARGETS = [("en", "collage-en"), ("chess", "collage-chess"), ("climb", "collage-climb")]


def _switcher_buttons(page):
    return page.locator(".view__bar .tools__group .tool--icon")


def test_three_buttons_after_a_divider_in_the_view_bar(open_site):
    page, _ = open_site(hash="#collage")
    tools = page.locator(".view__bar .view__tools")
    assert tools.locator(".tools__group").count() == 1
    assert tools.locator(".tools__rule").count() == 1
    assert _switcher_buttons(page).count() == 3

    order = page.evaluate(
        """() => [...document.querySelector('.view__bar .view__tools').children].map(el =>
            el.classList.contains('tools__group') ? 'jump-group'
            : el.classList.contains('tools__rule') ? 'rule'
            : el.classList.contains('themeswitch') ? 'theme'
            : el.classList.contains('langswitch') ? 'lang'
            : el.classList.contains('view__back') ? 'back'
            : el.className)"""
    )
    assert order == ["jump-group", "rule", "theme", "lang", "back"]


def test_buttons_have_the_expected_accessible_names(open_site):
    page, _ = open_site(hash="#collage")
    buttons = _switcher_buttons(page)
    labels = [buttons.nth(i).get_attribute("aria-label") for i in range(3)]
    titles = [buttons.nth(i).get_attribute("title") for i in range(3)]
    assert labels == [
        "Go to the English photographs",
        "Go to the chess photographs",
        "Go to the climbing photographs",
    ]
    assert titles == ["English", "Chess", "Climbing"]
    for i in range(3):
        assert buttons.nth(i).locator("svg").get_attribute("aria-hidden") == "true"


def test_glyphs_match_the_masthead_current_versions(open_site):
    """Regression guard: the in-view .view__group chess label glyph predated
    the masthead's P21 rework and drifted (6.25 rects vs the masthead's 7.5) —
    fixed alongside adding this switcher. Both the switcher and the
    .view__group label must now match the masthead's rect geometry."""
    page, _ = open_site(hash="#collage")
    buttons = _switcher_buttons(page)

    chess_rects = buttons.nth(1).locator("svg rect")
    assert chess_rects.count() == 4
    for i in range(4):
        assert chess_rects.nth(i).get_attribute("width") == "7.5"

    group_label_rects = page.locator("#collage-chess").locator(
        "xpath=preceding-sibling::p[contains(@class,'label--glyph')][1]"
    ).locator("svg rect")
    assert group_label_rects.count() == 4
    for i in range(4):
        assert group_label_rects.nth(i).get_attribute("width") == "7.5"


@pytest.mark.parametrize("jump_key,heading_id", JUMP_TARGETS)
def test_buttons_jump_between_groups_from_inside_the_view(open_site, jump_key, heading_id):
    """The actual fix: from inside #collage (already past the masthead, which
    is now inert), clicking one of these buttons still moves focus to the
    target group's heading without leaving or reopening the view."""
    page, _ = open_site(hash="#collage")
    page.wait_for_function("document.activeElement && document.activeElement.id === 'collage-title'")

    btn = page.locator(f'.view__bar [data-collage-jump="{jump_key}"]')
    assert btn.count() == 1
    btn.click()

    page.wait_for_function(
        "id => document.activeElement && document.activeElement.id === id", arg=heading_id
    )
    assert "#collage" in page.url  # never left the view

    page.wait_for_timeout(600)
    placed = page.locator(f"#{heading_id}").evaluate(
        """el => {
            const r = el.getBoundingClientRect();
            const bar = document.querySelector('#collage .view__bar').getBoundingClientRect();
            return r.top >= bar.bottom - 2 && r.top < innerHeight * 0.75;
        }"""
    )
    assert placed, f"{heading_id} not brought to the top of the view"


def test_bar_stays_inert_with_the_lightbox_open(open_site):
    """The switcher is a child of .view__bar, so it must inherit the existing
    inert-on-lightbox-open behaviour with no extra wiring."""
    page, _ = open_site(hash="#collage")
    page.wait_for_function("document.activeElement && document.activeElement.id === 'collage-title'")
    page.locator(".collage__trigger").first.click()
    page.wait_for_selector(".lightbox", state="visible")
    assert page.evaluate("document.querySelector('.view__bar').inert") is True


@pytest.mark.parametrize("width,visible", [(600, True), (430, True), (400, False), (375, False), (320, False)])
def test_switcher_hides_below_400px_rather_than_crowd(open_site, width, visible):
    """Below 400px the switcher's .tools__group has no flex-shrink override
    (unlike .tool, which treats its 44px target as a floor), so once
    .view__tools runs out of room flexbox crushes the group and its buttons
    visibly overlap the theme toggle next to it. Same crowding the masthead
    nav already hit at this exact width. Hidden below 400px rather than force
    a cramped fit; verify both the visibility switch and that nothing
    overlaps or overflows at any of these widths."""
    page, _ = open_site(hash="#collage", viewport={"width": width, "height": 700})
    page.wait_for_function("document.activeElement && document.activeElement.id === 'collage-title'")

    group = page.locator(".view__bar .tools__group")
    is_visible = group.evaluate("el => getComputedStyle(el).display") != "none"
    assert is_visible == visible, f"{width}px: expected switcher visible={visible}, got {is_visible}"

    assert not horizontal_overflow(page), f"{width}px overflows"

    if visible:
        boxes = [_switcher_buttons(page).nth(i).bounding_box() for i in range(3)] + [
            page.locator(".view__bar .themeswitch").bounding_box(),
            page.locator(".view__bar .langswitch").bounding_box(),
            page.locator(".view__back").bounding_box(),
        ]
        boxes.sort(key=lambda b: b["x"])
        for a, b in zip(boxes, boxes[1:]):
            assert a["x"] + a["width"] <= b["x"] + 0.5, f"{width}px: controls overlap ({a} vs {b})"
