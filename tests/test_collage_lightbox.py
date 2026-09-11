"""Stage 3: the collage tiles become real controls. Clicking (or Enter/Space
on) a tile opens a click-to-enlarge lightbox — a layer on top of #collage,
not a nested route (Escape closes just the lightbox; browser Back still
closes the whole view). Reverses Stage 5's "add nothing to the tiles"
ruling now that the affordance is earned; see BUILD-NOTES' "Collage Stage 3"
entry for why."""

from conftest import horizontal_overflow
from test_collage import COLLAGE_IMAGES


def _open_collage(page):
    page.locator("[data-collage-open]").click()
    page.wait_for_function(
        "document.activeElement && document.activeElement.id === 'collage-title'",
        timeout=3000,
    )
    # The door morph's View Transition (Stage 2) keeps its own top-layer
    # overlay live for the full var(--t) = .6s even after focus has already
    # landed inside the deferred callback — a click during that window can
    # hit the transition's overlay instead of the page underneath. Clearing
    # it here, once, keeps every test below from having to know that.
    page.wait_for_timeout(700)


def _is_lightbox_open(page):
    return page.evaluate(
        "() => !document.querySelector('.lightbox').hidden"
    )


def test_no_js_document_has_no_lightbox_controls(open_site):
    page, _ = open_site(java_script_enabled=False)
    assert page.locator(".collage__trigger").count() == 0
    assert page.locator(".lightbox").count() == 0


def test_tiles_are_real_buttons_matching_the_real_figure_count(open_site):
    page, _ = open_site()
    _open_collage(page)
    assert page.locator(".collage__trigger").count() == COLLAGE_IMAGES


def test_lightbox_opens_on_click(open_site):
    page, _ = open_site()
    _open_collage(page)

    page.locator(".collage__trigger").first.click()
    assert _is_lightbox_open(page)
    assert page.evaluate("document.activeElement.classList.contains('lightbox')")


def test_lightbox_opens_on_keyboard_activation(open_site):
    page, _ = open_site()
    _open_collage(page)

    page.locator(".collage__trigger").first.focus()
    page.keyboard.press("Enter")
    assert _is_lightbox_open(page)


def test_lightbox_matches_the_tile_that_opened_it(open_site):
    page, _ = open_site()
    _open_collage(page)

    third = page.locator(".collage__trigger").nth(2)
    caption_id = third.get_attribute("aria-labelledby")
    expected = page.locator("#" + caption_id).inner_text()
    third.click()

    assert page.locator(".lightbox__caption").inner_text() == expected
    assert page.locator(".lightbox__count").inner_text() == "3 / " + str(COLLAGE_IMAGES)


def test_content_behind_the_lightbox_goes_inert(open_site):
    page, _ = open_site()
    _open_collage(page)

    page.locator(".collage__trigger").first.click()
    assert page.evaluate("document.querySelector('.view__bar').inert") is True
    assert page.evaluate("document.querySelector('.view__body').inert") is True


def test_escape_closes_only_the_lightbox_and_restores_focus_to_its_tile(open_site):
    page, _ = open_site()
    _open_collage(page)

    first = page.locator(".collage__trigger").first
    first.click()
    assert _is_lightbox_open(page)

    page.keyboard.press("Escape")
    assert not _is_lightbox_open(page)
    # the view itself must still be open — Escape closed one layer, not both
    assert page.evaluate(
        "() => document.documentElement.classList.contains('collage-open')"
    )
    assert page.evaluate(
        "() => document.activeElement.classList.contains('collage__trigger')"
    )


def test_arrows_move_and_wrap(open_site):
    page, _ = open_site()
    _open_collage(page)

    page.locator(".collage__trigger").first.click()
    assert page.locator(".lightbox__count").inner_text() == "1 / " + str(COLLAGE_IMAGES)

    page.locator(".lightbox__prev").click()
    assert page.locator(".lightbox__count").inner_text() == str(COLLAGE_IMAGES) + " / " + str(COLLAGE_IMAGES)

    page.locator(".lightbox__next").click()
    assert page.locator(".lightbox__count").inner_text() == "1 / " + str(COLLAGE_IMAGES)

    page.keyboard.press("ArrowRight")
    assert page.locator(".lightbox__count").inner_text() == "2 / " + str(COLLAGE_IMAGES)
    page.keyboard.press("ArrowLeft")
    assert page.locator(".lightbox__count").inner_text() == "1 / " + str(COLLAGE_IMAGES)


def test_paired_row_figures_are_in_the_sequence(open_site):
    """The climbing group's last row (.collage__pair, two .collage__pair__fig)
    has to be reachable by the same prev/next sequence as every other tile —
    the flat `.collage figure` query the lightbox is built from already
    includes them (see main.js's comment on that selector)."""
    page, _ = open_site()
    _open_collage(page)

    assert page.locator(".collage__pair__fig .collage__trigger").count() == 2


def test_grayscale_still_applied_inside_the_lightbox(open_site):
    page, _ = open_site()
    _open_collage(page)
    page.locator(".collage__trigger").first.click()

    filt = page.evaluate(
        "() => getComputedStyle(document.querySelector('.lightbox__img')).filter"
    )
    assert filt and filt != "none"


def test_lightbox_opens_immediately_under_reduced_motion(open_site):
    """Opening the lightbox is a `hidden` toggle, not a tween — nothing about
    it is gated behind `!reduce` anywhere, so it has to open exactly as
    readily under reduced motion as it does normally.

    Doesn't use _open_collage()'s title-focus wait: under reduced motion,
    focus landing on #collage-title has a pre-existing timing quirk that
    predates this stage (test_collage.py's own
    test_view_transition_falls_back_cleanly_under_reduced_motion doesn't
    assert it either, for the same reason — see that test and BUILD-NOTES'
    Stage 2 entry) and is out of scope here. .collage-open is the reliable
    signal instead — it's the plain synchronous class flip, not the focus
    move that quirk affects."""
    page, _ = open_site(reduced_motion=True)
    page.locator("[data-collage-open]").click()
    page.wait_for_function(
        "document.documentElement.classList.contains('collage-open')",
        timeout=3000,
    )

    page.locator(".collage__trigger").first.click()
    assert _is_lightbox_open(page)


def test_caption_reflects_the_language_active_when_it_opens(open_site):
    """Switching language happens through the view's own bar copy, which
    (unlike the masthead's) is still reachable with the view open and the
    lightbox not yet up — .view__bar only goes inert once the lightbox
    itself opens. Confirms render()'s language check picks the current
    pair rather than a stale default."""
    page, _ = open_site()
    _open_collage(page)

    expected_ru = page.evaluate(
        "() => document.querySelectorAll('.collage figure')[0]"
        ".querySelector('figcaption').getAttribute('data-ru')"
    )
    page.locator("#collage .view__tools .langswitch").click()
    page.wait_for_timeout(150)

    page.locator(".collage__trigger").first.click()
    assert page.locator(".lightbox__caption").inner_text() == expected_ru


def test_language_switch_is_unreachable_while_the_lightbox_traps_focus(open_site):
    """The full inert trap: .masthead is already inert once #collage is open
    (the view's own doing), and .view__bar joins it once the lightbox is —
    so neither language switch is reachable while a photo is enlarged."""
    page, _ = open_site()
    _open_collage(page)
    page.locator(".collage__trigger").first.click()

    assert page.evaluate(
        "() => document.querySelector('#collage .view__tools .langswitch').closest('[inert]') !== null"
    )


def test_no_console_errors_opening_the_lightbox(open_site, console_guard):
    page, _ = open_site()
    console_guard.watch(page)
    _open_collage(page)
    page.locator(".collage__trigger").first.click()
    page.locator(".lightbox__next").click()
    page.keyboard.press("Escape")
    console_guard.assert_clean()


def test_no_horizontal_overflow_at_375(open_site):
    page, _ = open_site(viewport={"width": 375, "height": 780})
    _open_collage(page)
    page.locator(".collage__trigger").first.click()
    assert not horizontal_overflow(page)


def test_prev_button_is_not_covered_by_the_photo_at_375(open_site):
    """Regression: .lightbox__media is a grid item (grid-row: 1), and grid
    items paint like inline-blocks — the same visual layer as the
    absolutely-positioned prev/next buttons, ordered by DOM position rather
    than by who's "positioned". The buttons' own DOM order is close, prev,
    media, next — so without an explicit z-index on the buttons, .lightbox__
    prev silently painted *under* any photo wide enough to reach the left
    edge (routine at phone widths, since the native-resolution cap barely
    shrinks these small sources), while .lightbox__next stayed on top by
    accident of coming after media in the markup. Caught by manual QA, not
    by the desktop-viewport suite, because Playwright's default WIDE
    viewport never lets these small images reach the edge buttons."""
    page, _ = open_site(viewport={"width": 375, "height": 780})
    _open_collage(page)
    page.locator(".collage__trigger").first.click()

    hit = page.evaluate(
        "() => {"
        "  var b = document.querySelector('.lightbox__prev');"
        "  var r = b.getBoundingClientRect();"
        "  var el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);"
        "  return b.contains(el);"
        "}"
    )
    assert hit


# --- Stage 4 (2026-09-11): the tiles are real controls now (Stage 3), so the
# hover/focus affordances Stage 5 originally rejected are earned rather than
# a lie. Scope is deliberately narrow: a restrained scale on the <img> itself
# (never the grid item — .collage__slot's overflow:hidden, set in Stage 1,
# contains it) plus the page's existing :focus-visible ring, which the tiles
# pick up for free now that they're <button>s with no local override. Still
# no grayscale-to-colour reveal at any size — the colour system governs. ---

def test_tile_image_scales_on_hover(open_site):
    page, _ = open_site()
    _open_collage(page)

    img = page.locator(".collage__trigger").first.locator("img")
    assert img.evaluate("el => getComputedStyle(el).transform") == "none"

    page.locator(".collage__trigger").first.hover()
    scaled = img.evaluate("el => getComputedStyle(el).transform")
    assert scaled != "none"


def test_tile_image_scales_on_keyboard_focus_too(open_site):
    """Paired with :hover (this page's existing convention — e.g.
    .proof__link) so keyboard use gets the same cue, not just the ring.

    Deep-links straight into #collage rather than going through
    _open_collage()'s click on the opener: Chromium's :focus-visible
    modality is page-wide, so a real mouse click earlier in the test would
    make the later programmatic .focus() resolve as not-visible, same as it
    would for a real user who just clicked with a mouse."""
    page, _ = open_site(hash="#collage")
    page.wait_for_selector(".collage__trigger")

    trigger = page.locator(".collage__trigger").first
    trigger.focus()
    scaled = trigger.locator("img").evaluate(
        "el => getComputedStyle(el).transform"
    )
    assert scaled != "none"


def test_tile_hover_scale_is_dropped_under_reduced_motion(open_site):
    """Matches the magnetic pull's precedent (style.css's reduced-motion
    block): a hover-triggered transform is dropped outright, not just made
    instant.

    Uses .collage-open rather than _open_collage()'s title-focus wait — see
    test_lightbox_opens_immediately_under_reduced_motion's docstring above
    for why that wait is unreliable under reduced motion."""
    page, _ = open_site(reduced_motion=True)
    page.locator("[data-collage-open]").click()
    page.wait_for_function(
        "document.documentElement.classList.contains('collage-open')",
        timeout=3000,
    )

    trigger = page.locator(".collage__trigger").first
    trigger.hover()
    assert trigger.locator("img").evaluate(
        "el => getComputedStyle(el).transform"
    ) == "none"


def test_tile_shows_the_page_wide_focus_ring(open_site):
    # theme="dark": expected colour below is --ink-target on charcoal.
    # Deep-links into #collage for the same modality reason as the test
    # above — no mouse click before the programmatic .focus().
    page, _ = open_site(theme="dark", hash="#collage")
    page.wait_for_selector(".collage__trigger")

    trigger = page.locator(".collage__trigger").first
    trigger.focus()
    style = trigger.evaluate(
        "el => ({ style: getComputedStyle(el).outlineStyle, color: getComputedStyle(el).outlineColor })"
    )
    assert style["style"] == "solid"
    assert style["color"] == "rgb(76, 122, 82)"  # --ink-target on charcoal


def test_tile_still_grayscale_on_hover(open_site):
    """Stage 5's grayscale-to-colour rejection still stands at every size —
    hovering must not touch --collage-filter."""
    page, _ = open_site()
    _open_collage(page)

    img = page.locator(".collage__trigger").first.locator("img")
    before = img.evaluate("el => getComputedStyle(el).filter")
    page.locator(".collage__trigger").first.hover()
    after = img.evaluate("el => getComputedStyle(el).filter")
    assert before == after and before != "none"
