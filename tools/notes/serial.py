"""/notes/serial/: Igor's LinkedIn post and slide "I love watching serials"
(23 November 2026, read from LinkedIn on 2026-11-28; reference/linkedin-posts/).
The Russian is his post, lightly cleaned (ты → вы, as on the rest of the
site); the English is a translation, a DRAFT for Igor. What was written for
the note is marked DRAFT below (SITE-PLAN.md NQ14).

Rebuilt after a cold review the same day: the standfirst no longer retells
the joke the figure tells; the table doesn't repeat the figure's fix; "why"
shows the sound (serial and cereal share one transcription) instead of
repeating the table.

Planned before building (reference/linkedin-posts/REVIEW.md): the hook is
the post's joke, set as type in the hero (what you mean, what you say, what
a native hears, what to say); the table is the cheat sheet; "why" carries
what the hero doesn't (the shared sound, and why серия is not series); the
practice is the same test as the actual note.
"""
from lib import both, ear_test, head2, hit, ipa, ladder, pull, register, section, tg

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'
RU = lambda s: f'<span lang="ru">{s}</span>'
CUT = lambda w: f'<span class="ear__cut">{w}</span>'

PHRASES = [
    # DRAFT for Igor: the post says "TV series or TV show"; the phrases are the note's.
    (RU(f"Мой любимый {hit('сериал', 'сериал')}"), f"my favourite {I('show')}"),
    (RU(f"Новый {hit('сериал', 'сериал')} на Netflix"), f"a new {I('series')} on Netflix"),
    (RU(f"Первая {hit('серия', 'серия')}"), f"the first {I('episode')}"),
    # DRAFT for Igor: not in the post; the word people need next.
    (RU(f"Второй {hit('сезон', 'сезон')}"), f"the second {I('season')}"),
    (RU(f"Два {hit('сериала', 'сериала')}"), f"two {I('series')}"),
    (RU(f"{hit('Серийный', 'Серийный')} номер, {hit('серийный', 'серийный')} убийца"), f"a {I('serial')} number, a {I('serial')} killer"),
]

# Which would a native speaker say? Five wrong, three right. The post's own:
# watching serials, серия → episode, one series / two series, serial number.
# The sentences around them are DRAFT. None uses series for a season, which
# British English does ("series two"), so every wrong line is wrong in both.
TEST = [
    (f"I love watching {CUT('serials')}.", False, "«смотреть сериалы»", "«смотреть сериалы»",
     f"I love watching TV {I('shows')}."),
    ("What’s the serial number on your laptop?", True, "", "", ""),
    (f"Have you seen the new {CUT('serial')} on Netflix?", False, "«новый сериал»", "«новый сериал»",
     f"Have you seen the new {I('series')} on Netflix?"),
    (f"Each {CUT('series')} is about forty minutes long.", False, "«каждая серия»", "«каждая серия»",
     f"Each {I('episode')} is about forty minutes long."),
    ("Both series are on Netflix.", True, "", "", ""),
    (f"I watched three {CUT('series')} last night.", False, "«три серии»", "«три серии»",
     f"I watched three {I('episodes')} last night."),
    (f"This {CUT('serial')} has five seasons.", False, "«у этого сериала»", "«у этого сериала»",
     f"This {I('show')} has five seasons."),
    ("I watched two episodes before bed.", True, "", "", ""),
]

FIGURE = ladder([
    (f"I love watching {D('serials')}.", "en", "you say", "вы говорите"),
    # The slide's own headline: what a native speaker hears, in Russian.
    ("Я люблю смотреть <em>хлопья</em>.", "ru", "they hear", "носитель слышит"),
    (f"I love watching TV {I('shows')}.", "en", "say", "скажите"),
], "Fig. 1. {{serial}} and {{cereal}} sound the same, and {{cereal}} is breakfast.",
   "Рис. 1. {{serial}} и {{cereal}} звучат одинаково, а {{cereal}} — это хлопья.", "fig-serial")

MSG_EN = "Hi! I took the test in your note about “serial”: {n}/{t}. I’d like a free trial English lesson."
MSG_RU = "Здравствуйте! Мой результат в тесте из заметки про «serial»: {n}/{t}. Хочу записаться на бесплатное пробное занятие по английскому."


def body(note):
    words = section("words", "\n".join([
        head2("A word for each.", "Каждому слову — своё.",
              "Russian has {{сериал}}, {{серия}}, {{сезон}} and {{серийный}}, and English has a word for each. [[In everyday English, serial means серийный.]]",
              "{{сериал}}, {{серия}}, {{сезон}}, {{серийный}} — у каждого своё английское слово. [[В обычной речи serial — это «серийный».]]"),
        register("Six phrases with сериал, серия and серийный, and what English says",
                 "Шесть фраз с «сериал», «серия» и «серийный» и как сказать по-английски",
                 [("In Russian", "По-русски"), ("In English", "По-английски")],
                 [[ru, ("register__w", en)] for ru, en in PHRASES], cls=" register--pairs"),
        # DRAFT for Igor (NQ14): British English keeps serial for a story in parts.
        '  <p class="note-cite reveal"><span data-l="en">serial does exist, for a story told in parts (a BBC serial, '
        'the podcast Serial), but for Netflix shows people say series or show.</span><span data-l="ru">serial в '
        'английском есть: так называют историю с продолжением (a BBC serial, подкаст Serial). Но про сериалы на '
        'Netflix говорят series или show.</span></p>',
    ]))
    why = section("why", "\n".join([
        # DRAFT for Igor: the post gives the facts; the wording is the note's.
        head2("One sound, two spellings.", "Один звук, два слова.",
              "{{serial}} and {{cereal}} are said the same way, so a native speaker hears what they pour every morning: [[cereal]]. {{series}} sounds different, and it is the whole show: one {{series}}, two {{series}}. One part of it is an {{episode}}.",
              "{{serial}} и {{cereal}} произносятся одинаково, и носитель слышит то, что ест на завтрак: [[хлопья]]. {{series}} звучит иначе и значит весь сериал: one {{series}}, two {{series}}. Одна серия — {{episode}}."),
        pull([
            ("серийный", "serial", ipa("/ˈsɪəriəl/")),
            ("хлопья", "cereal", ipa("/ˈsɪəriəl/")),
            ("сериал", "series", ipa("/ˈsɪəriːz/")),
        ]),
    ]))
    test = section("practice", "\n".join([
        head2("Which would a native speaker say?", "Какие фразы сказал бы носитель?",
              "Pick every sentence that sounds right to you, then check. [[Some are fine, most are not]].",
              "Отметьте все фразы, которые звучат правильно, и проверьте. [[Какие-то в порядке, большинство — нет]]."),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ14): the sentences around the post's own phrases. -->",
        ear_test(TEST, MSG_EN, MSG_RU, tg(note["tg_en"])),
    ]), cls=" sec--ear")
    return "\n\n".join([words, why, test])


NOTE = dict(
    slug="serial",
    iso="2026-11-23",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="23 November 2026", date_long_ru="23 ноября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7530525758075658240/",
    from_linkedin=True,
    kind_en="Vocabulary", kind_ru="Лексика",
    count_en="serial · 6 phrases · a test", count_ru="serial · 6 фраз · тест",
    title_en="Series, not cereal.", title_ru="Сериалы, а не хлопья.",
    short_en="Series, not cereal", short_ru="Сериалы, а не хлопья",
    ledger_spec=f'watching {D("serials")} <span class="ledger__to" aria-hidden="true">→</span> watching {I("TV shows")}',
    card_en="Series, <em>not cereal.</em>", card_ru="Сериалы, <em>а не хлопья.</em>",
    card_spec='watching <span class="x">serials</span><span class="to">→</span>watching <span class="ok">TV shows</span>',
    h1_en=["Series,", "not cereal."], h1_ru=["Сериалы,", "а не хлопья."],
    # The post's opening, cleaned, then the answer. The English is a DRAFT.
    stand_en="When a lesson turns to TV, I often hear “I love watching serials.” A native speaker hears cereals: breakfast. [[For сериал, English says TV series or TV show; for серия, episode.]]",
    stand_ru="Когда на уроке речь заходит о сериалах, я часто слышу «I love watching serials». Носитель слышит cereals — хлопья. [[Сериал по-английски — TV series или TV show, а серия — episode.]]",
    figure=FIGURE,
    comment="/notes/serial/: Igor's LinkedIn post and slide on serial and cereal, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="“I love watching serials”? Serial vs series — Igor Shatsev",
    title_ru_head="Сериал по-английски: serial или series? — Igor Shatsev",
    desc_en="Russian speakers say “I love watching serials”, and a native speaker hears cereals. Сериал is a TV series or a TV show, серия is an episode, and it’s one series, two series. With a quick test.",
    desc_ru="«I love watching serials» — носитель услышит «хлопья». Как сказать «сериал» и «серия» по-английски: series, show, episode, season, и почему two series, а не two serieses. Короткий тест.",
    og_title="Series, not cereal: сериал in English — Igor Shatsev",
    og_desc="serial sounds like cereal. Сериал is a TV series or a TV show, серия is an episode. Six phrases and a test.",
    og_alt="Series, not cereal. A note by Igor Shatsev on the word serial.",
    ld_headline="Series, not cereal: сериал is not serial",
    contact_lede_en="Mix-ups like this are hard to notice in your own English and easy to hear from outside. In the trial lesson we’ll find yours. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Такую путаницу трудно заметить у себя и легко услышать со стороны. На пробном занятии найдём вашу. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “serial”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «serial». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
