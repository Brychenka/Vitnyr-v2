"""Masthead discipline icons — open book / chess / screw-lock carabiner
(design handoff: `reference/design_handoff_collage_nav_icons/`).

History: the glyphs shipped as shortcuts into the home page's `#collage`
view (`data-collage-jump`, captioned "Photos"), while the discipline pages
used the same three glyphs to link to /english/, /chess/, /climbing/. SITE-PLAN
C4 (2026-11-20) gave them one meaning everywhere: on all four pages they are
links to the discipline pages, captioned "Coaching", the current page marked;
"Photos" is a plain text link to the gallery (masthead from 1140px, footer at
every width). The gallery keeps its own in-view switcher, which still carries
`data-collage-jump`. SITE-PLAN C5 (same day) set the phone masthead in two rows
instead of three, without shrinking any 44px target (J4).

Covers structure, accessible names, glyph fidelity, ink tokens, the links,
the gallery's switcher, and the responsive guards the sizing passes earned:
the wordmark's brand floor, icons never running off a phone screen, 44px
targets, the caption always visible.
"""

import pytest

from conftest import NARROW, WIDE, horizontal_overflow

ICON_NAMES = {"en": ["English", "Chess", "Climbing"],
              "ru": ["Английский", "Шахматы", "Скалолазание"]}
ICON_TITLES = ["English", "Chess", "Climbing"]
ICON_HREFS = ["/english/", "/chess/", "/climbing/"]
PAGES = [("index.html", None), ("english/", 0), ("chess/", 1), ("climbing/", 2)]

# data-collage-jump key -> the group heading id it must land focus on
JUMP_TARGETS = [("chess", "collage-chess"), ("climb", "collage-climb"), ("en", "collage-en")]

# --lockup's floor. 13vw only exceeds this above ~1354px, so both NARROW and
# WIDE (1280) sit on the floor.
LOCKUP_FLOOR = 176


def _icons(page):
    return page.locator(".tools .tools__group--nav .tool--icon")


def test_three_icon_links_after_a_divider(open_site):
    page, _ = open_site()
    tools = page.locator(".tools")
    # the section quick-nav (2026-09-19) adds a second rule + group after the
    # discipline cluster (desktop only, display:none below 900px).
    assert tools.locator(".tools__rule").count() == 2
    assert _icons(page).count() == 3

    # P17: two clusters with the divider at the seam — the util toggles that
    # mutate the current page, then the rule, then the nav cluster.
    top = page.evaluate(
        """() => [...document.querySelector('.tools').children].map(el =>
            el.classList.contains('tools__group--util') ? 'util'
            : el.classList.contains('tools__rule') ? 'rule'
            : el.classList.contains('tools__group--nav') ? 'nav'
            : el.classList.contains('tools__group--sections') ? 'sections'
            : el.className)"""
    )
    assert top == ["util", "rule", "nav", "rule", "sections"]
    order = page.evaluate(
        """() => [...document.querySelector('.tools__group--nav').children].map(el =>
            el.classList.contains('tool--icon') ? 'icon'
            : el.classList.contains('tools__label') ? 'label'
            : el.classList.contains('tools__photos') ? 'photos'
            : el.classList.contains('tools__notes') ? 'notes'
            : el.className)"""
    )
    # the caption opens the cluster, right before the icons it names; the
    # gallery link and the notes link close it
    assert order == ["label", "icon", "icon", "icon", "photos", "notes"]


@pytest.mark.parametrize("path,current", PAGES)
def test_icons_link_to_the_discipline_pages_on_every_page(open_site, path, current):
    """C4: one meaning per icon. Same three links on all four pages; the page
    you're on is aria-current and underlined, home has none current. None
    of them is a collage jump any more."""
    page, _ = open_site(path=path)
    icons = _icons(page)
    assert icons.count() == 3
    assert [icons.nth(i).get_attribute("href") for i in range(3)] == ICON_HREFS
    assert [icons.nth(i).get_attribute("title") for i in range(3)] == ICON_TITLES
    assert page.locator(".masthead [data-collage-jump]").count() == 0
    marked = [icons.nth(i).get_attribute("aria-current") for i in range(3)]
    assert marked == [("page" if i == current else None) for i in range(3)]


@pytest.mark.parametrize("lang", ["en", "ru"])
def test_icon_links_are_named_in_both_languages(open_site, lang):
    """Icon-only links: the name comes from a visually hidden span that
    theme.js swaps with the language, never from the SVG (aria-hidden)."""
    page, _ = open_site(lang=lang)
    icons = _icons(page)
    names = [icons.nth(i).evaluate("el => el.textContent.trim()") for i in range(3)]
    assert names == ICON_NAMES[lang]
    for i in range(3):
        assert icons.nth(i).locator("svg").get_attribute("aria-hidden") == "true"


def test_icon_glyphs_are_pasted_verbatim_from_the_handoff(open_site):
    """Guards against "redrawing/optimising" the glyphs — the handoff README
    is explicit that the path data is final. Checks the discriminating
    geometry of each glyph, not just its presence."""
    for path, _cur in PAGES:
        page, _ = open_site(path=path)
        icons = _icons(page)

        chess_rects = icons.nth(1).locator("svg rect")
        assert chess_rects.count() == 4
        fills = [chess_rects.nth(i).get_attribute("fill") for i in range(4)]
        assert fills == ["currentColor", "none", "none", "currentColor"]

        climb_paths = icons.nth(2).locator("svg path")
        assert climb_paths.count() == 4
        assert climb_paths.nth(0).get_attribute("d").startswith("M16.9 8.4C17.7 5.7")
        assert climb_paths.nth(3).get_attribute("stroke-linejoin") == "miter"

        book_paths = icons.nth(0).locator("svg path")
        assert book_paths.count() == 2
        assert book_paths.nth(0).get_attribute("d") == "M4.5 5.5c2-1 4.5-1 6.8 0v13.2c-2.3-1-4.8-1-6.8 0z"
        assert book_paths.nth(1).get_attribute("d") == "M19.5 5.5c-2-1-4.5-1-6.8 0v13.2c2.3-1 4.8-1 6.8 0z"

        for i in range(3):
            assert icons.nth(i).locator("svg").get_attribute("viewBox") == "0 0 24 24"


@pytest.mark.parametrize("scheme,expected_fg2", [("dark", "rgb(168, 171, 169)"), ("light", "rgb(90, 95, 96)")])
def test_icons_use_the_theme_ink_token_no_new_colour(open_site, scheme, expected_fg2):
    """No colour value in the handoff except currentColor/none — the glyph's
    rendered colour must trace to --fg2, the same token every other .tool
    uses at rest, in both pairs."""
    page, _ = open_site(theme=scheme)
    icons = _icons(page)
    for i in range(3):
        assert icons.nth(i).evaluate("el => getComputedStyle(el).color") == expected_fg2
        colours = icons.nth(i).locator("svg").evaluate(
            """svg => [...svg.querySelectorAll('*')].flatMap(el => [
                el.getAttribute('fill'), el.getAttribute('stroke')
            ]).filter(v => v && v !== 'none' && v !== 'currentColor')"""
        )
        assert colours == []


def test_icon_svgs_render_at_the_specified_24px(open_site):
    # 17 -> 19 -> 22 (P18) -> 24 with stroke-width 1.5 (P20, "carry the nav
    # cluster with scale, not weight"). See .tool--icon svg in style.css.
    page, _ = open_site()
    for i in range(3):
        box = _icons(page).nth(i).locator("svg").bounding_box()
        assert box["width"] == pytest.approx(24, abs=0.5)
        assert box["height"] == pytest.approx(24, abs=0.5)


# --- the gallery: reached by name, not by the icons ---

def test_masthead_photos_link_opens_the_gallery_on_home(open_site):
    page, _ = open_site()
    link = page.locator(".masthead .tools__photos")
    assert link.get_attribute("href") == "#collage"
    assert link.is_visible()          # WIDE is 1280, over its 1140px floor
    link.click()
    page.wait_for_selector("html.collage-open")
    assert "#collage" in page.url
    # Back returns focus to the link that opened it
    page.locator(".view__back").click()
    page.wait_for_function("!document.documentElement.classList.contains('collage-open')")
    page.wait_for_function(
        "document.activeElement && document.activeElement.classList.contains('tools__photos')")


@pytest.mark.parametrize("path", ["english/", "chess/", "climbing/"])
def test_discipline_pages_link_to_the_gallery_by_name(open_site, path):
    page, _ = open_site(path=path)
    for sel in (".masthead .tools__photos", ".foot__photos"):
        assert page.locator(sel).get_attribute("href") == "/#collage"


def test_masthead_photos_link_steps_aside_below_1140(open_site):
    """Measured: below 1140px a discipline page's five numerals, the caption
    and this link don't share one row. The footer's link is there at every
    width."""
    page, _ = open_site(viewport={"width": 1100, "height": 800}, path="chess/")
    assert not page.locator(".masthead .tools__photos").is_visible()
    page, _ = open_site(viewport=NARROW, has_touch=True, path="chess/")
    assert not page.locator(".masthead .tools__photos").is_visible()
    assert page.locator(".foot__photos").count() == 1


def test_see_me_at_work_is_still_the_door_that_morphs(open_site):
    """The band stays the one [data-collage-open] the router treats as the
    door (it morphs into the view's label); the "Photos" links carry
    data-collage-link instead, so they can't take its place."""
    page, _ = open_site()
    assert page.locator("[data-collage-open]").count() == 1
    assert "proof__link" in page.locator("[data-collage-open]").get_attribute("class")
    assert page.locator("[data-collage-link]").count() == 2


@pytest.mark.parametrize("jump_key,heading_id", JUMP_TARGETS)
def test_gallery_switcher_jumps_to_its_group(open_site, jump_key, heading_id):
    """Inside the open gallery, the switcher's three glyphs (same drawings)
    still carry data-collage-jump: a click slides that group's label under
    the sticky bar and moves focus onto its heading."""
    page, _ = open_site(hash="#collage")
    page.wait_for_selector("html.collage-open")
    btn = page.locator(f'#collage .view__tools [data-collage-jump="{jump_key}"]')
    assert btn.count() == 1
    btn.click()
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


def test_nothing_opens_the_view_on_load(open_site):
    page, _ = open_site()
    assert "collage-open" not in page.locator("html").get_attribute("class")
    assert "#collage" not in page.url


# --- the wordmark's floor and the phone masthead ---

def test_lockup_holds_its_brand_minimum_with_icons_present(open_site):
    """Regression: flexbox once shrank .lockup below --lockup's 176px floor to
    make room for the icon row. See the flex:none comment on .lockup."""
    for viewport in (NARROW, WIDE):
        page, _ = open_site(viewport=viewport)
        width = page.locator(".lockup").bounding_box()["width"]
        assert width == pytest.approx(LOCKUP_FLOOR, abs=1), viewport


@pytest.mark.parametrize("width", [603, 900, 1280])
def test_masthead_is_one_row_from_603px(open_site, width):
    page, _ = open_site(viewport={"width": width, "height": 800})
    lockup = page.locator(".lockup").bounding_box()
    theme = page.locator(".masthead .themeswitch").bounding_box()
    icon = _icons(page).first.bounding_box()
    assert icon["y"] == pytest.approx(theme["y"], abs=3)
    assert theme["y"] < lockup["y"] + lockup["height"], f"{width}px: tools dropped under the mark"


@pytest.mark.parametrize("width", [320, 375, 414, 602])
@pytest.mark.parametrize("lang", ["en", "ru"])
@pytest.mark.parametrize("scrolled", [False, True])
def test_phone_masthead_is_two_rows(open_site, width, lang, scrolled):
    """C5: row 1 is the mark with theme + language beside it, row 2 the
    caption and the three icons, right-aligned. Same layout before and
    after scrolling; the caption never steps aside."""
    page, _ = open_site(viewport={"width": width, "height": 780}, has_touch=True, lang=lang)
    if scrolled:
        page.evaluate("window.scrollTo(0, 50)")
    page.wait_for_timeout(250)
    assert not horizontal_overflow(page)

    lockup = page.locator(".lockup").bounding_box()
    theme = page.locator(".masthead .themeswitch").bounding_box()
    lang_btn = page.locator(".masthead .langswitch").bounding_box()
    label = page.locator(".tools__label").bounding_box()
    icons = [_icons(page).nth(i).bounding_box() for i in range(3)]

    lock_mid = lockup["y"] + lockup["height"] / 2
    for box in (theme, lang_btn):          # row 1, beside the mark
        assert abs(box["y"] + box["height"] / 2 - lock_mid) < 6
        assert box["x"] >= lockup["x"] + lockup["width"]
    row2 = icons[0]["y"]
    assert row2 > lockup["y"] + lockup["height"] - 1   # row 2, under it
    for box in icons + [label]:
        assert abs(box["y"] + box["height"] / 2 - (row2 + icons[0]["height"] / 2)) < 6
    assert page.locator(".tools__label").evaluate("el => getComputedStyle(el).display") != "none"
    height = page.locator(".masthead").bounding_box()["height"]
    assert height <= 150, f"{width}/{lang}: masthead {height}px tall"


def test_phone_masthead_no_taller_than_two_rows_without_js(open_site):
    page, _ = open_site(viewport={"width": 375, "height": 700}, has_touch=True, java_script_enabled=False)
    assert page.locator(".tools__label").evaluate("el => getComputedStyle(el).display") != "none"
    assert page.locator(".masthead").bounding_box()["height"] <= 150


def test_the_mark_stays_clickable_under_the_tools_box(open_site):
    """On a phone .tools spans both rows on a subgrid and so overlaps the
    mark's cell; it must let the pointer through to the mark."""
    page, _ = open_site(viewport={"width": 375, "height": 780}, has_touch=True)
    box = page.locator(".lockup").bounding_box()
    hit = page.evaluate(
        "([x, y]) => document.elementFromPoint(x, y).closest('.lockup') !== null",
        [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2])
    assert hit


@pytest.mark.parametrize("width", [320, 360, 375, 390, 414, 480, 602])
@pytest.mark.parametrize("lang", ["en", "ru"])
def test_nav_icons_stay_inside_the_viewport_on_a_phone(open_site, width, lang):
    """2026-09-10: an over-full row once ran the icons off the right edge
    silently (scrollWidth stayed clean). Measured against the viewport, on a
    coarse pointer, where touch padding makes the row widest."""
    page, _ = open_site(viewport={"width": width, "height": 780}, has_touch=True, lang=lang)
    page.wait_for_timeout(200)
    vw = page.evaluate("() => window.innerWidth")
    for sel in (".tools__label", ".masthead .themeswitch", ".masthead .langswitch"):
        box = page.locator(sel).bounding_box()
        assert box["x"] >= -0.5 and box["x"] + box["width"] <= vw + 0.5, f"{sel} clipped at {width}/{lang}"
    for i in range(3):
        box = _icons(page).nth(i).bounding_box()
        assert box["x"] >= -0.5, f"icon {i} runs off the LEFT at {width}px/{lang}"
        assert box["x"] + box["width"] <= vw + 0.5, f"icon {i} clipped at {width}px/{lang}"
        assert box["width"] >= 43.5, f"icon {i} target shrank at {width}px/{lang}"


def test_masthead_does_not_overlap_hero_content(open_site):
    """--head still clears the two-row phone masthead."""
    for touch in (False, True):
        page, _ = open_site(viewport={"width": 375, "height": 780}, has_touch=touch)
        mb = page.locator(".masthead").bounding_box()
        eyebrow_top = page.locator(".eyebrow").bounding_box()["y"]
        assert eyebrow_top >= mb["y"] + mb["height"] - 1


def test_icon_touch_target_is_44px_on_coarse_pointers(open_site):
    page, _ = open_site(viewport={"width": 375, "height": 780}, has_touch=True)
    assert page.evaluate("matchMedia('(pointer: coarse)').matches")
    for i in range(3):
        box = _icons(page).nth(i).bounding_box()
        assert box["width"] >= 44 and box["height"] >= 44


# --- C2: the text controls beside those icons used to sit as low as 19x23 on
# a coarse pointer — under WCAG 2.2's 24px minimum. ---

def test_text_tool_touch_targets_clear_24px_on_coarse_pointers(open_site):
    page, _ = open_site(viewport={"width": 375, "height": 780}, has_touch=True)
    assert page.evaluate("matchMedia('(pointer: coarse)').matches")
    for selector in (".masthead .themeswitch", ".masthead .langswitch", ".foot__photos", ".foot__top"):
        box = page.locator(selector).bounding_box()
        assert box["width"] >= 24 and box["height"] >= 24, f"{selector}: {box}"


def test_view_back_touch_target_clears_24px_on_coarse_pointers(open_site):
    page, _ = open_site(hash="#collage", viewport={"width": 375, "height": 780}, has_touch=True)
    assert page.evaluate("matchMedia('(pointer: coarse)').matches")
    box = page.locator(".view__back").bounding_box()
    assert box["width"] >= 24 and box["height"] >= 24, box


# --- P10: the icons carry one shared visible caption (a touch reader never
# sees aria-label or title). ---

def test_icons_have_one_shared_visible_caption(open_site):
    page, _ = open_site()
    label = page.locator(".tools .tools__label")
    assert label.count() == 1
    assert label.text_content().strip() == "Coaching"
    assert label.evaluate("el => getComputedStyle(el).display") != "none"
    assert page.evaluate(
        """() => {
            const label = document.querySelector('.tools__label');
            const firstIcon = document.querySelector('.tools .tools__group--nav .tool--icon');
            return label.closest('.tools__group--nav')
                && (label.compareDocumentPosition(firstIcon) & Node.DOCUMENT_POSITION_FOLLOWING);
        }"""
    )


def test_icon_caption_is_localised(open_site):
    page, _ = open_site(lang="ru")
    assert page.locator(".tools .tools__label").text_content().strip() == "Направления"
    assert page.locator(".masthead .tools__photos").text_content().strip() == "Фото"
