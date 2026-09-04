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
    page.locator(".langswitch").click()
    # class is cleared while the fresh tween runs, then re-set on complete
    page.wait_for_function(
        "document.documentElement.classList.contains('hero-done')", timeout=6000
    )
    offsets = _line_offsets(page)
    assert offsets and all(abs(y) < 0.5 for y in offsets), offsets
    # the Russian lines are the visible ones now
    assert page.locator('.hero__title span[data-l="ru"]').is_visible()


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
