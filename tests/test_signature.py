"""SITE-PLAN Category F (2026-11-20): the signature pieces — new blocks added
beside what exists, never replacing it. Each works in both languages and
both widths, uses only the two inks (amber = the mistake, green = the natural
form), and with JavaScript off is simply hidden.

F1: English, "Test your ear".
F2: chess, "Is your rating actually stuck?" (lives further down this file).
"""

import json
import re
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
    # unnumbered: the 01-05 count is untouched
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


# ---------------------------------------------------------------- F2 ---
# Tests never call the real Lichess: page.route answers for it.

RATING_API = "https://lichess.org/api/user/*/rating-history"


def _series(start, step, n=40, every=8):
    import datetime
    today = datetime.date.today()
    pts = []
    for i in range(n):
        d = today - datetime.timedelta(days=(n - i) * every)
        pts.append([d.year, d.month - 1, d.day, start + step * i])
    return pts


def _fake_lichess(page, status=200, body=None, seen=None):
    def handle(route):
        if seen is not None:
            seen.append(route.request.url)
        route.fulfill(status=status, content_type="application/json",
                      body=json.dumps(body if body is not None else {}),
                      headers={"access-control-allow-origin": "*"})
    page.route(RATING_API, handle)


def _ask(page, user="some_player"):
    page.locator("#rating").scroll_into_view_if_needed()
    page.fill(".rating__input", user)
    page.locator(".rating__go").click()


FLAT = [{"name": "Bullet", "points": []},
        {"name": "Blitz", "points": _series(1640, 1)},
        {"name": "Puzzles", "points": _series(1500, 10, 80)}]   # not a playing pool
RISING = [{"name": "Rapid", "points": _series(1400, 9)},
          {"name": "Blitz", "points": _series(1500, 0, 5)}]


def test_rating_check_lives_on_the_chess_page_only(open_site):
    page, _ = open_site(path="chess/")
    order = page.locator(".sec[id]").evaluate_all("els => els.map(e => e.id)")
    assert order.index("rating") == order.index("specimen") + 1
    assert order.index("method") == order.index("rating") + 1
    assert page.locator("#rating .label .num").count() == 0
    note = page.locator(".rating__note").inner_text()
    assert "Nothing is stored" in note
    inp = page.locator(".rating__input")
    assert inp.get_attribute("autocomplete") == "off" and inp.get_attribute("spellcheck") == "false"
    for path in ("index.html", "english/", "climbing/"):
        other, _ = open_site(path=path)
        assert other.locator("#rating, .rating").count() == 0


def test_a_flat_year_reads_as_a_plateau(open_site):
    page, _ = open_site(path="chess/")
    seen = []
    _fake_lichess(page, body=FLAT, seen=seen)
    _ask(page, "Some_Player-1")
    page.wait_for_selector(".rating__out:not([hidden])")
    assert seen and seen[0].endswith("/api/user/Some_Player-1/rating-history")
    assert page.locator(".rating__say").inner_text() == "Last 12 months, Blitz: between 1640 and 1679."
    assert page.locator(".rating__verdict").inner_text().startswith("That’s a plateau.")
    assert page.locator(".rating__chart svg .rating__line").count() == 1
    assert page.locator(".rating__chart svg .rating__bracket").count() == 1
    bracket = page.locator(".rating__bracket").evaluate("el => getComputedStyle(el).stroke")
    amber = page.evaluate(
        "() => { const d = document.createElement('i'); d.style.color = 'var(--ink-specimen)';"
        " document.body.appendChild(d); const c = getComputedStyle(d).color; d.remove(); return c; }")
    assert bracket == amber, "the bracket is the specimen ink, nothing new"
    href = unquote(page.locator(".rating__send").get_attribute("href"))
    assert "My Lichess is Some_Player-1" in href and "chess" in href


def test_a_rising_year_is_still_moving_and_picks_the_busiest_pool(open_site):
    page, _ = open_site(path="chess/")
    _fake_lichess(page, body=RISING)
    _ask(page)
    page.wait_for_selector(".rating__out:not([hidden])")
    assert page.locator(".rating__say").inner_text().startswith("Last 12 months, Rapid:")
    assert page.locator(".rating__verdict").inner_text().startswith("Still moving.")


@pytest.mark.parametrize("status,body,expected", [
    (404, {"error": "Not found"}, "Lichess doesn’t know that username."),
    (429, {}, "Lichess asks to wait a minute. Try again shortly."),
    (200, [{"name": "Blitz", "points": [[2019, 0, 1, 1500]]}], "No rated games on Lichess in the last 12 months."),
    (200, [], "Lichess isn’t sharing a rating history for that username right now."),
])
def test_rating_check_says_plainly_what_went_wrong(open_site, status, body, expected):
    page, _ = open_site(path="chess/")
    _fake_lichess(page, status=status, body=body)
    _ask(page)
    page.wait_for_function("document.querySelector('.rating__status').textContent.length > 20"
                           " && !document.querySelector('.rating__status').textContent.startsWith('Asking')")
    assert page.locator(".rating__status").inner_text() == expected
    assert page.locator(".rating__out").is_hidden()


def test_a_malformed_username_never_leaves_the_page(open_site):
    page, _ = open_site(path="chess/")
    seen = []
    _fake_lichess(page, body=FLAT, seen=seen)
    _ask(page, "no spaces/please")
    page.wait_for_timeout(200)
    assert seen == []
    assert "2 to 30" in page.locator(".rating__status").inner_text()


def test_rating_check_in_russian(open_site):
    page, _ = open_site(path="chess/", lang="ru")
    _fake_lichess(page, body=FLAT)
    _ask(page)
    page.wait_for_selector(".rating__out:not([hidden])")
    assert page.locator(".rating__say").inner_text() == "Последние 12 месяцев, блиц: от 1640 до 1679."
    assert unquote(page.locator(".rating__send").get_attribute("href")).find("по шахматам") > 0


def test_rating_check_is_hidden_without_js(open_site):
    page, _ = open_site(path="chess/", java_script_enabled=False)
    assert page.locator("#rating").evaluate("el => getComputedStyle(el).display") == "none"


@pytest.mark.parametrize("lang", ["en", "ru"])
def test_rating_check_fits_a_phone(open_site, lang):
    page, _ = open_site(path="chess/", viewport=NARROW, has_touch=True, lang=lang)
    _fake_lichess(page, body=RISING)
    _ask(page)
    page.wait_for_selector(".rating__out:not([hidden])")
    assert not horizontal_overflow(page)
    svg = page.locator(".rating__chart svg").bounding_box()
    assert svg["x"] >= 0 and svg["x"] + svg["width"] <= NARROW["width"] + 0.5
    assert page.locator(".rating__input").bounding_box()["height"] >= 44
