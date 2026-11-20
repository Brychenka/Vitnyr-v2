#!/bin/sh
# Cloudflare Pages build: publish only the site, not reference/, tests/,
# notes or plan documents. Output directory in Pages settings: dist
set -e
rm -rf dist
mkdir dist
cp index.html style.css theme.js main.js favicon.ico robots.txt sitemap.xml 404.html _headers dist/
cp -R assets dist/assets
# the three discipline pages and the notes, each <folder>/index.html
for d in english chess climbing notes; do cp -R "$d" dist/; done
# share-card.html is the source the PNGs were exported from, not part of the site
rm -f dist/assets/share/share-card.html

# Ship the CSS and JS minified (only the dist/ copies; the sources keep their
# comments). esbuild is pinned. If the minifier can't run (no network for
# npx, say), the deploy still ships, just unminified.
# Locally: ESBUILD=/path/to/esbuild sh build.sh
minify() {
  if [ -n "$ESBUILD" ]; then "$ESBUILD" "$@"; else npx --yes esbuild@0.24.0 "$@"; fi
}
for f in style.css main.js theme.js; do
  minify "dist/$f" --minify --allow-overwrite --outfile="dist/$f" --log-level=warning \
    || echo "build.sh: minifying $f failed; shipping it unminified"
done
