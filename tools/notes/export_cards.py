"""Export the notes' share cards: python3 tools/notes/export_cards.py

Serves the repo on a free local port, opens assets/share/share-card.html for
the index and every note in tools/notes/build.py's ORDER, in English and
Russian, and writes assets/share/og-notes(-ru).png and
og-note-<slug>(-ru).png at 1200x630. Run build.py first (it writes the
cards' text into share-card.html). Needs Playwright with Chromium (the test
suite's environment has it: tests/.venv/bin/python tools/notes/export_cards.py).
"""
import functools
import http.server
import importlib
import socketserver
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import ORDER  # noqa: E402
from lib import ROOT  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402


def main():
    slugs = [importlib.import_module(m).NOTE["slug"] for m in ORDER]
    jobs = [("notes", "og-notes")] + [(f"note-{s}", f"og-note-{s}") for s in slugs]
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a: None
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            for page, name in jobs:
                for lang, suf in (("en", ""), ("ru", "-ru")):
                    pg.goto(f"http://127.0.0.1:{port}/assets/share/share-card.html?page={page}&lang={lang}",
                            wait_until="networkidle")
                    pg.evaluate("document.fonts.ready")
                    pg.wait_for_timeout(600)
                    out = ROOT / "assets" / "share" / f"{name}{suf}.png"
                    pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
                    print("wrote", out.relative_to(ROOT))
            b.close()
        srv.shutdown()


if __name__ == "__main__":
    main()
