"""Build the notes: python3 tools/notes/build.py

Writes, all committed like hand-written files (no build step at deploy):
  notes/index.html             the ledger, newest first
  notes/<slug>/index.html      one page per note, in ORDER below
  sitemap.xml                  the notes block (both languages, lastmod)
  assets/share/share-card.html the notes block of the card source

Each note is one module next to this file (au.py, noun_verb_stress.py, ...)
that defines NOTE. The masthead, contact section and footer are taken from
english/index.html on every run (lib.py), so change them there, then re-run
this. Share-card PNGs are a separate step: tools/notes/export_cards.py.

To add a note: copy a note module, fill it in, add it to ORDER (newest
first), run this, then export_cards.py, then the tests. The checklist is in SITE-PLAN.md, under H4.
"""
import importlib
import re
import sys

from lib import (ARROW, PERSON, RIGHT_VH, ROOT, SITE, WRONG_VH, article_ld, breadcrumb, hero, label,
                 page, pager)

ORDER = ["weigh", "api_key", "serial", "actual", "feel", "could_you", "au", "noun_verb_stress"]  # newest first
# agree.py ("I am agree") is parked on feature/notes-agree until Igor decides (2026-11-20).


def load():
    notes = [importlib.import_module(m).NOTE for m in ORDER]
    slugs = [n["slug"] for n in notes]
    assert len(set(slugs)) == len(slugs), "two notes share a slug"
    return notes


def build_note(note, nxt, wrapped):
    path = f"/notes/{note['slug']}/"
    card = f"og-note-{note['slug']}"
    kind = ("Newest note", "Самая новая заметка") if wrapped else ("Earlier note", "Предыдущая заметка")
    body = "\n\n".join([hero(note), note["body"](note), pager(nxt, *kind) if nxt else ""])
    page(path=path, comment=note["comment"],
         title_en=note["title"], title_ru=note["title_ru_head"],
         desc_en=note["desc_en"], desc_ru=note["desc_ru"],
         og_title=note["og_title"], og_desc=note["og_desc"], og_image=card, og_alt=note["og_alt"],
         og_type="article",
         jsonld=article_ld(path, note["ld_headline"], note["og_desc"], note["short_en"], note["iso"], card),
         body=body,
         contact_lede_en=note["contact_lede_en"], contact_lede_ru=note["contact_lede_ru"],
         tg_en=note["tg_en"], tg_ru=note["tg_ru"], preload=True)


INDEX_TG_EN = "Hi! I came from your notes. I'd like to book a free trial English lesson."
INDEX_TG_RU = "Здравствуйте! Я с ваших заметок. Хочу записаться на бесплатное занятие по английскому."


LEDGER_TO = '<span class="ledger__to" aria-hidden="true">→</span>'


def ledger_spec(n):
    """The row's lead: the reader's own mistake, then the fix, labelled for
    screen readers the way the specimens are (the arrow is hidden)."""
    wrong, right = n["ledger_spec"].split(LEDGER_TO)
    return (f'{WRONG_VH}<span lang="en">{wrong.strip()}</span> {LEDGER_TO} '
            f'{RIGHT_VH}<span lang="en">{right.strip()}</span>')


def build_index(notes):
    # Mistake first, the note's title under it as the punchline. No date:
    # every note shows its own, and the JSON-LD carries datePublished.
    ledger = "\n".join(f"""    <li class="ledger__item reveal">
      <a class="ledger__link" href="/notes/{n['slug']}/">
        <span class="ledger__meta"><span class="ledger__kind" data-en="{n['kind_en']}" data-ru="{n['kind_ru']}">{n['kind_en']}</span><span class="ledger__count" data-en="{n['count_en']}" data-ru="{n['count_ru']}">{n['count_en']}</span></span>
        <span class="ledger__main">
          <span class="ledger__spec">{ledger_spec(n)}</span>
          <span class="ledger__title" data-en="{n['title_en']}" data-ru="{n['title_ru']}">{n['title_en']}</span>
        </span>
        <span class="ledger__arrow" aria-hidden="true">{ARROW}</span>
      </a>
    </li>""" for n in notes)
    items_ld = ",\n".join(
        f'        {{ "@type": "ListItem", "position": {i + 1}, "url": "{SITE}/notes/{n["slug"]}/", "name": "{n["short_en"]}" }}'
        for i, n in enumerate(notes))
    jsonld = f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "CollectionPage",
      "@id": "{SITE}/notes/#page",
      "url": "{SITE}/notes/",
      "name": "Notes from the lessons — Igor Shatsev",
      "inLanguage": ["en", "ru"],
      "isPartOf": {{ "@id": "{SITE}/#website" }},
      "about": {{ "@id": "{SITE}/english/#service" }},
      "author": {{ "@id": "{SITE}/#igor" }},
      "mainEntity": {{ "@id": "{SITE}/notes/#list" }},
      "breadcrumb": {{ "@id": "{SITE}/notes/#breadcrumb" }}
    }},
    {{
      "@type": "ItemList",
      "@id": "{SITE}/notes/#list",
      "itemListOrder": "https://schema.org/ItemListOrderDescending",
      "itemListElement": [
{items_ld}
      ]
    }},
{breadcrumb("/notes/", [("Igor Shatsev", "/"), ("Notes", "/notes/")])},
{PERSON}
  ]
}}"""
    # true only while every note started as a LinkedIn post
    every_post = all(n.get("from_linkedin") for n in notes)
    origin_en = ' <strong class="mark">Each one starts as a post on LinkedIn.</strong>' if every_post else ""
    origin_ru = ' <strong class="mark">Каждая сначала выходит постом в LinkedIn.</strong>' if every_post else ""
    body = f"""<section class="hero hero--page hero--notes" id="hero">
  <p class="eyebrow reveal">
    <a class="eyebrow__home" href="/" data-en="Igor Shatsev" data-ru="Igor Shatsev">Igor Shatsev</a>
    <span class="sep">/</span>
    <span data-en="Notes" data-ru="Заметки">Notes</span>
    <span class="sep">/</span>
    <span data-en="English" data-ru="Английский">English</span>
  </p>
  <h1 class="hero__title">
    <span data-l="en">
      <span class="line"><span class="line__inner">Notes</span></span>
      <span class="line"><span class="line__inner"><em>from the lessons.</em></span></span>
    </span>
    <span data-l="ru">
      <span class="line"><span class="line__inner">Заметки</span></span>
      <span class="line"><span class="line__inner"><em>с занятий.</em></span></span>
    </span>
  </h1>
  <div class="hero__foot page-hero__foot">
    <div class="page-hero__text">
      <p class="stand reveal" data-l="en">The mistakes I hear from Russian-speaking professionals, taken apart one at a time: what goes wrong, why, and what to say instead.{origin_en}</p>
      <p class="stand reveal" data-l="ru">Ошибки, которые я слышу у русскоязычных специалистов. Каждая разобрана отдельно: в чём ошибка, откуда берётся и как правильно.{origin_ru}</p>
    </div>
  </div>
</section>

<!-- The library is the page: no booking ask above it (the masthead, the
     phone bar and the contact section below carry that) and no second
     heading restating the hero. -->
<section class="sec sec--ledger" id="notes" aria-labelledby="notes-title">
{label("01", "Notes", "Заметки")}
  <h2 class="vh" id="notes-title" data-en="All notes" data-ru="Все заметки">All notes</h2>
  <ol class="ledger" reversed>
{ledger}
  </ol>
  <!-- No "follow me on LinkedIn" line here (removed 2026-11-27): the
       contact section's channels row, right below, says it ("I write about
       English here"). -->
</section>"""
    page(path="/notes/",
         comment="/notes/: the library of mistakes, one real mistake per note. Not a blog.",
         title_en="Notes on English for Russian speakers — Igor Shatsev",
         title_ru="Заметки об английском для русскоязычных — Igor Shatsev",
         desc_en="The English mistakes Russian speakers make, taken apart one at a time: pronunciation, stress, grammar. Why Russian pulls them in and how it should sound. By Igor Shatsev, English coach.",
         desc_ru="Ошибки русскоязычных в английском, разобранные по одной: произношение, ударение, грамматика. Почему так тянет русский и как должно звучать. Igor Shatsev, коуч по английскому.",
         og_title="Notes from the lessons — Igor Shatsev",
         og_desc="The English mistakes Russian speakers make, taken apart one at a time.",
         og_image="og-notes", og_alt="Notes from the lessons. Igor Shatsev, English coach in Yerevan.",
         og_type="website", jsonld=jsonld,
         body=body,
         contact_lede_en="Tell me where your English breaks now: at work, on calls, in conversation. [[The 30-minute trial lesson is free, and you owe me nothing after it]]. If it fits, we agree on a plan, online or in Yerevan.",
         contact_lede_ru="Напишите, где ваш английский ломается сейчас: на работе, на созвонах, в разговоре. [[Пробное занятие — 30 минут, бесплатно и ни к чему не обязывает]]. Если подходит — составляем план, онлайн или в Ереване.",
         tg_en=INDEX_TG_EN, tg_ru=INDEX_TG_RU)


def url_entry(path, lastmod):
    alts = "\n".join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{path}{q}"/>'
                     for h, q in (("en", ""), ("ru", "?lang=ru"), ("x-default", "")))
    return "\n".join(f"""  <url>
    <loc>{SITE}{path}{q}</loc>
    <lastmod>{lastmod}</lastmod>
{alts}
  </url>""" for q in ("", "?lang=ru"))


def build_sitemap(notes):
    p = ROOT / "sitemap.xml"
    xml = p.read_text(encoding="utf-8")
    # drop every notes entry, then write the block again before </urlset>
    xml = re.sub(r"  <url>\s*<loc>https://vitnyrcoach\.com/notes/.*?</url>\n", "", xml, flags=re.S)
    newest = max(n["iso"] for n in notes)
    block = "\n".join([url_entry("/notes/", newest)] + [url_entry(f"/notes/{n['slug']}/", n["iso"]) for n in notes])
    xml = xml.replace("</urlset>", block + "\n</urlset>")
    p.write_text(xml, encoding="utf-8")


def build_cards(notes):
    p = ROOT / "assets" / "share" / "share-card.html"
    html = p.read_text(encoding="utf-8")
    start, end = "<!-- notes:cards (tools/notes/build.py) -->", "<!-- /notes:cards -->"
    block = "\n".join(f"""    <div data-page="note-{n['slug']}">
      <p class="headline" data-l="en">{n['card_en']}</p>
      <p class="headline" data-l="ru">{n['card_ru']}</p>
      <p class="spec">{n['card_spec']}</p>
    </div>""" for n in notes)
    i, j = html.index(start) + len(start), html.index(end)
    p.write_text(html[:i] + "\n" + block + "\n    " + html[j:], encoding="utf-8")


def main():
    notes = load()
    for i, note in enumerate(notes):
        wrapped = i == len(notes) - 1 and len(notes) > 1
        nxt = notes[(i + 1) % len(notes)] if len(notes) > 1 else None
        build_note(note, nxt, wrapped)
    build_index(notes)
    build_sitemap(notes)
    build_cards(notes)
    print("built", len(notes), "notes:", ", ".join(n["slug"] for n in notes))


if __name__ == "__main__":
    sys.exit(main())
