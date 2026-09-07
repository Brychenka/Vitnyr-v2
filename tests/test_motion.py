"""The motion system, with animation allowed: the hero plays and lands, and the
reveal rhythm fires once per element as it enters view. The measured numbers
count up to their value again (Spark Order move 17 removed the count-up; it was
restored as "separate instruments") — test_numbers_count_up_to_their_values and
test_numbers_finish_at_different_times hold that line."""

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


def test_numbers_count_up_to_their_values(open_site):
    """Spark Order: the facts row runs its numbers up again. Once settled, every
    value is exactly its confirmed figure — 8, 100+, 2100 — and 7c (not a
    number, no data-count) is untouched throughout."""
    page, _ = open_site()
    page.locator(".facts").scroll_into_view_if_needed()
    page.wait_for_function(
        """() => [...document.querySelectorAll('.facts .n')]
            .map(n => n.textContent.trim()).join('|') === '8|100+|2100|7c'""",
        timeout=6000,
    )
    seventh = page.evaluate(
        "() => document.querySelector('.fact--grade .n').textContent.trim()"
    )
    assert seventh == "7c"


def test_numbers_finish_at_different_times(open_site):
    """The count-up came back deliberately NOT as one synced gauge (Spark Order,
    "separate instruments"): each number has its own duration plus a stagger, so
    8, 100+ and 2100 do not all land on the same frame. Would fail against the
    old shared-1.6s countUp, where all three finished within a frame or two.
    Replaces test_numbers_do_not_animate / the pre-move-17 counter pair."""
    page, _ = open_site()
    page.locator(".facts").scroll_into_view_if_needed()
    finished_at = page.evaluate(
        """async () => {
            const want = { '8': '8', '100': '100+', '2100': '2100' };
            const num = { '8': 8, '100': 100, '2100': 2100 };
            const els = [...document.querySelectorAll('.facts .n[data-count]')];
            const t0 = performance.now();
            const low = {}, done = {};
            await new Promise(resolve => {
                const tick = () => {
                    els.forEach(el => {
                        const k = el.dataset.count;
                        const v = parseInt(el.textContent, 10);
                        // only trust a "finished" reading once the number has
                        // actually been seen counting (below its target) — the
                        // literal markup value matches want[k] before the tween's
                        // first frame and would otherwise register instantly.
                        if (Number.isFinite(v) && v < num[k]) low[k] = true;
                        if (low[k] && !(k in done) && el.textContent.trim() === want[k]) {
                            done[k] = performance.now() - t0;
                        }
                    });
                    if (Object.keys(done).length === els.length) return resolve();
                    if (performance.now() - t0 > 9000) return resolve();
                    requestAnimationFrame(tick);
                };
                requestAnimationFrame(tick);
            });
            return done;
        }"""
    )
    assert set(finished_at.keys()) == {"8", "100", "2100"}
    times = sorted(finished_at.values())
    # three separate instruments: the last number lands well after the first,
    # not in lockstep. Spread is ~0.8s by construction; 250ms clears jitter.
    assert times[-1] - times[0] > 250


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


# --- Spark Order S4 / move 02: the custom dot borrows the page's two
# accents — specimen amber over a control inside #specimen, target green
# over the contact CTA. Colour lives in the stylesheet off --ink-*; main.js
# only toggles .is-specimen / .is-target on .cursor. ---

def test_cursor_takes_target_ink_over_the_contact_cta(open_site):
    page, _ = open_site()
    cursor = page.locator(".cursor")
    dot = page.locator(".cursor__dot")

    page.locator(".contact__cta").hover()
    page.wait_for_timeout(200)
    assert "is-target" in (cursor.get_attribute("class") or "")
    # .cursor__dot transitions its background over --t, so let it settle
    page.wait_for_timeout(700)
    assert dot.evaluate("el => getComputedStyle(el).backgroundColor") == _resolve_var(
        page, "--ink-target"
    )

    # leaving the target clears the accent again
    page.mouse.move(5, 5)
    page.wait_for_timeout(200)
    cls = cursor.get_attribute("class") or ""
    assert "is-target" not in cls and "is-specimen" not in cls


def test_cursor_takes_specimen_ink_over_a_control_inside_specimen(open_site):
    """#specimen has no interactive control yet (S6 adds them), so the branch
    is exercised against an injected hot target — the delegated handler keys
    off `closest('#specimen')`, which is what matters here."""
    page, _ = open_site()
    page.evaluate(
        """() => {
            const b = document.createElement('button');
            b.id = 'spec-probe';
            b.setAttribute('data-magnetic', '');
            b.textContent = 'probe';
            b.style.cssText = 'display:block;width:120px;height:44px;margin:20px 0';
            document.querySelector('#specimen .specs').prepend(b);
        }"""
    )
    probe = page.locator("#spec-probe")
    probe.scroll_into_view_if_needed()
    probe.hover()
    page.wait_for_timeout(200)

    cursor = page.locator(".cursor")
    assert "is-specimen" in (cursor.get_attribute("class") or "")
    page.wait_for_timeout(700)   # let .cursor__dot's background transition finish
    assert page.locator(".cursor__dot").evaluate(
        "el => getComputedStyle(el).backgroundColor"
    ) == _resolve_var(page, "--ink-specimen")


@pytest.mark.parametrize(
    "scheme,active_token",
    [("dark", "--ink-target"), ("light", "--ink-specimen")],
)
def test_cursor_active_ink_follows_the_theme(open_site, scheme, active_token):
    """C15 (2026-09-07): the dot's active fill is --cursor-active-ink — target
    green on charcoal, specimen amber on cream (Igor's call: green read muddy on
    the warm ground). The generic active state and .is-target both read from it,
    so the contact CTA follows the theme too; .is-specimen stays amber in both."""
    page, _ = open_site(color_scheme=scheme)
    dot = page.locator(".cursor__dot")

    # generic control: the hero scrollcue link
    page.locator(".scrollcue").hover()
    page.wait_for_timeout(200)
    assert "cursor-active" in (page.locator("html").get_attribute("class") or "")
    page.wait_for_timeout(700)
    generic = dot.evaluate("el => getComputedStyle(el).backgroundColor")
    assert generic == _resolve_var(page, "--cursor-active-ink")
    assert generic == _resolve_var(page, active_token)

    # the contact CTA (.is-target) resolves to the same theme-dependent ink
    page.locator(".contact__cta").hover()
    page.wait_for_timeout(200)
    assert "is-target" in (page.locator(".cursor").get_attribute("class") or "")
    page.wait_for_timeout(700)
    assert dot.evaluate("el => getComputedStyle(el).backgroundColor") == _resolve_var(
        page, "--cursor-active-ink"
    )

    if scheme == "light":
        assert generic != _resolve_var(page, "--ink-target"), (
            "on cream the active dot must be amber, not green"
        )


def test_cursor_absent_on_touch_devices(open_site):
    """initCursor() returns early without a fine pointer, so the dot is never
    shown and the native pointer is never hidden."""
    page, _ = open_site(has_touch=True)
    assert page.evaluate("matchMedia('(pointer: coarse)').matches")
    page.mouse.move(200, 300)
    page.mouse.move(400, 400)
    page.wait_for_timeout(200)
    assert not page.evaluate(
        "document.documentElement.classList.contains('has-cursor')"
    )
    assert page.locator(".cursor").evaluate("el => getComputedStyle(el).display") == "none"


def _translate_xy(page, selector):
    """(tx, ty) from the element's computed transform matrix; (0, 0) for none."""
    return page.locator(selector).evaluate(
        """el => {
            const t = getComputedStyle(el).transform;
            if (!t || t === 'none') return [0, 0];
            const m = t.match(/matrix\\(([^)]+)\\)/);
            if (!m) return [0, 0];
            const p = m[1].split(',').map(Number);
            return [p[4], p[5]];
        }"""
    )


def test_magnetic_pull_moves_a_control_but_not_a_text_link(open_site):
    """C16 (2026-09-07): initMagnetic is back, scoped to .tool / .view__back.
    A hovered control eases toward the pointer and returns to rest on leave;
    a text link that also carries data-magnetic gets the dot's colour cue but
    never moves."""
    page, _ = open_site()
    page.mouse.move(400, 300)

    sw = page.locator(".tools__group--util .langswitch")
    box = sw.bounding_box()
    sw.hover()                      # enter → the field captures the box at centre
    page.wait_for_timeout(150)
    # a point near the right edge, vertically centred: a clear +x pull, ~0 y
    page.mouse.move(box["x"] + box["width"] - 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(500)      # quickTo runs over D.state (0.6s)
    tx, ty = _translate_xy(page, ".tools__group--util .langswitch")
    assert tx > 1.5, f"the switch should be pulled toward the pointer (tx={tx})"
    assert abs(ty) < 3, f"a mid-height hover pulls almost pure-x (ty={ty})"

    # leaving retargets the same tween back to rest
    page.mouse.move(400, 300)
    page.wait_for_timeout(700)
    tx, ty = _translate_xy(page, ".tools__group--util .langswitch")
    assert abs(tx) < 0.5 and abs(ty) < 0.5, "the switch must settle back to rest"

    # a text link with data-magnetic (the hero scrollcue) never moves
    cue = page.locator(".scrollcue")
    cbox = cue.bounding_box()
    cue.hover()
    page.wait_for_timeout(150)
    page.mouse.move(cbox["x"] + cbox["width"] - 2, cbox["y"] + cbox["height"] / 2)
    page.wait_for_timeout(500)
    assert "cursor-active" in (page.locator("html").get_attribute("class") or "")  # colour cue on
    tx, ty = _translate_xy(page, ".scrollcue")
    assert tx == 0 and ty == 0, f"a text link must not be pulled (tx={tx}, ty={ty})"


def test_magnetic_pull_reaches_the_origin_mark(open_site):
    """C17 (2026-09-07): the §04 origin mark (interactive V glyph) joins the
    pull. It is also a .reveal target, so initMagnetic drops `transform` from
    its transition on the first enter and GSAP owns the channel: the mark eases
    toward the pointer and back to rest, and the lighting still works."""
    page, _ = open_site()
    mark = page.locator(".origin__mark")
    mark.scroll_into_view_if_needed()
    page.wait_for_timeout(1200)          # let the reveal rise + glyph draw settle
    # revealed and settled: transform is back to none before any hover
    tx, ty = _translate_xy(page, ".origin__mark")
    assert abs(tx) < 0.5 and abs(ty) < 0.5

    box = mark.bounding_box()
    mark.hover()
    page.wait_for_timeout(150)
    page.mouse.move(box["x"] + box["width"] - 3, box["y"] + box["height"] / 2)
    page.wait_for_timeout(500)
    tx, ty = _translate_xy(page, ".origin__mark")
    assert tx > 1.5, f"the origin mark should be pulled toward the pointer (tx={tx})"
    # the transform channel was handed over — no `transform` left in the transition
    assert page.locator(".origin__mark").evaluate(
        "el => el.style.transitionProperty"
    ) == "opacity"
    # lighting still responds: hovering the chess stroke lights its panel line
    page.locator(".origin__hit--right").hover()
    page.wait_for_timeout(200)
    assert page.locator('.origin__panel-item[data-discipline="chess"]').evaluate(
        "el => el.classList.contains('is-active')"
    )

    page.mouse.move(400, 300)
    page.wait_for_timeout(700)
    tx, ty = _translate_xy(page, ".origin__mark")
    assert abs(tx) < 0.5 and abs(ty) < 0.5, "the mark must settle back to rest"


def test_magnetic_pull_absent_under_reduced_motion(open_site):
    """initMagnetic sits past the reduced-motion return, and the sheet pins the
    controls flat as well — a reduce reader gets no nudge."""
    page, _ = open_site(reduced_motion=True)
    sw = page.locator(".tools__group--util .langswitch")
    box = sw.bounding_box()
    sw.hover()
    page.wait_for_timeout(150)
    page.mouse.move(box["x"] + box["width"] - 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(400)
    tx, ty = _translate_xy(page, ".tools__group--util .langswitch")
    assert tx == 0 and ty == 0


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


def _rotation_deg(page, selector):
    """Signed degrees from the element's computed transform matrix; 0 for none.
    A completed 360deg turn reads as 0 here — identical to rest, which is the
    point (360 lands the mark back on its own geometry)."""
    return page.locator(selector).evaluate(
        """el => {
            const t = getComputedStyle(el).transform;
            if (!t || t === 'none') return 0;
            const m = t.match(/matrix\\(([^)]+)\\)/);
            if (!m) return 0;
            const p = m[1].split(',').map(Number);
            return Math.atan2(p[1], p[0]) * 180 / Math.PI;
        }"""
    )


def test_footer_mark_turns_once_on_hover_and_snaps_back_on_leave(open_site):
    """F1 (2026-09-07): hovering the footer wordmark spins it one full clockwise
    turn (transition on :hover only, so leave snaps 360->0 with no reverse). The
    turn runs on --t-turn (1.2s) and the one brand ease."""
    page, _ = open_site()
    mark = page.locator(".foot .footmark")
    mark.scroll_into_view_if_needed()
    page.mouse.move(400, 300)
    page.wait_for_timeout(150)

    # at rest: no rotation, and no transition armed on the base rule
    assert abs(_rotation_deg(page, ".foot .footmark")) < 0.5
    assert mark.evaluate("el => getComputedStyle(el).transitionDuration") == "0s"

    mark.hover()
    page.wait_for_timeout(250)
    # mid-turn: the transition is armed on transform for 1.2s and the mark has
    # visibly rotated off its rest angle
    assert mark.evaluate("el => getComputedStyle(el).transitionDuration") == "1.2s"
    assert "transform" in mark.evaluate("el => getComputedStyle(el).transitionProperty")
    assert abs(_rotation_deg(page, ".foot .footmark")) > 5, "the mark should be mid-turn"

    # after the turn: back on its own geometry (360deg == rest)
    page.wait_for_timeout(1300)
    assert abs(_rotation_deg(page, ".foot .footmark")) < 0.5

    # leaving: no transition, so it snaps home with no animated reverse spin
    page.mouse.move(400, 300)
    page.wait_for_timeout(60)
    assert page.locator(".foot .footmark").evaluate(
        "el => getComputedStyle(el).transitionDuration"
    ) == "0s"
    assert abs(_rotation_deg(page, ".foot .footmark")) < 0.5


def test_footer_mark_does_not_turn_under_reduced_motion(open_site):
    """F1: the reduced-motion block pins .footmark:hover to transform:none, so a
    reduce reader gets no spin (without it the global transition-duration
    override would just instant-flip it)."""
    page, _ = open_site(reduced_motion=True)
    mark = page.locator(".foot .footmark")
    mark.scroll_into_view_if_needed()
    mark.hover()
    page.wait_for_timeout(300)
    assert abs(_rotation_deg(page, ".foot .footmark")) < 0.5


# --- Spark Order S6 / moves 06 + 01: the correction is FLIP over an
# aria-hidden clone. It is the S0 "bend" — a transform carrying layout — and
# is only allowed because it is transient: every transform is cleared and the
# frame is handed back to the untouched static pair. ---

def test_correction_leaves_no_residual_transform(open_site):
    """Guards the S0 bend. After the beat settles, no specimen node holds a
    transform — none or the identity matrix only. Must never be deleted."""
    page, _ = open_site()
    page.wait_for_timeout(200)
    page.locator("#specimen").scroll_into_view_if_needed()
    page.wait_for_timeout(3000)   # beat + settle

    assert page.locator(".spec__perform").count() == 0
    bad = page.eval_on_selector_all(
        "#specimen .spec[data-op='delete'] *",
        """els => els
            .map(e => getComputedStyle(e).transform)
            .filter(t => t !== 'none' && t !== 'matrix(1, 0, 0, 1, 0, 0)')""")
    assert bad == [], bad
    op = page.eval_on_selector_all(
        "#specimen .spec[data-op='delete'] .line-spec",
        "els => els.map(e => getComputedStyle(e).opacity)")
    assert all(float(x) > 0.98 for x in op), op


def test_correction_replays_after_language_switch(open_site):
    """Switch language at the top of the page (beat not yet triggered), then
    scroll down: the still-armed observer fires, the sentence performs, and
    nothing holds NaN-derived geometry."""
    page, _ = open_site()
    page.wait_for_function(
        "document.documentElement.classList.contains('hero-done')", timeout=6000)
    page.locator(".masthead .langswitch").click()
    page.wait_for_timeout(300)

    page.locator("#specimen").scroll_into_view_if_needed()
    seen = False
    for _ in range(60):
        if page.locator(".spec__perform").count():
            seen = True
            break
        page.wait_for_timeout(25)
    assert seen, "the beat did not run after a language switch"

    page.wait_for_timeout(3000)
    assert page.locator(".spec__perform").count() == 0
    nan = page.eval_on_selector_all(
        "#specimen *",
        "els => els.filter(e => /nan/i.test(getComputedStyle(e).transform)).length")
    assert nan == 0
    op = page.eval_on_selector_all(
        "#specimen .spec[data-op='delete'] .line-spec",
        "els => els.map(e => getComputedStyle(e).opacity)")
    assert all(float(x) > 0.98 for x in op), op


def _clip_heights(page):
    # getBBox() reflects the live (CSS-animated) rect geometry; getComputedStyle
    # reports "auto" for a rect whose CSS height is 0 or auto, which parses to
    # nothing.
    return page.evaluate(
        """() => ['glyphClipLeft', 'glyphClipRight', 'glyphClipStem'].map(id =>
            document.querySelector('#' + id + ' rect').getBBox().height)"""
    )


def test_origin_mark_draws_its_three_strokes_once(open_site):
    """S7 move 03: on first reveal the mark assembles from its three strokes in
    order — the two V arms, then the stem — by growing each clip rect from zero,
    then holds. It is a real draw (a partial state is seen), the arms fill before
    the stem, and it is one-shot: still full ~1s later, no loop or reset."""
    page, _ = open_site()
    page.locator("#origin").scroll_into_view_if_needed()
    data = page.evaluate(
        """async () => {
            const ids = ['glyphClipLeft', 'glyphClipRight', 'glyphClipStem'];
            const full = { glyphClipLeft: 100, glyphClipRight: 100, glyphClipStem: 44 };
            const h = id => document.querySelector('#' + id + ' rect').getBBox().height;
            const t0 = performance.now();
            const firstFull = {};
            let sawPartial = false;
            await new Promise(res => {
                const tick = () => {
                    ids.forEach(id => {
                        const cur = h(id);
                        if (cur > 1 && cur < full[id] * 0.6) sawPartial = true;
                        if (!(id in firstFull) && cur >= full[id] * 0.98) {
                            firstFull[id] = performance.now() - t0;
                        }
                    });
                    if (Object.keys(firstFull).length === ids.length
                        || performance.now() - t0 > 4000) return res();
                    requestAnimationFrame(tick);
                };
                requestAnimationFrame(tick);
            });
            await new Promise(r => setTimeout(r, 900));
            return { firstFull, sawPartial, held: ids.map(h) };
        }"""
    )
    ff = data["firstFull"]
    assert set(ff) == {"glyphClipLeft", "glyphClipRight", "glyphClipStem"}, data
    assert data["sawPartial"], data
    # assembled in order: each V arm reaches full before the stem does
    assert ff["glyphClipLeft"] < ff["glyphClipStem"], ff
    assert ff["glyphClipRight"] < ff["glyphClipStem"] + 30, ff
    # one-shot: still drawn ~1s after it finished, nothing reset it
    held = data["held"]
    assert held[0] > 98 and held[1] > 98 and held[2] > 42, held


def test_origin_mark_holds_still_for_the_hover_states(open_site):
    """S7 move 03 step 3: the draw must finish before, and never fight, the
    is-active/is-dim states. Focusing a hit-region after the draw lights that
    stroke without disturbing the (now full) clip geometry."""
    page, _ = open_site()
    page.locator("#origin").scroll_into_view_if_needed()
    page.wait_for_timeout(1800)   # draw done
    before = _clip_heights(page)
    page.locator('.origin__hit[data-discipline="chess"]').focus()
    page.wait_for_timeout(200)
    after = _clip_heights(page)
    assert before[0] > 98 and before[1] > 98 and before[2] > 42, before
    assert after == pytest.approx(before, abs=0.5), (before, after)
    assert page.locator('.glyph__part--right').evaluate(
        "el => el.classList.contains('is-active')") is True
