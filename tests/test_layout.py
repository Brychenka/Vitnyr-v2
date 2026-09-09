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


# --- C10: specimens rebuilt as full-width rows (were three cramped columns)
# with the sentence pair beside its explanation, not stacked above it. ---

def test_specimen_pair_sits_beside_its_explanation_at_desktop_width(open_site):
    page, _ = open_site(viewport=WIDE)
    first = page.locator(".spec").first
    lines_box = first.locator(".spec__lines").bounding_box()
    why_box = first.locator(".spec__why:visible").bounding_box()
    assert abs(lines_box["y"] - why_box["y"]) < 20, "columns aren't top-aligned"
    assert why_box["x"] > lines_box["x"] + lines_box["width"] - 20, "explanation isn't beside the pair"
    # and it runs the section's full width, not a third of it
    assert lines_box["width"] + why_box["width"] > 900


def test_specimen_pair_stacks_above_its_explanation_at_mobile_width(open_site):
    page, _ = open_site(viewport=NARROW)
    first = page.locator(".spec").first
    lines_box = first.locator(".spec__lines").bounding_box()
    why_box = first.locator(".spec__why:visible").bounding_box()
    assert why_box["y"] > lines_box["y"] + lines_box["height"] - 5


def test_specimen_sentence_pair_reads_at_showpiece_size(open_site):
    page, _ = open_site(viewport=WIDE)
    # the visible half of the pair, and the reveal button that stands in for the
    # other half, both at the showpiece size
    for sel in ("#specimen .line-spec.right", "#specimen .spec__prompt"):
        size = page.locator(sel).first.evaluate(
            "el => parseFloat(getComputedStyle(el).fontSize)"
        )
        assert size >= 17, f"{sel} still {size}px — the cramped three-column size was 14px"


def test_wrong_and_right_lines_have_a_visible_gap(open_site):
    """C11: .wrong's border sat flush against .right's — two adjacent boxes
    with no margin between them, so a 2px amber rule ran straight into a 2px
    green one and read as one stroke changing colour halfway down, right
    where the wrong/right distinction is the entire point of the device.
    Measured without JS, where both lines of the static pair are on screen."""
    lines = "#specimen .spec__lines"
    page, _ = open_site(viewport=WIDE, java_script_enabled=False)
    wrong = page.locator(f"{lines} >> .wrong").first
    right = page.locator(f"{lines} >> .right").first
    wrong_box = wrong.bounding_box()
    right_box = right.bounding_box()
    gap = right_box["y"] - (wrong_box["y"] + wrong_box["height"])
    assert gap > 4, f"only {gap}px between the two rules"


# --- C12: .sec's own top rule spans its full 1320px box; the row dividers
# inside a section (.mechanisms/.specs/.domains/.rows/.channels/.proof) used
# to sit --gut narrower on each side, purely as a side effect of .sec's own
# padding — two rule widths with no stated relationship. Bled back out so
# every hairline on the page is exactly one width. ---

@pytest.mark.parametrize("container", [
    "#method .mechanisms", "#specimen .specs", "#disciplines .domains",
    "#who .rows", "#contact .channels", "#disciplines .proof",
])
def test_row_dividers_are_flush_with_their_sections_own_rule(open_site, container):
    page, _ = open_site(viewport=WIDE)
    sec_box = page.locator(container.split(" ")[0]).bounding_box()
    inner_box = page.locator(container).bounding_box()
    assert abs(inner_box["x"] - sec_box["x"]) < 1, (container, inner_box, sec_box)
    assert abs(inner_box["width"] - sec_box["width"]) < 1, (container, inner_box, sec_box)


def test_row_dividers_content_keeps_its_original_inset(open_site):
    """The bleed is on the row/border box only — text inside still lines up
    with the sec__head heading above it, not with the section's raw edge."""
    page, _ = open_site(viewport=WIDE)
    heading_x = page.locator("#method .sec__head h2:visible").bounding_box()["x"]
    first_row_x = page.locator("#method .mechanisms > li").first.bounding_box()["x"]
    assert abs(heading_x - first_row_x) < 1


# --- P14: each .mechanisms > li is its own grid, so the old fixed middle
# track sized itself against the *paragraph* column, not its own heading —
# "Load management" got the same ~470px as the page's longest heading. ---

def test_mechanisms_heading_column_sizes_to_its_own_heading(open_site):
    page, _ = open_site(viewport=WIDE)
    rows = page.locator("#method .mechanisms > li")
    widths = []
    for i in range(rows.count()):
        h3 = rows.nth(i).locator("h3")
        p = rows.nth(i).locator("p:visible")
        h3_box = h3.bounding_box()
        p_box = p.bounding_box()
        widths.append(h3_box["width"])
        # paragraph starts shortly after the heading column, not ~470px later
        gap = p_box["x"] - (h3_box["x"] + h3_box["width"])
        assert 0 <= gap < 100, f"row {i}: {gap}px between heading and paragraph"
    # not every row given the same fixed width any more
    assert len(set(round(w) for w in widths)) > 1, widths
    # and none of them balloon past the declared cap
    assert all(w <= 260 for w in widths), widths


# --- P13: at a short mobile viewport the header's own two-line height plus
# .hero's centring used to push the actual headline down by more than the
# header itself — reclaim that by anchoring hero content near the top. ---

def test_mobile_hero_copy_starts_well_above_a_third_of_the_viewport(open_site):
    page, _ = open_site(viewport={"width": 390, "height": 844})
    line = page.locator(".hero__title .line:visible").first
    top = line.bounding_box()["y"]
    assert top < 260, f"first line of copy starts at y={top} of an 844px viewport"


def test_desktop_hero_still_centres(open_site):
    """The P13 fix is scoped to the mobile breakpoint — desktop keeps its
    vertically centred hero."""
    page, _ = open_site(viewport=WIDE)
    justify = page.locator(".hero").evaluate("el => getComputedStyle(el).justifyContent")
    assert justify == "center"


# --- C9: the handle used to sit in its own grid column pinned to the far
# right at 13px mono, up to 950px from the platform name it belongs to. ---

def test_contact_handle_sits_close_behind_its_platform_name(open_site):
    page, _ = open_site(viewport=WIDE)
    first = page.locator("#contact .channels li").first
    k_box = first.locator(".ch__k").bounding_box()
    v_box = first.locator(".ch__v").bounding_box()
    gap = v_box["x"] - (k_box["x"] + k_box["width"])
    assert 0 <= gap < 40, f"{gap}px between the platform name and its handle"


def test_contact_row_carries_the_proof_style_arrow_at_its_right_edge(open_site):
    page, _ = open_site(viewport=WIDE)
    row = page.locator("#contact .channels a").first
    row_box = row.bounding_box()
    arrow_box = row.locator(".ch__arrow").bounding_box()
    assert arrow_box["x"] + arrow_box["width"] > row_box["x"] + row_box["width"] - 5


# --- P9: "See the work" used to rest at --fg2 with its underline drawn in
# only on hover — the most recessive large element guarding the one visible
# door into the collage view. ---

# --- P8 (Stage 6, 2026-09-06): "Message me." used to be plain text — the
# page's one actual conversion goal (the free intro call) had no control
# anywhere on it. Now a real, localized Telegram deep link. ---

def test_contact_heading_is_a_real_telegram_link(open_site):
    page, _ = open_site(viewport=WIDE)
    cta = page.locator(".contact__big .contact__cta")
    assert cta.get_attribute("href").startswith("https://t.me/yngvil?text=")
    assert cta.get_attribute("target") == "_blank"
    assert cta.get_attribute("rel") == "noopener"


def test_contact_cta_prefill_text_is_localized(open_site):
    page, _ = open_site(viewport=WIDE)
    cta = page.locator(".contact__big .contact__cta")
    en_href = cta.get_attribute("href")
    assert "book%20the%20free%20intro%20call" in en_href

    page.locator(".masthead .langswitch").click()
    ru_href = cta.get_attribute("href")
    assert ru_href != en_href
    assert ru_href.startswith("https://t.me/yngvil?text=")
    # decodes to Cyrillic, not a re-encoded copy of the English string
    decoded = page.evaluate("href => decodeURIComponent(href.split('?text=')[1])", ru_href)
    assert "бесплатный" in decoded


def test_see_the_work_reads_at_full_foreground_and_underlined_at_rest(open_site):
    page, _ = open_site(theme="dark", viewport=WIDE)
    link = page.locator(".proof__link")
    text_color = link.locator(".proof__text").evaluate("el => getComputedStyle(el).color")
    body_fg = page.evaluate("getComputedStyle(document.body).color")
    assert text_color == body_fg == "rgb(242, 239, 232)"  # --fg on charcoal, not --fg2
    after_transform = link.evaluate("el => getComputedStyle(el, '::after').transform")
    assert after_transform in ("matrix(1, 0, 0, 1, 0, 0)", "none")


# --- Spark Order S3 / move 08: the "breath" block between #specimen and
# #disciplines is sized by content + padding, never 100vh — a viewport-height
# slab pushes the rest of the page out of frame on a short laptop. ---

@pytest.mark.parametrize("lang", ["en", "ru"])
def test_breath_block_is_not_viewport_height(open_site, lang):
    page, _ = open_site(lang=lang, viewport={"width": 375, "height": 780})
    page.wait_for_timeout(300)
    h = page.locator(".breath").evaluate("el => el.getBoundingClientRect().height")
    assert 120 < h < 780, f"{lang}: breath block is {h}px in a 780px viewport"


def test_breath_block_takes_no_section_number(open_site):
    """It is not a section: no .label, no 01–06 numeral, and the numbering
    test still counts exactly six."""
    page, _ = open_site()
    assert page.locator(".breath").count() == 1
    assert page.locator(".breath .label").count() == 0
    assert page.locator(".breath .num").count() == 0
    nums = page.locator(".sec .label .num").all_inner_texts()
    assert [n.strip() for n in nums] == ["01", "02", "03", "04", "05", "06"]


# --- Spark Order S5 / move 19: section 05's four "which of these is you?"
# rows are selectable — an invisible overlay <button> per row toggles a
# first-person clause onto the section 06 Telegram CTA. Single-choice,
# toggleable, marked with a hairline rule, gone entirely without JS. ---

_CTA = ".contact__cta"


def _decoded_text(page, href):
    return page.evaluate("h => decodeURIComponent((h.split('?text=')[1]) || '')", href)


def test_selecting_a_row_rewrites_the_cta_prefill(open_site):
    page, _ = open_site()
    default_href = page.locator(_CTA).get_attribute("href")
    row = page.locator(".rows > li").nth(1)
    row.locator(".row__pick").click()

    assert row.locator(".row__pick").get_attribute("aria-pressed") == "true"
    assert "is-picked" in (row.get_attribute("class") or "")
    href = page.locator(_CTA).get_attribute("href")
    assert href != default_href
    text = _decoded_text(page, href)
    clause = row.get_attribute("data-prefill-en")
    assert clause and clause in text
    assert text.startswith("Hi! I'd like to book the free intro call. — ")


def test_deselecting_restores_the_default_prefill(open_site):
    page, _ = open_site()
    default_href = page.locator(_CTA).get_attribute("href")
    pick = page.locator(".rows > li").first.locator(".row__pick")
    pick.click()
    assert page.locator(_CTA).get_attribute("href") != default_href
    pick.click()   # toggle the selected row off
    assert pick.get_attribute("aria-pressed") == "false"
    assert page.locator(_CTA).get_attribute("href") == default_href
    assert page.locator(".rows > li.is-picked").count() == 0


def test_picking_a_second_row_replaces_the_first(open_site):
    page, _ = open_site()
    rows = page.locator(".rows > li")
    rows.nth(0).locator(".row__pick").click()
    rows.nth(2).locator(".row__pick").click()
    assert rows.nth(0).locator(".row__pick").get_attribute("aria-pressed") == "false"
    assert rows.nth(2).locator(".row__pick").get_attribute("aria-pressed") == "true"
    assert page.locator(".rows > li.is-picked").count() == 1
    assert rows.nth(2).get_attribute("data-prefill-en") in _decoded_text(
        page, page.locator(_CTA).get_attribute("href")
    )


def test_rows_are_keyboard_operable(open_site):
    """Tab to a row button, press Enter — it toggles, natively, because it is
    a real <button> (the origin mark's hit-regions are the house precedent)."""
    page, _ = open_site()
    pick = page.locator(".rows > li").first.locator(".row__pick")
    pick.focus()
    assert page.evaluate(
        "document.activeElement === document.querySelector('.rows > li .row__pick')"
    )
    page.keyboard.press("Enter")
    assert pick.get_attribute("aria-pressed") == "true"
    page.keyboard.press("Enter")
    assert pick.get_attribute("aria-pressed") == "false"


def test_who_rows_are_plain_and_cta_static_without_js(open_site):
    page, _ = open_site(java_script_enabled=False)
    assert page.locator(".row__pick").count() == 0
    cta = page.locator(_CTA)
    assert cta.get_attribute("href") == cta.get_attribute("data-href-en")
