#!/bin/sh
# Cloudflare Pages build: publish only the site, not reference/, tests/,
# notes or plan documents. Output directory in Pages settings: dist
set -e
rm -rf dist
mkdir dist
cp index.html style.css theme.js main.js favicon.ico robots.txt sitemap.xml 404.html _headers dist/
cp -R assets dist/assets
# Discipline pages (DISCIPLINE-PAGES-PLAN.md): each is <folder>/index.html.
# Copied only if present, so the build works at every stage of that plan.
for d in english chess climbing; do if [ -d "$d" ]; then cp -R "$d" dist/; fi; done
# share-card.html is the source the PNGs were exported from, not part of the site
rm -f dist/assets/share/share-card.html
rm -f dist/assets/collage/PLACEHOLDERS.md

# SITE-PLAN G2 (2026-11-20): ship the CSS and JS without their comments.
# About 59% of style.css and half of main.js is commentary: worth everything
# in the repo, worth nothing to a visitor's phone. Only the dist/ copies are
# minified; the source files keep every comment. esbuild is pinned. If the
# minifier can't run (no network for npx, say), the deploy still ships, just
# unminified. Locally: ESBUILD=/path/to/esbuild sh build.sh
minify() {
  if [ -n "$ESBUILD" ]; then "$ESBUILD" "$@"; else npx --yes esbuild@0.24.0 "$@"; fi
}
for f in style.css main.js theme.js; do
  minify "dist/$f" --minify --allow-overwrite --outfile="dist/$f" --log-level=warning \
    || echo "build.sh: minifying $f failed; shipping it unminified"
done
