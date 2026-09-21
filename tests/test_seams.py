"""Cheap guards for values that two files must keep equal by hand."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_spark_duration_in_css_matches_spark_ms_in_js():
    """--spark-d (style.css) and SPARK_MS (main.js) are the codebase's only
    CSS-to-JS coupling; a comment in each file used to be the whole guard."""
    css = (ROOT / "style.css").read_text()
    js = (ROOT / "main.js").read_text()
    css_s = float(re.search(r"--spark-d:\s*([\d.]+)s", css).group(1))
    js_ms = int(re.search(r"SPARK_MS\s*=\s*(\d+)", js).group(1))
    assert round(css_s * 1000) == js_ms
