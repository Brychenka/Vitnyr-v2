"""The collage: one file, routed like its own page. Deep-linkable, own header,
browser back works, focus moves to the heading, the page behind goes inert and
stops scrolling, theme/language persist, scroll resets on the way back."""

import pytest

# Photographs currently in the view. Real frames land in batches (commit 5970eae
# dropped the two chess stand-ins, 18 -> 15), so keep the count in one place and
# update this line when the shoot adds more.
COLLAGE_IMAGES = 15


def _is_open(page):
    return page.evaluate(
        "() => document.documentElement.classList.contains('collage-open')"
    )


def test_opener_routes_into_the_view(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    # Stage 2's door morph routes this open through a View Transition, so the
    # class flip and focus move land inside its deferred update callback
    # rather than synchronously with the click (main.js's withTransition()
    # has a 100ms failsafe as the outer bound).
    page.wait_for_function(
        "document.activeElement && document.activeElement.id === 'collage-title'",
        timeout=1000,
    )

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


def test_cold_deep_link_returns_to_the_top_on_close(open_site):
    """The cold-open counterpart to the warm-path test above — the case
    collage-plan.md's "Notes for the next chat" flagged as asserted nowhere:
    open #collage in a fresh tab, then close, and confirm the page behind is
    at the very top.

    Today this holds for a belt-and-braces reason: the <head> script sets
    .collage-open before first paint so #app never takes layout, the document
    can't scroll, and the browser's scroll-to-fragment toward #collage (the
    last element in the DOM) is a no-op. applyOpen(cold) also pins savedScroll
    to 0 and a post-load settle() re-asserts it. This test pins the outcome so
    that if either guard is later weakened (an open transition that renders
    #app, a change to the head-script gate), a close that lands mid-page fails
    here instead of shipping."""
    page, _ = open_site(hash="#collage")
    assert _is_open(page)
    # let the head script's paint, the browser's fragment jump, and applyOpen's
    # post-load settle() all run before we leave
    page.wait_for_timeout(300)

    page.locator(".view__back").click()
    page.wait_for_timeout(600)

    assert not _is_open(page)
    assert page.evaluate("location.hash") in ("", "#")
    after = page.evaluate("window.__lenis ? window.__lenis.scroll : window.scrollY")
    assert after < 40, f"cold-open close landed at {after}, expected the top"


def test_theme_and_language_persist_through_the_view(open_site):
    page, _ = open_site(theme="dark")
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


# --- C1: the language switch, not just the theme switch, reaches into the
# collage bar — previously the only Cream/Charcoal-and-EN/RU control open to
# a reader once the view covers the masthead was the theme switch. ---

def test_language_switch_inside_the_collage_bar_actually_works(open_site):
    page, _ = open_site(hash="#collage")
    bar_lang = page.locator("#collage .view__tools .langswitch")
    assert bar_lang.is_visible()
    assert bar_lang.text_content().strip() == "RU"

    bar_lang.click()
    html = page.locator("html")
    assert html.get_attribute("data-lang") == "ru"
    assert bar_lang.text_content().strip() == "EN"
    # the masthead's own copy (behind the view, but still in the DOM) is
    # kept in sync by the same querySelectorAll loop theme.js already ran
    # for .themeswitch
    assert page.locator(".masthead .langswitch").text_content().strip() == "EN"
    # the group heading itself re-rendered in Russian too
    assert "Сама работа" in page.locator("#collage-en").text_content()


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


# --- Stage 1: photographs get a wipe (clip-path on .collage__slot) instead
# of the body-copy rise (translateY). Same .9s/var(--e)/var(--d) rhythm, only
# the distance channel changes, and the ratio box must never move while it
# fires (the wipe clips the frame in place, it does not resize it). ---

def test_collage_tile_wipe_is_clipped_before_it_reveals(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)

    last_slot = page.locator("#collage .view__group").last.locator(".reveal").last.locator(".collage__slot")
    assert last_slot.evaluate("el => getComputedStyle(el).clipPath") == "inset(100% 0px 0px)"


def test_collage_tile_wipe_settles_to_full_frame_on_reveal(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)

    last_tile = page.locator("#collage .view__group").last.locator(".reveal").last
    last_slot = last_tile.locator(".collage__slot")
    last_tile.scroll_into_view_if_needed()
    page.wait_for_timeout(1500)

    assert "is-in" in (last_tile.get_attribute("class") or "")
    assert last_slot.evaluate("el => getComputedStyle(el).clipPath") == "inset(0px)"


def test_collage_tile_wipe_is_inert_under_reduced_motion(open_site):
    page, _ = open_site(reduced_motion=True)
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)
    assert page.evaluate(
        "() => [...document.querySelectorAll('#collage .collage__slot')]"
        ".every(s => getComputedStyle(s).clipPath === 'none')"
    )


def test_collage_tile_wipe_still_settled_on_reopen(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(300)
    page.locator("#collage .view__back").click()
    page.wait_for_timeout(400)
    page.locator("[data-collage-open]").click()
    # the .9s clip-path transition on the forced-settled tiles (applyClose()
    # adds .is-in to every tile, not just the ones the observer had already
    # fired) needs to actually finish before the shape reads as fully open
    page.wait_for_timeout(1200)
    assert page.evaluate(
        "() => [...document.querySelectorAll('#collage .collage__slot')]"
        ".every(s => getComputedStyle(s).clipPath === 'inset(0px)')"
    )


def test_collage_tile_ratio_box_is_unaffected_by_the_wipe(open_site):
    """The wipe animates clip-path only — the box the aspect-ratio class
    reserves must be pixel-identical hidden vs. revealed, or the wipe would
    be silently riding on a layout shift instead of clipping in place."""
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(400)

    last_tile = page.locator("#collage .view__group").last.locator(".reveal").last
    last_slot = last_tile.locator(".collage__slot")
    before = last_slot.bounding_box()

    last_tile.scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    after = last_slot.bounding_box()

    assert before["width"] == after["width"]
    assert before["height"] == after["height"]


# --- B4: the 18 figures are fetched only once the view actually opens ---
# The view sits opacity:0/visibility:hidden, not display:none, so the
# browser's native loading="lazy" (distance-from-viewport) fetched every one
# of them on ordinary page load — 1,231 KB no visit ever displayed. They now
# ship as data-src/data-srcset, inert to the browser's loader, and main.js
# promotes them to real attributes on first open.

def _fetched_collage_jpegs(page):
    return page.evaluate(
        "() => performance.getEntriesByType('resource')"
        ".filter(r => r.name.includes('/assets/collage/') && r.name.endsWith('.jpg')).length"
    )


def test_collage_images_are_not_fetched_before_the_view_opens(open_site):
    page, _ = open_site()
    page.wait_for_timeout(300)
    assert _fetched_collage_jpegs(page) == 0
    assert page.evaluate(
        "() => document.querySelectorAll('#collage img[data-src]').length"
    ) == COLLAGE_IMAGES


def test_collage_images_promote_and_fetch_on_first_open(open_site):
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(600)
    assert page.evaluate(
        "() => document.querySelectorAll('#collage img[data-src]').length"
    ) == 0
    assert _fetched_collage_jpegs(page) == COLLAGE_IMAGES


def test_collage_images_have_noscript_fallback_in_markup(open_site):
    page, _ = open_site()
    html = page.content()
    assert html.count('<noscript><img src="assets/collage/') == COLLAGE_IMAGES


# --- S7 move 04, extended at Stage 2: the route now takes a View Transition
# on both directions, and the door ("See the work") morphs into the view's
# own "Photographs" label on the way in. The old guarantee — a stray focus
# never gets stranded behind a deferred update callback — is restated rather
# than dropped: focus lands once the transition's update has actually run,
# and lands synchronously on every path that cannot run one at all. ---

def test_view_transition_focuses_once_the_update_has_run(open_site):
    """Opening through the door takes a View Transition when one is available
    (Chromium, motion allowed, tab visible), so focus is not guaranteed on the
    same tick as the click any more — but it is guaranteed within the update
    callback's own lifetime, with main.js's 100ms failsafe as the outer bound
    if that callback is ever lost rather than merely slow. Closing still
    returns focus to the opener button."""
    page, _ = open_site()
    page.locator("[data-collage-open]").click()
    page.wait_for_function(
        "document.activeElement && document.activeElement.id === 'collage-title'",
        timeout=1000,
    )
    assert _is_open(page)

    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    assert not _is_open(page)
    assert page.evaluate("() => document.activeElement.matches('[data-collage-open]')")


def test_view_transition_open_is_synchronous_with_no_api(open_site):
    """With startViewTransition absent, opening is the same direct call it has
    always been — focus lands with no wait at all."""
    page, _ = open_site()
    page.evaluate("() => { document.startViewTransition = undefined; }")
    page.locator("[data-collage-open]").click()
    assert page.evaluate("document.activeElement.id") == "collage-title"


def test_view_transition_open_is_synchronous_in_a_hidden_tab(open_site):
    """canTransition() checks document.visibilityState itself rather than
    trusting the API to handle backgrounding — a hidden tab is exactly where a
    deferred update callback might never run, so it takes the direct path."""
    page, _ = open_site()
    page.evaluate(
        "() => Object.defineProperty(document, 'visibilityState', "
        "{ value: 'hidden', configurable: true })"
    )
    page.locator("[data-collage-open]").click()
    assert page.evaluate("document.activeElement.id") == "collage-title"


def test_view_transition_failsafe_opens_if_the_update_callback_never_runs(open_site):
    """A startViewTransition that never invokes its callback and never settles
    updateCallbackDone (lost, not just slow) still can't strand the open —
    withTransition()'s failsafe calls the same idempotent mutation directly."""
    page, _ = open_site()
    page.evaluate("""() => {
        document.startViewTransition = function () {
            return {
                updateCallbackDone: new Promise(function () {}),
                ready: new Promise(function () {}),
                finished: new Promise(function () {})
            };
        };
    }""")
    page.locator("[data-collage-open]").click()
    page.wait_for_timeout(250)
    assert _is_open(page)
    assert page.evaluate("document.activeElement.id") == "collage-title"


def test_door_morph_clears_its_view_transition_name_after_opening(open_site):
    """The door and its destination only carry view-transition-name for the
    life of one transition. Left behind, either name would collide with
    whatever transition runs next on that element."""
    page, _ = open_site()
    opener = page.locator("[data-collage-open]")
    opener.click()
    page.wait_for_function(
        "document.activeElement && document.activeElement.id === 'collage-title'",
        timeout=1000,
    )
    # cleared inside the same synchronous mutate() that lands focus
    assert opener.evaluate("el => el.style.viewTransitionName") in ("", None)
    # cleared only once the transition's own `finished` promise settles,
    # which takes the full route duration (--t, .6s)
    page.wait_for_timeout(900)
    door_label = page.locator("#collage .view__body > .label").first
    assert door_label.evaluate("el => el.style.viewTransitionName") in ("", None)


def test_view_transition_falls_back_cleanly_under_reduced_motion(open_site):
    """Reduced motion skips startViewTransition entirely (an explicit gate, not
    a reliance on the API's own PRM handling). Open and close still route on
    location.hash and the class flip is instant."""
    page, _ = open_site(reduced_motion=True)
    page.evaluate("""() => { window.__vt = 0; const o = document.startViewTransition;
        if (o) document.startViewTransition = function (cb) { window.__vt++; return o.call(document, cb); }; }""")
    page.locator("[data-collage-open]").click()
    assert page.evaluate("location.hash") == "#collage"
    assert _is_open(page)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    assert not _is_open(page)
    assert page.evaluate("window.__vt") == 0, "startViewTransition should not run under reduced motion"
