"""/notes/agree/: "I am agree", the first specimen on /english/ (NOTES-COUNCIL
K7, a PREVIEW for Igor: "show me how it looks and then we'll decide").
The standfirst reuses the specimen's approved explanation; everything else
(forms, look-alikes, practice, the Russian) is a DRAFT for Igor.
The slug leaves out "am": on /english/ that word stays hidden until the
reader asks for it (W1, J6(b)), and the specimen links here."""
from lib import both, head2, hit, ladder, practice, pull, register, section, spec_pair

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'

FORMS = [
    (f"I {D('am')} agree", f"I {I('agree')}"),
    (f"I{D('’m')} not agree", f"I {I('don’t')} agree"),
    (f"{D('Are')} you agree?", f"{I('Do')} you agree?"),
    (f"We {D('are')} agree", f"We {I('agree')}"),
    (f"He {D('is')} agree", f"He {I('agrees')}"),
    (f"I {D('was')} agree", f"I {I('agreed')}"),
]
LOOKALIKES = [
    ("уверен", "I’m sure", both("adjective · am stays", "прилагательное · am на месте")),
    ("готов", "I’m ready", both("adjective · am stays", "прилагательное · am на месте")),
    ("прав", "I’m right", both("adjective · am stays", "прилагательное · am на месте")),
    (hit("согласен", "согласен"), "I agree", both("a verb · no am", "глагол · без am")),
]
PRACTICE = [
    "I <b>agree</b> with your point.",
    "I <b>don’t agree</b> with the estimate.",
    "<b>Do</b> you <b>agree</b> with the plan?",
    "We all <b>agree</b> on the deadline.",
    "She <b>agreed</b> to the new terms.",
    "I’m sure, and I <b>agree</b>.",
]

FIGURE = ladder([
    ("Я согласен.", "ru", "Russian · a state", "по-русски · состояние"),
    (f"I {D('am')} agree.", "en", "the habit", "привычка"),
    (f"I {I('agree')}.", "en", "English · an action", "по-английски · действие"),
], "Fig. 1. согласен is a state; agree is already the action.",
   "Фиг. 1. «Согласен» — состояние; agree — уже действие.", "fig-agree")


def body(note):
    words = section("words", "01", "Six forms", "Шесть форм", "\n".join([
        head2("One habit, six forms.", "Одна привычка, шесть форм.",
              "The same extra word slips into every tense and every person. Each line: [[what comes out, and what English says]].",
              "Одно и то же лишнее слово пролезает в любое время и любое лицо. В каждой строке: [[как звучит и как по-английски]]."),
        spec_pair(f"I {D('am')} agree with you.", f"I {I('agree')} with you."),
        register("Six forms of “I am agree”, and what English says", "Шесть форм «I am agree» и как по-английски",
                 [("What comes out", "Как звучит"), ("What English says", "Как по-английски")],
                 [[w, ("register__w", r)] for w, r in FORMS], cls=" register--pairs"),
    ]))
    why = section("why", "02", "Why it happens", "Почему так", "\n".join([
        head2("Russian says it with an adjective.", "По-русски это прилагательное.",
              "уверен, готов, прав, согласен: Russian describes all four as states. English keeps three of them as adjectives with am, which is exactly why the fourth slips through: [[agree is a verb]].",
              "уверен, готов, прав, согласен — в русском все четыре описывают состояние. В английском три из них так и остаются прилагательными с am, поэтому четвёртое и проскакивает: [[agree — это глагол]]."),
        pull(LOOKALIKES),
    ]))
    say = section("practice", "03", "Say it out loud", "Скажите вслух", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "agree is the verb. The last line is the trap: sure keeps its am, agree never takes one.",
              "agree — это глагол. Последняя фраза — ловушка: у sure am остаётся, у agree его не бывает."),
        practice(PRACTICE, "DRAFT for Igor (K7 preview): i. is the specimen's own line; ii.–vi. are new."),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="agree",
    iso="2026-11",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="November 2026", date_long_ru="ноябрь 2026",
    from_linkedin=False,
    kind_en="Grammar", kind_ru="Грамматика",
    count_en="agree · 6 forms", count_ru="agree · 6 форм",
    title_en="A state or an action?", title_ru="Состояние или действие?",
    short_en="A state or an action?", short_ru="Состояние или действие?",
    ledger_spec=f'I {D("am")} agree <span class="ledger__to" aria-hidden="true">→</span> I {I("agree")}',
    card_en="A state <em>or an action?</em>", card_ru="Состояние <em>или действие?</em>",
    card_spec='I <span class="x">am</span> agree<span class="to">→</span>I <span class="ok">agree</span>',
    h1_en=["A state", "or an action?"], h1_ru=["Состояние", "или действие?"],
    stand_en="“I am agree” is one of the three mistakes I hear most often. The Russian word behind it, согласен, describes a state, not an action. [[Its English counterpart, agree, already is the action.]] Add am anyway and it still sounds fine, so nobody catches the mistake, and it lives on for years.",
    stand_ru="«I am agree» — одна из трёх ошибок, которые я слышу чаще всего. Русское слово «согласен» описывает состояние, а не действие. [[Английский аналог, agree, — это и есть действие.]] Добавляя am, мы всё равно звучим понятно, поэтому ошибку никто не ловит, так она живёт годами.",
    figure=FIGURE,
    comment="/notes/agree/ (NOTES-COUNCIL K7 preview). The English page's first specimen as a note. DRAFT for Igor.",
    title="“I am agree” or “I agree”? A state or an action — Igor Shatsev",
    title_ru_head="I am agree или I agree? Почему русскоязычные говорят am — Igor Shatsev",
    desc_en="Why Russian speakers say “I am agree”, and the six forms the habit takes: I’m not agree, are you agree, I was agree. agree is a verb; согласен is a state.",
    desc_ru="Почему русскоязычные говорят «I am agree» и в каких шести формах живёт эта привычка: I’m not agree, are you agree, I was agree. agree — глагол, а «согласен» — состояние.",
    og_title="A state or an action? “I am agree” — Igor Shatsev",
    og_desc="agree is already the action. Six forms of one habit, and the fix.",
    og_alt="A state or an action? A note by Igor Shatsev on “I am agree”.",
    ld_headline="A state or an action? Why Russian speakers say “I am agree”",
    nav=[("01", "#words", "The forms", "Формы"), ("02", "#why", "Why it happens", "Почему так"),
         ("03", "#practice", "Say it out loud", "Скажите вслух")],
    contact_lede_en="Not sure which habits slip into your English? The trial lesson is a good place to find out. [[It’s 30 minutes, free, and you owe me nothing after it]]. Online or in Yerevan.",
    contact_lede_ru="Не уверены, какие привычки пролезают в ваш английский? На пробном занятии это легко проверить. [[Это 30 минут, бесплатно и ни к чему не обязывает]]. Онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “I am agree”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «I am agree». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
