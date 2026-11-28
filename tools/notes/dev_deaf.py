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
Russian cognates that carry it into English; practice is two columns to
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
    "He’s <b>deaf</b>.",
    "My <b>back</b> hurts.",
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
], "Fig. 1. Russian mutes the last sound of a word. English keeps it, and stretches the vowel before it.",
   "Рис. 1. Русский оглушает последний звук слова. Английский — нет, и гласная перед ним тянется.", "fig-dev-deaf")


def cell(word, ru):
    """A word and its meaning in Russian, as on slide 09-pairs. Both words
    of a pair are real, so neither takes a mistake's ink."""
    return f'{word} <span class="pull__ipa" lang="ru">{ru}</span>'


def body(note):
    words = section("words", "\n".join([
        # From slide 03-length.
        head2("A voiced ending changes the word.", "Звонкий конец меняет слово.",
              "The secret isn’t the last letter. [[Before a voiced consonant the vowel stretches]], and the listener hears it before the {{v}} itself.",
              "Секрет не в последней букве. [[Перед звонким согласным гласная тянется]], и это слышно раньше, чем сам {{v}}."),
        register("Seven pairs: a voiced ending and a voiceless one", "Семь пар: звонкий конец и глухой",
                 [("Voiced: a longer vowel", "Звонкий: гласная длиннее"), ("Voiceless: a shorter vowel", "Глухой: гласная короче")],
                 [[cell(f"<b>{a}</b>", b), ("register__w", cell(f"<b>{c}</b>", d))]
                  for a, b, c, d in PAIRS], cls=" register--pairs"),
    ]))
    why = section("why", "\n".join([
        # From slide 06-dub; the cognate rows are DRAFT.
        head2("Russian mutes the end. English doesn’t.", "Русский глушит конец. Английский — нет.",
              "In Russian {{дуб}} is said [дуп], {{код}} [кот], {{глаз}} [глас]: a voiced consonant at the end of a word goes voiceless, and nobody notices. [[The habit comes with you into English]], where the last sound can change the word. Words Russian shares with English carry it straight in:",
              "По-русски {{дуб}} звучит как [дуп], {{код}} — [кот], {{глаз}} — [глас]: звонкий на конце слова оглушается, и никто этого не замечает. [[Привычка переезжает с вами в английский]], а там от последнего звука зависит слово. Особенно легко она переходит в слова, общие для двух языков:"),
        pull([
            ("код [кот]", "code", "≠ coat"),
            ("приз [прис]", "prize", "≠ price"),
            ("блог [блок]", "blog", "≠ block"),
        ]),
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "Left column: hold the vowel and let the last sound buzz. Right column: keep the vowel short and the end crisp.",
              "Левая колонка: тяните гласную, последний звук — со звоном. Правая: гласная короче, конец чёткий."),
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
    title_en="I’m a dev, not deaf.", title_ru="Разработчик, а не глухой.",
    short_en="I’m a dev, not deaf", short_ru="Разработчик, а не глухой",
    ledger_spec=f'I’m a de{D("f")} <span class="ledger__to" aria-hidden="true">→</span> I’m a de{I("v")}',
    card_en="I’m a dev, <em>not deaf.</em>", card_ru="Разработчик, <em>а не глухой.</em>",
    card_spec='I’m a de<span class="x">f</span><span class="to">→</span>I’m a de<span class="ok">v</span>',
    h1_en=["I’m a dev,", "not deaf."], h1_ru=["Разработчик,", "а не глухой."],
    # The post, lightly cleaned. The English is a DRAFT.
    stand_en="A client of mine is a developer. When he says “I’m a dev”, it comes out as “I’m deaf”. If native speakers smile on a call, it isn’t always because they’re friendly: maybe you just made them laugh. [[Watch the voiced and voiceless sounds at the ends of words.]]",
    stand_ru="Мой клиент — разработчик. Когда он говорит «I’m a dev», слышится «I’m deaf». Если носители улыбаются на созвоне, это не всегда потому, что они очень дружелюбные: может, вы их просто рассмешили. [[Аккуратнее со звонкими и глухими звуками на конце слов.]]",
    figure=FIGURE,
    comment="/notes/dev-deaf/: Igor's LinkedIn post on dev and deaf, with the slides he made for it, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="“I’m a dev” or “I’m deaf”? Voiced endings in English — Igor Shatsev",
    title_ru_head="Звонкие согласные на конце слова в английском: dev или deaf — Igor Shatsev",
    desc_en="Russian speakers mute the last sound of a word, so “I’m a dev” comes out as “I’m deaf”. Seven pairs (bag and back, prize and price), why it happens, and sentences to say out loud.",
    desc_ru="Почему «I’m a dev» звучит как «I’m deaf»: русское оглушение согласных на конце слова. Семь пар (bag и back, prize и price), откуда привычка и фразы, чтобы потренироваться вслух.",
    og_title="I’m a dev, not deaf: voiced endings in English — Igor Shatsev",
    og_desc="Russian mutes the last sound of a word; English keeps it. Seven pairs and sentences to say out loud.",
    og_alt="I’m a dev, not deaf. A note by Igor Shatsev on voiced endings.",
    ld_headline="I’m a dev, not deaf: voiced endings in English",
    contact_lede_en="You can’t hear your own final consonants, because to you they sound right. I can. In the trial lesson we’ll find the endings that go voiceless. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Свои последние звуки не слышно: вам они кажутся правильными. Мне слышно. На пробном занятии найдём окончания, которые у вас оглушаются. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “dev” and “deaf”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «dev» и «deaf». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
