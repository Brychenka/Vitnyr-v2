"""Accessibility guarantees the build commits to: one h1, real landmarks,
a working skip link (focus move, not just scroll), accessible names on every
control, and a fully readable page under prefers-reduced-motion."""

import pytest


def test_single_h1_and_main_landmark(open_site):
    page, _ = open_site()
    assert page.locator("h1").count() == 1
    assert page.locator("main#main").count() == 1
    assert page.locator("header.masthead").count() == 1
    assert page.locator("footer").count() == 1


def test_skip_link_moves_focus_to_main(open_site):
    page, _ = open_site()
    page.locator(".skip").focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(400)
    focused_id = page.evaluate("document.activeElement.id")
    assert focused_id == "main", f"focus landed on #{focused_id!r}, not #main"


def test_every_link_and_button_has_an_accessible_name(open_site):
    page, _ = open_site()
    nameless = page.evaluate(
        """() => {
            const bad = [];
            document.querySelectorAll('a[href], button').forEach(el => {
                // textContent, not innerText: the collage controls sit in a
                // visibility:hidden container until the view opens, and
                // innerText would report them as empty.
                const svg = el.querySelector('svg[aria-label]');
                const name = (el.textContent || '').trim()
                    || (el.getAttribute('aria-label') || '').trim()
                    || (svg && svg.getAttribute('aria-label') || '').trim();
                if (!name) bad.push(el.outerHTML.slice(0, 90));
            });
            return bad;
        }"""
    )
    assert nameless == [], nameless


def test_decorative_svgs_are_hidden_from_a11y_tree(open_site):
    """Icon SVGs inside links/labels carry aria-hidden; the branded marks
    carry role=img + aria-label instead."""
    page, _ = open_site()
    problems = page.evaluate(
        """() => {
            const bad = [];
            document.querySelectorAll('svg').forEach(svg => {
                const labelled = svg.getAttribute('role') === 'img'
                    && svg.getAttribute('aria-label');
                const hidden = svg.getAttribute('aria-hidden') === 'true';
                if (!labelled && !hidden) bad.push(svg.outerHTML.slice(0, 70));
            });
            return bad;
        }"""
    )
    assert problems == [], problems


def test_specimen_rows_have_text_equivalent_for_correctness(open_site):
    """correct/incorrect is carried by a visually-hidden label, not colour +
    glyph alone."""
    page, _ = open_site()
    vh = page.locator(".line-spec .vh")
    assert vh.count() == 6
    texts = {t.strip() for t in vh.all_inner_texts()}
    assert texts == {"Incorrect:", "Correct:"}


def test_reduced_motion_shows_all_content_immediately(open_site):
    page, _ = open_site(reduced_motion=True)
    page.wait_for_timeout(300)

    state = page.evaluate(
        """() => {
            const rev = [...document.querySelectorAll('.reveal')];
            const hidden = rev.filter(el => parseFloat(getComputedStyle(el).opacity) < 0.99);
            const lines = [...document.querySelectorAll('.line__inner')]
                .filter(el => el.offsetParent !== null);
            const masked = lines.filter(el => {
                const t = getComputedStyle(el).transform;
                return t !== 'none' && !t.includes('matrix(1, 0, 0, 1, 0, 0)');
            });
            return {
                heroDone: document.documentElement.classList.contains('hero-done'),
                hiddenReveals: hidden.length,
                maskedLines: masked.length,
            };
        }"""
    )
    assert state == {"heroDone": True, "hiddenReveals": 0, "maskedLines": 0}, state


def test_origin_mark_shows_all_disciplines_statically_without_js(open_site):
    """No-JS floor: with the interaction mechanism unavailable, the three
    discipline/stat pairs must all be visible at once, not hover-gated."""
    page, _ = open_site(java_script_enabled=False)
    items = page.locator(".origin__panel-item")
    assert items.count() == 3
    for i in range(3):
        assert items.nth(i).evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95
    text = page.evaluate("() => document.querySelector('.origin__panel').innerText").lower()
    assert "english" in text and "chess" in text and "climbing" in text


def test_origin_mark_still_interactive_under_reduced_motion(open_site):
    """Reduced motion removes the animation, not the interaction: focusing a
    hit-region must still switch the active discipline."""
    page, _ = open_site(reduced_motion=True)
    btn = page.locator('.origin__hit[data-discipline="climbing"]')
    btn.focus()
    page.wait_for_timeout(100)
    assert btn.get_attribute("aria-pressed") == "true"
    item = page.locator('.origin__panel-item[data-discipline="climbing"]')
    assert item.evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95


def test_reduced_motion_counters_show_final_value_without_animating(open_site):
    page, _ = open_site(reduced_motion=True)
    page.wait_for_timeout(200)
    values = page.locator(".facts .n").all_inner_texts()
    assert [v.strip() for v in values] == ["8", "100+", "2100", "7c"]


def test_focus_visible_ring_is_the_target_green(open_site):
    page, _ = open_site()
    page.locator(".scrollcue").focus()
    outline = page.locator(".scrollcue").evaluate(
        "el => getComputedStyle(el).outlineColor"
    )
    # --ink-target on charcoal = #4C7A52
    assert outline == "rgb(76, 122, 82)"
