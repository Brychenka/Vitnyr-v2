"""Page loads, its own resources resolve, and nothing errors on the console."""

import pytest


def test_document_loads_with_title(open_site):
    page, _ = open_site()
    assert page.title() == "Igor Shatsev — Vitnyr"
    # get_by_role, not locator("h1"): #collage carries its own h1 too (C3),
    # exposed to the accessibility tree only once that view is open.
    assert page.get_by_role("heading", level=1).count() == 1


def test_no_console_errors_on_load(open_site, console_guard):
    page, _ = open_site()
    console_guard.watch(page)
    page.reload(wait_until="load")
    page.wait_for_timeout(1500)  # let the font race / hero settle
    console_guard.assert_clean()


def test_local_resources_all_resolve(open_site):
    """Every same-origin request the page makes returns < 400. Font CDN and
    other cross-origin hosts are out of scope."""
    page, _ = open_site()
    failures = []
    origin = page.url.split("/index.html")[0]

    def on_response(resp):
        if resp.url.startswith(origin) and resp.status >= 400:
            failures.append(f"{resp.status} {resp.url}")

    page.on("response", on_response)
    page.reload(wait_until="load")
    page.wait_for_timeout(500)
    assert not failures, "broken same-origin resources:\n" + "\n".join(failures)


def test_core_assets_referenced_exist(open_site):
    page, _ = open_site()
    for path in ("style.css", "theme.js", "main.js", "favicon.ico"):
        resp = page.request.get(f"{page.url.split('/index.html')[0]}/{path}")
        assert resp.ok, f"{path} -> {resp.status}"


def test_third_party_libraries_are_present(open_site):
    """GSAP + CustomEase + Lenis load from CDN; the motion layer is a no-op
    without them but they should be arriving in a normal run."""
    page, _ = open_site()
    page.wait_for_timeout(1500)
    libs = page.evaluate(
        "() => ({ gsap: !!window.gsap, ease: !!window.CustomEase, lenis: !!window.Lenis })"
    )
    assert libs == {"gsap": True, "ease": True, "lenis": True}, libs
