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
