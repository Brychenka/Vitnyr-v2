"""/notes/dev-deaf/: Igor's LinkedIn post on dev and deaf (24 November
2026, read from LinkedIn on 2026-11-28; reference/linkedin-posts/BACKLOG.md
#1). The Russian is his post, lightly cleaned (вы, "I'm a dev" with its
article); the English is a translation, a DRAFT for Igor.

The post is short; the rest comes from ten slides Igor made for it and did
not post (~/Downloads/dev-deaf-10-images/, 21 Nov): the pairs list
(09-pairs), the vowel-length rule (03-length) and Russian devoicing
(06-dub). Their use is confirmed with Igor (SITE-PLAN.md NQ19). What was
written for the note is marked DRAFT below.

Planned before building (reference/linkedin-posts/REVIEW.md): serial's
ladder as the hero; the pairs as the table; the why is devoicing, with
Russian loans from English (баг, лог, блог) that carry it straight in; practice is two columns to
say out loud, as on the stress note.
"""
from lib import head2, ladder, practice_pair, pull, register, section

D = lambda w: f'<del class="mark--specimen">{w}</del>'
I = lambda w: f'<ins class="mark--target">{w}</ins>'

# Slide 09-pairs, in its order, then one DRAFT pair from work.
PAIRS = [
    ("dev", "разработчик", "deaf", "глухой"),
    ("bad", "плохой", "bat", "летучая мышь"),
    ("bag", "сумка", "back", "спина"),
    ("leave", "уходить", "leaf", "лист"),
    ("eyes", "глаза", "ice", "лёд"),
    ("prize", "приз", "price", "цена"),
    ("code", "код", "coat", "пальто"),  # DRAFT
]

# DRAFT for Igor (NQ19): not from the post or the slides.
VOICED = [
    "I’m a <b>dev</b>.",
    "Where’s my <b>bag</b>?",
    "Time to <b>leave</b>.",
    "We won the <b>prize</b>.",
    "Check the <b>code</b>.",
    "I read your <b>blog</b>.",
]
VOICELESS = [
    "She’s <b>deaf</b> in one ear.",
    "I hurt my <b>back</b>.",
    "A yellow <b>leaf</b>.",
    "What’s the <b>price</b>?",
    "Take your <b>coat</b>.",
    "Walk round the <b>block</b>.",
]

FIGURE = ladder([
    (f"I’m a de{D('f')}.", "en", "you say", "вы говорите"),
    # Slide 08-reply: what the other side of the call hears.
    ("Я <em>глухой</em>.", "ru", "they hear", "носитель слышит"),
    (f"I’m a de{I('v')}.", "en", "say", "скажите"),
], "Fig. 1. One sound, and it’s a different conversation.",
   # Slide 08-reply's line: «Один звук. Совсем другой созвон.»
   "Рис. 1. Один звук — и совсем другой созвон.", "fig-dev-deaf")


def cell(word, ru):
    """A word and its meaning in Russian, as on slide 09-pairs. Both words
    of a pair are real, so neither takes a mistake's ink."""
    return f'{word} <span class="pull__ipa" lang="ru">{ru}</span>'


def body(note):
    words = section("words", "\n".join([
        # From slide 03-length.
        head2("The vowel gives it away.", "Выдаёт гласная.",
              "The secret isn’t the last letter. [[Before a voiced consonant the vowel stretches]], and the listener hears it before the {{v}} itself.",
              "Секрет не в последней букве. [[Перед звонким согласным гласная тянется]], и это слышно раньше, чем сам {{v}}."),
        register("Seven pairs: a voiced ending and a voiceless one", "Семь пар: звонкий конец и глухой",
                 [("Voiced (v d g z)", "Звонкий (v d g z)"), ("Voiceless (f t k s)", "Глухой (f t k s)")],
                 [[cell(f"<b>{a}</b>", b), ("register__w", cell(f"<b>{c}</b>", d))]
                  for a, b, c, d in PAIRS], cls=" register--pairs"),
    ]))
    why = section("why", "\n".join([
        # From slide 06-dub; the loanword rows are DRAFT (cold review: код and приз came from French).
        head2("Russian devoices the end of a word. English doesn’t.", "В русском звонкий на конце оглушается. В английском — нет.",
              "In Russian {{дуб}} is said [дуп], {{код}} [кот], {{глаз}} [глас]: a voiced consonant at the end of a word goes voiceless, and you never hear yourself do it. [[The habit comes with you into English]], where the last sound can change the word. Words Russian borrowed from English bring it straight in:",
              "По-русски {{дуб}} звучит как [дуп], {{код}} — [кот], {{глаз}} — [глас]: звонкий на конце слова оглушается, и мы этого не замечаем. [[Эта привычка переходит и в английский]], а там от последнего звука может зависеть смысл. Легче всего она проскальзывает в словах, пришедших из английского:"),
        pull([
            ("баг [бак]", "bug", "≠ buck"),
            ("лог [лок]", "log", "≠ lock"),
            ("блог [блок]", "blog", "≠ block"),
        ]),
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "Left column: hold the vowel, then close the word softly, with no “uh” after it. Right column: keep the vowel short and the last sound crisp.",
              "Левая колонка: тяните гласную и мягко закрывайте слово, без «э» на конце. Правая: гласная короче, последний звук глухой и чёткий."),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ19): these twelve sentences are not from the post. -->",
        practice_pair(("Voiced ending", "Звонкий конец", "a longer vowel", "гласная длиннее", VOICED),
                      ("Voiceless ending", "Глухой конец", "a shorter vowel", "гласная короче", VOICELESS)),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="dev-deaf",
    iso="2026-11-24",
    date_short_en="Nov 2026", date_short_ru="ноябрь 2026",
    date_long_en="24 November 2026", date_long_ru="24 ноября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7530918568402513920/",
    from_linkedin=True,
    kind_en="Pronunciation", kind_ru="Произношение",
    count_en="dev · 7 pairs", count_ru="dev · 7 пар",
    title_en="I’m a dev, not deaf.", title_ru="Dev, а не deaf.",
    short_en="I’m a dev, not deaf", short_ru="Dev, а не deaf",
    ledger_spec=f'I’m a de{D("f")} <span class="ledger__to" aria-hidden="true">→</span> I’m a de{I("v")}',
    card_en="I’m a dev, <em>not deaf.</em>", card_ru="Dev, <em>а не deaf.</em>",
    card_spec='I’m a de<span class="x">f</span><span class="to">→</span>I’m a de<span class="ok">v</span>',
    h1_en=["I’m a dev,", "not deaf."], h1_ru=["Dev,", "а не deaf."],
    # The post, lightly cleaned. The English is a DRAFT.
    stand_en="A client of mine is a developer. When he says “I’m a dev”, it comes out as “I’m deaf”. If native speakers smile in a meeting, it isn’t always because they’re such friendly people: maybe you just made them laugh. [[Watch the voiced and voiceless sounds at the ends of words.]]",
    stand_ru="Мой клиент — разработчик. Когда он говорит «I’m a dev», слышится «I’m deaf». Если носители улыбаются на встрече, это не всегда потому, что они очень дружелюбные ребята: может, вы их просто рассмешили. [[Аккуратнее со звонкими и глухими звуками на конце слов.]]",
    figure=FIGURE,
    comment="/notes/dev-deaf/: Igor's LinkedIn post on dev and deaf, with the slides he made for it, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="“I’m a dev” or “I’m deaf”? Voiced endings in English — Igor Shatsev",
    title_ru_head="Звонкие согласные на конце слова в английском: dev или deaf — Igor Shatsev",
    desc_en="Russian speakers devoice the last consonant of a word, so “I’m a dev” comes out as “I’m deaf”. Seven pairs (bag and back, prize and price), why it happens, and sentences to say out loud.",
    desc_ru="Почему «I’m a dev» звучит как «I’m deaf»: русское оглушение согласных на конце слова. Семь пар (bag и back, prize и price), откуда берётся привычка, и фразы для тренировки вслух.",
    og_title="I’m a dev, not deaf: voiced endings in English — Igor Shatsev",
    og_desc="Russian devoices the last consonant of a word; English doesn’t. Seven pairs and sentences to say out loud.",
    og_alt="I’m a dev, not deaf. A note by Igor Shatsev on voiced endings.",
    ld_headline="I’m a dev, not deaf: voiced endings in English",
    contact_lede_en="You can’t hear your own final consonants, because to you they sound right. I can. In the trial lesson we’ll find the endings that go voiceless. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Свои конечные согласные вы не слышите: вам кажется, что всё правильно. А мне слышно. На пробном занятии найдём, где вы оглушаете согласные на конце слова. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “dev” and “deaf”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «dev» и «deaf». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
