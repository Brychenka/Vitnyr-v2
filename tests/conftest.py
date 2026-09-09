"""
Shared fixtures for the Vitnyr site-v2 QA suite.

The site is static (no build, no framework). These fixtures:
  * serve the repo root over HTTP on an ephemeral port, once per session
    (CLAUDE.md: check under a real server, not file://),
  * hand each test a `base_url`,
  * provide `open_site(...)` to load a page under a chosen theme, language,
    reduced-motion setting and viewport, with localStorage seeded *before*
    first paint so theme.js stamps the right pair with no flash,
  * expose `console_guard` to assert a page produced no console errors.
"""

import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Widths and the media pairs CLAUDE.md's manual checklist calls out.
NARROW = {"width": 375, "height": 780}
WIDE = {"width": 1280, "height": 900}

THEME_KEY = "vitnyr-theme"
LANG_KEY = "vitnyr-lang"


def _wait_for_port(host: str, port: int, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"server on {host}:{port} never came up")


@pytest.fixture(scope="session")
def http_server():
    """`python -m http.server` rooted at the repo, on a free port."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_port("127.0.0.1", port)
        yield f"http://127.0.0.1:{port}"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.fixture(scope="session")
def site_url(http_server):
    # not named `base_url`: pytest-base-url ships a session-scoped consumer of
    # that name and it collides with a per-test fixture.
    return http_server


@pytest.fixture
def open_site(site_url, browser):
    """
    Factory: open index.html in a fresh context.

      open_site(theme=None|'light'|'dark',   # explicit stored choice; the ONLY
                                             # way to select the charcoal pair
                color_scheme='light'|'dark',  # OS preference; the page ignores it
                lang=None|'en'|'ru',          # stored language choice
                query='',                     # e.g. '?lang=ru'
                hash='',                      # e.g. '#collage'
                reduced_motion=False,
                viewport=WIDE,
                has_touch=False)          # True => (pointer: coarse) matches

    Returns (page, context). localStorage is seeded via an init script so the
    values are present on the very first execution of theme.js.
    """
    contexts = []

    def _open(
        theme=None,
        # Cream is the default pair since 2026-09-07 and `prefers-color-scheme`
        # no longer has a say (theme.js `effectiveTheme`, BUILD-NOTES "Cream is
        # the default pair; charcoal is opt-in only"). This knob therefore only
        # sets the OS preference the page is *allowed to ignore* — it does not
        # choose the pair. A test that wants the charcoal pair must seed the
        # explicit stored choice with theme="dark".
        color_scheme="light",
        lang=None,
        query="",
        hash="",
        reduced_motion=False,
        viewport=None,
        java_script_enabled=True,
        has_touch=False,
    ):
        context = browser.new_context(
            viewport=viewport or WIDE,
            color_scheme=color_scheme,
            reduced_motion="reduce" if reduced_motion else "no-preference",
            java_script_enabled=java_script_enabled,
            has_touch=has_touch,
        )
        contexts.append(context)

        seed = []
        if theme is not None:
            seed.append(f"localStorage.setItem({THEME_KEY!r}, {theme!r});")
        if lang is not None:
            seed.append(f"localStorage.setItem({LANG_KEY!r}, {lang!r});")
        if seed:
            context.add_init_script("try{" + "".join(seed) + "}catch(e){}")

        page = context.new_page()
        page.goto(f"{site_url}/index.html{query}{hash}", wait_until="load")
        return page, context

    yield _open

    for c in contexts:
        c.close()


@pytest.fixture
def console_guard():
    """
    Attach to a page, then call .assert_clean() to fail on any console error
    or uncaught page exception.

        def test_x(open_site, console_guard):
            page, _ = open_site()
            console_guard.watch(page)
            ...
            console_guard.assert_clean()
    """

    class Guard:
        def __init__(self):
            self.errors = []

        def watch(self, page):
            page.on(
                "console",
                lambda m: self.errors.append(f"console.{m.type}: {m.text}")
                if m.type == "error"
                else None,
            )
            page.on("pageerror", lambda exc: self.errors.append(f"pageerror: {exc}"))

        def assert_clean(self):
            assert not self.errors, "page reported errors:\n" + "\n".join(self.errors)

    return Guard()


def horizontal_overflow(page) -> bool:
    """True if the document is wider than the viewport (ignoring the parked
    skip link, which lives at left:-9999px by design)."""
    return page.evaluate(
        """() => {
            const de = document.documentElement;
            // width of content excluding elements deliberately parked off-canvas
            return de.scrollWidth > de.clientWidth + 1;
        }"""
    )


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _relative_luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (_srgb_to_linear(c / 255) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb_a: tuple[float, float, float], rgb_b: tuple[float, float, float]) -> float:
    """WCAG contrast ratio between two *already-flattened* (alpha-free) sRGB
    triples — the standard (L1+0.05)/(L2+0.05) with the lighter one first."""
    la, lb = _relative_luminance(rgb_a), _relative_luminance(rgb_b)
    lighter, darker = (la, lb) if la >= lb else (lb, la)
    return (lighter + 0.05) / (darker + 0.05)


def rule_contrast(page) -> float:
    """P12: --rule is a translucent overlay, not a flat colour, so its
    effective contrast against --bg depends on what it's composited over.
    Flattens both from actual computed styles (not hand-typed hex, which
    drifts from the stylesheet) and returns the WCAG ratio. --bg/--rule are
    authored in different formats (hex, rgba()) across the stylesheet, so
    each is normalised through a probe element's computed style rather than
    regexed by hand — the browser resolves either format to "rgb(a)(...)"."""
    bg, rule = page.evaluate(
        """() => {
            const cs = getComputedStyle(document.documentElement);
            const probe = document.createElement('div');
            probe.style.display = 'none';
            document.body.appendChild(probe);
            const toRgba = (token) => {
                probe.style.color = 'initial';
                probe.style.color = token;
                const computed = getComputedStyle(probe).color;  // "rgb(r,g,b)" or "rgba(r,g,b,a)"
                const m = computed.match(/[\\d.]+/g).map(Number);
                return { r: m[0], g: m[1], b: m[2], a: m.length > 3 ? m[3] : 1 };
            };
            const result = [toRgba(cs.getPropertyValue('--bg')), toRgba(cs.getPropertyValue('--rule'))];
            probe.remove();
            return result;
        }"""
    )
    flattened = (
        bg["r"] + rule["a"] * (rule["r"] - bg["r"]),
        bg["g"] + rule["a"] * (rule["g"] - bg["g"]),
        bg["b"] + rule["a"] * (rule["b"] - bg["b"]),
    )
    return contrast_ratio(flattened, (bg["r"], bg["g"], bg["b"]))
