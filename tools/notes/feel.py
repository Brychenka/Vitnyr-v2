"""/notes/feel/: "I feel myself good", the second specimen on /english/
(Igor kept it). Written for the note,
not yet line-edited by Igor. Note: the English page explains this one as a Russian "reflexive
ending built into the verb"; чувствую себя uses a separate reflexive word
(себя), not an ending, so this note says "reflexive word". The slug leaves
out "myself", which /english/ keeps hidden until the reader asks (W1)."""
from lib import both, head2, hit, ladder, practice, pull, register, section, spec_pair

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'

PHRASES = [
    (f"I feel {D('myself')} good", f"I {I('feel')} good"),
    (f"I feel {D('myself')} tired", f"I {I('feel')} tired"),
    (f"I feel {D('myself')} better", f"I {I('feel')} better"),
    (f"How do you feel {D('yourself')}?", f"How do you {I('feel')}?"),
    (f"I feel {D('myself')} at home", f"I {I('feel')} at home"),
    (f"I felt {D('myself')} stupid", f"I {I('felt')} stupid"),
]
# "-\u2060self": the word joiner stops a line break between the hyphen and
# "self" (the heading broke as "keeps -" / "self for actions" at 1280px).
LOOKALIKES = [
    ("представиться", "introduce myself", both("an action · -\u2060self stays", "действие · -\u2060self на месте")),
    ("ушибиться", "hurt myself", both("an action · -\u2060self stays", "действие · -\u2060self на месте")),
    (hit("чувствую себя", "себя"), "I feel", both("a feeling · no -\u2060self", "ощущение · без -\u2060self")),
]
PRACTICE = [
    "I <b>feel</b> good today.",
    "I <b>feel</b> much better after the call.",
    "How do you <b>feel</b> about the new job?",
    "I <b>felt</b> nervous before the interview.",
    "Let me <b>introduce myself</b>.",
    "<b>Make yourself</b> at home.",
]

FIGURE = ladder([
    ("Я чувствую себя хорошо.", "ru", "Russian · with себя", "по-русски · с «себя»"),
    (f"I feel {D('myself')} good.", "en", "the habit", "привычка"),
    (f"I {I('feel')} good.", "en", "English · feel is enough", "по-английски · хватает feel"),
], "Fig. 1. {{feel}} works on its own. Nothing to add.",
   "Рис. 1. Хватает одного {{feel}}. Добавлять нечего.", "fig-feel")


def body(note):
    words = section("words", "\n".join([
        head2("One habit, six phrases.", "Одна привычка, шесть фраз.",
              "Wherever Russian says {{чувствую себя}}, [[English just says {{feel}}]].",
              "Там, где по-русски {{чувствую себя}}, [[по-английски просто {{feel}}]]."),
        spec_pair(f"I feel {D('myself')} good today.", f"I {I('feel')} good today."),
        register("Six phrases with an extra myself, and what English says", "Шесть фраз с лишним myself и как правильно",
                 [("What comes out", "Привычка"), ("What English says", "Правильно")],
                 [[w, ("register__w", r)] for w, r in PHRASES], cls=" register--pairs"),
        # DRAFT for Igor (copy review 2026-11-28): where feel myself is right.
        '  <p class="note-cite reveal"><span data-l="en">feel myself does exist, just not before an adjective: I’m not feeling myself today '
        'means I’m not my usual self.</span><span data-l="ru">feel myself всё же бывает, но не перед прилагательным: '
        'I’m not feeling myself today — «я сегодня сам не свой».</span></p>',
    ]))
    why = section("why", "\n".join([
        head2("English keeps -\u2060self for actions.", "В английском -\u2060self — для действий.",
              "English does have {{myself}}, but for something you do to yourself, not for how you feel: [[{{introduce myself}}, {{hurt myself}}]]. A feeling goes straight after {{feel}}.",
              "В английском {{myself}} есть, но для того, что вы делаете с собой, а не для того, как себя чувствуете: [[{{introduce myself}}, {{hurt myself}}]]. Ощущение идёт сразу после {{feel}}."),
        pull(LOOKALIKES),
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "{{feel}}, then the feeling. The last two are actions, so they keep {{-\u2060self}}.",
              "{{feel}} — и сразу ощущение. Последние две — действия, поэтому {{-\u2060self}} остаётся."),
        practice(PRACTICE, "i. is the specimen's own line; ii.–vi. were written for the note."),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="feel",
    iso="2026-11",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="November 2026", date_long_ru="ноябрь 2026",
    from_linkedin=False,
    kind_en="Grammar", kind_ru="Грамматика",
    count_en="feel · 6 phrases", count_ru="feel · 6 фраз",
    title_en="Nothing to add.", title_ru="Добавлять нечего.",
    short_en="Nothing to add", short_ru="Добавлять нечего",
    ledger_spec=f'I feel {D("myself")} good <span class="ledger__to" aria-hidden="true">→</span> I {I("feel")} good',
    card_en="Nothing <em>to add.</em>", card_ru="Добавлять <em>нечего.</em>",
    card_spec='I feel <span class="x">myself</span> good<span class="to">→</span>I <span class="ok">feel</span> good',
    h1_en=["Nothing", "to add."], h1_ru=["Добавлять", "нечего."],
    stand_en="“I feel myself good” is one of the mistakes I hear most. Russian needs {{себя}} here, {{чувствую себя}}, so the instinct is to add {{myself}} in English too. [[But {{feel}} works on its own.]]",
    stand_ru="«I feel myself good» — одна из самых частых ошибок, которые я слышу. По-русски мы говорим {{чувствую себя}}, и рука сама тянется добавить {{myself}}. [[Но английскому {{feel}} это не нужно.]]",
    figure=FIGURE,
    comment="/notes/feel/: the English page's second specimen as a note.",
    title="“I feel myself good”? Just “I feel good” — Igor Shatsev",
    title_ru_head="I feel myself good или I feel good? Лишнее «себя» в английском — Igor Shatsev",
    desc_en="Why Russian speakers say “I feel myself good” (чувствую себя), six phrases where the extra myself creeps in, and when English does use -self.",
    desc_ru="Почему русскоязычные говорят «I feel myself good» (чувствую себя), шесть фраз, где появляется лишнее myself, и когда -self в английском всё-таки нужен.",
    og_title="Nothing to add: “I feel myself good” — Igor Shatsev",
    og_desc="feel works on its own. Six phrases, and when -self does belong.",
    og_alt="Nothing to add. A note by Igor Shatsev on “I feel myself good”.",
    ld_headline="Nothing to add: why Russian speakers say “I feel myself good”",
    contact_lede_en="Habits like this one sit so deep you stop hearing them. In the trial lesson they’re quick to find. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Такие привычки сидят так глубоко, что их перестаёшь слышать. На пробном занятии их легко найти. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “I feel myself”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «I feel myself». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
