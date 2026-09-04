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

      open_site(theme=None|'light'|'dark',   # explicit stored choice
                color_scheme='light'|'dark',  # the OS-level preference
                lang=None|'en'|'ru',          # stored language choice
                query='',                     # e.g. '?lang=ru'
                hash='',                      # e.g. '#collage'
                reduced_motion=False,
                viewport=WIDE)

    Returns (page, context). localStorage is seeded via an init script so the
    values are present on the very first execution of theme.js.
    """
    contexts = []

    def _open(
        theme=None,
        color_scheme="dark",
        lang=None,
        query="",
        hash="",
        reduced_motion=False,
        viewport=None,
        java_script_enabled=True,
    ):
        context = browser.new_context(
            viewport=viewport or WIDE,
            color_scheme=color_scheme,
            reduced_motion="reduce" if reduced_motion else "no-preference",
            java_script_enabled=java_script_enabled,
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
