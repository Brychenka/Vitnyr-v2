"""/notes/weigh/: Igor's LinkedIn post and slide on weight and weigh
(22 October 2026, read from LinkedIn on 2026-11-28; reference/linkedin-posts/).
The only one of the eight posts written in English: here the English is his
post, lightly cleaned, and the Russian is a translation, a DRAFT for Igor.
What was written for the note is marked DRAFT below (SITE-PLAN.md NQ16).

Planned before building (reference/linkedin-posts/REVIEW.md): the headline
is the slide's line; the hero is the slide's picture as the au note's tiles
(WEIGHT over WEIGH, the t gone); the table is the cheat sheet, with one
honest row (a weighted average); "why" is the post's reason, nouns working
as verbs; practice is the ear test.
"""
from lib import ear_test, head2, hit, ipa, pull, register, section, strong, tg, tile

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'
RU = lambda s: f'<span lang="ru">{s}</span>'
CUT = lambda w: f'<span class="ear__cut">{w}</span>'

PHRASES = [
    # DRAFT for Igor: the post's two sentences are rows 2 and 3; the rest are the note's.
    (RU(f"Я {hit('вешу', 'вешу')} 80 кг."), f"I {I('weigh')} 80 kg."),
    (RU(f"Я {hit('весил', 'весил')} 80 кг."), f"I {I('weighed')} 80 kg."),
    (RU(f"Это {hit('весит', 'весит')} 2 фунта."), f"It {I('weighs')} 2 pounds."),
    (RU(f"Сколько вы {hit('весите', 'весите')}?"), f"How much do you {I('weigh')}?"),
    (RU(f"Можете {hit('взвесить', 'взвесить')}?"), f"Could you {I('weigh')} it?"),
    (RU(f"Мой {hit('вес', 'вес')}"), f"my {I('weight')}"),
    (RU(f"{hit('Средневзвешенное', 'взвешенное')} значение"), f"a {I('weighted')} average"),
]

# Five wrong, three right. The post's own: I weighted 80 kg, It weights 2
# pounds. The rest are DRAFT. "A weighted average" is right on purpose.
TEST = [
    (f"I {CUT('weighted')} 80 kg last year.", False, "«я весил»", "«я весил»",
     f"I {I('weighed')} 80 kg last year."),
    ("What’s your weight?", True, "", "", ""),
    (f"It {CUT('weights')} two pounds.", False, "«это весит»", "«это весит»",
     f"It {I('weighs')} two pounds."),
    (f"How much do you {CUT('weight')}?", False, "«сколько вы весите»", "«сколько вы весите»",
     f"How much do you {I('weigh')}?"),
    ("The baby weighed 3.5 kg at birth.", True, "", "", ""),
    (f"Can you {CUT('weight')} my bag?", False, "«взвесить»", "«взвесить»",
     f"Can you {I('weigh')} my bag?"),
    ("We used a weighted average.", True, "", "", ""),
    (f"My suitcase {CUT('weights')} too much.", False, "«чемодан весит»", "«чемодан весит»",
     f"My suitcase {I('weighs')} too much."),
]

T = "".join(tile(c) for c in "WEIGH")
FIGURE = f"""    <figure class="note-fig tiles reveal" aria-labelledby="fig-weigh">
      <div class="tiles__row" aria-hidden="true">{T}{tile('T', ' tile--specimen')}</div>
      <div class="tiles__row" aria-hidden="true">{"".join(tile(c, ' tile--target') for c in "WEIGH")}</div>
      <figcaption id="fig-weigh"><span data-l="en">{strong("Fig. 1. Weighing has no t.")} I {D("weighted")} → I {I("weighed")} 80 kg.</span><span data-l="ru">{strong("Рис. 1. У «весить» нет t.")} I {D("weighted")} → I {I("weighed")} 80 kg.</span></figcaption>
    </figure>"""

MSG_EN = "Hi! I took the test in your note about “weigh”: {n}/{t}. I’d like a free trial English lesson."
MSG_RU = "Здравствуйте! Мой результат в тесте из заметки про «weigh»: {n}/{t}. Хочу записаться на бесплатное пробное занятие по английскому."


def body(note):
    words = section("words", "\n".join([
        head2("Every form, no t.", "Ни в одной форме нет t.",
              f"{{{{weigh}}}}, {{{{weighs}}}}, {{{{weighed}}}}, {{{{weighing}}}}. [[weigh sounds like way, {ipa('/weɪ/')}]]; weighed is {ipa('/weɪd/')}.",
              f"{{{{weigh}}}}, {{{{weighs}}}}, {{{{weighed}}}}, {{{{weighing}}}}. [[weigh звучит как way, {ipa('/weɪ/')}]]; weighed — {ipa('/weɪd/')}."),
        register("Seven phrases with вес and весить, and what English says",
                 "Семь фраз с «вес» и «весить» и как сказать по-английски",
                 [("In Russian", "По-русски"), ("In English", "По-английски")],
                 [[ru, ("register__w", en)] for ru, en in PHRASES], cls=" register--pairs"),
        # DRAFT for Igor: the weighted row's footnote.
        '  <p class="note-cite reveal"><span data-l="en">No slip in the last row: weight is a verb too, but it means to add '
        'weight (a weighted blanket) or to give extra importance (a weighted average). It never means to measure.</span>'
        '<span data-l="ru">В последней строке ошибки нет: weight — тоже глагол, но значит «утяжелить» (weighted blanket — '
        'утяжелённое одеяло) или «придать вес» (weighted average — средневзвешенное). «Взвешивать» оно не значит.</span></p>',
    ]))
    why = section("why", "\n".join([
        # Cold review: the first heading said this noun doesn't work as a verb,
        # but to weight is a verb (weight the data); and "older" was loose.
        head2("Nouns turn into verbs. Weighing has its own.", "Существительное становится глаголом. Но у «весить» своё слово.",
              "Nouns in English often work overtime as verbs: you {{email}} someone, you {{text}} them. So {{weight}} looks like the verb for weighing. [[It’s the other way round: weight comes from weigh.]]",
              "В английском существительные часто работают глаголами: {{to email}} — написать письмо, {{to text}} — написать сообщение. Вот и {{weight}} кажется глаголом «весить». [[На деле всё наоборот: weight происходит от weigh.]]"),
        # DRAFT for Igor: the post states the reason; the rows are the note's.
        pull([
            ("написать письмо", "to email", "= an email"),
            ("написать сообщение", "to text", "= a text"),
            ("весить, взвесить", "to weigh", "≠ a weight"),
        ]),
    ]))
    test = section("practice", "\n".join([
        head2("Which would a native speaker say?", "Какие фразы сказал бы носитель?",
              "Pick every sentence that sounds right to you, then check. [[One of them has a t on purpose]].",
              "Отметьте все фразы, которые звучат правильно, и проверьте. [[В одной t стоит не случайно]]."),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ16): the sentences beyond the post's two. -->",
        ear_test(TEST, MSG_EN, MSG_RU, tg(note["tg_en"])),
    ]), cls=" sec--ear")
    return "\n\n".join([words, why, test])


NOTE = dict(
    slug="weigh",
    iso="2026-10-22",
    date_short_en="Oct 2026", date_short_ru="октябрь 2026",
    date_long_en="22 October 2026", date_long_ru="22 октября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7518999079339737088/",
    from_linkedin=True,
    kind_en="Grammar", kind_ru="Грамматика",
    count_en="weigh · 7 phrases · a test", count_ru="weigh · 7 фраз · тест",
    title_en="Doing it? Drop the t.", title_ru="Это действие? Уберите t.",
    short_en="Doing it? Drop the t", short_ru="Это действие? Уберите t",
    ledger_spec=f'I {D("weighted")} 80 kg <span class="ledger__to" aria-hidden="true">→</span> I {I("weighed")} 80 kg',
    card_en="Doing it? <em>Drop the t.</em>", card_ru="Это действие? <em>Уберите t.</em>",
    card_spec='I <span class="x">weighted</span><span class="to">→</span>I <span class="ok">weighed</span>',
    h1_en=["Doing it?", "Drop the t."], h1_ru=["Это действие?", "Уберите t."],
    # The post's opening, then its answer. The Russian is a DRAFT translation.
    stand_en="I’ve seen this mistake a thousand times, and it’s understandable: “I weighted 80 kg”, “It weights 2 pounds”. [[The noun is weight; the verb is weigh, said like way.]]",
    stand_ru="Я видел эту ошибку тысячу раз, и понятно, откуда она берётся: «I weighted 80 kg», «It weights 2 pounds». [[Существительное — weight, глагол — weigh, и звучит он как way.]]",
    figure=FIGURE,
    comment="/notes/weigh/: Igor's LinkedIn post and slide on weight and weigh, set as a note. The English is his post, lightly cleaned; the Russian is a translation, a draft for Igor to confirm.",
    title="“I weighted 80 kg”? Weight vs weigh — Igor Shatsev",
    title_ru_head="Весить по-английски: weight или weigh? — Igor Shatsev",
    desc_en="“I weighted 80 kg” and “It weights 2 pounds” are wrong: the verb is weigh, said like way. Seven phrases with вес and весить, when weighted is right, and a quick test.",
    desc_ru="«I weighted 80 kg» — ошибка: глагол «весить» — weigh, звучит как way. Семь фраз с «вес» и «весить», когда weighted всё-таки верно, и короткий тест.",
    og_title="Doing it? Drop the t: weight vs weigh — Igor Shatsev",
    og_desc="weight is the thing; to weigh is the action, said like way. Seven phrases and a test.",
    og_alt="Doing it? Drop the t. A note by Igor Shatsev on weight and weigh.",
    ld_headline="Doing it? Drop the t: weight vs weigh",
    contact_lede_en="One letter too many is easy to miss in your own speech. I’ll hear it straight away, and that’s what the trial lesson is for. [[It’s 30 minutes, free, and you owe me nothing after it]]. If it fits, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Одну лишнюю букву в своей речи легко пропустить. Я услышу её сразу — для этого и нужно пробное занятие. [[Это 30 минут, бесплатно и ни к чему не обязывает]]. Если подходит — составляем план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “weigh”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «weigh». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
