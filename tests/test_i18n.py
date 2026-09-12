"""Dual-language DOM: the switch, persistence, the URL override, and the two
translation mechanisms (data-en/data-ru attributes and data-l blocks)."""

import re

import pytest


def test_default_language_is_english(open_site):
    page, _ = open_site()
    assert page.locator("html").get_attribute("data-lang") == "en"
    assert page.locator("html").get_attribute("lang") == "en"
    assert page.locator(".masthead .langswitch").inner_text().strip() == "RU"


def test_switch_to_russian_updates_dom_and_button(open_site):
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()

    html = page.locator("html")
    assert html.get_attribute("data-lang") == "ru"
    assert html.get_attribute("lang") == "ru"
    assert page.locator(".masthead .langswitch").inner_text().strip() == "EN"
    # a data-en/data-ru node now shows its Russian text
    eyebrow_city = page.locator('.eyebrow span[data-ru="Ереван"]')
    # text_content(), not inner_text(): the eyebrow is text-transform:uppercase
    assert eyebrow_city.text_content().strip() == "Ереван"


def test_data_l_blocks_swap_visibility(open_site):
    page, _ = open_site()
    assert page.locator('.hero__title span[data-l="en"]').is_visible()
    assert page.locator('.hero__title span[data-l="ru"]').is_hidden()

    page.locator(".masthead .langswitch").click()
    assert page.locator('.hero__title span[data-l="ru"]').is_visible()
    assert page.locator('.hero__title span[data-l="en"]').is_hidden()


def test_language_choice_persists_across_reload(open_site):
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()
    assert page.evaluate("localStorage.getItem('vitnyr-lang')") == "ru"

    page.reload(wait_until="load")
    assert page.locator("html").get_attribute("data-lang") == "ru"


def test_seeded_language_applies_before_paint(open_site):
    page, _ = open_site(lang="ru")
    assert page.locator("html").get_attribute("data-lang") == "ru"


def test_lang_query_param_overrides_storage(open_site):
    # storage says RU, ?lang=en must win for this load
    page, _ = open_site(lang="ru", query="?lang=en")
    assert page.locator("html").get_attribute("data-lang") == "en"


def test_every_data_attr_node_has_both_languages(open_site):
    page, _ = open_site()
    missing = page.evaluate(
        """() => {
            const out = [];
            document.querySelectorAll('[data-en], [data-ru]').forEach(el => {
                if (el.dataset.en == null || el.dataset.ru == null)
                    out.push(el.outerHTML.slice(0, 80));
            });
            return out;
        }"""
    )
    assert missing == [], missing


# --- P2 (Stage 6, 2026-09-06): the URL used to only ever be read on load,
# never written back — a reader who switched to Russian and copied the URL
# handed everyone else an English page. ---

def test_switch_mirrors_the_choice_into_the_url(open_site):
    page, _ = open_site()
    assert "lang=" not in page.url
    page.locator(".masthead .langswitch").click()
    assert page.url.endswith("?lang=ru") or "lang=ru" in page.url

    page.locator(".masthead .langswitch").click()
    assert "lang=en" in page.url


def test_url_mirroring_does_not_reload_or_lose_hash(open_site):
    page, _ = open_site(hash="#collage")
    page.wait_for_timeout(200)
    page.locator(".view__tools .langswitch").click()
    assert page.url.endswith("#collage") or "#collage" in page.url
    assert "lang=ru" in page.url
    # still the same document — a real navigation would have reset scroll
    # restoration / re-run theme.js's DOMContentLoaded seeding
    assert page.locator("html").get_attribute("data-lang") == "ru"


def test_plain_load_does_not_rewrite_a_clean_url(open_site):
    """Only a switch mirrors the URL — a first, ordinary visit (browser-
    language or stored-preference detection) must not silently append
    ?lang= to every reader's address bar."""
    page, _ = open_site(lang="ru")
    assert "lang=" not in page.url


def test_no_untranslated_placeholder_text_leaks(open_site):
    """After a switch, no element should still be showing its English default
    because a data-ru value was blank."""
    page, _ = open_site()
    page.locator(".masthead .langswitch").click()
    blank = page.evaluate(
        """() => {
            const out = [];
            document.querySelectorAll('[data-en][data-ru]').forEach(el => {
                if (!el.dataset.ru.trim()) out.push(el.dataset.en);
            });
            return out;
        }"""
    )
    assert blank == [], f"data-ru empty for: {blank}"


# --- Spark Order S4 / move 05: the language swap now reads as a transition.
# theme.js still owns the swap and still runs it synchronously (every test
# above depends on that); main.js layers a crossfade of #app over the top
# through the window.__vitnyrLangFade hook, present only under GSAP + motion. ---

def test_language_swap_fades_app_but_not_the_masthead(open_site):
    page, _ = open_site()
    assert page.evaluate("typeof window.__vitnyrLangFade") == "function"

    page.locator(".masthead .langswitch").click()
    # fromTo() sets #app to opacity 0 on the same tick as the click, then
    # tweens it back — so a read taken right after the click catches the dip.
    assert page.locator("#app").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) < 0.9
    # the control the reader just pressed must stay solid to answer them
    assert page.locator(".masthead").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) == 1
    # the swap itself still happened synchronously
    assert page.locator("html").get_attribute("data-lang") == "ru"

    page.wait_for_timeout(900)
    assert page.locator("#app").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) > 0.98


def test_rapid_repeated_clicks_never_strand_the_app_faded(open_site):
    """The callback runs on every call and the one opacity tween is
    retargeted, not stacked — three fast clicks end fully visible on the
    third language state, not dark on the first."""
    page, _ = open_site()
    sw = page.locator(".masthead .langswitch")
    sw.click()
    sw.click()
    sw.click()
    page.wait_for_timeout(1200)
    assert page.locator("#app").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) > 0.98
    assert page.locator("html").get_attribute("data-lang") == "ru"  # en->ru->en->ru


@pytest.mark.parametrize("scheme", ["dark", "light"])
@pytest.mark.parametrize("vp_name", ["wide", "narrow"])
def test_language_switch_button_does_not_move_when_toggled(open_site, vp_name, scheme):
    """The label swap (RU/EN, Photos/Фото, Cream/Charcoal <-> Крем/Уголь)
    resizes .tools, and .tools is right-anchored (space-between on .masthead),
    so a content-sized RU/EN button rides the reflow and visibly jumps. The
    langswitch and the Photos caption reserve a fixed box (a zero-height
    ::before holding the widest string), which pins RU/EN — and everything
    downstream of it, the collage nav icons included — in place across a
    toggle, both directions. .themeswitch is deliberately left free."""
    from conftest import NARROW, WIDE

    page, _ = open_site(
        color_scheme=scheme, reduced_motion=True,
        viewport=WIDE if vp_name == "wide" else NARROW,
    )
    page.wait_for_timeout(200)

    def left_edges():
        return page.evaluate(
            """() => {
                const x = s => Math.round(
                    document.querySelector(s).getBoundingClientRect().left * 100) / 100;
                return {
                    lang: x('.masthead .langswitch'),
                    icon: x('.masthead .tool--icon'),
                };
            }"""
        )

    sw = page.locator(".masthead .langswitch")
    before = left_edges()
    assert sw.inner_text().strip() == "RU"

    sw.click()                       # -> Russian
    page.wait_for_timeout(200)
    assert sw.inner_text().strip() == "EN"
    mid = left_edges()

    sw.click()                       # -> back to English
    page.wait_for_timeout(200)
    after = left_edges()

    for key in ("lang", "icon"):
        assert abs(mid[key] - before[key]) < 1.0, (
            f"{key} moved {mid[key] - before[key]:+.2f}px on EN->RU ({vp_name}/{scheme})"
        )
        assert abs(after[key] - before[key]) < 1.0, (
            f"{key} did not return on RU->EN ({vp_name}/{scheme})"
        )


def test_language_swap_is_instant_under_reduced_motion(open_site):
    """The hook is installed past main.js's reduced-motion return, so a
    reduced-motion reader gets theme.js's plain synchronous swap."""
    page, _ = open_site(reduced_motion=True)
    assert page.evaluate("typeof window.__vitnyrLangFade") == "undefined"
    page.locator(".masthead .langswitch").click()
    assert page.locator("html").get_attribute("data-lang") == "ru"
    assert page.locator("#app").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) == 1


def test_language_swap_degrades_to_instant_without_gsap(open_site):
    """With GSAP blocked, main.js early-returns and never installs the hook;
    theme.js falls back to calling the swap directly — the switch still works
    instantly and correctly, which is the required degradation."""
    page, context = open_site()
    context.route(re.compile(r"(gsap|lenis|customease)", re.I),
                  lambda route: route.abort())
    page.reload(wait_until="load")
    assert page.evaluate("typeof window.__vitnyrLangFade") == "undefined"
    assert not page.evaluate("document.documentElement.classList.contains('js')")

    page.locator(".masthead .langswitch").click()
    # no wait: nothing is hooked, so the swap is synchronous exactly as before
    assert page.locator("html").get_attribute("data-lang") == "ru"
    assert page.locator("#app").evaluate(
        "el => parseFloat(getComputedStyle(el).opacity)"
    ) == 1


# --- Spark Order S5 / move 19: a selected who-row and the language switch
# compose through one updateCta() that reads both — a switch recomposes the
# clause in the new language, never a re-encoded English string. ---

def test_row_selection_and_language_compose(open_site):
    page, _ = open_site()
    row = page.locator(".rows > li").nth(1)
    row.locator(".row__pick").click()

    page.locator(".masthead .langswitch").click()
    page.wait_for_timeout(200)

    href = page.locator(".contact__cta").get_attribute("href")
    text = page.evaluate("h => decodeURIComponent((h.split('?text=')[1]) || '')", href)
    ru_clause = row.get_attribute("data-prefill-ru")
    assert ru_clause and ru_clause in text
    # 2026-09-12: base offer text updated to Igor's own CTA wording.
    assert "скрининг" in text          # the RU base message
    assert "screening" not in text     # not a re-encoded English one
    # the selection itself survived the switch
    assert row.locator(".row__pick").get_attribute("aria-pressed") == "true"
