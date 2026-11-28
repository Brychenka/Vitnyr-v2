"""/notes/manage/: Igor's LinkedIn post and two slides on manage to
(1 October 2026, read from LinkedIn on 2026-11-28; the text and the slides
are in reference/linkedin-posts/BACKLOG.md). The Russian is his post,
lightly cleaned (ты → вы); the English is a translation, a DRAFT for Igor.
What was written for the note is marked DRAFT below (SITE-PLAN.md NQ18).

Planned before building (reference/linkedin-posts/REVIEW.md): the post
names a gap (manage is known only as управлять), so the note names what
fills it, could (DRAFT). Reviewed cold and rebuilt the same day; the hero is actual's dictionary entry; "why" is
мог is could, смог is managed to; practice is the test, with slide 2's three
sentences in it.
"""
from lib import both, ear_test, head2, hit, ipa, pull, register, section, strong, tg

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'
RU = lambda s: f'<span lang="ru">{s}</span>'
CUT = lambda w: f'<span class="ear__cut">{w}</span>'

PHRASES = [
    # The post's two.
    (RU(f"Я {hit('справлюсь', 'справлюсь')}."), f"I’ll {I('manage')}."),
    (RU(f"У меня {hit('получилось', 'получилось')} пофиксить баг."), f"I {I('managed to')} fix the bug."),
    # DRAFT for Igor: not in the post.
    (RU(f"Еле {hit('успел', 'успел')} на рейс."), f"I only just {I('managed to')} catch my flight."),
    (RU(f"Как вы {hit('справляетесь', 'справляетесь')}?"), f"How are you {I('managing')}?"),
    (RU(f"{hit('Сможете', 'Сможете')} в пятницу?"), f"Can you {I('manage')} Friday?"),
    (RU(f"Не {hit('удалось', 'удалось')} дозвониться."), f"I didn’t {I('manage to')} get through to her."),
]

# Which would a native speaker say? Five wrong, three right. Slide 2's
# three sentences come first, as English: the first wrong (could), the other
# two right. The rest are DRAFT. Cold review: each wrong could is anchored in
# the past (out of context "I could deploy it by Friday" is a fine offer),
# and one wrong sentence drops the to, so could isn't the only pattern.
# "We couldn't agree on a price" is right on purpose: not managing can take
# couldn't.
TEST = [
    (f"Yesterday I {CUT('could')} deploy it just before the deadline.", False, "«мне удалось»", "«мне удалось»",
     f"Yesterday I {I('managed to')} deploy it just before the deadline."),
    ("Don’t worry, I’ll manage.", True, "", "", ""),
    ("We didn’t manage to reach an agreement with the client.", True, "", "", ""),
    (f"Finally I {CUT('could')} fix the bug.", False, "«у меня получилось»", "«у меня получилось»",
     f"Finally I {I('managed to')} fix the bug."),
    ("We couldn’t agree on a price.", True, "", "", ""),
    (f"I {CUT('succeeded to')} finish the report on time.", False, "«мне удалось закончить»", "«мне удалось закончить»",
     f"I {I('managed to')} finish the report on time."),
    (f"We {CUT('managed solve')} it in one day.", False, "«удалось решить»", "«удалось решить»",
     f"We {I('managed to solve')} it in one day."),
    (f"After three tries I {CUT('could')} log in.", False, "«удалось войти»", "«удалось войти»",
     f"After three tries I {I('managed to')} log in."),
]


def role(en, ru):
    return f'<span class="weights__role" data-en="{en}" data-ru="{ru}">{en}</span>'


FIGURE = f"""    <figure class="note-fig entry reveal" aria-labelledby="fig-manage">
      <p class="entry__head" lang="en"><span class="entry__w">manage</span>{ipa("/ˈmænɪdʒ/")}</p>
      <div class="ladder">
        <div class="ladder__row"><span class="ladder__s" lang="ru">управлять</span>{role("you know", "вы знаете")}</div>
        <div class="ladder__row"><span class="ladder__s" lang="ru">справиться, суметь</span>{role("it also means", "а ещё значит")}</div>
        <div class="ladder__row"><span class="ladder__s" lang="en">I {D("could")} {I("managed to")} fix it</span>{role("say", "говорите так")}</div>
      </div>
      <figcaption id="fig-manage"><span data-l="en">{strong("Fig. 1. {{manage to}}: it wasn’t easy, but you did it.")}</span><span data-l="ru">{strong("Рис. 1. {{manage to}} — было непросто, но вы смогли.")}</span></figcaption>
    </figure>"""

MSG_EN = "Hi! I took the test in your note about “manage”: {n}/{t}. I’d like a free trial English lesson."
MSG_RU = "Здравствуйте! Мой результат в тесте из заметки про «manage»: {n}/{t}. Хочу записаться на бесплатное пробное занятие по английскому."


def body(note):
    words = section("words", "\n".join([
        head2("Six phrases. Not one manager.", "Шесть фраз. Ни одного менеджера.",
              "{{managed to}} takes a plain verb: managed to fix, managed to catch. [[Without a verb, manage alone means справиться: I’ll manage.]]",
              "После {{managed to}} — глагол без изменений: managed to fix, managed to catch. [[Без глагола manage — это «справиться»: I’ll manage.]]"),
        register("Six phrases with справиться and получилось, and what English says",
                 "Шесть фраз со «справиться» и «получилось» и как сказать по-английски",
                 [("In Russian", "По-русски"), ("In English", "По-английски")],
                 [[ru, ("register__w", en)] for ru, en in PHRASES], cls=" register--pairs"),
    ]))
    why = section("why", "\n".join([
        # DRAFT for Igor: the why is the note's; the post gives the meaning.
        head2("Мог is could. Смог isn’t.", "Мог — это could. Смог — нет.",
              "School teaches {{could}} as {{мочь}}, so {{смог}} turns into could too. But could is {{мог}}: what you were able to do in general. [[Смог, a one-off success that took effort, is managed to]] (or was able to).",
              "В школе {{could}} учат как {{мочь}}, и {{смог}} тоже становится could. Но could — это {{мог}}: что вы умели вообще. [[А «смог» — разовый успех, который дался с трудом, — это managed to]] (или was able to)."),
        pull([
            ("в пять лет я мог читать", "could", both("in general", "умел вообще")),
            ("я смог починить", "managed to", both("once, with effort", "один раз, с трудом")),
            ("не смог договориться", "couldn’t", "= didn’t manage to"),
        ]),
    ]))
    test = section("practice", "\n".join([
        head2("Which would a native speaker say?", "Какие фразы сказал бы носитель?",
              "Pick every sentence that sounds right to you, then check. [[One of them has couldn’t on purpose]].",
              "Отметьте все фразы, которые звучат правильно, и проверьте. [[В одной couldn’t стоит не случайно]]."),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ18): the sentences beyond slide 2's three. -->",
        ear_test(TEST, MSG_EN, MSG_RU, tg(note["tg_en"])),
    ]), cls=" sec--ear")
    return "\n\n".join([words, why, test])


NOTE = dict(
    slug="manage",
    iso="2026-10-01",
    date_short_en="Oct 2026", date_short_ru="октябрь 2026",
    date_long_en="1 October 2026", date_long_ru="1 октября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7511389838995062785/",
    from_linkedin=True,
    kind_en="Vocabulary", kind_ru="Лексика",
    count_en="manage · 6 phrases · a test", count_ru="manage · 6 фраз · тест",
    title_en="Not just for managers.", title_ru="Не только для менеджеров.",
    short_en="Not just for managers", short_ru="Не только для менеджеров",
    ledger_spec=f'I {D("could")} fix it yesterday <span class="ledger__to" aria-hidden="true">→</span> I {I("managed to")} fix it yesterday',
    card_en="Not just <em>for managers.</em>", card_ru="Не только <em>для менеджеров.</em>",
    card_spec='I <span class="x">could</span><span class="to">→</span>I <span class="ok">managed to</span>',
    h1_en=["Not just", "for managers."], h1_ru=["Не только", "для менеджеров."],
    # The post's opening, cleaned, then its answer. The English is a DRAFT.
    stand_en="Most B1 learners don’t know the most useful meaning of {{manage}}. When I ask my students, the first word they think of is управлять. It has another meaning, more versatile and more useful: [[manage to means справиться, получилось: it wasn’t easy, but you did it.]]",
    stand_ru="Большинство учеников уровня B1 не знакомы с самым полезным значением слова {{manage}}. Когда я их спрашиваю, первая ассоциация — «управлять». У него есть ещё одно значение, более универсальное и полезное: [[manage to — справиться, получилось: было непросто, но вы смогли.]]",
    figure=FIGURE,
    comment="/notes/manage/: Igor's LinkedIn post and slides on manage to, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="“I could fix it”? Manage to vs could — Igor Shatsev",
    title_ru_head="«Удалось» и «справился» по-английски: manage to — Igor Shatsev",
    desc_en="manage isn’t only управлять: manage to means справиться, получилось. Why “I could fix it” is wrong for one success, six phrases with manage, and a quick test.",
    desc_ru="Как сказать «удалось», «получилось», «справлюсь» по-английски: manage to, а не could. Шесть фраз с manage, почему «I could fix it» звучит не так и короткий тест.",
    og_title="Not just for managers: manage to vs could — Igor Shatsev",
    og_desc="manage to means справиться, получилось: it wasn’t easy, but you did it. Six phrases and a test.",
    og_alt="Not just for managers. A note by Igor Shatsev on manage to.",
    ld_headline="Not just for managers: manage to, not could",
    contact_lede_en="A could where managed to belongs is easy to miss in your own speech. In the trial lesson I’ll catch slips like this as you talk. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Could на месте managed to в своей речи легко не заметить. На пробном занятии я поймаю такие оговорки прямо в разговоре. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “manage”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «manage». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
