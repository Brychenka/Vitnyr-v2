"""/notes/api-key/: two of Igor's LinkedIn posts in one note, because one
phrase carries both mistakes: "key" (30 October 2026: key said as [кей],
the name of the letter K) and "abbreviations" (25 November 2026: CEO, API,
MR, PR read as words; spell them). Read from LinkedIn on 2026-11-28
(reference/linkedin-posts/). The Russian is his posts, lightly cleaned
(ты → вы); the English is a translation, a DRAFT for Igor. What was written
for the note is marked DRAFT below (SITE-PLAN.md NQ15).

Planned before building (reference/linkedin-posts/REVIEW.md): the hero is
the abbreviations slide's A·P·I as the au note's tiles, written over said;
the table is the posts' eight words; "why" gives the cause the posts leave
out (the school names of Latin letters); practice is "Say it out loud", as
on the other pronunciation notes.
"""
from lib import both, head2, ipa, practice, pull, register, section, strong, tile

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'

# The posts' own words: the abbreviations post's four, the key post's four.
# The Russian spellings of the sounds are Igor's (си и оу, эй пи ай, эм ар,
# ки); the rest follow them.
WORDS = [
    ("CEO", "си-и-оу", "/ˌsiː iː ˈəʊ/"),
    ("API", "эй-пи-ай", "/ˌeɪ piː ˈaɪ/"),
    ("MR", "эм-ар", "/ˌem ˈɑː/"),
    ("PR", "пи-ар", "/ˌpiː ˈɑː/"),
    ("key", "ки", "/kiː/"),
    ("hotkey", "хот-ки", "/ˈhɒtkiː/"),
    ("keyboard", "ки-борд", "/ˈkiːbɔːd/"),
    ("keynote", "ки-ноут", "/ˈkiːnəʊt/"),
]

# DRAFT for Igor: the cause is the note's, not the posts'. Russian speakers
# meet Latin letters in maths and physics (а плюс бэ), named the Latin way.
# English class teaches эй, би, си, but the maths names are the habit.
# Cold review: the first build said "in school" (English class does teach
# эй, би, си) and blamed кей on the letter's name; it is the spelling.
LETTERS = [
    ("а", "A", "/eɪ/", "эй"),
    ("е", "E", "/iː/", "и"),
    ("и", "I", "/aɪ/", "ай"),
    ("эр", "R", "/ɑː/", "ар"),
]

# DRAFT for Igor (SITE-PLAN.md NQ15): not from the posts.
PRACTICE = [
    "Can you send me the <b>API</b> <b>key</b>?",
    "Our <b>CEO</b> wants a demo on Friday.",
    "I left two comments on your <b>PR</b>.",
    "The <b>MR</b> is ready for review.",
    "There’s a <b>hotkey</b> for that.",
    "Who’s giving the <b>keynote</b>?",
]

FIGURE = f"""    <figure class="note-fig tiles reveal" aria-labelledby="fig-api-key">
      <div class="tiles__row" aria-hidden="true">{tile('A')}{tile('P')}{tile('I')}{tile('key', ' tile--merged')}</div>
      <div class="tiles__row" aria-hidden="true">{tile('эй', ' tile--target')}{tile('пи', ' tile--target')}{tile('ай', ' tile--target')}{tile('ки', ' tile--target tile--merged')}</div>
      <figcaption id="fig-api-key"><span data-l="en">{strong("Fig. 1. Spell the three letters; say key as one word.")} Say {I("эй-пи-ай ки")}, not {D("апи кей")}.</span><span data-l="ru">{strong("Рис. 1. Три буквы — по буквам, одно слово — целиком.")} Говорите {I("эй-пи-ай ки")}, а не {D("апи кей")}.</span></figcaption>
    </figure>"""


def body(note):
    words = section("words", "\n".join([
        head2("Spell the letters. Say the word.", "Буквы — по буквам. Слово — целиком.",
              "A short abbreviation is read letter by letter, with the English names of the letters. [[{{key}} is a word, and it sounds like {{ки}}.]]",
              "Короткую аббревиатуру читают по буквам, английскими названиями букв. [[{{key}} — это слово, и звучит оно как {{ки}}.]]"),
        register("Eight words from work, and how each one sounds", "Восемь рабочих слов и как каждое звучит",
                 [("Written", "Пишется"), ("Say", "Звучит")],
                 [[word, ("register__w", say)] for word, say, tr in WORDS], cls=" register--pairs"),
        # DRAFT for Igor: the posts' rule is "2-3 letters: spell it"; this keeps it honest.
        '  <p class="note-cite reveal"><span data-l="en">The rule isn’t strict: a few short ones are read as words, '
        'like RAM and PIN. If you’re not sure, spell it.</span><span data-l="ru">Правило не железное: некоторые '
        'короткие аббревиатуры читают словом, например RAM и PIN. Не уверены — читайте по буквам.</span></p>',
    ]))
    why = section("why", "\n".join([
        # DRAFT for Igor: the cause; the posts give the effect.
        head2("The letters from maths class.", "Буквы с уроков математики.",
              "Russian speakers learn Latin letters in school maths and physics, with Latin names: {{а}} plus {{бэ}}. Those names come back in English, so {{API}} turns into {{а-пэ-и}}, or into one word, {{апи}}. {{key}} goes wrong another way: it is read like {{hey}}. But {{кей}} [[is the English name of the letter K]], so that is what a native speaker hears.",
              "Латинские буквы мы знаем со школы, по математике и физике, и называем на латинский манер: {{а}} плюс {{бэ}}. Эти названия переходят в английский, и {{API}} превращается в {{а-пэ-и}} или в одно слово, {{апи}}. С {{key}} другая история: его читают как {{hey}}. Но {{кей}} — [[это английское название буквы K]], и носитель слышит именно её."),
        pull([(ru, en, f"{ipa(tr)} {say}") for ru, en, tr, say in LETTERS]),
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "Abbreviations go letter by letter, with the stress on the last letter: эй-пи-{{АЙ}}. Every {{key}} is {{ки}}, in hotkey and keynote too.",
              "Аббревиатуры — по буквам, с ударением на последнюю букву: эй-пи-{{АЙ}}. Любой {{key}} — это {{ки}}, и в hotkey, и в keynote."),
        practice(PRACTICE, "DRAFT for Igor (SITE-PLAN.md NQ15): these six sentences are not from the LinkedIn posts."),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="api-key",
    iso="2026-11-25",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="25 November 2026", date_long_ru="25 ноября 2026",
    # the newer of the two posts (abbreviations); the key post is
    # https://www.linkedin.com/feed/update/urn:li:activity:7521873815056969728/
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7531299698327023617/",
    from_linkedin=True,
    kind_en="Pronunciation", kind_ru="Произношение",
    count_en="API key · 8 words", count_ru="API key · 8 слов",
    title_en="Three letters and a key.", title_ru="Эй-пи-ай, а не апи.",
    short_en="Three letters and a key", short_ru="Эй-пи-ай, а не апи",
    ledger_spec=f'{D("апи кей")} <span class="ledger__to" aria-hidden="true">→</span> {I("эй-пи-ай ки")}',
    card_en="Three letters <em>and a key.</em>", card_ru="Эй-пи-ай, <em>а не апи.</em>",
    card_spec='<span class="x">апи кей</span><span class="to">→</span><span class="ok">эй-пи-ай ки</span>',
    h1_en=["Three letters", "and a key."], h1_ru=["Эй-пи-ай,", "а не апи."],
    # The posts' observations, cleaned, then the answer. The English is a DRAFT.
    stand_en="Many programmers say “апи кей”: two words, two mistakes. The abbreviation is read as a word, and key as [кей], which a native speaker hears as the letter K. [[API is spelled out, эй-пи-ай, and key is ки.]]",
    stand_ru="Многие программисты по привычке говорят «апи кей»: два слова — две ошибки. Аббревиатуру читают как слово, а key — как [кей], и носитель слышит букву K. [[API читается по буквам, эй-пи-ай, а key — ки.]]",
    figure=FIGURE,
    comment="/notes/api-key/: two of Igor's LinkedIn posts (key, abbreviations) set as one note. The Russian is his posts, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="How to pronounce API key, CEO, PR — Igor Shatsev",
    title_ru_head="Как произносить API, key, CEO по-английски — Igor Shatsev",
    desc_en="API is not апи and key is not кей. How to say API key, CEO, PR, MR, hotkey and keynote in English, why Russian speakers get them wrong, and six sentences to say out loud.",
    desc_ru="API — не «апи», key — не «кей». Как произносить API key, CEO, PR, MR, hotkey и keynote по-английски, откуда ошибка и шесть фраз, чтобы потренироваться.",
    og_title="Three letters and a key: how to say API key — Igor Shatsev",
    og_desc="API is spelled out, эй-пи-ай; key is ки, not кей. Eight words from work and how they sound.",
    og_alt="Three letters and a key. A note by Igor Shatsev on saying API key.",
    ld_headline="Three letters and a key: how to say API key",
    contact_lede_en="If you work in IT, you say these words on calls every week. Say a few of them to me in the trial lesson, and you’ll know how they sound. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Если вы в IT, эти слова звучат у вас на созвонах каждую неделю. Скажите мне несколько на пробном занятии — и узнаете, как они звучат. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “API key”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «API key». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
