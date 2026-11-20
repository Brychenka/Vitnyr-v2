"""/notes/feel/: "I feel myself good", the second specimen on /english/
(NOTES-COUNCIL K7, a PREVIEW for Igor). Everything here is a DRAFT for
Igor. Note: the English page explains this one as a Russian "reflexive
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
LOOKALIKES = [
    ("представиться", "introduce myself", both("an action · -self stays", "действие · -self на месте")),
    ("ушибиться", "hurt myself", both("an action · -self stays", "действие · -self на месте")),
    (hit("чувствую себя", "себя"), "I feel", both("a feeling · no -self", "ощущение · без -self")),
]
PRACTICE = [
    "I <b>feel</b> good today.",
    "I <b>feel</b> much better after the call.",
    "How do you <b>feel</b> about the release?",
    "I <b>felt</b> nervous before the interview.",
    "Let me <b>introduce myself</b>.",
    "<b>Make yourself</b> at home.",
]

FIGURE = ladder([
    ("Я чувствую себя хорошо.", "ru", "Russian · with себя", "по-русски · с «себя»"),
    (f"I feel {D('myself')} good.", "en", "the habit", "привычка"),
    (f"I {I('feel')} good.", "en", "English · feel is enough", "по-английски · хватает feel"),
], "Fig. 1. feel already carries the feeling. Nothing to add.",
   "Фиг. 1. feel уже несёт ощущение. Добавлять нечего.", "fig-feel")


def body(note):
    words = section("words", "01", "Six phrases", "Шесть фраз", "\n".join([
        head2("One habit, six phrases.", "Одна привычка, шесть фраз.",
              "Wherever Russian says чувствую себя, [[English just says feel]].",
              "Там, где по-русски «чувствую себя», [[по-английски просто feel]]."),
        spec_pair(f"I feel {D('myself')} good today.", f"I {I('feel')} good today."),
        register("Six phrases with an extra myself, and what English says", "Шесть фраз с лишним myself и как по-английски",
                 [("What comes out", "Как звучит"), ("What English says", "Как по-английски")],
                 [[w, ("register__w", r)] for w, r in PHRASES], cls=" register--pairs"),
    ]))
    why = section("why", "02", "Why it happens", "Почему так", "\n".join([
        head2("English keeps -self for actions.", "В английском -self — для действий.",
              "English does have myself, but for something you do to yourself, not for how you feel: [[introduce myself, hurt myself]]. A feeling goes straight after feel.",
              "В английском myself есть, но для того, что вы делаете с собой, а не для того, как себя чувствуете: [[introduce myself, hurt myself]]. Ощущение идёт сразу после feel."),
        pull(LOOKALIKES),
    ]))
    say = section("practice", "03", "Say it out loud", "Скажите вслух", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "feel, then the feeling. The last two are actions, so they keep -self.",
              "feel — и сразу ощущение. Последние две — действия, поэтому -self остаётся."),
        practice(PRACTICE, "DRAFT for Igor (K7 preview): i. is the specimen's own line; ii.–vi. are new."),
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
    stand_en="“I feel myself good” is one of the three mistakes I hear most often. Russian says it with a reflexive word, чувствую себя, so the instinct is to bolt the same thing onto the English, [[onto a verb that was never missing it]]. In English, feel already carries the feeling.",
    stand_ru="«I feel myself good» — одна из трёх ошибок, которые я слышу чаще всего. По-русски — «чувствую себя», с возвратным словом, и рефлекс — приставить то же самое и в английском, [[к глаголу, которому это не нужно]]. В английском feel уже несёт ощущение сам.",
    figure=FIGURE,
    comment="/notes/feel/ (NOTES-COUNCIL K7 preview). The English page's second specimen as a note. DRAFT for Igor.",
    title="“I feel myself good”? Just “I feel good” — Igor Shatsev",
    title_ru_head="I feel myself good или I feel good? Лишнее «себя» в английском — Igor Shatsev",
    desc_en="Why Russian speakers say “I feel myself good” (чувствую себя), six phrases where the extra myself creeps in, and when English does use -self.",
    desc_ru="Почему русскоязычные говорят «I feel myself good» (чувствую себя), шесть фраз, где появляется лишнее myself, и когда -self в английском всё-таки нужен.",
    og_title="Nothing to add: “I feel myself good” — Igor Shatsev",
    og_desc="feel already carries the feeling. Six phrases, and when -self does belong.",
    og_alt="Nothing to add. A note by Igor Shatsev on “I feel myself good”.",
    ld_headline="Nothing to add: why Russian speakers say “I feel myself good”",
    nav=[("01", "#words", "The phrases", "Фразы"), ("02", "#why", "Why it happens", "Почему так"),
         ("03", "#practice", "Say it out loud", "Скажите вслух")],
    contact_lede_en="Not sure which habits slip into your English? The trial lesson is a good place to find out. [[It’s 30 minutes, free, and you owe me nothing after it]]. Online or in Yerevan.",
    contact_lede_ru="Не уверены, какие привычки пролезают в ваш английский? На пробном занятии это легко проверить. [[Это 30 минут, бесплатно и ни к чему не обязывает]]. Онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “I feel myself”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «I feel myself». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
