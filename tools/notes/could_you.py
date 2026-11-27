"""/notes/could-you/: "Send me the report, please", the third specimen on
/english/ (Igor kept it). The standfirst reuses
the specimen's approved explanation; the rest was written for the note. The
slug leaves out "please", which /english/ keeps hidden until asked (W1)."""
from lib import both, head2, hit, ladder, practice, pull, register, section, spec_pair

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'
P = '<span class="hit">please</span>'

REQUESTS = [
    (f"Send me the report, {P}.", f"{I('Could you')} send me the report?"),
    (f"Check my draft, {P}.", f"{I('Could you')} take a look at my draft?"),
    (f"Give me access, {P}.", f"{I('Could I')} get access to the folder?"),
    (f"Explain this, {P}.", f"{I('Would you mind')} explaining this?"),
    (f"Call me tomorrow, {P}.", f"{I('Can we')} talk tomorrow?"),
    (f"Answer quickly, {P}.", f"{I('Could you')} get back to me today?"),
]
SOFTENERS = [
    (hit("пожалуйста", "пожалуйста"), "please", both("not enough on its own", "одного мало")),
    ("вы", "could you…?", both("the question does the work", "работает вопрос")),
    ("не могли бы вы", "could you possibly…?", both("softer still", "ещё мягче")),
    ("вы не против, если…", "would you mind…?", both("more tentative", "осторожнее")),
    ("если будет минутка", "when you get a chance", both("the softest", "мягче всего")),
]
PRACTICE = [
    "<b>Could you</b> send me the report today?",
    "<b>Could you</b> take a look at my draft?",
    "<b>Would you mind</b> moving the call to four?",
    "<b>Can we</b> go over the plan tomorrow?",
    "<b>When you get a chance</b>, could you review my comments?",
    "<b>I was wondering if</b> you could share the slides.",
]

FIGURE = ladder([
    ("Пришлите мне отчёт сегодня, пожалуйста.", "ru", "Russian · polite", "по-русски · вежливо"),
    (f"Send me the report today, <span class=\"mark--specimen\">please</span>.", "en", "English · still a command", "по-английски · всё ещё команда"),
    (f"{I('Could you')} send me the report today?", "en", "English · a request", "по-английски · просьба"),
], "Fig. 1. In English the softening lives in the question, not in {{please}}.",
   "Рис. 1. В английском вежливость — в вопросе, а не в {{please}}.", "fig-please")


def body(note):
    words = section("words", "\n".join([
        head2("Six requests, from order to request.", "Шесть просьб: от приказа к вопросу.",
              "Each line: the order with {{please}}, and [[what a colleague would actually say]].",
              "В каждой строке: приказ с {{please}} и [[как на самом деле сказал бы коллега]]."),
        spec_pair(f"Send me the report today{D(', please')}.", f"{I('Could you')} send me the report today?"),
        register("Six requests: an order with please, and what English says", "Шесть просьб: приказ с please и как сказать по-английски",
                 [("With please", "С please"), ("What English says", "Как по-английски")],
                 [[w, ("register__w", r)] for w, r in REQUESTS], cls=" register--pairs"),
    ]))
    why = section("why", "\n".join([
        head2("Russian softens with a word. English, with grammar.", "Русский смягчает словом, английский — грамматикой.",
              "Russian is polite with {{пожалуйста}} and with {{вы}}. English does it with grammar: a question, a modal verb ({{could}}, {{would}}, {{can}}) [[and a little distance]].",
              "В русском вежливость — это {{пожалуйста}} и {{вы}}. В английском — грамматика: вопрос, модальный глагол ({{could}}, {{would}}, {{can}}) [[и немного дистанции]]."),
        pull(SOFTENERS),
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "Every line is a question. Once it is, {{please}} is optional.",
              "Каждая строка — вопрос. А раз вопрос, {{please}} — по желанию."),
        practice(PRACTICE, "i. is the specimen's own line; ii.–vi. were written for the note."),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="could-you",
    iso="2026-11",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="November 2026", date_long_ru="ноябрь 2026",
    from_linkedin=False,
    kind_en="Register", kind_ru="Регистр",
    count_en="please · 6 requests", count_ru="please · 6 просьб",
    title_en="Please isn’t enough.", title_ru="Одного please мало.",
    short_en="Please isn’t enough", short_ru="Одного please мало",
    ledger_spec=f'Send it{D(", please")} <span class="ledger__to" aria-hidden="true">→</span> {I("Could you")} send it?',
    card_en="Please <em>isn’t enough.</em>", card_ru="Одного please <em>мало.</em>",
    card_spec='Send it<span class="x">, please</span><span class="to">→</span><span class="ok">Could you</span> send it?',
    h1_en=["Please", "isn’t enough."], h1_ru=["Одного please", "мало."],
    stand_en="“Send me the report today, please” is a mistake I hear all the time, and the grammar is fine. It still sounds like an order. In Russian, {{пожалуйста}} softens it; [[in English, {{please}} alone doesn’t]].",
    stand_ru="«Send me the report today, please» — эту ошибку я слышу постоянно, и дело не в грамматике: с ней всё в порядке, но фраза звучит как распоряжение. В русском его смягчает {{пожалуйста}}, [[а в английском одного {{please}} мало]].",
    figure=FIGURE,
    comment="/notes/could-you/: the English page's third specimen as a note.",
    title="Why “please” isn’t enough in English requests — Igor Shatsev",
    title_ru_head="Почему одного please мало: как вежливо просить по-английски — Igor Shatsev",
    desc_en="“Send me the report, please” still sounds like an order. Why Russian speakers lean on please, and how English actually asks: could you, would you mind, when you get a chance.",
    desc_ru="«Send me the report, please» всё равно звучит как приказ. Почему русскоязычные полагаются на please и как в английском просят на самом деле: could you, would you mind, when you get a chance.",
    og_title="Please isn’t enough: how English asks — Igor Shatsev",
    og_desc="An order with please is still an order. Six requests, and how English softens them.",
    og_alt="Please isn’t enough. A note by Igor Shatsev on polite requests.",
    ld_headline="Please isn’t enough: how to make a request in English",
    contact_lede_en="How a request lands is hard to judge from the inside. Bring a few of yours to the trial lesson, and I’ll tell you how they sound to a native ear. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Как звучит ваша просьба, изнутри не понять. Принесите на пробное занятие пару своих — скажу, как их слышит носитель. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “please”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «please». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
