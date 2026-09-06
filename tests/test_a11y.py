"""Accessibility guarantees the build commits to: one h1, real landmarks,
a working skip link (focus move, not just scroll), accessible names on every
control, and a fully readable page under prefers-reduced-motion."""

import pytest


def _exposed_ids(page, tag):
    """ids of <tag> elements actually reachable by assistive tech: not under
    an inert ancestor (real browsers drop inert subtrees from the
    accessibility tree; Playwright's own role engine doesn't model that, so
    this checks the underlying rule directly) and not visibility:hidden."""
    return page.evaluate(
        """(tag) => [...document.querySelectorAll(tag)]
            .filter(el => !el.closest('[inert]')
                && getComputedStyle(el).visibility !== 'hidden')
            .map(el => el.id)""",
        tag,
    )


def test_single_h1_and_main_landmark(open_site):
    page, _ = open_site()
    # #collage carries its own h1/<main> too (C3 — it behaves like its own
    # page), so the raw DOM count of each is 2 by design; exactly one of
    # each is actually exposed while the view sits closed (visibility:hidden).
    assert page.locator("h1").count() == 2
    assert _exposed_ids(page, "h1") == [""]  # the site's own, unlabelled
    assert _exposed_ids(page, "main") == ["main"]
    assert page.locator("main#main").count() == 1
    assert page.locator("header.masthead").count() == 1
    assert page.locator("footer").count() == 1


def test_single_h1_and_main_landmark_when_collage_view_is_open(open_site):
    """The reverse of the case above: with #collage open, #app (the site's
    own h1 and <main>) is made inert, so exactly one h1 and one <main> stay
    exposed — the collage's own — never both at once."""
    page, _ = open_site(hash="#collage")
    assert _exposed_ids(page, "h1") == ["collage-title"]
    assert _exposed_ids(page, "main") == ["collage-main"]


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
    glyph alone. The register specimen (P5) isn't a grammar error — its wrong
    line is grammatically fine, just badly pitched — so it carries its own
    "Reads as" / "Better as" pair instead of overstating it as "Incorrect"."""
    page, _ = open_site()
    vh = page.locator(".line-spec .vh")
    assert vh.count() == 6
    texts = {t.strip() for t in vh.all_inner_texts()}
    assert texts == {"Incorrect:", "Correct:", "Reads as:", "Better as:"}

    register = page.locator(".spec", has=page.locator("text=Register, not grammar"))
    # .line-spec .vh, same scope as the count above: the specimen also carries a
    # .vh inside its permalink label now (S9A / move 09), which isn't a
    # correctness equivalent and shouldn't be swept in here.
    register_labels = {t.strip() for t in register.locator(".line-spec .vh").all_inner_texts()}
    assert register_labels == {"Reads as:", "Better as:"}


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


def test_origin_mark_is_complete_under_reduced_motion(open_site):
    """S7 move 03: the stroke draw is motion; under prefers-reduced-motion the
    mark is simply present and whole. Each clip rect sits at full geometry — no
    stroke left clipped away by a rect held at zero (a `height: auto` on a clip
    rect collapses to 0 here, so the reset uses explicit px)."""
    page, _ = open_site(reduced_motion=True)
    page.locator("#origin").scroll_into_view_if_needed()
    page.wait_for_timeout(150)
    heights = page.evaluate(
        """() => ['glyphClipLeft', 'glyphClipRight', 'glyphClipStem'].map(id =>
            document.querySelector('#' + id + ' rect').getBBox().height)"""
    )
    assert heights[0] > 90 and heights[1] > 90 and heights[2] > 40, heights


def test_reduced_motion_facts_row_shows_every_value(open_site):
    """The reduced-motion branch in main.js returns early; the facts must still
    read out in full. It calls countUp(true), which settles every number to its
    final text with no tween — so reduced-motion readers get the values, never a
    count. This guards both that settle and the early-return path itself."""
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


def test_origin_mark_shows_a_focus_ring_on_the_visible_figure(open_site):
    """The hit regions (.origin__hit) are invisible, oversized rectangles —
    a ring drawn on one of them wouldn't trace anything the reader can see,
    so it used to be suppressed outright (C7) with only a colour/opacity
    change on the glyph to mark focus. The ring now lands on .origin__mark,
    the figure the reader actually sees, via :has(.origin__hit:focus-visible)."""
    page, _ = open_site()
    mark = page.locator(".origin__mark")
    assert mark.evaluate("el => getComputedStyle(el).outlineStyle") == "none"

    page.locator('.origin__hit[data-discipline="chess"]').focus()
    style = mark.evaluate(
        "el => ({ style: getComputedStyle(el).outlineStyle, color: getComputedStyle(el).outlineColor })"
    )
    assert style["style"] == "solid"
    assert style["color"] == "rgb(76, 122, 82)"  # --ink-target on charcoal
    # the hit rectangle itself still carries no ring of its own
    hit_outline = page.locator('.origin__hit[data-discipline="chess"]').evaluate(
        "el => getComputedStyle(el).outlineStyle"
    )
    assert hit_outline == "none"


# --- C14 (2026-09-07): the dot is the pointer now — present everywhere on a
# fine pointer, not just over hot targets, and it never balloons. So
# cursor:none is page-wide and hovering plain body copy shows the dot, not a
# native I-beam. Its one signal is colour: the fill eases to an accent over a
# control (mouseover/mouseout toggle .cursor-active), same size either way. ---

def test_dot_is_the_pointer_page_wide(open_site):
    page, _ = open_site()
    page.mouse.move(400, 300)
    page.mouse.move(400, 760)   # inside .stand, well clear of any control
    page.wait_for_timeout(200)
    assert page.evaluate("document.documentElement.classList.contains('has-cursor')")
    # native cursor is suppressed page-wide, not just on links
    assert page.locator(".stand:visible").evaluate(
        "el => getComputedStyle(el).cursor"
    ) == "none"
    # and the dot itself is visible over plain text, no longer gated to links
    assert page.locator(".cursor").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) > 0.95


def test_dot_stays_one_size_and_only_recolours_over_hot_targets(open_site):
    """The dot never changes size. Its one state change is colour: .cursor-active
    is added over a link/button (fill -> --ink-target) and removed off it, while
    the dot stays visible either way."""
    page, _ = open_site()
    dot = page.locator(".cursor")
    dot_dot = page.locator(".cursor__dot")
    link = page.locator('a[href="#method"]')  # the scrollcue

    page.mouse.move(400, 300)
    page.mouse.move(400, 760)   # plain text
    page.wait_for_timeout(200)
    assert page.evaluate("document.documentElement.classList.contains('has-cursor')")
    assert dot.evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95
    assert "cursor-active" not in (page.locator("html").get_attribute("class") or "")
    rest_box = dot.bounding_box()

    box = link.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(300)
    assert "cursor-active" in (page.locator("html").get_attribute("class") or "")
    # no balloon — the dot's rendered size does not change over a hot target
    hot_box = dot.bounding_box()
    assert abs(hot_box["width"] - rest_box["width"]) < 0.5
    assert abs(hot_box["height"] - rest_box["height"]) < 0.5
    # colour is the whole effect; let .cursor__dot's background settle over --t
    page.wait_for_timeout(700)
    assert (
        dot_dot.evaluate("el => getComputedStyle(el).backgroundColor")
        == "rgb(76, 122, 82)"  # --ink-target on charcoal (open_site default)
    )

    page.mouse.move(400, 760)
    page.wait_for_timeout(400)
    assert "cursor-active" not in (page.locator("html").get_attribute("class") or "")
    assert dot.evaluate("el => parseFloat(getComputedStyle(el).opacity)") > 0.95


# --- Spark Order S6 (moves 06 + 01): the specimen correction is performed on
# a throwaway aria-hidden clone; the static <del>/<ins> pair stays the source
# of truth for no-JS, reduced-motion and screen-reader readers, and the
# ✕/✓ glyphs are now real proofreading marks. ---

def _spec_pair_readable(page):
    for cls in (".wrong", ".right"):
        loc = page.locator(f"#specimen .line-spec{cls}")
        assert loc.count() == 3
        for i in range(3):
            assert loc.nth(i).is_visible()
            assert loc.nth(i).inner_text().strip()


def test_specimen_static_pair_survives_without_js(open_site):
    page, _ = open_site(java_script_enabled=False)
    _spec_pair_readable(page)
    # and no performance layer was built
    assert page.locator(".spec__perform").count() == 0
    assert page.locator("#specimen .line-spec del").count() == 3


def test_specimen_static_pair_survives_reduced_motion(open_site):
    page, _ = open_site(reduced_motion=True)
    page.wait_for_timeout(300)
    page.locator("#specimen").scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    _spec_pair_readable(page)
    assert page.locator(".spec__perform").count() == 0
    # nothing was left dimmed
    op = page.eval_on_selector_all(
        "#specimen .line-spec", "els => els.map(e => getComputedStyle(e).opacity)")
    assert all(float(x) > 0.98 for x in op), op


def test_correction_performance_is_hidden_from_assistive_tech(open_site):
    page, _ = open_site()
    page.wait_for_timeout(200)
    page.locator("#specimen").scroll_into_view_if_needed()
    # catch a perf element while the beat is running
    seen_hidden = False
    for _ in range(60):
        perf = page.locator(".spec__perform")
        if perf.count():
            assert perf.first.get_attribute("aria-hidden") == "true"
            seen_hidden = True
            break
        page.wait_for_timeout(25)
    assert seen_hidden, "the performance element never appeared"
    # the real paragraphs are untouched: no aria-hidden, real text, and the
    # corrected sentence is findable by an assistive-tech reader
    for cls in (".wrong", ".right"):
        for i in range(3):
            assert page.locator(f"#specimen .line-spec{cls}").nth(i).get_attribute("aria-hidden") is None
    assert page.get_by_text("I feel good today.").count() >= 1
    page.wait_for_timeout(2600)
    assert page.locator(".spec__perform").count() == 0   # torn down when it settles


def test_specimen_marks_are_proofreading_notation(open_site):
    """move 06: the ✕/✓ pair (path 'M1 1 L9 9 ...') is replaced by a dele
    loop / caret / transpose hook. The register specimen restructures, so its
    mark differs from the two deletion specimens'."""
    page, _ = open_site()
    ds = page.eval_on_selector_all(
        "#specimen .line-spec .sig svg path", "els => els.map(e => e.getAttribute('d'))")
    assert len(ds) == 6
    assert not any("M1 1 L9 9" in d for d in ds), "old ✕ glyph still present"
    # specimen 3 (restructure) uses a different mark than specimens 1-2 (delete)
    assert ds[0] != ds[4] and ds[1] != ds[5]


def test_specimen_permalink_names_the_specimen_not_just_the_hash(open_site):
    """Spark Order S9A / move 09: the label link's accessible name is the
    specimen's own wording plus an intent phrase — never a bare "#". The
    decorative # glyph is hidden from assistive tech."""
    page, _ = open_site()
    a = page.locator("#specimen-reflexive .spec__permalink")
    name = a.evaluate("el => el.textContent.replace('#', '').trim()")
    assert name == "Reflexive carried across, link to this specimen"
    assert a.locator(".spec__permalink-mark").get_attribute("aria-hidden") == "true"
    # the copy confirmation is inert until a successful copy
    status = page.locator("#specimen-reflexive .spec__permalink-status")
    assert status.get_attribute("hidden") is not None
    assert status.evaluate("el => getComputedStyle(el).display") == "none"


def test_specimen_permalink_degrades_to_a_plain_anchor_without_js(open_site):
    """With main.js absent the label is still an ordinary in-page anchor to a
    real element id — the browser handles the jump, nothing is lost."""
    page, _ = open_site(java_script_enabled=False)
    for sid in ("specimen-reflexive", "specimen-copula", "specimen-register"):
        a = page.locator(f"#{sid} .spec__permalink")
        assert a.get_attribute("href") == f"#{sid}"
        assert page.locator(f"article#{sid}").count() == 1
    # no JS => no clipboard confirmation shown
    assert page.locator("#specimen .spec__permalink-status:not([hidden])").count() == 0
