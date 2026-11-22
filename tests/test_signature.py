"""SITE-PLAN Category F (2026-11-20): the signature pieces — new blocks added
beside what exists, never replacing it. Each works in both languages and
both widths, uses only the two inks (amber = the mistake, green = the natural
form), and with JavaScript off is simply hidden.

F1: English, "Test your ear".
F2 (chess, "Is your rating actually stuck?") was removed on 2026-11-23.
"""

from urllib.parse import unquote

import pytest

from conftest import NARROW, horizontal_overflow


# ---------------------------------------------------------------- F1 ---

def _ear(page):
    return page.locator("#ear")


def test_ear_test_lives_on_the_english_page_only(open_site):
    page, _ = open_site(path="english/")
    assert _ear(page).count() == 1
    # beside the specimens, never inside them (#specimen's prose may carry no
    # digit, and this block shows a score), and before the method
    order = page.locator(".sec[id]").evaluate_all("els => els.map(e => e.id)")
    assert order.index("ear") == order.index("specimen") + 1
    assert order.index("method") == order.index("ear") + 1
    assert page.locator("#specimen #ear").count() == 0
    # unnumbered: the section count is untouched
    assert _ear(page).locator(".label .num").count() == 0
    for path in ("index.html", "chess/", "climbing/"):
        other, _ = open_site(path=path)
        assert other.locator("#ear, .ear").count() == 0


def test_ear_test_toggles_checks_and_scores(open_site):
    page, _ = open_site(path="english/")
    picks = page.locator(".ear__pick")
    assert picks.count() == 8
    for i in range(8):
        assert picks.nth(i).get_attribute("aria-pressed") == "false"
    # nothing gives the answer away before the check
    assert page.locator(".ear__fix:visible, .ear__verdict:visible").count() == 0
    assert page.locator(".ear__item .ear__s del, .ear__item .ear__s ins").count() == 0

    picks.nth(3).click()                      # a natural sentence: right to pick
    picks.nth(0).click()                      # "I am agree": wrong to pick
    picks.nth(0).click()                      # ...changed my mind
    picks.nth(4).click()                      # "explain me this": wrong to pick
    assert picks.nth(3).get_attribute("aria-pressed") == "true"
    assert picks.nth(0).get_attribute("aria-pressed") == "false"

    page.locator(".ear__check").click()
    assert page.locator(".ear__result").is_visible()
    # 8 items: picked 3 (right) and 4 (wrong); missed control 6 -> 6 correct
    assert page.locator(".ear__score").inner_text() == "You judged 6 of 8 correctly."
    habit = page.locator(".ear__habit").inner_text()
    assert "word order" in habit
    # every wrong sentence now shows its natural form, and the picks are locked
    assert page.locator(".ear__fix:visible").count() == 6
    assert page.locator(".ear__item.is-miss").count() == 2
    assert picks.nth(1).is_disabled()
    # the score travels in a prefilled Telegram message, naming the discipline
    href = unquote(page.locator(".ear__send").get_attribute("href"))
    assert href.startswith("https://t.me/yngvil?text=")
    assert "6/8" in href and "English" in href


def test_ear_test_marks_use_the_two_inks_only(open_site):
    page, _ = open_site(path="english/")
    page.locator(".ear__check").click()
    cut = page.locator(".ear__cut").first.evaluate("el => getComputedStyle(el).textDecorationLine")
    assert "line-through" in cut
    amber = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--amber-text').trim()")
    green = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--green-text').trim()")
    probe = page.evaluate(
        """([a, g]) => { const d = document.createElement('i'); document.body.appendChild(d);
             d.style.color = a; const A = getComputedStyle(d).color;
             d.style.color = g; const G = getComputedStyle(d).color; d.remove(); return [A, G]; }""",
        [amber, green])
    assert page.locator(".ear__cut").first.evaluate("el => getComputedStyle(el).color") == probe[0]
    assert page.locator(".ear__fix ins").first.evaluate("el => getComputedStyle(el).color") == probe[1]


def test_ear_test_follows_a_language_switch_after_the_check(open_site):
    page, _ = open_site(path="english/")
    page.locator(".ear__check").click()
    page.evaluate("document.querySelector('.masthead .langswitch').click()")
    page.wait_for_timeout(100)
    assert page.locator(".ear__score").inner_text().startswith("Вы верно оценили")
    href = unquote(page.locator(".ear__send").get_attribute("href"))
    assert "по английскому" in href


def test_ear_test_try_again_resets_everything(open_site):
    page, _ = open_site(path="english/")
    page.locator(".ear__pick").nth(2).click()
    page.locator(".ear__check").click()
    page.locator(".ear__again").click()
    assert page.locator(".ear__result").is_hidden()
    assert page.locator(".ear__check").is_visible() and page.locator(".ear__again").is_hidden()
    assert page.locator('.ear__pick[aria-pressed="true"]').count() == 0
    assert page.locator(".ear__fix:visible").count() == 0
    assert not page.locator(".ear__pick").first.is_disabled()


def test_ear_test_is_hidden_without_js(open_site):
    page, _ = open_site(path="english/", java_script_enabled=False)
    assert _ear(page).evaluate("el => getComputedStyle(el).display") == "none"


@pytest.mark.parametrize("lang", ["en", "ru"])
def test_ear_test_fits_a_phone(open_site, lang):
    page, _ = open_site(path="english/", viewport=NARROW, has_touch=True, lang=lang)
    page.locator(".ear__check").click()
    assert not horizontal_overflow(page)
    for i in range(8):
        box = page.locator(".ear__pick").nth(i).bounding_box()
        assert box["height"] >= 44, "touch target"
