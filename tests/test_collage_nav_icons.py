"""Collage nav icons — chess / screw-lock carabiner / open book buttons added
to `nav.tools` (design handoff: `reference/design_handoff_collage_nav_icons/`).

The glyphs shipped looks-only first (SVG paths pasted verbatim, `.tool`
reused as-is); they are now wired as shortcuts into the `#collage` view —
each carries `data-collage-jump` and, on click, opens the view and moves
focus to its domain group's heading (`main.js` `initCollageView`). Covers
structure, accessible names, glyph fidelity, ink tokens, the jump wiring,
and the two responsive bugs the sizing pass caught — the wordmark shrinking
below its brand-mandated floor, and the icon row having nowhere to go below
~600px.
"""

import pytest

from conftest import NARROW, WIDE, horizontal_overflow

ICON_LABELS = [
    "Jump to the chess photographs",
    "Jump to the climbing photographs",
    "Jump to the English coaching photographs",
]
ICON_TITLES = ["Chess", "Climbing", "English"]

# data-collage-jump key -> the group heading id it must land focus on
JUMP_TARGETS = [("chess", "collage-chess"), ("climb", "collage-climb"), ("en", "collage-en")]

# --lockup's floor. 13vw only exceeds this above ~1354px, so both NARROW and
# WIDE (1280) sit on the floor.
LOCKUP_FLOOR = 176


def _icon_buttons(page):
    return page.locator(".tools .tool--icon")


def test_three_icon_buttons_after_a_divider(open_site):
    page, _ = open_site()
    tools = page.locator(".tools")
    assert tools.locator(".tools__rule").count() == 1
    assert _icon_buttons(page).count() == 3

    # P17: .tools is two clusters with the divider at the seam — the util
    # toggles (theme + language) that mutate the current page, then
    # .tools__rule, then the collage-nav cluster (the "Photos" caption plus
    # the three jump icons it captions).
    top = page.evaluate(
        """() => [...document.querySelector('.tools').children].map(el =>
            el.classList.contains('tools__group--util') ? 'util'
            : el.classList.contains('tools__rule') ? 'rule'
            : el.classList.contains('tools__group--nav') ? 'nav'
            : el.className)"""
    )
    assert top == ["util", "rule", "nav"]

    def group_order(selector):
        return page.evaluate(
            """(sel) => [...document.querySelector(sel).children].map(el =>
                el.classList.contains('tool--icon') ? 'icon'
                : el.classList.contains('tools__label') ? 'label'
                : el.className)""",
            selector,
        )

    assert group_order(".tools__group--util") == ["tool themeswitch", "tool langswitch"]
    # P10: the shared "Photos" caption opens the nav cluster, right before
    # the icons it captions.
    assert group_order(".tools__group--nav") == ["label", "icon", "icon", "icon"]


def test_icon_buttons_have_the_exact_expected_accessible_names(open_site):
    page, _ = open_site()
    buttons = _icon_buttons(page)
    labels = [buttons.nth(i).get_attribute("aria-label") for i in range(3)]
    titles = [buttons.nth(i).get_attribute("title") for i in range(3)]
    assert labels == ICON_LABELS
    assert titles == ICON_TITLES
    # aria-hidden on the glyph: the name comes from the button, not the SVG.
    for i in range(3):
        svg = buttons.nth(i).locator("svg")
        assert svg.get_attribute("aria-hidden") == "true"


def test_icon_glyphs_are_pasted_verbatim_from_the_handoff(open_site):
    """Guards against "redrawing/optimising" the glyphs — the handoff README
    is explicit that the path data is final. Checks the discriminating
    geometry of each glyph, not just its presence."""
    page, _ = open_site()
    buttons = _icon_buttons(page)

    chess_rects = buttons.nth(0).locator("svg rect")
    assert chess_rects.count() == 4
    fills = [chess_rects.nth(i).get_attribute("fill") for i in range(4)]
    assert fills == ["currentColor", "none", "none", "currentColor"]

    climb_paths = buttons.nth(1).locator("svg path")
    assert climb_paths.count() == 4
    assert climb_paths.nth(0).get_attribute("d").startswith("M16.9 8.4C17.7 5.7")
    assert climb_paths.nth(3).get_attribute("stroke-linejoin") == "miter"

    book_paths = buttons.nth(2).locator("svg path")
    assert book_paths.count() == 2
    assert book_paths.nth(0).get_attribute("d") == "M4.5 5.5c2-1 4.5-1 6.8 0v13.2c-2.3-1-4.8-1-6.8 0z"
    assert book_paths.nth(1).get_attribute("d") == "M19.5 5.5c-2-1-4.5-1-6.8 0v13.2c2.3-1 4.8-1 6.8 0z"

    for i in range(3):
        assert buttons.nth(i).locator("svg").get_attribute("viewBox") == "0 0 24 24"


@pytest.mark.parametrize("scheme,expected_fg2", [("dark", "rgb(168, 171, 169)"), ("light", "rgb(90, 95, 96)")])
def test_icons_use_the_theme_ink_token_no_new_colour(open_site, scheme, expected_fg2):
    """No colour value in the handoff except currentColor/none — the glyph's
    rendered colour must trace to --fg2, the same token every other .tool
    uses at rest, in both pairs."""
    page, _ = open_site(theme=scheme)
    buttons = _icon_buttons(page)
    for i in range(3):
        assert buttons.nth(i).evaluate("el => getComputedStyle(el).color") == expected_fg2
        svg = buttons.nth(i).locator("svg")
        colours = svg.evaluate(
            """svg => [...svg.querySelectorAll('*')].flatMap(el => [
                el.getAttribute('fill'), el.getAttribute('stroke')
            ]).filter(v => v && v !== 'none' && v !== 'currentColor')"""
        )
        assert colours == []


def test_icon_svgs_render_at_the_specified_24px(open_site):
    # 17 -> 19 (48e40a0 / 597e188), 19 -> 22 at P18, then 22 -> 24 with
    # stroke-width 1.5 at P20 ("carry the nav cluster with scale, not weight",
    # 315eb8e). See the .tool--icon svg comment in style.css.
    page, _ = open_site()
    for i in range(3):
        box = _icon_buttons(page).nth(i).locator("svg").bounding_box()
        assert box["width"] == pytest.approx(24, abs=0.5)
        assert box["height"] == pytest.approx(24, abs=0.5)


@pytest.mark.parametrize("jump_key,heading_id", JUMP_TARGETS)
def test_icon_buttons_jump_to_their_collage_group(open_site, jump_key, heading_id):
    """Each icon carries data-collage-jump and, on click, opens the #collage
    view and moves focus onto that domain group's heading — clear of the
    sticky .view__bar and near the top of the view. See BUILD-NOTES.md's
    "collage nav icons" entry."""
    page, _ = open_site()
    btn = page.locator(f'.tools .tool--icon[data-collage-jump="{jump_key}"]')
    assert btn.count() == 1

    btn.click()
    page.wait_for_selector("html.collage-open")
    assert "#collage" in page.url

    # focus settles on the target heading (tabindex -1), not the view wrapper
    page.wait_for_function(
        "id => document.activeElement && document.activeElement.id === id", arg=heading_id
    )

    page.wait_for_timeout(600)  # let the smooth scroll finish before measuring
    placed = page.locator(f"#{heading_id}").evaluate(
        """el => {
            const r = el.getBoundingClientRect();
            const bar = document.querySelector('#collage .view__bar').getBoundingClientRect();
            return r.top >= bar.bottom - 2 && r.top < innerHeight * 0.75;
        }"""
    )
    assert placed, f"{heading_id} not brought to the top of the view"


def test_icons_do_not_open_the_view_on_load(open_site):
    """The wiring is click-only: a cold load must not have the view open or
    the hash set just because the icons exist."""
    page, _ = open_site()
    assert "collage-open" not in page.locator("html").get_attribute("class")
    assert "#collage" not in page.url


def test_lockup_holds_its_brand_minimum_with_icons_present(open_site):
    """Regression: flexbox was shrinking .lockup below --lockup's 176px floor
    to make room for the new icon row rather than letting .tools give way.
    See the flex:none comment on .lockup in style.css."""
    for viewport in (NARROW, WIDE):
        page, _ = open_site(viewport=viewport)
        width = page.locator(".lockup").bounding_box()["width"]
        assert width == pytest.approx(LOCKUP_FLOOR, abs=1), viewport


@pytest.mark.parametrize("width,wrapped", [(603, False), (602, True), (375, True), (320, True)])
def test_tools_row_wraps_below_600px_single_row_above(open_site, width, wrapped):
    """.masthead has exactly two flex children — .lockup and .tools — so
    wrapping moves .tools (Cream, RU, divider and all three icons together)
    onto its own line below the wordmark. It does not split the icons onto a
    separate line from Cream/RU: they're one flex item and move as a unit.

    J4 (Jury Pass II, 2026-09-12): below 400px that single-line guarantee now
    only holds once scrolled — .tools__group--nav gets its own line at rest
    so the Photos/Фото caption has room (see test_collage_icon_caption_* in
    test_layout.py). Scrolling first here keeps this test asserting the
    original invariant for the state it actually has to hold in: sticky and
    compact, mid-read, which is the state the 2026-09-10 fix this guards
    was written for."""
    page, _ = open_site(viewport={"width": width, "height": 700})
    if width <= 400:
        page.evaluate("window.scrollTo(0, 50)")
    page.wait_for_timeout(200)
    assert not horizontal_overflow(page), f"{width}px overflows"

    lockup_box = page.locator(".lockup").bounding_box()
    tools_box = page.locator(".tools").bounding_box()
    is_wrapped = tools_box["y"] >= lockup_box["y"] + lockup_box["height"] - 1
    assert is_wrapped == wrapped, f"{width}px: expected wrapped={wrapped}, got {is_wrapped}"

    # Cream/RU and the icons stay together on whichever line .tools lands on.
    theme_top = page.locator(".masthead .themeswitch").bounding_box()["y"]
    icon_top = _icon_buttons(page).first.bounding_box()["y"]
    assert icon_top == pytest.approx(theme_top, abs=3)

    # the mark still holds its floor even while .tools is wrapping under it
    assert lockup_box["width"] == pytest.approx(LOCKUP_FLOOR, abs=1)


# --- 2026-09-10: the row was running its own controls off the right edge.
# .masthead is overflow-clipped and .tools never wraps below 602px, so an
# over-full row neither scrolled nor stacked — the collage jumps simply left
# the viewport. documentElement.scrollWidth stayed clean throughout, which is
# why every existing layout guard passed while the book icon sat 35px outside
# the screen at 375/EN. Measure the icons against the viewport itself, on a
# COARSE pointer: touch padding makes the real phone row ~36px wider than the
# same width measured with a mouse, and that gap is the whole bug. ---

@pytest.mark.parametrize("width", [320, 360, 375, 390, 414, 480, 602])
@pytest.mark.parametrize("lang", ["en", "ru"])
def test_nav_icons_stay_inside_the_viewport_on_a_phone(open_site, width, lang):
    page, _ = open_site(
        viewport={"width": width, "height": 780}, has_touch=True, lang=lang
    )
    page.wait_for_timeout(200)

    vw = page.evaluate("() => window.innerWidth")
    boxes = [
        _icon_buttons(page).nth(i).bounding_box() for i in range(3)
    ]
    for i, box in enumerate(boxes):
        assert box["x"] >= -0.5, f"icon {i} runs off the LEFT at {width}px/{lang}"
        assert box["x"] + box["width"] <= vw + 0.5, (
            f"icon {i} runs {box['x'] + box['width'] - vw:.0f}px past the right "
            f"edge at {width}px/{lang} — clipped, and unreachable"
        )
        # the target itself must survive whatever tightening got it to fit
        assert box["width"] >= 43.5, f"icon {i} target shrank at {width}px/{lang}"


# --- J4 (Jury Pass II, 2026-09-12): the 2026-09-10 fix above stopped the
# nav row running off-screen by dropping its caption entirely below 400px —
# which also meant a touch reader, who never sees aria-label or title, had
# no name at all for the three icons on the phone widths most readers
# carry. It's back at rest (util and nav each get a full-width line, so the
# caption has room without repeating the overflow bug), and steps aside
# again once scrolled — a first-glance hint, not a permanent second row
# during actual reading. ---

@pytest.mark.parametrize("width", [320, 375, 400])
@pytest.mark.parametrize("lang", ["en", "ru"])
def test_collage_icon_caption_is_back_before_scrolling_on_phone(open_site, width, lang):
    page, _ = open_site(viewport={"width": width, "height": 700}, has_touch=True, lang=lang)
    page.wait_for_timeout(200)
    label = page.locator(".tools__label")
    assert label.evaluate("el => getComputedStyle(el).display") != "none"
    assert label.inner_text().strip() != ""
    assert not horizontal_overflow(page), f"{width}px/{lang} overflows with the caption showing"

    # still one nowrap line per group — never a re-opened wrap inside a row
    vw = page.evaluate("() => window.innerWidth")
    for i in range(3):
        box = _icon_buttons(page).nth(i).bounding_box()
        assert box["x"] + box["width"] <= vw + 0.5, f"icon {i} clipped at {width}px/{lang}"


@pytest.mark.parametrize("width", [320, 375, 400])
def test_collage_icon_caption_hides_again_once_scrolled_on_phone(open_site, width):
    page, _ = open_site(viewport={"width": width, "height": 700}, has_touch=True)
    page.evaluate("window.scrollTo(0, 50)")
    page.wait_for_timeout(200)
    assert "is-scrolled" in page.locator("html").get_attribute("class")
    label = page.locator(".tools__label")
    assert label.evaluate("el => getComputedStyle(el).display") == "none"
    assert not horizontal_overflow(page), f"{width}px overflows once scrolled"


def test_collage_icon_caption_never_hides_without_js(open_site):
    """No is-scrolled tracking without JS, so the caption — and the roomier
    layout it needs — stays. Degrading toward showing more, not less."""
    page, _ = open_site(viewport={"width": 375, "height": 700}, has_touch=True, java_script_enabled=False)
    label = page.locator(".tools__label")
    assert label.evaluate("el => getComputedStyle(el).display") != "none"


def test_phone_masthead_is_shorter_once_scrolled(open_site):
    """J9 measured the sticky phone masthead at a permanent 127.6px. Bringing
    the caption back made the unscrolled header taller still, so the
    reduction has to land in the state the reader actually reads in."""
    page, _ = open_site(viewport={"width": 375, "height": 700}, has_touch=True)
    page.wait_for_timeout(200)
    unscrolled_height = page.locator(".masthead").bounding_box()["height"]

    page.evaluate("window.scrollTo(0, 50)")
    page.wait_for_timeout(200)
    scrolled_height = page.locator(".masthead").bounding_box()["height"]

    assert scrolled_height < unscrolled_height
    assert scrolled_height < 130, f"scrolled masthead is {scrolled_height}px, no shorter than before J4"


def test_wrapped_masthead_does_not_overlap_hero_content(open_site):
    """--head grows in the same media query that wraps .tools, so the taller
    two-line header still clears the hero's eyebrow line underneath it."""
    page, _ = open_site(viewport={"width": 375, "height": 780})
    masthead_bottom = page.locator(".masthead").bounding_box()["y"] + page.locator(".masthead").bounding_box()["height"]
    eyebrow_top = page.locator(".eyebrow").bounding_box()["y"]
    assert eyebrow_top >= masthead_bottom - 1


def test_icon_touch_target_is_44px_on_coarse_pointers(open_site):
    page, _ = open_site(viewport={"width": 375, "height": 780}, has_touch=True)
    is_coarse = page.evaluate("matchMedia('(pointer: coarse)').matches")
    assert is_coarse, "context did not register as a coarse pointer"
    for i in range(3):
        box = _icon_buttons(page).nth(i).bounding_box()
        assert box["width"] >= 44 and box["height"] >= 44


# --- C2: the text controls beside those icons (theme, language, collage
# Back) used to sit as low as 19x23 on a coarse pointer — under WCAG 2.2's
# 24px minimum, next to icons calculated to exactly 44px. ---

def test_text_tool_touch_targets_clear_24px_on_coarse_pointers(open_site):
    page, _ = open_site(viewport={"width": 375, "height": 780}, has_touch=True)
    assert page.evaluate("matchMedia('(pointer: coarse)').matches")
    for selector in (".masthead .themeswitch", ".masthead .langswitch"):
        box = page.locator(selector).bounding_box()
        assert box["width"] >= 24 and box["height"] >= 24, f"{selector}: {box}"


def test_view_back_touch_target_clears_24px_on_coarse_pointers(open_site):
    page, _ = open_site(hash="#collage", viewport={"width": 375, "height": 780}, has_touch=True)
    assert page.evaluate("matchMedia('(pointer: coarse)').matches")
    box = page.locator(".view__back").bounding_box()
    assert box["width"] >= 24 and box["height"] >= 24, box


# --- P10: the three icons above used to carry no *visible* label at all —
# aria-label and a title tooltip, neither of which a touch reader ever
# sees, pointing at a view the reader hasn't been told exists yet. One
# shared visible caption instead. ---

def test_icons_have_one_shared_visible_caption(open_site):
    page, _ = open_site()
    label = page.locator(".tools .tools__label")
    assert label.count() == 1
    assert label.text_content().strip() == "Photos"
    assert label.evaluate("el => getComputedStyle(el).display") != "none"
    # P17: the caption opens the collage-nav cluster — past the divider,
    # inside .tools__group--nav, and before the three icons it captions, so
    # it still reads as their heading rather than as a sibling of the icons.
    assert page.evaluate(
        """() => {
            const label = document.querySelector('.tools__label');
            const firstIcon = document.querySelector('.tools .tool--icon');
            return label.closest('.tools__group--nav')
                && (label.compareDocumentPosition(firstIcon) & Node.DOCUMENT_POSITION_FOLLOWING);
        }"""
    )


def test_icon_caption_is_localised(open_site):
    page, _ = open_site(lang="ru")
    assert page.locator(".tools .tools__label").text_content().strip() == "Фото"
