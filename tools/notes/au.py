"""/notes/au/: Igor's LinkedIn post about the au sound (November 2026).
The Russian is his post, lightly cleaned; the English is a translation, a
DRAFT for Igor (SITE-PLAN.md NQ4). The practice sentences are drafts (NQ3)."""
from lib import head2, hit, ipa, practice, pull, register, section, spec_pair, tile, w

OO = '<span class="mark--target">ɔː</span>'

WORDS = [
    ("automate", "/ˈ{}təmeɪt/"),
    ("auction", "/ˈ{}kʃn/"),
    ("cause", "/k{}z/"),
    ("launch", "/l{}ntʃ/"),
    ("fault", "/f{}lt/"),
    ("authenticate", "/{}ˈθentɪkeɪt/"),
]
LOOKALIKES = [("автор", "ав", "author", "/ˈ{}θə/"), ("август", "ав", "August", "/ˈ{}ɡəst/"),
              ("аура", "ау", "aura", "/ˈ{}rə/"), ("аудио", "ау", "audio", "/ˈ{}diəʊ/")]
# DRAFT for Igor (SITE-PLAN.md NQ3), rewritten 2026-11-27 for work and
# life alike (the first set was all IT: release, outage, config, API).
PRACTICE = [
    "We l<b>au</b>nch on Monday.",
    "Let’s <b>au</b>tomate the reports.",
    "What c<b>au</b>sed the delay?",
    "It’s not your f<b>au</b>lt.",
    "The app asks you to <b>au</b>thenticate.",
    "The house went to <b>au</b>ction.",
]

FIGURE = f"""    <figure class="note-fig tiles reveal" aria-labelledby="fig-au">
      <div class="tiles__row" aria-hidden="true">{tile('L', 1)}{tile('A', 1, ' tile--specimen')}{tile('U', 1, ' tile--specimen')}{tile('N', 1)}{tile('C', 3)}{tile('H', 4)}</div>
      <div class="tiles__row" aria-hidden="true">{tile('L', 1)}{tile('ɔː', None, ' tile--target tile--merged', ' ipa')}{tile('N', 1)}{tile('C', 3)}{tile('H', 4)}</div>
      <figcaption id="fig-au"><span data-l="en">{w("launch")}: the {w("a")} and the {w("u")} are one sound, {ipa("/ɔː/")}.</span><span data-l="ru">{w("launch")}: {w("a")} и {w("u")} — это один звук, {ipa("/ɔː/")}.</span></figcaption>
    </figure>"""

IPA_OO = ipa("/ɔː/")
LAUNCH_IPA = ipa('/l<ins class="mark--target">ɔː</ins>ntʃ/')
AS ='<span class="note-spec__as" data-en="sounds like" data-ru="звучит как">sounds like</span>'


def body(note):
    words = section("words", "01", "Six words, one sound", "Шесть слов, один звук", "\n".join([
        head2("Six words. One sound in every one.", "Шесть слов. В каждом один звук.",
              f"Wherever the line is, {{{{au}}}} is a single long {IPA_OO}. Not {{{{а}}}} plus {{{{у}}}}, not {{{{а}}}} plus {{{{в}}}}.",
              f"Там, где черта, {{{{au}}}} — это один долгий звук {IPA_OO}. Не {{{{а}}}} плюс {{{{у}}}} и не {{{{а}}}} плюс {{{{в}}}}."),
        spec_pair(f'launch {AS} л<del class="mark--specimen">ау</del>нч',
                  f'launch {AS} {LAUNCH_IPA}'),
        register("Six words with au, and how each one sounds", "Шесть слов с au и как каждое звучит",
                 [("Word", "Слово"), ("Sound", "Звучание")],
                 [[hit(word, "au"), ("register__ipa", ipa(tr.format(OO)))] for word, tr in WORDS]),
        # the accent footnote. DRAFT for Igor (not in the post).
        f'  <p class="note-cite reveal"><span data-l="en">That is British {IPA_OO}; many Americans say {ipa("/ɑː/")}. '
        f'Either way it is one vowel, never two.</span><span data-l="ru">Это британское {IPA_OO}; многие американцы '
        f'говорят {ipa("/ɑː/")}. В любом случае это один гласный, а не два.</span></p>',
    ]))
    why = section("why", "02", "Why it happens", "Почему так", "\n".join([
        head2("The cause is in Russian.", "Причина кроется в родном языке.",
              "{{автор}}, {{август}}, {{аура}}, {{аудио}} and plenty more: a whole pool of Russian words that look like English ones, and they [[pull in the familiar Russian sound]].",
              "{{автор}}, {{август}}, {{аура}}, {{аудио}} и много других — это пул слов, которые схожи с английскими и которые [[притягивают привычное русское звучание]]."),
        pull([(hit(ru, trap), en, ipa(tr.format(OO))) for ru, trap, en, tr in LOOKALIKES]),
    ]))
    say = section("practice", "03", "Say it out loud", "Скажите вслух", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "One sound wherever the line is. No {{а}}, no {{у}}, no {{в}}.",
              "Там, где черта, — один звук. Без {{а}}, без {{у}}, без {{в}}."),
        practice(PRACTICE, "DRAFT for Igor (SITE-PLAN.md NQ3): these six sentences are not from the LinkedIn post."),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="au",
    iso="2026-11",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="November 2026", date_long_ru="ноябрь 2026",
    linkedin=None,  # set below: the post's own URL once Igor sends it (Q5)
    from_linkedin=True,
    kind_en="Pronunciation", kind_ru="Произношение",
    count_en="au · 6 words · 1 sound", count_ru="au · 6 слов · 1 звук",
    title_en="Two letters, one sound.", title_ru="Две буквы — один звук.",
    short_en="Two letters, one sound", short_ru="Две буквы — один звук",
    ledger_spec='launch: л<del class="mark--specimen">ау</del>нч <span class="ledger__to" aria-hidden="true">→</span> ' + ipa('/l<ins class="mark--target">ɔː</ins>ntʃ/'),
    card_en="Two letters, <em>one sound.</em>", card_ru="Две буквы — <em>один звук.</em>",
    card_spec='launch: л<span class="x">ау</span>нч<span class="to">→</span>' + ipa('/l<span class="ok">ɔː</span>ntʃ/'),
    h1_en=["Two letters,", "one sound."], h1_ru=["Две буквы —", "один звук."],
    # "Almost all my students" replaces "95% of my IT clients" (NQ2, Igor
    # 2026-11-27: soften it, and not IT-first).
    stand_en=f"Almost all my students mispronounce {{{{au}}}}: {{{{automate}}}}, {{{{auction}}}}, {{{{cause}}}}, {{{{launch}}}}, {{{{fault}}}}, {{{{authenticate}}}}. They come out as {{{{автомейт}}}}, {{{{аутомейт}}}}, {{{{лаунч}}}}, {{{{аусентикейт}}}}. To make them sound right, drop the {{{{а}}}}, the {{{{у}}}} and the {{{{в}}}}: [[you need one sound only, {IPA_OO}]].",
    stand_ru=f"Почти все мои ученики ошибаются в произношении сочетания {{{{au}}}}: {{{{automate}}}}, {{{{auction}}}}, {{{{cause}}}}, {{{{launch}}}}, {{{{fault}}}}, {{{{authenticate}}}}. Произносят эти слова как {{{{автомейт}}}}, {{{{аутомейт}}}}, {{{{лаунч}}}}, {{{{аусентикейт}}}}. Чтобы звучало красиво, надо убрать {{{{а}}}}, {{{{у}}}} и {{{{в}}}}: [[нужен только один звук, {IPA_OO}]].",
    figure=FIGURE,
    comment="/notes/au/: Igor's LinkedIn post about the au sound, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="How to pronounce au: automate, launch, cause — Igor Shatsev",
    title_ru_head="Как произносить au: automate, launch, cause — Igor Shatsev",
    desc_en="Russian speakers say launch as “лаунч” and automate as “автомейт”. Six words, one sound: /ɔː/. Why Russian pulls the wrong sound in, and how it should sound.",
    desc_ru="«Лаунч», «автомейт», «аусентикейт»: почему русскоязычные так произносят au и как правильно. Шесть слов, один звук /ɔː/.",
    og_title="Two letters, one sound: how to say au — Igor Shatsev",
    og_desc="automate, auction, cause, launch, fault, authenticate: six words, one sound, /ɔː/.",
    og_alt="Two letters, one sound. A note by Igor Shatsev on the au sound.",
    ld_headline="Two letters, one sound: how to pronounce au",
    contact_lede_en="Not sure how you say these six? The trial lesson is a good place to find out. [[It’s 30 minutes, free, and you owe me nothing after it]]. Online or in Yerevan.",
    contact_lede_ru="Не уверены, как вы произносите эти шесть слов? На пробном занятии это легко проверить. [[Это 30 минут, бесплатно и ни к чему не обязывает]]. Онлайн или в Ереване.",
    tg_en="Hi! I came from your note about the au sound. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про звук au. Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
