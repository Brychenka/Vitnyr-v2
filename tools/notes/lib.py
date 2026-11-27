"""Shared parts for the notes generator (tools/notes/build.py).

The masthead, contact section, footer, dock and scripts are not written here:
they are cut out of english/index.html every time the generator runs, so a
note can never fall behind the shared frame. Only
what a note owns is written here: its head, hero, sections and Telegram
prefills.
"""
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://vitnyrcoach.com"
LINKEDIN = "https://www.linkedin.com/in/vitnyrcoach/"
# PLACEHOLDER until Igor sends each post's own URL (SITE-PLAN.md NQ5)
LINKEDIN_ACTIVITY = "https://www.linkedin.com/in/vitnyrcoach/recent-activity/all/"

SRC = (ROOT / "english" / "index.html").read_text(encoding="utf-8")


def between(text, start, end, include_end=True):
    i = text.index(start)
    j = text.index(end, i)
    return text[i: j + (len(end) if include_end else 0)]


# ---------------------------------------------------------------- the frame
MAST = between(SRC, '<a class="skip"', "</header>")
CONTACT = between(SRC, '<section class="sec sec--contact" id="contact">', "</section>")
TAIL = SRC[SRC.index("</main>"):]
# favicons and the stylesheet, with the English page's own cache key
HEAD_SHARED = between(SRC, '<link rel="icon" href="/favicon.ico"', '<script src="/theme.js', include_end=False)
THEME_TAG = re.search(r'<script src="/theme\.js\?v=[^"]+"></script>', SRC).group(0)

# the English page's default prefills, swapped for each note's own
EN_TG = re.search(r'class="contact__cta"[^>]*?data-href-en="([^"]+)"', SRC, re.S).group(1)
RU_TG = re.search(r'class="contact__cta"[^>]*?data-href-ru="([^"]+)"', SRC, re.S).group(1)

# no discipline is "current" on a notes page; the Notes link is
assert MAST.count(' aria-current="page"') == 1, "english/index.html: expected one aria-current"
MAST = MAST.replace(' aria-current="page"', "")
assert 'class="tool tools__notes" href="/notes/"' in MAST, "masthead has no Notes link"
MAST = MAST.replace('class="tool tools__notes" href="/notes/"', 'class="tool tools__notes" href="/notes/" aria-current="page"')

# Inter, fetched with the HTML instead of after the CSS, on the note pages
# only: a late swap rewrapped the standfirst (now holding mono words) and
# moved everything under it, CLS up to 0.14 on a slow phone. JetBrains
# Mono needs no preload (its Courier New stand-in has the same advance).
# Not on the index: it never jumped, and the hero waits for every font
# (main.js, up to 1.5s), so a preload there only delayed its first text.
PRELOAD = "\n".join(
    f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>'
    for f in ("inter-latin-v20", "inter-cyrillic-v20"))

ARROW = '<svg aria-hidden="true" viewBox="0 0 26 8"><path d="M0 4h23M19 1l4 3-4 3" fill="none" stroke="currentColor" stroke-width="1"/></svg>'
WRONG_SIG = '<span class="sig" aria-hidden="true"><svg viewBox="0 0 10 10" aria-hidden="true"><path d="M7.6 2.6 C7.6 1.4 5.9 1 4.7 1.9 C3.2 3 3.2 5.6 4.7 6.7 C5.7 7.4 7 7.2 7.7 6.3 M2.2 8.4 L8.6 1.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
RIGHT_SIG = '<span class="sig" aria-hidden="true"><svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1.7 7.9 L5 3.5 L8.3 7.9 M5 3.7 L5 6.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
WRONG_VH = '<span class="vh" data-en="Incorrect: " data-ru="Неверно: ">Incorrect: </span>'
RIGHT_VH = '<span class="vh" data-en="Correct: " data-ru="Верно: ">Correct: </span>'
ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]


def tg(text):
    return "https://t.me/vitnyr?text=" + quote(text, safe="")


def w(s):
    """A word, letter or sound under examination inside prose, in the
    specimens' mono and without quotation marks (the same convention as
    .spec__why em on /english/). Whole quoted sentences keep their quotes."""
    return f'<span class="w">{s}</span>'


def ipa(s):
    """A transcription such as /lɔːntʃ/, set whole in one face that has
    every IPA glyph (--ipa): none of the site's own font files carry them,
    so letting the browser fall back glyph by glyph mixed two faces inside
    one word (and put the au tile's ɔː in Times)."""
    return f'<span class="ipa">{s}</span>'


def strong(t):
    """[[...]] marks the one sentence a lede stresses (.mark, as on the
    other pages); {{...}} marks a word under examination (w())."""
    if not t:
        return t
    t = re.sub(r"\{\{(.+?)\}\}", lambda m: w(m.group(1)), t)
    return t.replace("[[", '<strong class="mark">').replace("]]", "</strong>")


def must_sub(pattern, repl, text, flags=0):
    """re.sub that fails the build when the English page no longer has what
    it cuts, instead of quietly shipping the full section."""
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"notes build: english/index.html has no {pattern!r}; update note_contact()")
    return out


def note_contact(html):
    """The English page's contact section, cut down to a reading page's
    ending (2026-11-27): unnumbered (it is not a chapter of the note), no
    empty-chair engraving, and .sec--contact-note, which sets the CTA at the
    section-heading size and the channels as one row. The CTA, its Telegram
    prefill, the portrait and the channels stay the English page's own, so
    a handle changed there changes here."""
    html = must_sub(r'<section class="sec sec--contact" id="contact">',
                    '<section class="sec sec--contact sec--contact-note" id="contact">', html)
    html = must_sub(r'<span class="num">\d+</span>', "", html)
    html = must_sub(r'\s*<figure class="vig vig--empty-chair.*?</figure>', "", html, re.S)
    return html


def page(*, path, comment, title_en, title_ru, desc_en, desc_ru, og_title, og_desc, og_image, og_alt,
         og_type, jsonld, body, contact_lede_en, contact_lede_ru, tg_en, tg_ru, preload=False):
    """Write <path>/index.html: the note's own head and body inside the
    English page's frame. Returns the HTML."""
    url = SITE + path
    contact = note_contact(CONTACT)
    # the note's own lede replaces the English one; no smaller first step on
    # a note (Igor, 2026-11-20: no voice-message step on the notes)
    lede_old = between(contact, '<div class="sec__lede">', "</div>")
    contact = contact.replace(lede_old, (
        '<div class="sec__lede">\n'
        f'    <p class="reveal" data-l="en">{strong(contact_lede_en)}</p>\n'
        f'    <p class="reveal" data-l="ru">{strong(contact_lede_ru)}</p>\n'
        '  </div>'))
    tail = TAIL
    for old, new in ((EN_TG, tg(tg_en)), (RU_TG, tg(tg_ru))):
        contact = contact.replace(old, new)
        tail = tail.replace(old, new)
    head = f"""<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- {comment}
     GENERATED by tools/notes/build.py from tools/notes/*.py and the frame of
     english/index.html. Edit those and re-run; edits here are overwritten. -->
<title data-head-ru="{title_ru}">{title_en}</title>
<meta name="description" content="{desc_en}" data-head-ru="{desc_ru}">
<meta name="theme-color" content="#EFEBE3">

<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="ru_RU">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Vitnyr">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/share/{og_image}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="{SITE}/assets/share/{og_image}.png">

<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="ru" href="{url}?lang=ru">
<link rel="alternate" hreflang="x-default" href="{url}">

<script type="application/ld+json">
{jsonld.strip()}
</script>

{PRELOAD + chr(10) if preload else ""}{HEAD_SHARED}{THEME_TAG}
</head>
<body>

"""
    html = (head + MAST + '\n\n<div id="app">\n<main id="main">\n<span id="top"></span>\n\n'
            + body.strip() + "\n\n" + contact + "\n\n" + tail)
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return html


# ------------------------------------------------------------- structured data
def breadcrumb(path, items):
    els = ",\n".join(
        f'        {{ "@type": "ListItem", "position": {i + 1}, "name": "{n}", "item": "{SITE}{p}" }}'
        for i, (n, p) in enumerate(items))
    return f"""    {{
      "@type": "BreadcrumbList",
      "@id": "{SITE}{path}#breadcrumb",
      "itemListElement": [
{els}
      ]
    }}"""


PERSON = f"""    {{
      "@type": "Person",
      "@id": "{SITE}/#igor",
      "name": "Igor Shatsev",
      "url": "{SITE}/",
      "sameAs": ["{LINKEDIN}"]
    }}"""


def article_ld(path, headline, desc, crumb, iso, card):
    return f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "@id": "{SITE}{path}#article",
      "url": "{SITE}{path}",
      "mainEntityOfPage": "{SITE}{path}",
      "headline": "{headline}",
      "description": "{desc}",
      "inLanguage": ["en", "ru"],
      "datePublished": "{iso}",
      "author": {{ "@id": "{SITE}/#igor" }},
      "publisher": {{ "@id": "{SITE}/#igor" }},
      "isPartOf": {{ "@id": "{SITE}/notes/#page" }},
      "about": {{ "@id": "{SITE}/english/#service" }},
      "image": "{SITE}/assets/share/{card}.png",
      "breadcrumb": {{ "@id": "{SITE}{path}#breadcrumb" }}
    }},
{breadcrumb(path, [("Igor Shatsev", "/"), ("Notes", "/notes/"), (crumb, path)])},
{PERSON}
  ]
}}"""


# -------------------------------------------------------------- page pieces
def byline():
    """Who wrote this, in the confirmed facts only (CLAUDE.md)."""
    return """      <p class="note-byline reveal">
        <span data-en="Igor Shatsev, English coach" data-ru="Igor Shatsev, коуч по английскому">Igor Shatsev, English coach</span>
        <span class="sep" aria-hidden="true">·</span>
        <span>C2 · IELTS 9</span>
        <span class="sep" aria-hidden="true">·</span>
        <span data-en="10 years" data-ru="10 лет">10 years</span>
        <span class="sep" aria-hidden="true">·</span>
        <span data-en="100+ one-on-one clients" data-ru="100+ учеников на индивидуальных занятиях">100+ one-on-one clients</span>
      </p>"""


def source_line(note):
    """Where the note first appeared, and when. A note written for the site
    (no LinkedIn post behind it) shows only the date."""
    date = f'<time datetime="{note["iso"]}" data-en="{note["date_long_en"]}" data-ru="{note["date_long_ru"]}">{note["date_long_en"]}</time>'
    if not note.get("from_linkedin"):
        return f'      <p class="note-source reveal">{date}</p>'
    href = note.get("linkedin") or LINKEDIN_ACTIVITY
    return f"""      <p class="note-source reveal">
        <a class="note-source__link" href="{href}" target="_blank" rel="noopener" data-magnetic><span data-en="First posted on LinkedIn" data-ru="Впервые — в LinkedIn">First posted on LinkedIn</span><span class="vh" data-en=" (opens LinkedIn)" data-ru=" (откроется LinkedIn)"> (opens LinkedIn)</span></a>
        <span class="sep" aria-hidden="true">·</span>
        {date}
      </p>"""


def pager(nxt, kind_en, kind_ru):
    """'All notes', and the next note down the ledger (the oldest wraps to
    the newest)."""
    return f"""<nav class="note-pager" aria-labelledby="pager-title">
  <h2 class="vh" id="pager-title" data-en="More notes" data-ru="Ещё заметки">More notes</h2>
  <a class="note-pager__all" href="/notes/" data-magnetic><svg aria-hidden="true" viewBox="0 0 26 8"><path d="M26 4H3M7 1L3 4l4 3" fill="none" stroke="currentColor" stroke-width="1"/></svg><span data-en="All notes" data-ru="Все заметки">All notes</span></a>
  <a class="note-pager__next" href="/notes/{nxt['slug']}/" data-magnetic>
    <span class="note-pager__k" data-en="{kind_en}" data-ru="{kind_ru}">{kind_en}</span>
    <span class="note-pager__t"><span data-en="{nxt['short_en']}" data-ru="{nxt['short_ru']}">{nxt['short_en']}</span>{ARROW}</span>
  </a>
</nav>"""


def hero_lines(ls):
    out = []
    for i, l in enumerate(ls):
        inner = f"<em>{l}</em>" if i == len(ls) - 1 else l
        out.append(f'      <span class="line"><span class="line__inner">{inner}</span></span>')
    return "\n".join(out)


def hero(note):
    return f"""<section class="hero hero--page hero--note" id="hero">
  <p class="eyebrow reveal">
    <a class="eyebrow__home" href="/" data-en="Igor Shatsev" data-ru="Igor Shatsev">Igor Shatsev</a>
    <span class="sep">/</span>
    <a class="eyebrow__home" href="/notes/" data-en="Notes" data-ru="Заметки">Notes</a>
    <span class="sep">/</span>
    <span data-en="{note['kind_en']}" data-ru="{note['kind_ru']}">{note['kind_en']}</span>
  </p>
  <h1 class="hero__title">
    <span data-l="en">
{hero_lines(note['h1_en'])}
    </span>
    <span data-l="ru">
{hero_lines(note['h1_ru'])}
    </span>
  </h1>
  <div class="hero__foot page-hero__foot">
    <div class="page-hero__text">
      <p class="stand reveal" data-l="en">{strong(note['stand_en'])}</p>
      <p class="stand reveal" data-l="ru">{strong(note['stand_ru'])}</p>
    </div>
{note['figure']}
    <div class="note-meta">
{byline()}
{source_line(note)}
    </div>
  </div>
</section>"""


def label(num, en, ru):
    return f'  <p class="label reveal"><span class="num">{num}</span><span data-en="{en}" data-ru="{ru}">{en}</span></p>'


def head2(en, ru, lede_en=None, lede_ru=None):
    lede = ""
    if lede_en:
        lede = f"""
    <div class="sec__lede">
      <p class="reveal" data-l="en">{strong(lede_en)}</p>
      <p class="reveal" data-l="ru">{strong(lede_ru)}</p>
    </div>"""
    return f"""  <div class="sec__head">
    <h2 class="reveal" data-l="en">{en}</h2>
    <h2 class="reveal" data-l="ru">{ru}</h2>{lede}
  </div>"""


# Every note has the same three parts, so the labels are wayfinding, the same
# on every note, and the heading under each carries the note's own claim
# (the main pages do the same: "Mistakes I fix" over "Your mistakes have
# deep roots."). A label never repeats its heading.
PARTS = {
    "words": ("01", "The fix", "Как правильно"),
    "why": ("02", "Why it happens", "Почему так"),
    "practice": ("03", "Practice", "Практика"),
}


def section(sec_id, inner, cls=""):
    num, en, ru = PARTS[sec_id]
    return f"""<section class="sec{cls}" id="{sec_id}">
{label(num, en, ru)}
{inner}
</section>"""


def ear_test(items, msg_en, msg_ru, href):
    """The English page's "Test yourself" (initEarTest in main.js), as a
    note's practice: the reader taps the sentences that sound right, then
    checks. items: (html, right, habit_en, habit_ru, fix_html); a wrong
    sentence marks its culprit with .ear__cut and has a fix. The section
    carries .sec--ear, which hides it without JS. msg_*: the Telegram
    message after the check, {n} and {t} the score; href: before it."""
    rows = []
    for html, right, h_en, h_ru, fix in items:
        habit = "" if right else f' data-habit-en="{h_en}" data-habit-ru="{h_ru}"'
        fix_p = ("" if right else
                 f'\n        <p class="ear__fix" hidden><span class="vh" data-en="Natural: " data-ru="Естественно: ">Natural: </span>{fix}</p>')
        rows.append(f"""      <li class="ear__item" data-right="{'true' if right else 'false'}"{habit}>
        <button type="button" class="ear__pick" aria-pressed="false"><span class="ear__box" aria-hidden="true"></span><span class="ear__s" lang="en">{html}</span></button>
        <span class="ear__verdict" hidden></span>{fix_p}
      </li>""")
    rows = "\n".join(rows)
    return f"""  <div class="ear reveal" data-msg-en="{msg_en}" data-msg-ru="{msg_ru}">
    <ol class="ear__list">
{rows}
    </ol>
    <div class="ear__actions">
      <button type="button" class="ear__check page-cta" data-magnetic><span data-en="Check my answers" data-ru="Проверить">Check my answers</span></button>
      <button type="button" class="ear__again tool" hidden data-magnetic><span data-en="Try again" data-ru="Ещё раз">Try again</span></button>
    </div>
    <div class="ear__result" hidden>
      <p class="ear__score" aria-live="polite"></p>
      <p class="ear__habit"></p>
      <a class="lede__link ear__send" href="{href}" target="_blank" rel="noopener" data-magnetic><span data-en="Send me your score" data-ru="Отправить мне результат">Send me your score</span></a>
    </div>
  </div>"""


def spec_pair(wrong, right):
    return f"""  <div class="note-spec reveal">
    <p class="line-spec wrong">{WRONG_VH}{WRONG_SIG}<span>{wrong}</span></p>
    <p class="line-spec right">{RIGHT_VH}{RIGHT_SIG}<span>{right}</span></p>
  </div>"""


def practice_list(items):
    rows = "\n".join(f'      <li><span class="practice__n" aria-hidden="true">{ROMAN[i]}.</span><span class="practice__s" lang="en">{s}</span></li>'
                     for i, s in enumerate(items))
    return f'    <ol class="practice">\n{rows}\n    </ol>'


def practice(items, draft_note=None):
    c = f"  <!-- {draft_note} -->\n" if draft_note else ""
    return f"""{c}  <div class="practice-wrap reveal">
{practice_list(items)}
  </div>"""


def practice_pair(left, right):
    """left/right: (title_en, title_ru, rule_en, rule_ru, items)"""
    def col(t_en, t_ru, r_en, r_ru, items):
        return f"""    <div class="practice-wrap reveal">
      <h3 class="practice__h"><span data-l="en">{t_en}</span><span data-l="ru">{t_ru}</span> <span class="practice__rule" data-en="{r_en}" data-ru="{r_ru}">{r_en}</span></h3>
{practice_list(items)}
    </div>"""
    return f'  <div class="practice-pair">\n{col(*left)}\n{col(*right)}\n  </div>'


def register(caption_en, caption_ru, heads, rows, cls=""):
    """heads: [(en, ru), ...] for the columns after the number; rows: lists
    of cell HTML, the first cell a row header."""
    th = "".join(f'<th scope="col" data-en="{en}" data-ru="{ru}">{en}</th>' for en, ru in heads)
    body = "\n".join(
        f'      <tr><td class="register__n">{i + 1:02d}</td>'
        f'<th scope="row" class="register__w">{r[0]}</th>'
        + "".join(f'<td class="{c}">{v}</td>' for c, v in r[1:]) + "</tr>"
        for i, r in enumerate(rows))
    return f"""  <table class="register{cls} reveal">
    <caption class="vh"><span data-l="en">{caption_en}</span><span data-l="ru">{caption_ru}</span></caption>
    <thead><tr><th scope="col"><span class="vh" data-en="Number" data-ru="Номер">Number</span></th>{th}</tr></thead>
    <tbody>
{body}
    </tbody>
  </table>"""


def pull(rows):
    """The Russian look-alikes: (ru_html, en_html, aside_html)."""
    items = "\n".join(
        f'    <li class="pull__row reveal"><span class="pull__from"><span class="pull__ru" lang="ru">{ru}</span>'
        f'<span class="pull__arrow" aria-hidden="true">{ARROW}</span></span>'
        f'<span class="pull__to"><span class="pull__en" lang="en">{en}</span><span class="pull__ipa">{aside}</span></span></li>'
        for ru, en, aside in rows)
    return f'  <ul class="pull">\n{items}\n  </ul>'


def hit(word, letters):
    i = word.index(letters)
    return f'{word[:i]}<span class="hit">{letters}</span>{word[i + len(letters):]}'


def tile(ch, mod="", ch_cls=""):
    return f'<span class="tile{mod}"><span class="tile__ch{ch_cls}">{ch}</span></span>'


def ladder(rows, caption_en, caption_ru, fig_id):
    """A sentence-level hero figure for the grammar notes: one sentence per
    row, from the Russian through the habit to the English, the culprit and
    the fix in the same inks as .note-spec. rows: (html, lang, role_en, role_ru)."""
    out = "\n".join(
        f'      <div class="ladder__row"><span class="ladder__s" lang="{lang}">{html}</span>'
        f'<span class="weights__role" data-en="{ren}" data-ru="{rru}">{ren}</span></div>'
        for html, lang, ren, rru in rows)
    return f"""    <figure class="note-fig ladder reveal" aria-labelledby="{fig_id}">
{out}
      <figcaption id="{fig_id}"><span data-l="en">{strong(caption_en)}</span><span data-l="ru">{strong(caption_ru)}</span></figcaption>
    </figure>"""


def both(en, ru):
    """A short string in both languages (theme.js swaps it)."""
    return f'<span data-en="{en}" data-ru="{ru}">{en}</span>'
