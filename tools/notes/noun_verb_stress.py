"""/notes/noun-verb-stress/: Igor's LinkedIn post on noun/verb stress
(LinkedIn showed "2w" on 2026-11-20; the exact date is SITE-PLAN.md NQ6).
The Russian is his post, lightly cleaned; the English is a translation, a
DRAFT for Igor (Q4). The practice lines are transcribed from his carousel
slides "О вещах" and "О действиях"; action ii was hidden on the screenshot
and is a stand-in (Q1)."""
from lib import head2, practice_pair, register, section, spec_pair

PAIRS = [("CON", "flict", "con", "FLICT"), ("OB", "ject", "ob", "JECT"), ("PRO", "ject", "pro", "JECT"),
         ("PRO", "gress", "pro", "GRESS"), ("CON", "tract", "con", "TRACT"), ("CON", "trast", "con", "TRAST"),
         ("EX", "port", "ex", "PORT"), ("IM", "port", "im", "PORT"), ("CON", "sole", "con", "SOLE")]  # conSOLE: Q7
THINGS = ["create an <b>OB</b>ject", "my current <b>PRO</b>ject", "any <b>PRO</b>gress on the ticket?",
          "I signed the <b>CON</b>tract", "the data <b>EX</b>port failed", "check the <b>CON</b>sole"]
ACTIONS = ["I ob<b>JECT</b> to this approach", "we pro<b>JECT</b> a two-week delay",
           "the migration is pro<b>GRESS</b>ing", "con<b>TRAST</b> the two options",
           "ex<b>PORT</b> it to CSV", "im<b>PORT</b> the module"]

FIGURE = """    <figure class="note-fig weights reveal" aria-labelledby="fig-stress">
      <div class="weights__row" aria-hidden="true">
        <span class="weights__word"><span class="weights__heavy">PRO</span><span class="weights__light">ject</span></span>
        <span class="weights__role" data-en="noun · a thing" data-ru="существительное · вещь">noun · a thing</span>
      </div>
      <div class="weights__row" aria-hidden="true">
        <span class="weights__word"><span class="weights__light">pro</span><span class="weights__heavy">JECT</span></span>
        <span class="weights__role" data-en="verb · an action" data-ru="глагол · действие">verb · an action</span>
      </div>
      <figcaption id="fig-stress"><span data-l="en">Fig. 1. PROject is a thing. The weight is on the first syllable.</span><span data-l="ru">Фиг. 1. PROject — вещь. Вес на первом слоге.</span></figcaption>
    </figure>"""


def body(note):
    words = section("words", "01", "Nine words", "Девять слов", "\n".join([
        head2("Nine words whose stress moves.", "Девять слов, у которых ударение кочует.",
              "Capitals mark the stressed syllable. One spelling, two words: [[the thing and the action]].",
              "Заглавными — ударный слог. Пишется одинаково, а слова два: [[вещь и действие]]."),
        spec_pair('my current pro<del class="mark--specimen">JECT</del>', 'my current <ins class="mark--target">PRO</ins>ject'),
        register("Nine words: stress as a noun and as a verb", "Девять слов: ударение у существительного и у глагола",
                 [("A thing (noun)", "Вещь (существительное)"), ("An action (verb)", "Действие (глагол)")],
                 [[f"<b>{a}</b>{b}", ("register__w", f"{c}<b>{d}</b>")] for a, b, c, d in PAIRS],
                 cls=" register--pairs"),
    ]))
    why = section("why", "02", "Why it happens", "Почему так", "\n".join([
        head2("Russian “проЕкт” puts the weight in the wrong pan.", "Русское «проЕкт» кладёт гирю не на ту чашу.",
              "The pattern runs all through English. Russian has plenty of look-alikes, объект, проект, контракт, and they make it easy to slip. You’ll probably still be understood, but [[it adds friction and extra work for the listener]], and that can cost you the first impression.",
              "Этот паттерн часто проскакивает в английском языке. В русском много похожих слов, и из-за них легко ошибиться: объект, проект, контракт и т. д. Тебя, скорее всего, всё равно поймут, но [[это создаёт лишнее когнитивное трение и лишнюю работу для слушателя]], которая может ухудшить первое впечатление."),
        """  <dl class="note-stats">
    <div class="reveal"><dt>94%</dt><dd><span data-l="en">of two-syllable nouns are stressed on the first syllable</span><span data-l="ru">двусложных существительных — с ударением на первом слоге</span></dd></div>
    <div class="reveal"><dt>69%</dt><dd><span data-l="en">of two-syllable verbs are stressed on the second</span><span data-l="ru">двусложных глаголов — с ударением на втором</span></dd></div>
  </dl>
  <p class="note-cite reveal">Kelly &amp; Bock (1988). Stress in time. <i>Journal of Experimental Psychology: Human Perception and Performance</i>, 14(3), 389–403.</p>""",
    ]))
    say = section("practice", "03", "Say it out loud", "Скажите вслух", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "The capitals carry the weight. Read the things, then the actions.",
              "Вес — на заглавных. Сначала вещи, потом действия."),
        "  <!-- From the carousel slides \"О вещах\" and \"О действиях\". DRAFT for Igor (Q1): action ii was hidden on the screenshot and is a stand-in. -->",
        practice_pair(("Things", "О вещах", "stress on the first syllable", "ударение на первом слоге", THINGS),
                      ("Actions", "О действиях", "stress on the second syllable", "ударение на втором слоге", ACTIONS)),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="noun-verb-stress",
    iso="2026-11",  # PLACEHOLDER (SITE-PLAN.md NQ6): LinkedIn showed "2w" on 2026-11-20
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="November 2026", date_long_ru="ноябрь 2026",
    linkedin=None,
    from_linkedin=True,
    kind_en="Stress", kind_ru="Ударение",
    count_en="noun → verb · 9 words", count_ru="сущ. → глагол · 9 слов",
    title_en="The weight of stress.", title_ru="О весе ударения.",
    short_en="The weight of stress", short_ru="О весе ударения",
    ledger_spec='my current pro<del class="mark--specimen">JECT</del> <span class="ledger__to" aria-hidden="true">→</span> <ins class="mark--target">PRO</ins>ject',
    card_en="The weight <em>of stress.</em>", card_ru="О весе <em>ударения.</em>",
    card_spec='my current pro<span class="x">JECT</span><span class="to">→</span><span class="ok">PRO</span>ject',
    h1_en=["The weight", "of stress."], h1_ru=["О весе", "ударения."],
    stand_en="Another set of words my IT clients trip over, the same way they do with CONflict and conFLICT. [[As a noun, the weight sits on the first syllable. As a verb, it moves to the second.]]",
    stand_ru="Собрал ещё ряд слов, на ударении в которых спотыкаются мои IT-клиенты, как с CONflict и conFLICT. [[У существительного вес на первом слоге, у глагола — на втором.]]",
    figure=FIGURE,
    comment="/notes/noun-verb-stress/: Igor's LinkedIn post on noun/verb stress, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="PROject or proJECT? Noun and verb stress in English — Igor Shatsev",
    title_ru_head="PROject или proJECT? Ударение в существительных и глаголах — Igor Shatsev",
    desc_en="OBject or obJECT, PROject or proJECT: nine IT words that move their stress when the noun becomes a verb, and why Russian pulls it to the wrong syllable.",
    desc_ru="OBject или obJECT, PROject или proJECT: девять IT-слов, у которых ударение кочует между существительным и глаголом, и почему русский тянет его не туда.",
    og_title="The weight of stress: PROject or proJECT? — Igor Shatsev",
    og_desc="Nine IT words whose stress moves when the noun becomes a verb.",
    og_alt="The weight of stress. A note by Igor Shatsev on noun and verb stress.",
    ld_headline="The weight of stress: PROject or proJECT?",
    nav=[("01", "#words", "The words", "Слова"), ("02", "#why", "Why it happens", "Почему так"),
         ("03", "#practice", "Say it out loud", "Скажите вслух")],
    contact_lede_en="Not sure where your stress falls? The trial lesson is a good place to find out. [[It’s 30 minutes, free, and you owe me nothing after it]]. Online or in Yerevan.",
    contact_lede_ru="Не уверены, куда падает ваше ударение? На пробном занятии это легко проверить. [[Это 30 минут, бесплатно и ни к чему не обязывает]]. Онлайн или в Ереване.",
    tg_en="Hi! I came from your note about word stress. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про ударение. Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
