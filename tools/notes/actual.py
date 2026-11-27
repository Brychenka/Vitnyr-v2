"""/notes/actual/: Igor's LinkedIn post and carousel "Actual?" (8 October
2026, read from LinkedIn on 2026-11-28; reference/linkedin-posts/). The
Russian is his post, lightly cleaned (ты → вы, as on the rest of the site);
the English is a translation, a DRAFT for Igor. What was written for the
note is marked DRAFT below (SITE-PLAN.md NQ13).

Rebuilt the same day after a review (BUILD-NOTES.md): the standfirst ends
on the answer a searcher came for; the table is the cheat sheet (the
carousel's four phrases, then four more people search for); "why" carries
what the figure doesn't (where actual does belong, and actually); and the
practice is a test, the English page's own (initEarTest), because a
vocabulary note is practised by judging sentences, not by saying words.

The first vocabulary note, so it brings its own figure, a dictionary entry
(.entry): the headword, what it looks like, what it means, what to say."""
from lib import both, ear_test, head2, hit, ipa, pull, register, section, strong, tg

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'
RU = lambda s: f'<span lang="ru">{s}</span>'
CUT = lambda w: f'<span class="ear__cut">{w}</span>'

PHRASES = [
    # The carousel's four slides, in its order (slide 2 adds "the latest").
    (RU(f"Задача ещё {hit('актуальна', 'актуальна')}?"), f"Is this task still {I('relevant')}?"),
    (RU(f"{hit('Актуальная', 'Актуальная')} версия"), f"the {I('current')} (or {I('latest')}) version"),
    (RU(f"{hit('Актуальная', 'Актуальная')} информация"), f"{I('up-to-date')} information"),
    (RU(f"Уже {hit('неактуально', 'неактуально')}"), f"It’s not {I('needed')} anymore."),
    # DRAFT for Igor: not in the post; the uses people search for.
    (RU(f"Встреча ещё {hit('актуальна', 'актуальна')}?"), f"Is the meeting still {I('on')}?"),
    (RU(f"Предложение ещё {hit('актуально', 'актуально')}?"), f"Is the offer still {I('valid')}?"),
    (RU(f"{hit('Актуальная', 'Актуальная')} тема"), f"a {I('hot')} topic"),
    (RU(f"{hit('Актуальный', 'Актуальный')} курс"), f"the {I('current')} exchange rate"),
]

# Which would a native speaker say? Wrong ones: the carousel's four, then
# one DRAFT. Right ones: the post's two examples, then one DRAFT (actually).
# A miss names the Russian phrase behind it.
TEST = [
    (f"Is this task still {CUT('actual')}?", False, "«задача ещё актуальна»", "«задача ещё актуальна»",
     f"Is this task still {I('relevant')}?"),
    ("The actual deadline is Friday.", True, "", "", ""),
    (f"Please send me the {CUT('actual')} version.", False, "«актуальная версия»", "«актуальная версия»",
     f"Please send me the {I('current')} version."),
    (f"Is this information still {CUT('actual')}?", False, "«актуальная информация»", "«актуальная информация»",
     f"Is this information still {I('up to date')}?"),
    ("We had estimated about 300 visitors, but the actual number was much higher.", True, "", "", ""),
    (f"It’s not {CUT('actual')} anymore.", False, "«уже неактуально»", "«уже неактуально»",
     f"It’s not {I('needed')} anymore."),
    (f"Is the offer still {CUT('actual')}?", False, "«предложение ещё актуально»", "«предложение ещё актуально»",
     f"Is the offer still {I('valid')}?"),
    ("Actually, I meant Tuesday.", True, "", "", ""),
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
      <figcaption id="fig-actual"><span data-l="en">{strong("Fig. 1. {{actual}} is about what is real. For what matters now, English has other words.")}</span><span data-l="ru">{strong("Рис. 1. {{actual}} — про то, что есть на самом деле. Для того, что важно сейчас, в английском другие слова.")}</span></figcaption>
    </figure>"""

MSG_EN = "Hi! I took the test in your note about “actual”: {n}/{t}. I’d like a free trial English lesson."
MSG_RU = "Здравствуйте! Мой результат в тесте из заметки про «actual»: {n}/{t}. Хочу записаться на бесплатное пробное занятие по английскому."


def body(note):
    words = section("words", "\n".join([
        head2("Eight phrases. Not one actual.", "Восемь фраз. Ни одного actual.",
              "Wherever Russian says {{актуальный}}, English names what you mean: [[relevant, current, up to date, still on]].",
              "Там, где по-русски {{актуальный}}, по-английски говорят точнее: [[relevant, current, up to date, still on]]."),
        register("Eight phrases with актуальный, and what English says", "Восемь фраз с «актуальный» и как сказать по-английски",
                 [("In Russian", "По-русски"), ("In English", "По-английски")],
                 [[ru, ("register__w", en)] for ru, en in PHRASES], cls=" register--pairs"),
    ]))
    why = section("why", "\n".join([
        # DRAFT for Igor: the post says what actual means; the why (актуальный,
        # German and French) and the actually row were written for the note.
        head2("Same root, different job.", "Корень общий, смысл разный.",
              "{{актуальный}} is about now. {{actual}} is about fact: [[what really is, or really happened]]. German {{aktuell}} and French {{actuel}} mean “current” too; English went its own way. Translated into Russian, {{actual}} is one of these:",
              "{{актуальный}} — про «сейчас». {{actual}} — про факт: [[то, что есть или было на самом деле]]. Немецкое {{aktuell}} и французское {{actuel}} тоже значат «текущий», а английский пошёл своим путём. По-русски {{actual}} — это вот что:"),
        pull([
            ("настоящий, фактический", "actual", "the actual deadline"),
            ("на самом деле", "actually", both("not актуально", "не «актуально»")),
        ]),
    ]))
    test = section("practice", "\n".join([
        head2("Which would a native speaker say?", "Какие фразы сказал бы носитель?",
              "Pick every sentence that sounds right to you, then check. [[Some are fine, most are not]].",
              "Отметьте все фразы, которые звучат правильно, и проверьте. [[Какие-то в порядке, большинство — нет]]."),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ13): the offer line and the actually line are not from the post. -->",
        ear_test(TEST, MSG_EN, MSG_RU, tg(note["tg_en"])),
    ]), cls=" sec--ear")
    return "\n\n".join([words, why, test])


NOTE = dict(
    slug="actual",
    iso="2026-10-08",
    date_short_en="Oct 2026", date_short_ru="октябрь 2026",
    date_long_en="8 October 2026", date_long_ru="8 октября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7513908883929825280/",
    from_linkedin=True,
    kind_en="Vocabulary", kind_ru="Лексика",
    count_en="actual · 8 phrases · a test", count_ru="actual · 8 фраз · тест",
    title_en="Real, not current.", title_ru="Настоящий, а не актуальный.",
    short_en="Real, not current", short_ru="Настоящий, а не актуальный",
    ledger_spec=f'still {D("actual")}? <span class="ledger__to" aria-hidden="true">→</span> still {I("relevant")}?',
    card_en="Real, <em>not current.</em>", card_ru="Настоящий, <em>а не актуальный.</em>",
    card_spec='still <span class="x">actual</span>?<span class="to">→</span>still <span class="ok">relevant</span>?',
    h1_en=["Real,", "not current."], h1_ru=["Настоящий,", "а не актуальный."],
    # The post's opening, cleaned, then the answer (the post leaves it to the
    # slides). The English is a DRAFT translation.
    stand_en="If you write “Is this task still actual?” in a work chat, I have bad news for you. {{actual}} sounds like {{актуальный}}, but it means real, existing in fact. [[For актуальный, English says relevant, current or up to date.]]",
    stand_ru="Если вы пишете в рабочий чат «Is this task still actual?», у меня для вас плохие новости. {{actual}} звучит как {{актуальный}}, но значит «настоящий, действительный, реальный». [[Вместо «актуальный» по-английски говорят relevant, current или up to date.]]",
    figure=FIGURE,
    comment="/notes/actual/: Igor's LinkedIn post and carousel on actual, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="“Is this task still actual?” Actual vs актуальный — Igor Shatsev",
    title_ru_head="Актуальный по-английски: actual или relevant? — Igor Shatsev",
    desc_en="Russian speakers write “Is this task still actual?”, but actual means real, not current. Eight phrases with актуальный and what English says instead, and a quick test.",
    desc_ru="«Is this task still actual?» — частая ошибка: actual значит «настоящий». Как сказать «актуальный» по-английски: восемь фраз (relevant, current, up to date, still on) и короткий тест.",
    og_title="Real, not current: actual vs актуальный — Igor Shatsev",
    og_desc="actual means real. For актуальный, English says relevant, current or up to date. Eight phrases and a test.",
    og_alt="Real, not current. A note by Igor Shatsev on the word actual.",
    ld_headline="Real, not current: actual is not актуальный",
    contact_lede_en="Words like actual slip into English unnoticed. In the trial lesson we’ll find the ones that slip into yours. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Слова вроде actual пролезают в английский незаметно. На пробном занятии найдём те, что пролезают в ваш. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “actual”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «actual». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
