#!/bin/sh
# Cloudflare Pages build: publish only the site, not reference/, tests/,
# notes or plan documents. Output directory in Pages settings: dist
set -e
rm -rf dist
mkdir dist
cp index.html style.css theme.js main.js favicon.ico robots.txt sitemap.xml 404.html _headers dist/
cp -R assets dist/assets
# share-card.html is the source the PNGs were exported from, not part of the site
rm -f dist/assets/share/share-card.html
rm -f dist/assets/collage/PLACEHOLDERS.md
