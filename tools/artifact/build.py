"""Build the live claude.ai artifact ("Vitnyr Signature") from the repo.

    python3 tools/artifact/build.py <repo> <out-dir>

Reads the COMMITTED files (git show HEAD:...), never the working tree, so a
parallel chat's WIP can't ship. Writes a flat bundle the artifact host can
serve: index.html (home, skeleton tags stripped, since the host wraps the page
itself), english.html / chess.html / climbing.html (full documents, served as
they are), style.css, theme.js, main.js and assets/ (share cards left out).

The site links from the domain root (/chess/, /style.css), which on
claude.ai would point at claude.ai itself, so every root-absolute link is
rewritten relative: /chess/ -> chess.html, / -> index.html, /assets/ ->
assets/. Publish index.html as the page and everything else through `files`
(2026-11-20, the first multi-file publish).
"""
import os
import re
import shutil
import subprocess
import sys

PAGES = ['english', 'chess', 'climbing']

repo, out = sys.argv[1], sys.argv[2]


def show(path):
    return subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + path],
                          capture_output=True, check=True).stdout.decode('utf-8')


def relink(s):
    s = re.sub(r'(href|src)="/?(style\.css|theme\.js|main\.js)\?v=[^"]*"', r'\1="\2"', s)
    for d in PAGES:
        s = s.replace(f'href="/{d}/#', f'href="{d}.html#').replace(f'href="/{d}/"', f'href="{d}.html"')
    s = s.replace('href="/"', 'href="index.html"').replace('href="/#', 'href="index.html#')
    s = s.replace('="/assets/', '="assets/').replace(', /assets/', ', assets/')
    # the host supplies its own favicon
    s = re.sub(r'<link rel="(icon|apple-touch-icon)"[^>]*>\n?', '', s)
    # home's old-hash redirect (#chess -> /chess/)
    s = s.replace("location.replace('/' + page + '/' + location.search + hash)",
                  "location.replace(page + '.html' + location.search + hash)")
    return s


shutil.rmtree(out, ignore_errors=True)
os.makedirs(out)
for f in ['style.css', 'theme.js', 'main.js']:
    open(os.path.join(out, f), 'w', encoding='utf-8').write(show(f))

home = relink(show('index.html'))
for tag in [r'<!doctype html>\n?', r'<html[^>]*>\n?', r'</?head>\n?', r'<body[^>]*>\n?', r'</body>\n?', r'</html>\n?']:
    home = re.sub(tag, '', home, flags=re.I)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(home)
for d in PAGES:
    open(os.path.join(out, d + '.html'), 'w', encoding='utf-8').write(relink(show(d + '/index.html')))

for root, _, files in os.walk(os.path.join(repo, 'assets')):
    for fn in files:
        src = os.path.join(root, fn)
        rel = os.path.relpath(src, repo)
        if rel.startswith('assets/share') or fn.startswith('.'):
            continue
        os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True)
        shutil.copy(src, os.path.join(out, rel))

for f in ['index.html'] + [d + '.html' for d in PAGES]:
    s = open(os.path.join(out, f), encoding='utf-8').read()
    left = sorted(set(re.findall(r'(?:href|src|srcset|data-src)="(/[^"#]{0,40})', s)))
    print(f, len(s), 'root-absolute left:', left or 'none')
