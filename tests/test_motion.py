"""The motion system, with animation allowed: the hero plays and lands, and the
reveal rhythm fires once per element as it enters view. The measured numbers do
not animate — Spark Order move 17 removed the count-up; test_numbers_do_not_animate
holds that line."""

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


def test_origin_mark_rests_on_english_before_any_interaction(open_site):
    """C6: rest state is English lit, not neutral — English is the offer,
    chess and climbing are proof it transfers, not equal-weight
    alternatives. Checked immediately at load, with no scroll or hover, so
    this can't pass by coincidence with the idle hint's own preview cycle
    (which also starts with English, but only once the mark scrolls into
    view — this is the state before that's even possible)."""
    page, _ = open_site()
    page.wait_for_timeout(100)
    assert page.locator('.glyph__part--left').evaluate("el => el.classList.contains('is-active')")
    assert page.locator('.glyph__part--right').evaluate("el => el.classList.contains('is-dim')")
    assert page.locator('.glyph__part--stem').evaluate("el => el.classList.contains('is-dim')")


def test_glyph_dim_state_is_a_solid_fill_not_partial_opacity(open_site):
    """C5: dimming used to be opacity: .32, which blends with whatever
    renders behind the shape — including the *other* glyph part it overlaps
    at the mark's shared vertex, muddying exactly the seam the keyline below
    keeps clean. Explicit solid fill tokens per theme instead: full opacity,
    a real colour that can't bleed into a neighbour."""
    page, _ = open_site(color_scheme="dark")
    page.locator("#origin").scroll_into_view_if_needed()
    page.locator('.origin__hit[data-discipline="climbing"]').hover()
    page.wait_for_timeout(700)
    left = page.locator(".glyph__part--left")
    assert left.evaluate("el => getComputedStyle(el).opacity") == "1"
    assert left.evaluate("el => getComputedStyle(el).fill") == "rgb(74, 59, 33)"  # --amber-dim


def test_stem_no_longer_gets_an_extra_scale_on_activation(open_site):
    """C5: the stem used to scale(1.1) on activation — an intensity of
    feedback the two arms structurally can't match (they're clipped halves
    of one shared path; scaling would tear the clip from the mark
    underneath). Dropped rather than added to the arms, so colour is the one
    channel all three hit regions carry identically."""
    page, _ = open_site()
    page.locator("#origin").scroll_into_view_if_needed()
    page.locator('.origin__hit[data-discipline="climbing"]').hover()
    page.wait_for_timeout(700)
    transform = page.locator(".glyph__part--stem").evaluate(
        "el => getComputedStyle(el).transform"
    )
    assert transform in ("none", "matrix(1, 0, 0, 1, 0, 0)")


def test_glyph_parts_carry_a_bg_coloured_keyline(open_site):
    """Alongside C5, not a separate finding: the amber V and the green stem
    meet at a shared vertex, and two overlapping fills read as one two-tone
    shape at exactly the seam the page's own copy calls three separate
    strokes. A thin --bg stroke, not a change to any path coordinate, keeps
    the seam clean."""
    page, _ = open_site(color_scheme="dark")
    stroke = page.locator(".glyph__part--stem").evaluate("el => getComputedStyle(el).stroke")
    assert stroke == "rgb(20, 24, 26)"  # --bg on charcoal


def test_numbers_do_not_animate(open_site):
    """Spark Order move 17: the facts row no longer runs its numbers up. Caught
    right after it scrolls into view and again ~600ms later — the window the old
    1.6s count-up lived in — every value is already final and unchanged.
    Replaces test_counters_count_up_to_exact_values and test_counter_starts_below_its_target."""
    page, _ = open_site()
    page.locator(".facts").scroll_into_view_if_needed()
    read = "() => [...document.querySelectorAll('.facts .n')].map(n => n.textContent.trim())"
    first = page.evaluate(read)
    page.wait_for_timeout(600)
    second = page.evaluate(read)
    assert first == ["8", "100+", "2100", "7c"]
    assert second == first


def _progress_scale_x(page):
    return page.evaluate(
        """() => {
            const el = document.querySelector('.progress__fill--specimen');
            const t = getComputedStyle(el).transform;
            if (!t || t === 'none') return 1;   // no matrix => identity => full width
            return parseFloat(t.slice(t.indexOf('(') + 1).split(',')[0]);
        }"""
    )


def _resolve_var(page, name):
    return page.evaluate(
        """name => {
            const d = document.createElement('span');
            d.style.color = `var(${name})`;
            document.body.appendChild(d);
            const c = getComputedStyle(d).color;
            d.remove();
            return c;
        }""",
        name,
    )


def test_progress_rule_tracks_scroll(open_site):
    """Spark Order S3 / move 20: a 1px rule on the masthead's bottom edge
    scales with scroll depth. Sampled at the top, middle and end of the
    document — strictly increasing, ~0 at the top and ~full width at the end."""
    page, _ = open_site()
    page.wait_for_timeout(300)

    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(250)
    top = _progress_scale_x(page)

    page.evaluate(
        "window.scrollTo(0, (document.documentElement.scrollHeight - innerHeight) * 0.5)"
    )
    page.wait_for_timeout(450)
    mid = _progress_scale_x(page)

    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(650)
    end = _progress_scale_x(page)

    assert top < 0.05, f"top scaleX {top}"
    assert top < mid < end, (top, mid, end)
    assert end > 0.95, f"end scaleX {end}"


@pytest.mark.parametrize("scheme", ["dark", "light"])
def test_progress_rule_switches_ink_at_origin(open_site, scheme):
    """S3 / move 20: above #origin the rule carries specimen ink; from #origin
    down, target ink. The switch is an opacity crossfade between two fills that
    each keep their own token — never an amber->green interpolation (a third
    colour by the back door). Verified in both pairs."""
    page, _ = open_site(color_scheme=scheme)
    page.wait_for_timeout(300)

    specimen = page.locator(".progress__fill--specimen")
    target = page.locator(".progress__fill--target")
    assert specimen.evaluate("el => getComputedStyle(el).backgroundColor") == _resolve_var(
        page, "--ink-specimen"
    )
    assert target.evaluate("el => getComputedStyle(el).backgroundColor") == _resolve_var(
        page, "--ink-target"
    )

    # at the top of the page the target ink has not crossfaded in yet
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(750)
    assert float(target.evaluate("el => getComputedStyle(el).opacity")) < 0.05
    assert "past-origin" not in (page.locator("html").get_attribute("class") or "")

    # scrolled to #origin: .past-origin is set and the target ink is now shown
    origin_y = page.evaluate(
        "document.getElementById('origin').getBoundingClientRect().top"
        " + (window.__lenis ? window.__lenis.scroll : window.scrollY)"
    )
    page.evaluate(f"window.scrollTo(0, {origin_y} + 8)")
    page.wait_for_timeout(900)
    assert "past-origin" in (page.locator("html").get_attribute("class") or "")
    assert float(target.evaluate("el => getComputedStyle(el).opacity")) > 0.95


def test_back_to_top_returns_from_the_footer_to_hero(open_site):
    """P15: the footer used to be a dead end after 7,500px of scroll — no
    way back up. Goes through the same in-page Lenis link wiring every
    other #-href on the page already uses, not a new mechanism."""
    page, _ = open_site()
    page.locator("#top").scroll_into_view_if_needed()  # no-op, just settles the page first
    page.locator(".foot__top").scroll_into_view_if_needed()
    page.wait_for_timeout(200)
    assert page.evaluate("window.scrollY") > 4000
    page.locator(".foot__top").click()
    page.wait_for_function("window.scrollY < 50", timeout=3000)
