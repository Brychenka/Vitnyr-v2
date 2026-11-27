"""/notes/actual/: Igor's LinkedIn post and carousel "Actual?" (8 October
2026, read from LinkedIn on 2026-11-28; reference/linkedin-posts/). The
Russian is his post, lightly cleaned (ты → вы, as on the rest of the site);
the English is a translation, a DRAFT for Igor. The four phrases and their
fixes are his carousel's four slides; two of the practice lines are his
post's own examples. What was written for the note is marked DRAFT below.

The first vocabulary note, so it brings its own figure, a dictionary entry
(.entry): the headword, what it looks like, what it means, what to say."""
from lib import both, head2, hit, ipa, practice_pair, pull, register, section, spec_pair, strong

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'
RU = lambda s: f'<span lang="ru">{s}</span>'

# The carousel's four slides, in its order: the Russian, then the fix.
PHRASES = [
    (RU(f"Задача ещё {hit('актуальна', 'актуальна')}?"), f"Is this task still {I('relevant')}?"),
    (RU(f"{hit('Актуальная', 'Актуальная')} версия"), f"the {I('current')} version"),
    (RU(f"{hit('Актуальная', 'Актуальная')} информация"), f"{I('up-to-date')} information"),
    (RU(f"Уже {hit('неактуально', 'неактуально')}"), f"It’s not {I('needed')} anymore."),
]

# Left: the carousel's fixes as sentences (the second and third reframed as
# questions). Right: the post's two examples, then two DRAFT lines for Igor.
INSTEAD = [
    "Is this task still <b>relevant</b>?",
    "Is this the <b>current</b> version?",
    "Is this information <b>up to date</b>?",
    "It’s not <b>needed</b> anymore.",
]
REAL = [
    "The <b>actual</b> deadline is Friday.",
    "We had estimated about 300 visitors, but the <b>actual</b> number was much higher.",
    "What was the <b>actual</b> cost?",
    "That’s not the <b>actual</b> problem.",
]


def role(en, ru):
    return f'<span class="weights__role" data-en="{en}" data-ru="{ru}">{en}</span>'


FIGURE = f"""    <figure class="note-fig entry reveal" aria-labelledby="fig-actual">
      <p class="entry__head" lang="en"><span class="entry__w">actual</span>{ipa("/ˈæktʃuəl/")}</p>
      <div class="ladder">
        <div class="ladder__row"><span class="ladder__s" lang="ru">{D("актуальный")}</span>{role("looks like", "похоже на")}</div>
        <div class="ladder__row"><span class="ladder__s" lang="ru">настоящий, фактический</span>{role("means", "значит")}</div>
        <div class="ladder__row"><span class="ladder__s" lang="en">{I("current")}, {I("relevant")}</span>{role("say instead", "говорите так")}</div>
      </div>
      <figcaption id="fig-actual"><span data-l="en">{strong("Fig. 1. {{actual}} is about what is real. For what matters now, English has other words.")}</span><span data-l="ru">{strong("Фиг. 1. {{actual}} — про то, что есть на самом деле. Для того, что важно сейчас, в английском другие слова.")}</span></figcaption>
    </figure>"""


def body(note):
    words = section("words", "\n".join([
        head2("Four phrases. Four plain words.", "Четыре фразы. Четыре простых слова.",
              "Where Russian says {{актуальный}}, English names what you mean: [[current, relevant, up to date, still needed]].",
              "Там, где по-русски {{актуальный}}, английский называет то, что вы имеете в виду: [[current, relevant, up to date, needed]]."),
        spec_pair(f"Is this task still {D('actual')}?", f"Is this task still {I('relevant')}?"),
        register("Four phrases with актуальный, and what English says", "Четыре фразы с «актуальный» и как сказать по-английски",
                 [("In Russian", "По-русски"), ("In English", "По-английски")],
                 [[ru, ("register__w", en)] for ru, en in PHRASES], cls=" register--pairs"),
        # The carousel's second slide adds "Или the latest version."
        '  <p class="note-cite reveal">'
        + both_block("For a version, {{the latest version}} works too.", "Для версии подойдёт и {{the latest version}}.")
        + "</p>",
    ]))
    why = section("why", "\n".join([
        # DRAFT for Igor: the post says what actual means; the why (the
        # meaning of актуальный, and German and French) was written for the note.
        head2("Same root, different job.", "Корень общий, работа разная.",
              "{{актуальный}} is about now: current, topical. {{actual}} is about fact: [[what really is, or really happened]]. German {{aktuell}} and French {{actuel}} also mean “current”, so English is the odd one out, and the look-alike wins.",
              "{{актуальный}} — про «сейчас»: текущий, злободневный. {{actual}} — про факт: [[то, что есть или было на самом деле]]. Немецкое {{aktuell}} и французское {{actuel}} тоже значат «текущий», так что английский тут белая ворона, а похожее слово побеждает."),
        pull([
            (hit("актуальный", "актуальный"), "actual", both("means настоящий", "значит «настоящий»")),
            # DRAFT for Igor: not in the post; the same trap one word over.
            (hit("актуально", "актуально"), "actually", both("means на самом деле", "значит «на самом деле»")),
        ]),
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "First the word you need instead of {{actual}}, then the places where {{actual}} is the right word.",
              "Сначала слово, которое нужно вместо {{actual}}, потом — где {{actual}} как раз к месту."),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ3): the last two lines on the right are not from the post. -->",
        practice_pair(
            ("When you mean актуальный", "Когда хотите сказать «актуальный»", "current · relevant · up to date", "current · relevant · up to date", INSTEAD),
            ("When you mean настоящий", "Когда хотите сказать «настоящий»", "actual", "actual", REAL),
        ),
    ]))
    return "\n\n".join([words, why, say])


def both_block(en, ru):
    return f'<span data-l="en">{strong(en)}</span><span data-l="ru">{strong(ru)}</span>'


NOTE = dict(
    slug="actual",
    iso="2026-10-08",
    date_short_en="Oct 2026", date_short_ru="октябрь 2026",
    date_long_en="8 October 2026", date_long_ru="8 октября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7513908883929825280/",
    from_linkedin=True,
    kind_en="Vocabulary", kind_ru="Лексика",
    count_en="actual · 4 phrases", count_ru="actual · 4 фразы",
    title_en="Real, not current.", title_ru="Настоящий, а не актуальный.",
    short_en="Real, not current", short_ru="Настоящий, а не актуальный",
    ledger_spec=f'still {D("actual")}? <span class="ledger__to" aria-hidden="true">→</span> still {I("relevant")}?',
    card_en="Real, <em>not current.</em>", card_ru="Настоящий, <em>а не актуальный.</em>",
    card_spec='still <span class="x">actual</span>?<span class="to">→</span>still <span class="ok">relevant</span>?',
    h1_en=["Real,", "not current."], h1_ru=["Настоящий,", "а не актуальный."],
    # The post's opening, cleaned. The English is a DRAFT translation.
    stand_en="If you write “Is this task still actual?” in the work chat, I have bad news for you. {{actual}} sounds like {{актуальный}}, but [[in meaning it is closer to real, true, existing in fact]].",
    stand_ru="Если вы пишете в рабочий чат «Is this task still actual?», у меня для вас плохие новости. {{actual}} звучит как {{актуальный}}, но [[по значению ближе к «настоящий, действительный, реальный»]].",
    figure=FIGURE,
    comment="/notes/actual/: Igor's LinkedIn post and carousel on actual, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="“Is this task still actual?” Actual vs актуальный — Igor Shatsev",
    title_ru_head="Актуальный по-английски: actual или relevant? — Igor Shatsev",
    desc_en="Russian speakers write “Is this task still actual?”, but actual means real, not current. Four phrases with актуальный, what English says instead, and where actual belongs.",
    desc_ru="«Is this task still actual?» — частая ошибка: actual значит «настоящий», а не «актуальный». Как сказать «актуальный» по-английски: relevant, current, up to date.",
    og_title="Real, not current: actual vs актуальный — Igor Shatsev",
    og_desc="actual means real. For актуальный, English says current, relevant or up to date.",
    og_alt="Real, not current. A note by Igor Shatsev on the word actual.",
    ld_headline="Real, not current: actual is not актуальный",
    contact_lede_en="Not sure which Russian words slip into your English? The trial lesson is a good place to find out. [[It’s 30 minutes, free, and you owe me nothing after it]]. If it fits, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Не уверены, какие русские слова пролезают в ваш английский? На пробном занятии это легко проверить. [[Это 30 минут, бесплатно и ни к чему не обязывает]]. Если подходит — составляем план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “actual”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «actual». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
