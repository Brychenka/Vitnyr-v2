"""/notes/cafe/: Igor's LinkedIn post on café (5 October 2026, read from
LinkedIn on 2026-11-28; reference/linkedin-posts/BACKLOG.md #4). The
Russian is his post, lightly cleaned (its English words "mispronounced" and
"origin" put into Russian); the English is a translation, a DRAFT for Igor.

The post gives the mistake and both fixes. His one slide is the cover
(«Что не так с «кафэ» по-английски?»), which is the Russian headline.
Everything past the post is marked DRAFT below (SITE-PLAN.md NQ20).

Planned before building (reference/linkedin-posts/REVIEW.md): the au
note's tiles as the hero; the post's two sounds as the fix; the why is the
French é and English's /eɪ/, with six French words Russian and English
share; practice is "Say it out loud".
"""
from lib import head2, hit, ipa, practice, pull, register, section, strong, tile

EI_IPA = ipa("/eɪ/")

D = lambda w_: f'<del class="mark--specimen">{w_}</del>'
I = lambda w_: f'<ins class="mark--target">{w_}</ins>'
EI = '<span class="mark--target">eɪ</span>'
RU = lambda s: f'<span lang="ru">{s}</span>'

# DRAFT for Igor: six French words Russian and English both took. Russian
# ends them on э; English on /eɪ/. British IPA.
WORDS = [
    ("кафе", "café", "/ˈkæf{}/"),
    ("резюме", "résumé", "/ˈrezjuːm{}/"),
    ("клише", "cliché", "/ˈkliːʃ{}/"),
    ("пюре", "purée", "/ˈpjʊər{}/"),
    ("суфле", "soufflé", "/ˈsuːfl{}/"),
    ("канапе", "canapé", "/ˈkænəp{}/"),
]

# DRAFT for Igor (SITE-PLAN.md NQ20): not from the post.
PRACTICE = [
    "Let’s meet at the <b>café</b> downstairs.",
    "I’ve attached my <b>résumé</b>.",
    "That’s a bit of a <b>cliché</b>.",
    "There were <b>canapés</b> after the talk.",
    "The chocolate <b>soufflé</b> is worth the wait.",
    "I’ll have the fish with pea <b>purée</b>.",
]

FIGURE = f"""    <figure class="note-fig tiles reveal" aria-labelledby="fig-cafe">
      <div class="tiles__row" aria-hidden="true">{tile('C')}{tile('A', ' tile--specimen')}{tile('F')}{tile('É', ' tile--specimen')}</div>
      <div class="tiles__row" aria-hidden="true">{tile('C')}{tile('æ', ' tile--target', ' ipa')}{tile('F')}{tile('eɪ', ' tile--target tile--merged', ' ipa')}</div>
      <figcaption id="fig-cafe"><span data-l="en">{strong("Fig. 1. In café, the a and the é change.")} {D("кафэ")} becomes {I("кæфэй")}.</span><span data-l="ru">{strong("Рис. 1. В café меняются a и é.")} {D("кафэ")} превращается в {I("кæфэй")}.</span></figcaption>
    </figure>"""


def body(note):
    words = section("words", "\n".join([
        head2("Two sounds to change.", "Поменяйте два звука.",
              f"The first vowel is {ipa('/æ/')}: something between а and э, with the mouth open wide. The ending is {ipa('/eɪ/')}, as in day or okay. [[Together: {ipa('/ˈkæfeɪ/')}.]]",
              f"Первый гласный — {ipa('/æ/')}: что-то между «а» и «э», открывайте рот широко. Конец — {ipa('/eɪ/')}, как в day или okay. [[Вместе: {ipa('/ˈkæfeɪ/')}.]]"),
        pull([
            (f"к{D('а')}фэ", hit("café", "a"), ipa("/æ/")),
            (f"каф{D('э')}", hit("café", "é"), ipa("/eɪ/")),
        ]),
        # DRAFT for Igor: not in the post.
        '  <p class="note-cite reveal"><span data-l="en">Russian stresses the end, кафе́; British English stresses the first syllable. '
        'Americans usually stress the end and keep the same ' + EI_IPA + '. The word is often written cafe, '
        'without the mark, and sounds no different.</span><span data-l="ru">По-русски ударение на конце, кафе́; в британском английском — на первом слоге. '
        'Американцы обычно ставят ударение на последний слог, а ' + EI_IPA + ' остаётся тем же. По-английски слово часто пишут cafe, без значка; '
        'звучит оно так же.</span></p>',
    ]))
    why = section("why", "\n".join([
        # The post: the mark shows French origin. The mechanism is DRAFT.
        head2("The mark over the e says French.", "Значок над e — след французского.",
              "Russian took {{кафе}} from French and ends it on э. But French é is a closed [e], nearer to English " + EI_IPA + " than to э, and [[no English word ends in a short э]]. So English says é as " + EI_IPA + ". The same goes for these French words both languages share:",
              "Русский язык заимствовал {{кафе}} из французского и произносит конец как «э». Но французское é — закрытое [e], оно ближе к английскому " + EI_IPA + ", чем к «э», а [[на короткое «э» английские слова не заканчиваются]]. Поэтому в английском é звучит как " + EI_IPA + ". То же — во французских словах, которые есть в обоих языках:"),
        "  <!-- DRAFT for Igor (SITE-PLAN.md NQ20): the six words are not from the post. -->",
        register("Six French words in Russian and in English", "Шесть французских слов по-русски и по-английски",
                 [("In Russian", "По-русски"), ("In English", "По-английски"), ("Sound (British)", "Звучание (брит.)")],
                 [[RU(ru), ("register__w", f"<b>{en}</b>"), ("register__ipa", ipa(tr.format(EI)))]
                  for ru, en, tr in WORDS]),
        # Cold review: learners over-apply the rule to the first é of résumé.
        '  <p class="note-cite reveal"><span data-l="en">In résumé only the last é is ' + EI_IPA + '; the first one is short, as in bed.</span>'
        '<span data-l="ru">В résumé ' + EI_IPA + ' — только последнее é; первое короткое, как в bed.</span></p>',
    ]))
    say = section("practice", "\n".join([
        head2("Say it out loud.", "Скажите вслух.",
              "In café and canapé, open the mouth wide for the first {{a}}. Finish every word on " + EI_IPA + ", as in day.",
              "В café и canapé на первое {{a}} открывайте рот широко. Каждое слово заканчивайте на " + EI_IPA + ", как в day."),
        practice(PRACTICE, "DRAFT for Igor (SITE-PLAN.md NQ20): these six sentences are not from the post."),
    ]))
    return "\n\n".join([words, why, say])


NOTE = dict(
    slug="cafe",
    iso="2026-10-05",
    date_short_en="Oct 2026", date_short_ru="октябрь 2026",
    date_long_en="5 October 2026", date_long_ru="5 октября 2026",
    linkedin="https://www.linkedin.com/feed/update/urn:li:activity:7512837899248381952/",
    from_linkedin=True,
    kind_en="Pronunciation", kind_ru="Произношение",
    count_en="café · 6 words", count_ru="café · 6 слов",
    title_en="What’s wrong with your café?", title_ru="Что не так с «кафэ»?",
    short_en="What’s wrong with your café", short_ru="Что не так с «кафэ»",
    ledger_spec=f'{D("кафэ")} <span class="ledger__to" aria-hidden="true">→</span> {I("кæфэй")}',
    card_en="What’s wrong <em>with your café?</em>", card_ru="Что не так <em>с «кафэ»?</em>",
    card_spec='<span class="x">кафэ</span><span class="to">→</span><span class="ok">кæфэй</span>',
    h1_en=["What’s wrong", "with your café?"], h1_ru=["Что не так", "с «кафэ»?"],
    # The post, lightly cleaned. The English is a DRAFT.
    stand_en="One of the words my students get wrong most often is café. Few people notice the mark over the e: it shows the word came from French. I don’t know much French myself, but enough to watch how I pronounce it. Everyone I’ve worked with says it the Russian way, кафэ. [[The first vowel and the ending both change.]]",
    stand_ru="Café — одно из слов, которые ученики чаще всего произносят неправильно. Мало кто замечает значок над буквой e: он указывает на французское происхождение. Французский я знаю не очень, но достаточно, чтобы следить за произношением. Те, с кем я работал, поголовно говорят на русский манер: «кафэ». [[Меняются первый гласный и конец.]]",
    figure=FIGURE,
    comment="/notes/cafe/: Igor's LinkedIn post on café, set as a note. The Russian is his post, lightly cleaned; the English is a translation, a draft for Igor to confirm.",
    title="How to pronounce café in English — Igor Shatsev",
    title_ru_head="Как произносить café по-английски — Igor Shatsev",
    desc_en="Russian speakers say café as кафэ. Two sounds change: the a is /æ/ and the é is /eɪ/, as in day. Why it happens, five more French words that end the same way, and sentences to say out loud.",
    desc_ru="Как правильно произносить café по-английски: не «кафэ», а «кæфэй». Два звука, которые нужно поменять, почему так, ещё пять французских слов с тем же концом и фразы для тренировки вслух.",
    og_title="What’s wrong with your café? How to say it in English — Igor Shatsev",
    og_desc="Café isn’t кафэ: the a is /æ/ and the é is /eɪ/, as in day. Six French words and how they sound.",
    og_alt="What’s wrong with your café? A note by Igor Shatsev on saying café.",
    ld_headline="What’s wrong with your café? How to say it in English",
    contact_lede_en="Words like café slip past you because you have said them in Russian all your life. In the trial lesson I’ll pick out the ones that still sound Russian. [[It’s 30 minutes, free, no strings attached]]. If we’re a good fit, we agree on a plan, online or in Yerevan.",
    contact_lede_ru="Такие слова, как café, проскакивают незаметно: по-русски вы говорите их всю жизнь. На пробном занятии я найду те, что у вас всё ещё звучат по-русски. [[Это 30 минут, бесплатно, без обязательств]]. Если подойдём друг другу, составим план, онлайн или в Ереване.",
    tg_en="Hi! I came from your note about “café”. I'd like to book a free trial English lesson.",
    tg_ru="Здравствуйте! Я с вашей заметки про «café». Хочу записаться на бесплатное занятие по английскому.",
    body=body,
)
