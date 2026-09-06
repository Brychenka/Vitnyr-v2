"""The motion system, with animation allowed: the hero plays and lands, the
reveal rhythm fires once per element as it enters view, and the measured
numbers count up to exactly their stated value."""

import pytest

pytestmark = pytest.mark.slow


def _line_offsets(page):
    return page.evaluate(
        """() => [...document.querySelectorAll('.line__inner')]
            .filter(el => el.offsetParent !== null)
            .map(el => {
                const m = getComputedStyle(el).transform;
                if (!m || m === 'none') return 0;
                const p = m.match(/matrix\\(([^)]+)\\)/);
                return p ? parseFloat(p[1].split(',')[5]) : 0;
            })"""
    )


def test_hero_plays_and_settles_to_zero(open_site):
    page, _ = open_site()
    page.wait_for_function(
        "document.documentElement.classList.contains('hero-done')", timeout=6000
    )
    offsets = _line_offsets(page)
    assert offsets and all(abs(y) < 0.5 for y in offsets), offsets


def test_hero_replays_and_settles_after_language_switch(open_site):
    page, _ = open_site()
    page.wait_for_function(
        "document.documentElement.classList.contains('hero-done')", timeout=6000
    )
    page.locator(".masthead .langswitch").click()
    # class is cleared while the fresh tween runs, then re-set on complete
    page.wait_for_function(
        "document.documentElement.classList.contains('hero-done')", timeout=6000
    )
    offsets = _line_offsets(page)
    assert offsets and all(abs(y) < 0.5 for y in offsets), offsets
    # the Russian lines are the visible ones now
    assert page.locator('.hero__title span[data-l="ru"]').is_visible()


@pytest.mark.parametrize("height", [800, 900, 1080])
def test_hero_foot_is_visible_at_rest_without_scrolling(open_site, height):
    """.hero is min-height:100svh, so .hero__foot (.stand + .scrollcue) sits
    near the very bottom of the viewport at load — inside the -20% band the
    page observer holds back for content the reader hasn't scrolled to yet.
    .scrollcue's only job is to invite that scroll, so it above all must not
    require scrolling to appear. Regression for buildReveals() giving the
    hero its own rootMargin:0px observer instead of sharing the -20% one."""
    page, _ = open_site(viewport={"width": 1280, "height": height})
    page.wait_for_timeout(400)
    for selector in (".scrollcue", ".stand:visible"):
        el = page.locator(selector)
        opacity = el.evaluate("el => parseFloat(getComputedStyle(el).opacity)")
        assert opacity > 0.95, f"{selector} at {height}px: opacity {opacity}"
        assert "is-in" in (el.get_attribute("class") or "")


def test_reveals_start_hidden_then_show_on_scroll(open_site):
    page, _ = open_site()
    # a reveal well below the fold is still hidden right after load
    contact_label = page.locator("#contact .label.reveal")
    assert contact_label.evaluate("el => parseFloat(getComputedStyle(el).opacity)") < 0.1

    contact_label.scroll_into_view_if_needed()
    page.wait_for_timeout(1400)
    assert contact_label.evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95
    assert "is-in" in contact_label.get_attribute("class")


def test_every_reveal_eventually_resolves_visible(open_site):
    page, _ = open_site()
    page.evaluate(
        """async () => {
            for (let y = 0; y <= document.body.scrollHeight; y += 400) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 120));
            }
            window.scrollTo(0, 0);
        }"""
    )
    page.wait_for_timeout(1600)
    stuck = page.evaluate(
        """() => [...document.querySelectorAll('.reveal')]
            .filter(el => el.offsetParent !== null
                && parseFloat(getComputedStyle(el).opacity) < 0.9).length"""
    )
    assert stuck == 0


def test_origin_mark_keyboard_focus_reveals_its_panel(open_site):
    """Tab to the chess hit-region: no mouse involved, so this is the
    keyboard-only path through the interactive mark."""
    page, _ = open_site()
    btn = page.locator('.origin__hit[data-discipline="chess"]')
    btn.focus()
    page.wait_for_timeout(700)
    assert btn.get_attribute("aria-pressed") == "true"
    item = page.locator('.origin__panel-item[data-discipline="chess"]')
    assert item.evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95
    assert item.get_attribute("aria-hidden") == "false"
    other = page.locator('.origin__panel-item[data-discipline="english"]')
    assert other.evaluate("el => parseFloat(getComputedStyle(el).opacity)") < 0.05
    assert other.get_attribute("aria-hidden") == "true"


def test_origin_mark_hover_switches_between_disciplines(open_site):
    page, _ = open_site()
    english = page.locator('.origin__hit[data-discipline="english"]')
    english.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    english.hover()
    page.wait_for_timeout(700)
    assert page.locator('.glyph__part--left').evaluate("el => el.classList.contains('is-active')")

    page.locator('.origin__hit[data-discipline="climbing"]').hover()
    page.wait_for_timeout(700)
    stem = page.locator('.glyph__part--stem')
    assert stem.evaluate("el => el.classList.contains('is-active')")
    assert not stem.evaluate("el => el.classList.contains('is-dim')")
    left = page.locator('.glyph__part--left')
    assert left.evaluate("el => el.classList.contains('is-dim')")


def test_counters_count_up_to_exact_values(open_site):
    page, _ = open_site()
    page.locator(".facts").scroll_into_view_if_needed()
    page.wait_for_function(
        """() => {
            const t = [...document.querySelectorAll('.facts .n')].map(n => n.textContent.trim());
            return t.join('|') === '8|100+|2100|7c';
        }""",
        timeout=6000,
    )


def test_counter_starts_below_its_target(open_site):
    """The count actually animates: caught partway, the value is less than
    the final one."""
    page, _ = open_site()
    page.locator(".facts").scroll_into_view_if_needed()
    # sample quickly, before 1.6s of counting completes
    page.wait_for_timeout(120)
    mid = page.evaluate(
        "() => parseInt(document.querySelector('.facts .n[data-count=\"2100\"]').textContent, 10)"
    )
    assert 0 <= mid < 2100
