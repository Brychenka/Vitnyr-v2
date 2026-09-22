/* ============================================================
   Vitnyr — v2 motion
   One easing curve everywhere: cubic-bezier(.16, 1, .3, 1).
   One reveal rhythm: fade + 24px rise, 0.9s, 0.08s stagger, once.
   Pointer feedback: one dot that rides the pointer everywhere and answers a
   control by easing its fill to the page's accent ink — colour, not size, and
   no magnetic pull (both retired at C14). Not "the signature move" — from the
   Spark Order's S6 correction on, that performed edit is the page's one move;
   the cursor is just the pointer answering back.
   Everything degrades: no JS, no GSAP, reduced motion, touch, or a
   tab opened in the background all end with the same readable page.
   ============================================================ */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;

  // If GSAP didn't arrive, drop the hidden state and stop.
  if (!window.gsap) { root.classList.remove('js'); return; }

  // The guide's curve, as a real GSAP ease so JS and CSS match exactly.
  var EASE = 'power4.out';
  if (window.CustomEase) { CustomEase.create('brand', '.16, 1, .3, 1'); EASE = 'brand'; }

  /* Six durations, and nothing between them. Every ANIMATION timing on the
     page comes from this table so the whole thing reads as one instrument.
     Scrolling is separate: Lenis's own duration (1.1) and the two scrollTo
     calls (1.2) are scroll physics, not animation, and live outside the table.
       micro   — a thing appearing or disappearing outright
       state   — a hover, a magnet, a theme settling (this is --t in the sheet)
       follow  — the pointer catching up: a lag, not a duration
       correct — the specimen reflowing closed over a deleted word (S6)
       count   — a measured number running up to its value; the reference
                 length, scaled per number so each reads as its own instrument
       hero    — the single longest move on the page, used once
     The reveal's own 0.9s lives in the stylesheet, where the transition is. */
  var D = { micro: 0.3, state: 0.6, follow: 0.45, correct: 0.8, hero: 1.05 };
  var STAGGER = 0.08;

  /* ---------- first-frame gate ----------
     A tab that loads hidden has rAF suspended: gsap.ticker never advances and
     anything tween-driven sits at its from-state until the tab is looked at.
     So nothing time-based starts until a frame has actually been rendered.
     The test is rAF itself rather than document.hidden, because rAF is the
     thing the tweens need — it is deferred for a hidden tab and released the
     moment the page paints, whatever the visibility API happens to report
     (embedded panes and prerendered documents don't always agree with it). */
  function whenRendering(fn) { requestAnimationFrame(function () { fn(); }); }

  /* ---------- smooth scroll ---------- */
  var lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    window.__lenis = lenis;   // handle for debugging / disabling smooth scroll
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  // Drives the masthead's opaque ground — see .is-scrolled in the stylesheet.
  function setStuck(y) { root.classList.toggle('is-scrolled', y > 4); }

  /* The progress hairline (move 20) rides the SAME scroll source — no second
     listener. trackProgress scales .progress off document depth and, once the
     reader crosses the ink switch, flips .past-origin so the rule's ink
     crossfades from specimen to target (the CSS owns the crossfade; this only
     picks the side). Trifecta Order D / Stage D1 (2026-09-15): the switch
     used to anchor to #origin, which sat 4-of-6 down the page; #origin has
     moved to position 1, so anchoring there would flip the gauge on arrival
     and destroy the signal. Re-anchored to #disciplines, which inherited
     #origin's old page depth and read well: the gauge turned from specimen
     to target exactly where the page stopped examining errors (§03) and
     started showing results in three fields. 2026-09-18: §04 "Three
     domains" (the old #disciplines) was folded into §03 — see CLAUDE.md's
     "Content and positioning decisions" — so the switch is re-anchored again,
     to #who, the next section boundary after §03 now that specimen and
     domains share one section; the reading stays the same, just shifted one
     boundary later. The .past-origin class name is unchanged — renaming it
     would touch CSS and tests for no behavioural gain. INK_SWITCH_EL's page
     offset is measured once and re-measured on resize and language switch,
     not read on every scroll frame. */
  var progressEl = document.querySelector('.progress');
  var INK_SWITCH_EL = document.getElementById('who');
  var inkSwitchY = 0;
  function scrollPos() { return lenis ? lenis.scroll : (window.scrollY || 0); }
  function measureInkSwitch() {
    if (INK_SWITCH_EL) inkSwitchY = INK_SWITCH_EL.getBoundingClientRect().top + scrollPos();
  }
  function trackProgress(y) {
    if (!progressEl) return;
    var max = root.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
    progressEl.style.setProperty('--progress', p.toFixed(4));
    if (INK_SWITCH_EL) root.classList.toggle('past-origin', y + window.innerHeight * 0.5 >= inkSwitchY);
  }
  function onScroll(y) { setStuck(y); trackProgress(y); }

  if (lenis) lenis.on('scroll', function (e) { onScroll(e.scroll); });
  else window.addEventListener('scroll', function () { onScroll(window.scrollY); }, { passive: true });
  measureInkSwitch();
  onScroll(scrollPos());
  window.addEventListener('resize', function () { measureInkSwitch(); onScroll(scrollPos()); }, { passive: true });
  document.addEventListener('vitnyr:langchange', function () {
    requestAnimationFrame(function () { measureInkSwitch(); onScroll(scrollPos()); });
  });

  /* DP7 (DESIGN-PASS-III.md): every in-page destination needs to land clear
     of the fixed masthead, not at its own top edge. `scroll-margin-top` on
     .sec/.spec (style.css) covers the browser's OWN fragment navigation —
     a typed #hash, Back/Forward, or the no-Lenis/no-JS fallback below — but
     Lenis computes its target from getBoundingClientRect() and has no idea
     CSS scroll-margin exists, so every Lenis-driven jump needs the same
     clearance passed by hand as a negative offset. Measured live off the
     masthead's own rendered height (same technique jumpToGroup() below uses
     for the collage view's sticky bar) rather than read from --head, which
     getComputedStyle can't resolve back into a used pixel value for a
     custom property built out of calc()/clamp(). */
  function headerHeight() {
    var el = document.querySelector('.masthead');
    return el ? el.getBoundingClientRect().height : 0;
  }

  // In-page links go through Lenis so the easing stays consistent.
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    if (a.hasAttribute('data-collage-open')) return;   // the collage router owns this one
    if (a.hasAttribute('data-permalink')) return;      // initSpecimenPermalinks owns these
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(target, { offset: -headerHeight(), duration: 1.2 });
      else target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
      /* Scrolling is not navigating. preventDefault also cancels the focus move
         the browser would have made, which for the skip link is the entire
         point of the link — a keyboard user would land back in the masthead. */
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    });
  });

  /* The collage view is routing, not motion — it has to work under reduced
     motion and with GSAP present but Lenis off, so it is wired before the
     reduced-motion path returns. */
  initCollageView();
  initWhoRows();
  initSpecimenPermalinks();
  initSpecimenReveal();   // an affordance, not motion — wired before the reduced-motion return
  initMechanismFold();    // same: a disclosure, not motion — CSS handles the open/close transition itself
  initSectionNav();       // wayfinding, not motion — same reasoning as the three lines above

  /* ---------- masthead section quick-nav: active-section tracking ----------
     Scrollspy for the numeral links added in index.html. IntersectionObserver,
     not the scroll-position math trackProgress() uses above — five zones read
     more reliably off "which section is crossing a band near the middle of
     the viewport" than off scroll-offset arithmetic, and it's the same tool
     buildReveals() already uses elsewhere in this file. A thin band
     (-45%/-50% margins collapse the viewport to a ~5% strip near its centre)
     rather than the whole section, so the active link changes when a section
     is actually in reading position, not the instant its top edge appears. */
  function initSectionNav() {
    var links = document.querySelectorAll('.tools__group--sections .tool[href^="#"]');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var sections = Object.keys(map).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    if (!sections.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = map[entry.target.id];
        if (link) link.classList.toggle('is-active', entry.isIntersecting);
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    sections.forEach(function (el) { io.observe(el); });
  }

  /* ---------- reduced motion: show the finished state and stop ---------- */
  if (reduce) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
    gsap.set('.line__inner', { y: '0%' });
    root.classList.add('hero-done');
    // Unlike cursor/magnetic (pure decoration, nothing lost by skipping
    // them), the origin panel is the only way — short of no-JS — to see
    // which stroke maps to which discipline. Reduced motion drops the
    // animation, not the content, so this still has to wire up: initOrigin()
    // already gates its own idle-hint animation behind `reduce` internally.
    initOrigin();
    return;
  }

  /* ---------- language crossfade (Spark Order S4 / move 05) ----------
     theme.js does the language swap synchronously inside its own click
     handler, so main.js can't slot a fade in front of it without racing.
     The hook inverts the control: theme.js calls window.__vitnyrLangFade
     with the swap as a callback when it exists, and runs the swap bare
     otherwise (no main.js, no GSAP, reduced motion — an instant switch,
     which test_seeded_language_applies_before_paint and the no-JS path
     both depend on). Installed here, past the reduced-motion return, so it
     is only ever present when GSAP is loaded and motion is allowed.

     The swap runs synchronously the moment we're called, then #app is cut
     to transparent and fades back over D.state on the brand ease — a
     page-wide transition rather than a hard text swap. It is not deferred
     to the bottom of a fade-out: there is no second, old-language layer to
     fade out (that needs S6's clone/FLIP machinery), and deferring it
     would desync every existing i18n test that asserts on the same tick as
     the click — which S4 must keep green. #app only: the masthead switch
     the reader just pressed stays solid so they see it answer. A second
     click mid-fade re-runs its own swap and retargets the one tween, so a
     double-click can never strand the page faded with the old language. */
  var appEl = document.getElementById('app');
  if (appEl) {
    var langFadeTween = null;
    window.__vitnyrLangFade = function (swap) {
      swap();                                   // always, first thing
      if (langFadeTween) langFadeTween.kill();  // no stacked opacity tweens
      langFadeTween = gsap.fromTo(appEl, { opacity: 0 },
        { opacity: 1, duration: D.state, ease: EASE,
          onComplete: function () { langFadeTween = null; } });
    };
  }

  /* ---------- hero: line masks, once, on load ---------- */
  var heroTween = null, heroLang = null, heroStarted = false, heroGuard = 0;

  // Reads what is actually on screen rather than what GSAP believes it set,
  // which is the only reading that can catch a tween that never rendered.
  function translateY(el) {
    var m = getComputedStyle(el).transform;
    if (!m || m === 'none') return 0;
    var p = m.match(/matrix(3d)?\(([^)]+)\)/);
    if (!p) return 0;
    var v = p[2].split(',').map(parseFloat);
    return v.length === 6 ? v[5] : v[13];
  }

  /* Re-armed on every play, not just the first. The hero is the h1, it is the
     only thing above the fold, and a language switch starts a fresh tween that
     the one-shot page failsafe below has already come and gone for. */
  function armHeroGuard() {
    clearTimeout(heroGuard);
    heroGuard = setTimeout(function () {
      var stuck = false;
      document.querySelectorAll('.line__inner').forEach(function (el) {
        if (el.offsetParent !== null && Math.abs(translateY(el)) > 0.5) stuck = true;
      });
      if (stuck) showHeroNow();
    }, 2500);
  }

  function playHero() {
    var lang = root.getAttribute('data-lang') || 'en';
    if (heroStarted && heroLang === lang) return;   // nothing actually changed
    heroLang = lang;
    heroStarted = true;

    var visible = [], parked = [];
    document.querySelectorAll('.line__inner').forEach(function (el) {
      (el.offsetParent !== null ? visible : parked).push(el);
    });
    if (!visible.length) return;

    // Kill the outgoing run first, or its set() would snap live lines back.
    if (heroTween) heroTween.kill();
    root.classList.remove('hero-done');
    /* Only ever the lines that are actually showing. y is a percentage of the
       element's own height, and the twins in the other language are display:none
       — measuring a zero-height box leaves NaN in GSAP's transform cache, and
       every later tween on that element then renders nothing at all. The parked
       twins are handed back to the stylesheet, which already masks them, so they
       are measured fresh the next time they are the ones on screen. */
    if (parked.length) gsap.set(parked, { clearProps: 'transform' });
    gsap.set(visible, { y: '110%' });
    heroTween = gsap.to(visible, {
      y: '0%', duration: D.hero, ease: EASE, stagger: 0.09, delay: 0.15,
      onComplete: function () {
        root.classList.add('hero-done');
        // D2.5: the §04 mark sequences its own draw-in after this, listening
        // for the event rather than initOrigin() reaching into this tween.
        document.dispatchEvent(new CustomEvent('vitnyr:heroin'));
      }
    });
    armHeroGuard();
  }

  function showHeroNow() {
    clearTimeout(heroGuard);
    if (heroTween) heroTween.kill();
    var live = [];
    document.querySelectorAll('.line__inner').forEach(function (el) {
      if (el.offsetParent !== null) live.push(el);
    });
    if (live.length) gsap.set(live, { y: '0%' });
    root.classList.add('hero-done');
    heroStarted = true;
    document.dispatchEvent(new CustomEvent('vitnyr:heroin'));
  }

  /* ---------- the reveal rhythm ----------
     One pattern for the whole page: 24px rise + fade, 0.9s, the brand curve,
     staggered 0.08s, fired once when the element itself is 20% into view.
     Observed per element rather than per section: a section boundary is not
     something the reader can see, and observing whole sections meant items a
     thousand pixels below the fold had already finished animating by the time
     they were scrolled to. */
  var REVEAL_CAP = 4;   // past four beats a stagger stops reading as rhythm and
                        // starts reading as lag, so the chain restarts its count

  // The one place a batch of .reveal targets turns into a staggered entrance.
  // Shared so the collage view's own observer (armCollageReveals) runs the
  // exact same rhythm as the page's, off a different scroll root.
  function fireReveals(entries, io) {
    var shown = [];
    entries.forEach(function (e) { if (e.isIntersecting) shown.push(e); });
    if (!shown.length) return;
    // Ordered by where they sit, not by DOM order or callback order, so a
    // stagger always runs top-to-bottom on screen.
    shown.sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
    shown.forEach(function (entry, i) {
      var el = entry.target;
      el.style.setProperty('--d', ((i % (REVEAL_CAP + 1)) * STAGGER).toFixed(2) + 's');
      el.classList.add('is-in');
      io.unobserve(el);
    });
  }

  function buildReveals() {
    // The collage tiles are .reveal too, but they live in a display-toggled
    // fixed view that is never scrolled *into* — the page observer's viewport
    // root would fire them all at load while the view is hidden. They start
    // .is-in in the markup and are handed to their own observer on first open
    // (armCollageReveals). Everything else is the page's to reveal.
    var items = [];
    document.querySelectorAll('.reveal').forEach(function (el) {
      if (!el.closest('#collage')) items.push(el);
    });
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    // The hero is on screen at load, not something the reader scrolls down
    // to — the -20% margin below is for content that isn't there yet. Left
    // on the hero, that margin instead cuts a dead zone across the bottom
    // fifth of the viewport, and .scrollcue lives in exactly that band: the
    // one element whose job is to invite scrolling sat un-rendered until the
    // reader had already started (measured stuck at 800/900/1080 viewport
    // heights). The hero gets its own observer against the true viewport;
    // -20% stays correct for everything below it.
    var hero = [], rest = [];
    items.forEach(function (el) {
      // D2.5: the §04 mark is still in `items` above (so a no-IO browser
      // still force-shows it via the fallback), but its own .is-in is
      // sequenced after the hero by initOrigin() rather than fired on
      // ordinary scroll visibility — leave it out of both queues here.
      if (el.classList.contains('origin__mark')) return;
      (el.closest('.hero') ? hero : rest).push(el);
    });

    var io = new IntersectionObserver(function (entries) { fireReveals(entries, io); },
      { rootMargin: '0px 0px -20% 0px', threshold: 0 });
    // Twins in the language that isn't showing are display:none, so the
    // observer never reports them and they don't eat stagger beats. They stay
    // observed, and fire correctly if the reader switches language.
    rest.forEach(function (el) { io.observe(el); });

    var heroIo = new IntersectionObserver(function (entries) { fireReveals(entries, heroIo); },
      { rootMargin: '0px', threshold: 0 });
    hero.forEach(function (el) { heroIo.observe(el); });
  }

  /* The collage view's tiles run the page's reveal rhythm off the view's own
     overflow:auto root. Wired on first open, not at load: the view is
     position:fixed + visibility:hidden until then, so a viewport-rooted
     observer would report every tile as "in view" and burn the whole
     entrance while nobody is looking. Tiles ship .is-in (visible with JS
     absent, under reduced motion, and while the view is closed); this strips
     it back off so the observer can stagger them in. Fires once. */
  /* The 18 collage figures shipped src/srcset directly, so every one of them
     downloaded on ordinary page load even though the view sits hidden
     (opacity:0, not display:none — the browser's native loading="lazy" goes
     by viewport distance, and a position:fixed panel over the same viewport
     reads as close enough to fetch anyway; measured at 1,231 KB of images no
     visit ever displays). They ship as data-src/data-srcset instead — inert
     to the browser's own loader — and are only promoted to real attributes
     here, on first open. A <noscript> copy alongside each keeps the no-JS
     page whole. Fires once; reopening finds the real attributes already in
     place. */
  var collageImagesPromoted = false;
  function promoteCollageImages(view) {
    if (collageImagesPromoted) return;
    collageImagesPromoted = true;
    view.querySelectorAll('img[data-src]').forEach(function (img) {
      if (img.dataset.srcset) img.srcset = img.dataset.srcset;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      img.removeAttribute('data-srcset');
    });
  }

  var collageRevealsArmed = false;
  function armCollageReveals(view) {
    if (collageRevealsArmed) return;
    collageRevealsArmed = true;
    var tiles = view.querySelectorAll('.reveal');
    if (reduce || !('IntersectionObserver' in window)) return;   // leave them .is-in
    tiles.forEach(function (el) {
      el.classList.remove('is-in');
      el.style.removeProperty('--d');
    });
    var io = new IntersectionObserver(function (entries) { fireReveals(entries, io); },
      { root: view, rootMargin: '0px 0px -10% 0px', threshold: 0 });
    tiles.forEach(function (el) { io.observe(el); });
    armFailsafe();   // belt-and-braces: force-show any tile the observer misses
  }

  /* ---------- collage lightbox (Stage 3) ----------
     Reverses Stage 5's "add nothing to the tiles" ruling (BUILD-NOTES,
     collage-plan.md) now that Igor has asked for click-to-enlarge: a tile
     is a real control, so the affordance stops being a lie. Every bit of
     it — the per-tile <button> and the dialog itself — is built here at
     runtime, the same way initSpecimenReveal() builds its "+ Show the
     common mistake" control: absent this file, the no-JS document keeps
     15 plain <figure>s and ships zero dead buttons.

     Routing stays outside location.hash on purpose (see the plan): Escape
     closes the lightbox, closing it returns focus to the tile that opened
     it, and browser Back still closes the whole #collage view — the
     router's own keydown handler below checks the shared lightboxOpen
     flag and no-ops while this is open, so Escape only ever closes one
     layer at a time. The focus trap reuses the view's own inert idea
     rather than a hand-rolled one: .view__bar and .view__body go inert
     while the box is open, so Tab can only reach the lightbox's own
     controls (main.js:750-758 already proved this pattern for #app).

     Accessible name comes straight off the figure's own <figcaption> — the
     dialog's aria-labelledby and the caption node both point at real
     bilingual text that already carries data-en/data-ru, so theme.js's
     existing applyLang() loop (`[data-en][data-ru]`) keeps every language
     switch in sync for free; no bespoke vitnyr:langchange handler needed
     here, which is the same "don't invent a third i18n mechanism" rule
     CLAUDE.md states for markup applied to runtime-built markup instead. */
  var lightboxOpen = false;
  var lightboxArmed = false;
  function initCollageLightbox(view) {
    if (lightboxArmed) return;
    lightboxArmed = true;

    var figures = Array.prototype.slice.call(view.querySelectorAll('.collage figure'));
    if (!figures.length) return;

    var bar = view.querySelector('.view__bar');
    var body = view.querySelector('.view__body');
    var canInert = 'inert' in HTMLElement.prototype;

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.hidden = true;
    box.tabIndex = -1;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-labelledby', 'lightbox-caption');

    var media = document.createElement('div');
    media.className = 'lightbox__media';
    var img = document.createElement('img');
    img.className = 'lightbox__img';
    img.decoding = 'async';
    media.appendChild(img);

    var caption = document.createElement('p');
    caption.className = 'lightbox__caption';
    caption.id = 'lightbox-caption';

    var count = document.createElement('p');
    count.className = 'lightbox__count';
    count.setAttribute('aria-hidden', 'true');

    // Icon-only controls: plain English aria-label, matching the masthead's
    // own icon-nav (data-collage-jump), which is aria-label without a
    // bilingual pair too — no new pattern introduced.
    function iconButton(cls, label, path) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = cls;
      b.setAttribute('aria-label', label);
      b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + path + '</svg>';
      return b;
    }
    var closeBtn = iconButton('lightbox__close', 'Close',
      '<path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>');
    var prevBtn = iconButton('lightbox__prev', 'Previous photograph',
      '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>');
    var nextBtn = iconButton('lightbox__next', 'Next photograph',
      '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>');

    box.appendChild(closeBtn);
    box.appendChild(prevBtn);
    box.appendChild(media);
    box.appendChild(nextBtn);
    box.appendChild(caption);
    box.appendChild(count);
    view.appendChild(box);

    var index = 0;
    var returnFocusTo = null;
    function isRu() { return root.getAttribute('data-lang') === 'ru'; }

    // Re-run on open and on every prev/next step. Language itself is left
    // to theme.js's own applyLang() loop (see comment above) — this only
    // ever sets the pair fresh for the newly-shown photo.
    function render() {
      var fig = figures[index];
      var srcImg = fig.querySelector('img');
      var cap = fig.querySelector('figcaption');
      img.src = (srcImg && (srcImg.currentSrc || srcImg.src)) || '';
      img.srcset = (srcImg && srcImg.srcset) || '';
      img.sizes = '100vw';
      img.alt = (srcImg && srcImg.alt) || '';
      var en = cap ? (cap.getAttribute('data-en') || '') : '';
      var ru = cap ? (cap.getAttribute('data-ru') || '') : '';
      caption.setAttribute('data-en', en);
      caption.setAttribute('data-ru', ru);
      caption.textContent = isRu() ? ru : en;
      count.textContent = (index + 1) + ' / ' + figures.length;
    }

    // Open/close motion: additive only, same rule as every other animation
    // in this file (see the reveal/motion comment block above buildReveals).
    // With GSAP absent or prefers-reduced-motion, open() just flips `hidden`
    // as before — nothing here is load-bearing for the dialog to work.
    // canAnimate is re-checked on every call rather than cached once, and
    // killBoxTween guards a rapid double-click from stacking two tweens on
    // the same element, same pattern as langFadeTween above.
    function canAnimate() { return !reduce && window.gsap; }
    var boxTween = null;
    function killBoxTween() { if (boxTween) { boxTween.kill(); boxTween = null; } }

    function open(i, opener) {
      index = i;
      returnFocusTo = opener;
      lightboxOpen = true;
      render();
      box.hidden = false;
      root.classList.add('lightbox-open');
      if (canInert) {
        if (bar) bar.inert = true;
        if (body) body.inert = true;
      }
      box.focus({ preventScroll: true });

      if (canAnimate()) {
        killBoxTween();
        // The photo grows in from wherever the tile that opened it actually
        // sat, not from a fixed centre — the one cheap trick that makes a
        // "grow to full view" read as a photo *responding to the click*
        // rather than a generic dialog. transform-origin is relative to
        // media's own box, so the opener's rect has to be re-measured
        // against media's rect *after* box.hidden flips (geometry is live
        // synchronously the same frame, same assumption jumpToGroup makes
        // above) rather than reused from any earlier read.
        var mediaRect = media.getBoundingClientRect();
        var openerRect = opener ? opener.getBoundingClientRect() : null;
        if (openerRect && mediaRect.width && mediaRect.height) {
          var ox = (openerRect.left + openerRect.width / 2) - mediaRect.left;
          var oy = (openerRect.top + openerRect.height / 2) - mediaRect.top;
          media.style.transformOrigin = ox + 'px ' + oy + 'px';
        } else {
          media.style.transformOrigin = '50% 50%';
        }
        gsap.set(box, { opacity: 0 });
        gsap.set(media, { opacity: 0, scale: 0.88 });
        boxTween = gsap.timeline({ onComplete: function () { boxTween = null; } })
          .to(box, { opacity: 1, duration: D.micro, ease: EASE }, 0)
          .to(media, { opacity: 1, scale: 1, duration: D.state, ease: EASE }, 0);
      }
    }
    // Close stays synchronous, unlike open() — Escape/close-button/prev-
    // trigger-click all read .lightbox's `hidden` state and focus location
    // back out immediately (test_escape_closes_only_the_lightbox_and_
    // restores_focus_to_its_tile asserts this with no wait), and a
    // keyboard user tabbing right after Escape has to land back on real,
    // reachable content the instant this returns, not one tween later.
    // The open-only motion still reads as intentional rather than
    // lopsided: an entrance you watch happen invites a beat of attention; a
    // dismissal doesn't need one, and instant-close is the normal feel for
    // this exact interaction (most native image viewers close immediately).
    function close() {
      if (!lightboxOpen) return;
      lightboxOpen = false;
      killBoxTween();
      box.hidden = true;
      root.classList.remove('lightbox-open');
      if (canInert) {
        if (bar) bar.inert = false;
        if (body) body.inert = false;
      }
      if (returnFocusTo && returnFocusTo.focus) returnFocusTo.focus({ preventScroll: true });
    }
    function step(delta) {
      index = (index + delta + figures.length) % figures.length;
      if (canAnimate()) {
        gsap.fromTo(img, { opacity: 0 }, { opacity: 1, duration: D.micro, ease: EASE });
      }
      render();
    }

    // Wraps each figure's existing .collage__slot in a real button — the
    // slot's own border/ratio/grayscale styling is untouched, only now
    // reachable by click and by Enter/Space (native <button> behaviour,
    // no extra key handling needed for that half). Flat figure order
    // (querySelectorAll above) already includes the climbing group's
    // .collage__pair__fig pair, so prev/next crosses it for free.
    figures.forEach(function (fig, i) {
      var slot = fig.querySelector('.collage__slot');
      var cap = fig.querySelector('figcaption');
      if (!slot) return;
      var trigger = document.createElement('button');
      trigger.type = 'button';
      trigger.className = 'collage__trigger';
      if (cap) {
        if (!cap.id) cap.id = 'collage-cap-' + i;
        trigger.setAttribute('aria-labelledby', cap.id);
      }
      fig.insertBefore(trigger, slot);
      trigger.appendChild(slot);
      trigger.addEventListener('click', function () { open(i, trigger); });
    });

    closeBtn.addEventListener('click', close);
    prevBtn.addEventListener('click', function () { step(-1); });
    nextBtn.addEventListener('click', function () { step(1); });

    document.addEventListener('keydown', function (e) {
      if (!lightboxOpen) return;
      if (e.key === 'Escape' || e.key === 'Esc') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowLeft') { step(-1); }
      else if (e.key === 'ArrowRight') { step(1); }
    });
  }

  /* ---------- origin: interactive mark ----------
     Trifecta Order D / Stage D2 (2026-09-15): the dial (the three strokes)
     is wired to the readout (the three panel rows) with two distinct
     gestures, per Igor's brief. Hover (fine pointer) or keyboard focus is a
     PREVIEW: ink only — the stroke lights, the row's name lights — and it
     reverts to the committed discipline the moment the pointer leaves or
     focus moves on. Click, Enter, Space, or tap is a COMMIT: it moves
     .origin__marker to that row and flips aria-pressed, and it sticks until
     the next commit. Both the three glyph hit-buttons and the three panel
     rows share one preview()/commit() pair, so a hybrid device never gets
     two handlers fighting over the same element, and the mapping between a
     stroke and its row is symmetric in both directions.
     The panel rows used to be hidden-until-active under html.js (a
     cross-fade overlay); Stage D2 removed that, so all three are now always
     visible and aria-hidden is never touched here — there is nothing left
     to hide.
     The idle hint below shares paint() with preview()/commit() rather than
     defining its own visual language — a real engagement and the hint
     produce identical-looking states, just triggered differently. */
  function initOrigin() {
    // `mark` stays the single §01 figure — it's the only one the S7 draw-in
    // and the idle hint below key off (see drawThenHint()). `marks` is every
    // instance of the control that exists (§01's, plus §03's specimen-switch
    // mini added 2026-09-17, if present) — hits/parts/sigils are queried
    // document-wide below so a single paint()/previewSigil()/sparkSigil()
    // call updates whichever of these actually exist, in sync, without the
    // mini needing its own copy of any of this logic.
    var mark = document.querySelector('.origin__mark');
    if (!mark) return;
    var marks = document.querySelectorAll('.origin__mark');
    var hits = document.querySelectorAll('.origin__hit');
    var parts = document.querySelectorAll('.glyph__part');
    var panel = document.querySelector('.origin__panel');
    var panelItems = panel ? panel.querySelectorAll('.origin__panel-item') : [];
    var marker = panel ? panel.querySelector('.origin__marker') : null;
    // D3 (2026-09-15): the readout's body — see .reading in style.css and
    // index.html. Queried once here rather than re-queried per commit; a
    // row with no matching value for the newly-committed discipline (every
    // row, until D4 adds chess/climbing) is simply left showing whatever it
    // already had, which today is always English.
    var readingValues = panel ? panel.querySelectorAll('.reading__value') : [];
    // Trifecta D follow-up (2026-09-15): §03 (Specimens) is now one of three
    // discipline-scoped groups, swapped the same way updateReading() swaps
    // the readout's values. Queried once here, same reasoning as
    // readingValues above.
    var specimenGroups = document.querySelectorAll('#specimen .specimens-group');
    if (!hits.length) return;

    // Specimen sigils (2026-09-17): the small masthead-icon copies at each
    // stroke's tip (index.html), on every mark instance — see the `marks`
    // comment above.
    var sigils = document.querySelectorAll('.origin__sigil');

    var idleTl = null;
    // True the instant any real engagement happens (preview or commit),
    // permanently. Checked by every idle-timeline step, rather than trusting
    // .kill() alone to be synchronous: a step already queued on GSAP's
    // ticker for the current frame can still fire after .kill() is called
    // mid-frame, which without this guard could paint a stale idle
    // discipline right over a real one landing in the same frame.
    var engaged = false;

    // C6 (2026-09-06): rest state is English lit, not neutral — English is
    // the offer, chess and climbing are proof it transfers, not equal-weight
    // alternatives. committed tracks whichever discipline was last actually
    // clicked/tapped/entered; it starts on 'english' to match the HTML's own
    // default aria-pressed="true" on that row.
    var committed = 'english';

    // The visual half of activation — glyph active/dim plus which panel
    // row's name is lit — shared by preview, commit, and the idle hint
    // below, so none of the three can drift into a differently-styled
    // "active" state.
    function paint(name) {
      parts.forEach(function (el) {
        var on = el.dataset.discipline === name;
        el.classList.toggle('is-active', on);
        el.classList.toggle('is-dim', !on);
      });
      panelItems.forEach(function (el) {
        el.classList.toggle('is-active', el.dataset.discipline === name);
      });
    }

    function clearPaint() {
      paint(committed);
    }

    // Specimen sigils: deliberately NOT folded into paint() above. paint()
    // runs on load and on every blur/pointerleave-back-to-committed, and a
    // sigil must stay invisible through both of those — it only shows for
    // an actual, current hover/keyboard-focus preview, never as a
    // persistent "this is the committed one" indicator (the glyph's own
    // dim/lit fill already carries that job). previewSigil(null) hides all
    // three.
    function previewSigil(name) {
      sigils.forEach(function (el) {
        el.classList.toggle('is-preview', el.dataset.discipline === name);
      });
    }

    // One-shot flourish at the instant of commit, not a lit state — the
    // class is removed again after SPARK_MS (kept in sync with --spark-d /
    // the sigil-spark keyframes in style.css) so a repeat commit of the
    // same discipline (e.g. re-clicking the already-committed stroke)
    // retriggers the pop instead of being a no-op class toggle.
    var SPARK_MS = 500;
    var sparkTimers = {}; // keyed by discipline name — committing a second
    // discipline before the first's timer fires must not leave the first
    // sigil's class stuck; each name cleans up only its own timer.
    function sparkSigil(name) {
      sigils.forEach(function (el) {
        if (el.dataset.discipline !== name) return;
        if (sparkTimers[name]) clearTimeout(sparkTimers[name]);
        el.classList.remove('is-spark');
        el.offsetWidth; // restart the animation even on a repeat commit
        el.classList.add('is-spark');
        sparkTimers[name] = setTimeout(function () {
          el.classList.remove('is-spark');
          sparkTimers[name] = null;
        }, SPARK_MS);
      });
    }

    // D3: swaps the readout's body — only ever called from commit(), never
    // preview(), per D2's own split (hover is ink-only; a commit is what
    // "swaps" the readout). A row with no value for `name` is left as-is:
    // there is nothing to switch to for chess/climbing until D4 gives every
    // row a sibling .reading__value for them.
    function updateReading(name) {
      var exists = false;
      readingValues.forEach(function (el) { if (el.dataset.discipline === name) exists = true; });
      if (!exists) return;
      readingValues.forEach(function (el) {
        var on = el.dataset.discipline === name;
        el.classList.toggle('is-active', on);
        el.setAttribute('aria-hidden', on ? 'false' : 'true');
        el.inert = !on;
      });
    }

    // Swaps §03's discipline-scoped group. Unlike updateReading(), every
    // discipline always has a group to switch to (no partial-rollout guard
    // needed) — all three shipped together this stage.
    function updateSpecimens(name) {
      specimenGroups.forEach(function (el) {
        el.classList.toggle('is-active', el.dataset.disciplineGroup === name);
      });
    }

    // Slides .origin__marker to sit against the named row. Measures the
    // row's real offsetTop/offsetHeight against the panel rather than
    // assuming a fixed height, since that height differs across the EN/RU
    // languages and the <900px stacked layout. animate=false is used for the
    // initial placement and for resize/language reflows, so the marker
    // never visibly slides for a reason the reader didn't cause.
    function positionMarker(name, animate) {
      if (!marker) return;
      var item = null;
      panelItems.forEach(function (el) { if (el.dataset.discipline === name) item = el; });
      if (!item) return;
      var prevTransition = marker.style.transition;
      if (!animate) marker.style.transition = 'none';
      marker.style.transform = 'translateY(' + item.offsetTop + 'px)';
      marker.style.height = item.offsetHeight + 'px';
      if (!animate) {
        marker.offsetHeight; // force reflow before restoring the transition
        marker.style.transition = prevTransition;
      }
    }

    // PREVIEW: ink only, never sticks, never touches aria-pressed.
    function preview(name) {
      engaged = true;
      // D2.5: a real engagement shows the mark outright, regardless of
      // whether the hero-gated draw sequence has started yet — a reader who
      // tabs in during that wait must not land on an invisible control.
      mark.classList.add('is-in');
      if (idleTl) { idleTl.kill(); idleTl = null; }
      paint(name);
    }

    // D5 (2026-09-15): #english/#chess/#climbing are the ids Order B reserved
    // for its future dossier sections — with none built yet, they act here as
    // a plain selector rather than a scroll target. Kept a selector, not a
    // jump: syncHash uses replaceState so the address bar stays shareable
    // without stacking history entries a reader would have to Back through
    // one at a time. Never assign location.hash directly — that fires
    // hashchange, which wakes the collage router's routeAfterHashChange()
    // (main.js) on every commit; initSpecimenPermalinks() above is the
    // pattern this copies, pushState swapped for replaceState because this is
    // a selector, not a jump (a correction to what TRIFECTA-C-MARK-NAV.md's
    // C1 recommends for the jump case).
    var HASH_NAMES = ['english', 'chess', 'climbing'];
    // DP8 (DESIGN-PASS-III.md): a specimen permalink's id names no discipline
    // directly (`#specimen-chess-calculation`), but sits inside a
    // .specimens-group that does. Cold-loading one of those six chess/climbing
    // permalinks left `committed` at its English default, so the target group
    // was still `display: none` — a 0×0 box the browser can't scroll to,
    // which is why those six landed mid-English-list with no error. Resolving
    // the id's own ancestor group here means a specimen hash commits that
    // discipline exactly like a bare #chess/#climbing hash already did.
    function groupFromSpecimenHash(id) {
      var target = id && document.getElementById(id);
      var group = target && target.closest('.specimens-group[data-discipline-group]');
      return group ? group.dataset.disciplineGroup : null;
    }
    function nameFromHash() {
      var id = (location.hash || '').slice(1);
      if (HASH_NAMES.indexOf(id) !== -1) return id;
      return groupFromSpecimenHash(id);
    }
    function syncHash(name) {
      if (window.history.replaceState) window.history.replaceState(null, '', '#' + name);
    }

    // COMMIT: sticks, moves the marker, and is the only thing that writes
    // aria-pressed — which now means "committed", not "currently previewed".
    function commit(name) {
      engaged = true;
      mark.classList.add('is-in');   // see preview() above
      if (idleTl) { idleTl.kill(); idleTl = null; }
      committed = name;
      paint(name);
      updateReading(name);
      updateSpecimens(name);
      positionMarker(name, true);
      syncHash(name);
      sparkSigil(name);
      hits.forEach(function (el) {
        el.setAttribute('aria-pressed', el.dataset.discipline === name ? 'true' : 'false');
      });
      panelItems.forEach(function (el) {
        el.setAttribute('aria-pressed', el.dataset.discipline === name ? 'true' : 'false');
      });
    }

    // A cold load of #chess/#climbing selects that discipline before the
    // resting default below ever paints English — so committed starts as the
    // deep-linked discipline instead of drifting to it in a second, visible
    // step.
    var deepLinked = nameFromHash();
    if (deepLinked) committed = deepLinked;

    // Establishes the resting default from the first frame — covers reduced
    // motion (the idle hint below never runs there) and the gap before the
    // hint's own IntersectionObserver fires.
    clearPaint();
    updateReading(committed);
    updateSpecimens(committed);
    positionMarker(committed, false);
    hits.forEach(function (el) {
      el.setAttribute('aria-pressed', el.dataset.discipline === committed ? 'true' : 'false');
    });
    panelItems.forEach(function (el) {
      el.setAttribute('aria-pressed', el.dataset.discipline === committed ? 'true' : 'false');
    });

    // The reader lands *inside* the readout, not merely near it — scroll
    // alone is not navigation (see the skip-link bug in BUILD-NOTES). This
    // only applies to a bare #english/#chess/#climbing hash: a specimen
    // hash (DP8, below) has its own, more specific destination and must not
    // also land here first. preventScroll because #origin is already the
    // scroll target below; without it, focus() would fight that scroll with
    // its own native jump. offset clears the fixed masthead (DP7) — see
    // headerHeight() near the top of this file.
    var hashId = (location.hash || '').slice(1);
    if (HASH_NAMES.indexOf(hashId) !== -1 && panel) {
      var origin = document.getElementById('origin');
      if (origin) {
        if (lenis) lenis.scrollTo(origin, { offset: -headerHeight(), immediate: reduce });
        else origin.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
      }
      if (!panel.hasAttribute('tabindex')) panel.setAttribute('tabindex', '-1');
      panel.focus({ preventScroll: true });
    }

    // DP8, continued: the group above is now committed and visible, so the
    // specimen itself is a real, measurable target — land on it the same
    // way the bare-hash case lands on the readout.
    var deepLinkedSpecimen = HASH_NAMES.indexOf(hashId) === -1 ? document.getElementById(hashId) : null;
    if (deepLinkedSpecimen && deepLinkedSpecimen.classList.contains('spec')) {
      if (lenis) lenis.scrollTo(deepLinkedSpecimen, { offset: -headerHeight(), immediate: reduce });
      else deepLinkedSpecimen.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
      if (!deepLinkedSpecimen.hasAttribute('tabindex')) deepLinkedSpecimen.setAttribute('tabindex', '-1');
      deepLinkedSpecimen.focus({ preventScroll: true });
    }

    function wire(el) {
      var name = el.dataset.discipline;
      el.addEventListener('click', function () { commit(name); });
      el.addEventListener('focus', function () { preview(name); previewSigil(name); });
      el.addEventListener('blur', function () { preview(committed); previewSigil(null); });
      if (finePointer) {
        el.addEventListener('pointerenter', function () { preview(name); previewSigil(name); });
        el.addEventListener('pointerleave', function () { preview(committed); previewSigil(null); });
      }
    }
    hits.forEach(wire);
    panelItems.forEach(wire);

    // Row heights can change under the reader without a commit happening —
    // a resize crossing the 900px breakpoint, or a language switch changing
    // how far RU text wraps. Re-measure without animating either way.
    window.addEventListener('resize', function () { positionMarker(committed, false); }, { passive: true });
    document.addEventListener('vitnyr:langchange', function () { positionMarker(committed, false); });

    // One-shot hint, not a loop: previews all three discipline/stat pairs a
    // couple of times when the section first scrolls into view, then settles
    // back to the neutral resting state on its own. It has to preview the
    // panel too, not just the glyph — a shimmer with no text next to it
    // teaches nothing about what hovering actually does. Skipped outright
    // under reduced motion; the real interaction above still works either
    // way, and paint() carries no aria side effects, so this stays silent to
    // assistive tech.
    if (reduce || !('IntersectionObserver' in window)) return;
    // S7 move 03: the mark draws its three strokes on the reveal (~0.9s of
    // CSS, keyed off .is-in). Hold the idle preview until that has finished
    // so the draw and the hint never drive the same strokes in one frame.
    var DRAW_HOLD = 1.0;
    // D2.5: at position 1 the mark is on screen at load, same as the hero —
    // racing its draw-in against the hero's line-mask reads as four timed
    // systems firing in the same viewport. Sequence instead: hero lands,
    // then the mark draws, then the hint walks. buildReveals() no longer
    // queues .origin__mark (see there), so this is the only place that adds
    // its .is-in. Never reach into playHero() itself — it already carries a
    // NaN-transform-cache scar from an earlier coupling attempt — just listen
    // for the completion event it emits, or fall back on a fixed wait if
    // that event is somehow missed (e.g. the mark only becomes visible after
    // a late scroll, once the one-time event has already fired).
    var HERO_WAIT_MS = 1800;
    function drawThenHint() {
      if (engaged || mark.classList.contains('is-in')) return;
      mark.classList.add('is-in');
      if (engaged) return;   // a real interaction can land in the same tick
      var order = ['english', 'chess', 'climbing'];
      var tl = gsap.timeline({
        delay: DRAW_HOLD,
        repeat: 1,
        onComplete: function () { if (!engaged) clearPaint(); idleTl = null; }
      });
      order.forEach(function (name) {
        tl.call(function () { if (!engaged) paint(name); }).to({}, { duration: 1 });
      });
      idleTl = tl;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        if (engaged) return;
        if (root.classList.contains('hero-done')) { drawThenHint(); return; }
        var fallback = setTimeout(drawThenHint, HERO_WAIT_MS);
        document.addEventListener('vitnyr:heroin', function () {
          clearTimeout(fallback);
          drawThenHint();
        }, { once: true });
      });
    }, { threshold: 0.4 });
    io.observe(mark);
  }

  /* ---------- pointer: the dot ----------
     C14 (2026-09-07): a single dot rides the pointer everywhere on a
     fine-pointer device — it IS the cursor now (cursor:none is page-wide in
     the sheet under .has-cursor), not a flourish that only turns up over
     links. It never changes size. The one signal it gives is colour: its
     fill eases from --fg to --ink-target green over a control, or to
     --ink-specimen amber over a control inside #specimen — the same
     token-to-token crossfade the progress hairline uses, declared in the
     stylesheet off the same --ink-* tokens (no hex here). The 3x balloon that
     used to fire here is gone for good (C14); the magnetic pull came back at
     C16 but lives in initMagnetic() below and only on non-text controls, not
     on this size/colour path. Everything still degrades — no JS, no GSAP,
     reduced motion or touch all keep the native cursor and no dot. */
  function initCursor() {
    if (!finePointer) return;
    var el = document.querySelector('.cursor');
    if (!el) return;

    var setX = gsap.quickSetter(el, 'x', 'px');
    var setY = gsap.quickSetter(el, 'y', 'px');
    var mx = 0, my = 0, cx = 0, cy = 0;
    var shown = false, running = false;

    // The lerp is the whole effect, so it writes straight to the transform.
    // A quickTo here would smooth an already-smoothed value and the dot would
    // swim behind the pointer instead of trailing it.
    function frame() {
      var ex = mx - cx, ey = my - cy;
      if (Math.abs(ex) < 0.05 && Math.abs(ey) < 0.05) {
        cx = mx; cy = my; setX(cx); setY(cy);
        running = false;                 // caught up: stop burning frames
        return;
      }
      cx += ex * 0.15;
      cy += ey * 0.15;
      setX(cx); setY(cy);
      requestAnimationFrame(frame);
    }
    function kick() { if (!running) { running = true; requestAnimationFrame(frame); } }

    window.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (!shown) {
        // First real move: arm .has-cursor, which both suppresses the native
        // pointer page-wide and fades the dot in (opacity lives in the sheet).
        shown = true;
        cx = mx; cy = my;
        gsap.set(el, { x: mx, y: my });
        root.classList.add('has-cursor');
      }
      root.classList.remove('cursor-out');   // back inside the window
      kick();
    }, { passive: true });

    /* The dot is the pointer now, so it has to answer the pointer leaving the
       window — otherwise it strands at the last edge it saw. mouseleave on the
       root fires as the pointer crosses out; mouseenter and the next mousemove
       both clear it. Opacity is the sheet's (html.has-cursor.cursor-out). */
    root.addEventListener('mouseleave', function () { root.classList.add('cursor-out'); });
    root.addEventListener('mouseenter', function () { root.classList.remove('cursor-out'); });

    /* The one signal is colour: .cursor-active plus the two ink variants.
       No size change here — the sheet owns every visual, this only says which
       state the dot is in. Move 02 (Spark Order S4): over a control inside
       #specimen the dot takes specimen amber (the error under examination),
       over the contact CTA it takes target green (the outcome); off the
       stylesheet's --ink-* tokens, no hex here. */
    var HOT = 'a, button, [data-magnetic]';
    document.addEventListener('mouseover', function (e) {
      var hot = e.target.closest && e.target.closest(HOT);
      if (!hot) return;
      root.classList.add('cursor-active');
      el.classList.toggle('is-specimen', !!hot.closest('#specimen'));
      el.classList.toggle('is-target', !!hot.closest('.contact__cta'));
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest && e.target.closest(HOT)) {
        root.classList.remove('cursor-active');
        el.classList.remove('is-specimen', 'is-target');
      }
    });
  }

  /* ---------- pointer: magnetic pull on controls ----------
     C16 (2026-09-07): the hover pull is back, but only where C14's note said
     it could return — non-text controls: the Cream/RU switches, the collage
     icon-nav buttons, the footer "Back to top", the collage "Back". Never on
     running copy or standalone text links (that was the half Igor flagged as
     "the way the cursor gets over letters"), so this keys off the control
     classes .tool / .view__back, not the broad [data-magnetic] hint the dot's
     colour still reads. Same field as before: a 60px halo, ≤12px displacement,
     peaking halfway out and back to zero at the rim so it's continuous where
     the field ends. Past the reduced-motion return, so a reduce reader never
     sees it.

     C17 (2026-09-07): the §04 origin mark (the interactive V glyph — three
     real <button> hit-regions, already focusable, already answers hover by
     lighting a stroke) joins the set. It is also a .reveal target, so the
     transform channel is shared with the one-shot rise: the reveal uses it
     for 0.9s, once, then leaves it at `none` forever (CLAUDE.md's motion
     note — a transient transform is allowed to hand the channel back). The
     first mouseenter here is always well after §04 has revealed and settled,
     so on that first enter we drop `transform` from the element's transition
     list — GSAP's quickTo then owns the channel unopposed, with no CSS
     transform-transition double-easing every nudge. The lighting/panel path
     (initOrigin) is untouched. */
  function initMagnetic() {
    if (!finePointer) return;
    var RADIUS = 60, PULL = 12;
    document.querySelectorAll('.tool, .view__back, .origin__mark, .tools__hint').forEach(function (el) {
      var qx = gsap.quickTo(el, 'x', { duration: D.state, ease: EASE });
      var qy = gsap.quickTo(el, 'y', { duration: D.state, ease: EASE });
      var box = null;
      var freed = false;

      /* Measured once on enter, with the element's own translate subtracted,
         so the reading can't feed the displacement back into itself — and no
         layout is forced on every mousemove. */
      function capture() {
        /* A .reveal target still lists `transform` in its transition (for the
           rise). By the first hover that rise is long done; hand the channel
           to the pull so quickTo isn't fighting a 0.9s CSS ease. */
        if (!freed && el.classList.contains('reveal')) {
          el.style.transitionProperty = 'opacity';
          freed = true;
        }
        var r = el.getBoundingClientRect();
        var tx = Number(gsap.getProperty(el, 'x')) || 0;
        var ty = Number(gsap.getProperty(el, 'y')) || 0;
        box = {
          cx: r.left + r.width / 2 - tx,
          cy: r.top + r.height / 2 - ty,
          rx: r.width / 2 + RADIUS,
          ry: r.height / 2 + RADIUS
        };
      }

      el.addEventListener('mouseenter', capture);
      el.addEventListener('mousemove', function (e) {
        if (!box) capture();
        /* Normalised per axis against the element's own half-size, so a wide
           switch answers the pointer the same way a 19px icon button does
           instead of pinning at full pull across almost all of itself. */
        var nx = (e.clientX - box.cx) / box.rx;
        var ny = (e.clientY - box.cy) / box.ry;
        var d = Math.hypot(nx, ny);
        /* The vector is scaled, not each axis clamped, so PULL is a real
           ceiling on the distance moved — a diagonal can't reach PULL√2.
           Peaks at PULL halfway out and returns to zero at the edge, which
           keeps it continuous where the field ends. */
        var k = 4 * Math.max(0, 1 - d) * PULL;
        qx(nx * k); qy(ny * k);
      });
      el.addEventListener('mouseleave', function () {
        box = null;
        qx(0); qy(0);   // the same tween, retargeted — not a second one fighting it
      });
    });
  }

  /* ---------- masthead mark: draw-in (P22) ----------
     The V/Y symbol assembles from its three strokes — left arm of the V, then
     the right, then the stem (see style.css). It plays exactly ONCE, a short
     beat after load, then holds — no hover replay: a wordmark is a fixed point
     on the page, not something that re-performs every time the pointer crosses
     it. Pure decoration: wired past the reduced-motion return, so a reduce
     reader never reaches it and the stylesheet pins the clip rects open for
     them instead.

     .is-drawing on .lockup is all the CSS needs; the three rects sit at
     `forwards`, so the finished mark holds once the class is on. Because it is
     added once and never removed, no restart/guard machinery is needed. */
  var LOCKMARK_INTRO = 150;   // ms after this runs before the one-time draw starts
  function initLockmark() {
    var lockup = document.querySelector('.lockup');
    if (!lockup) return;
    // A short beat, not frame 0, so it reads as deliberate rather than a
    // glitch. failsafe() is the backstop if this timer never fires.
    setTimeout(function () { lockup.classList.add('is-drawing'); }, LOCKMARK_INTRO);
  }

  /* ---------- specimen permalinks (Spark Order S9A / move 09) ----------
     Each <article class="spec"> carries a stable id, and its label is an
     anchor to that id — so a reader who recognises one of the three errors
     as their own can link straight to it. A click also drops the full URL on
     the clipboard and says so, briefly, in the page's own two languages.
     Everything here is enhancement over a plain in-page anchor: with this
     file absent the label is still <a href="#specimen-...">, the browser
     still jumps, and the status line stays hidden. Wired before the
     reduced-motion return because it is navigation, not motion — the only
     concession to reduced motion is an instant scroll instead of a smooth
     one, which is the same rule the generic #-anchor handler above follows. */
  function initSpecimenPermalinks() {
    var links = document.querySelectorAll('.spec__permalink[data-permalink]');
    if (!links.length) return;
    links.forEach(function (a) {
      var status = a.parentNode.querySelector('.spec__permalink-status');
      var clearStatus = null;
      a.addEventListener('click', function (e) {
        var id = (a.getAttribute('href') || '').slice(1);
        var target = id && document.getElementById(id);
        if (!target) return;   // nothing to route to — let the browser decide
        e.preventDefault();
        /* The address bar becomes the shareable link. pushState (not a raw
           hash assignment) keeps Back working and does NOT fire hashchange,
           so the collage router's routeAfterHashChange stays out of it. */
        if (window.history.pushState) window.history.pushState(null, '', '#' + id);
        else location.hash = id;
        if (lenis) lenis.scrollTo(target, { offset: -headerHeight(), duration: 1.2 });
        else target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
        if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });   // land inside the specimen, not just near it
        if (status && navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(location.href).then(function () {
            status.hidden = false;               // role="status" announces the visible language
            clearTimeout(clearStatus);
            clearStatus = setTimeout(function () { status.hidden = true; }, 1800);
          }).catch(function () {});               // clipboard blocked — the URL bar still carries it
        }
      });
    });
  }

  /* ---------- collage: a hash-routed full-screen view ----------
     One file, but #collage behaves like its own page. location.hash is the
     single source of truth, so the browser back and forward buttons work for
     free: back drops the hash, hashchange fires, the view closes. Entering it
     makes #app and the masthead inert (focus can't wander behind the view,
     the page behind can't scroll), moves focus to the heading, and parks the
     Lenis scroll. With this whole file absent the view is the last section of
     the document and the "See the work" link is an ordinary anchor to it. */
  function initCollageView() {
    var view = document.getElementById('collage');
    if (!view) return;
    var title = document.getElementById('collage-title');
    var backBtn = view.querySelector('.view__back');
    var opener = document.querySelector('[data-collage-open]');
    // The view's own "Photographs" label — always the first .label in
    // view__body, always in the viewport the moment the view opens — is the
    // door's morph target (S7 Stage 2). The group labels further down share
    // the class but sit later in document order, so the first match is this one.
    var doorLabel = view.querySelector('.label');
    var canInert = 'inert' in HTMLElement.prototype;
    // everything that is NOT the view — made inert while it is open so focus
    // can't wander behind it and the skip link can't jump into inert content
    var behind = [
      document.getElementById('app'),
      document.querySelector('.masthead'),
      document.querySelector('.skip')
    ].filter(Boolean);
    function setBehindInert(on) { if (canInert) behind.forEach(function (el) { el.inert = on; }); }
    var returnFocus = null;
    var savedScroll = 0;   // where the site was when the view opened
    var applied = false;   // have the open side-effects run? (the .collage-open
                           // class can already be set by the <head> script on a
                           // deep link, so the class alone isn't the test)

    function bgScroll() { return lenis ? lenis.scroll : (window.scrollY || 0); }
    function bgScrollTo(y) {
      if (lenis) lenis.scrollTo(y, { immediate: true });
      else window.scrollTo(0, y);
    }

    // Stage 2 pitfall: a warm open's own click also lands #collage in the URL,
    // and the browser's native scroll-to-fragment for it turns out not to be
    // pushState-exempt after all — it still runs, just on a delayed task
    // (invisible before Stage 2, whose warm opens always ran applyOpen() in
    // the very same tick as the click, before that task got a turn). Wrapping
    // the open in a View Transition gives it a real gap to land in, so the
    // scroll/focus snapshot has to be taken here — synchronously, before
    // withTransition() ever schedules the deferred half — not inside
    // applyOpen() itself, which now sometimes runs a frame or more later.
    var openCaptured = false;
    function captureOpenState(cold) {
      returnFocus = (document.activeElement && document.activeElement !== document.body)
        ? document.activeElement : opener;
      savedScroll = cold ? 0 : bgScroll();
      openCaptured = true;
    }

    function applyOpen(cold) {
      if (applied) return;
      applied = true;
      if (!openCaptured) {
        // A deep link makes the browser scroll the document toward the
        // #collage element (last in the DOM); a cold open therefore returns
        // to the top, a warm one returns exactly where the reader was.
        returnFocus = (document.activeElement && document.activeElement !== document.body)
          ? document.activeElement : opener;
        savedScroll = cold ? 0 : bgScroll();
      }
      openCaptured = false;
      root.classList.add('collage-open');        // CSS flips the view visible synchronously
      setBehindInert(true);
      if (lenis) lenis.stop();
      view.scrollTop = 0;
      promoteCollageImages(view);   // first open: let the 18 figures actually fetch
      armCollageReveals(view);   // first open: hand the tiles to their own observer
      initCollageLightbox(view);   // first open: wrap the tiles in real controls
      // Synchronous: the view is visible the moment the class lands, and rAF
      // can be suspended in a background tab (see whenRendering above) — a
      // deferred focus move is a focus move that might never happen.
      if (title) title.focus({ preventScroll: true });
      /* On a deep link the browser runs its own scroll-to-fragment after this,
         and because html.js .view is an overflow:auto scroll container it is
         browser-focusable — so the fragment step lands focus on #collage (an
         unlabelled wrapper) instead of the heading, and undoes the line above.
         Re-assert the heading once the document has settled, and reset the
         saved scroll so the way back still returns to the top. */
      if (cold) {
        var settle = function () {
          if (!applied) return;
          savedScroll = 0;
          if (title && document.activeElement !== title) title.focus({ preventScroll: true });
        };
        if (document.readyState === 'complete') requestAnimationFrame(settle);
        else window.addEventListener('load', function reassert() {
          window.removeEventListener('load', reassert);
          settle();
        });
      }
    }

    function applyClose() {
      if (!applied) return;
      applied = false;
      root.classList.remove('collage-open');
      setBehindInert(false);
      if (lenis) lenis.start();
      bgScrollTo(savedScroll);
      if (returnFocus && returnFocus.focus) returnFocus.focus({ preventScroll: true });
      // Reopen lands on a settled view, not a half-run stagger: put every tile
      // back to .is-in. Any the observer hasn't fired yet stay observed and
      // will still catch up on scroll.
      view.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
    }

    function sync(cold) { (location.hash === '#collage') ? applyOpen(cold) : applyClose(); }

    /* S7 move 04, extended at Stage 2 — animate the route with a View
       Transition on BOTH directions. Closing already proved this safe: focus
       returns to the opener and every close test settles first. Opening used
       to be excluded because applyOpen() focuses the heading synchronously
       and startViewTransition defers its update callback ~1 frame — a
       deferred focus is a focus that might never land, a bug this view has
       shipped once already (see BUILD-NOTES). Stage 2's fix isn't to avoid
       the callback, it's to keep living inside it: applyOpen()'s class flip
       and focus move are two lines apart and both run synchronously *within*
       whichever call fires them, VT callback or not, so the one thing that
       changes is which frame that pair happens on — never whether they stay
       adjacent to each other. withTransition()'s failsafe below covers the
       one real risk (the callback never running at all). */
    function canTransition() {
      return typeof document.startViewTransition === 'function' && !reduce
        && document.visibilityState === 'visible';
    }
    // Shared by every VT-eligible route. `mutate` is always one of sync()'s
    // two idempotent halves (applyOpen/applyClose each guard on `applied`),
    // so if startViewTransition's update callback is merely slow rather than
    // lost, racing a direct call after a short failsafe costs nothing — the
    // real call either already ran (the direct call is a no-op) or is about
    // to (the deferred callback's own call becomes the no-op instead).
    function withTransition(mutate) {
      if (!canTransition()) { mutate(); return null; }
      var t = document.startViewTransition(mutate);
      var settled = false;
      var mark = function () { settled = true; };
      t.updateCallbackDone.then(mark, mark);
      setTimeout(function () { if (!settled) mutate(); }, 100);
      return t;
    }
    function routeAfterHashChange() {
      // Only an actual open<->closed flip takes the transition — otherwise
      // sync() is a no-op and wrapping a no-op update in startViewTransition
      // just fires an invisible cross-fade on every unrelated in-page hash
      // (the specimen permalinks, #top, #method).
      var opening = !applied && location.hash === '#collage';
      var closing = applied && location.hash !== '#collage';
      if (opening) captureOpenState(false);   // before the transition's own delay, see applyOpen
      if (opening || closing) withTransition(function () { sync(false); });
      else sync(false);
    }

    /* The door: "See the work" morphs into the view's own "Photographs"
       label, so the way in reads as one element moving and growing rather
       than a swap-and-fade — the shared-element move Stage 2 adds on top of
       the plain cross-fade every other route gets. Both ends carry the same
       view-transition-name only for the life of one transition: the source
       before the call (tagging its pre-transition snapshot), the destination
       inside the callback (tagging its post-transition snapshot), cleared
       again once the transition settles so neither element carries a stale
       name into some later, unrelated transition. Only this one entry point
       gets the named morph — the masthead glyph jumps keep their existing
       smooth scroll and plain cross-fade (their destinations sit off-screen
       at capture time; see BUILD-NOTES for why that morph doesn't work). */
    var DOOR_NAME = 'collage-door';
    function openWithDoorMorph() {
      if (!canTransition() || !opener || !doorLabel) { sync(false); return; }
      captureOpenState(false);   // before the transition's own delay, see applyOpen
      opener.style.viewTransitionName = DOOR_NAME;
      var t = withTransition(function () {
        sync(false);
        opener.style.viewTransitionName = '';
        doorLabel.style.viewTransitionName = DOOR_NAME;
      });
      if (t) {
        var release = function () { doorLabel.style.viewTransitionName = ''; };
        t.finished.then(release, release);
      }
    }

    function leave() {
      // Real history keeps forward working; only synthesise a state if we'd
      // otherwise walk off the site (deep link opened in a fresh tab).
      if (window.history.length > 1) window.history.back();
      else {
        history.replaceState(null, '', location.pathname + location.search);
        routeAfterHashChange();
      }
    }

    if (opener) opener.addEventListener('click', function (e) {
      e.preventDefault();
      if (history.pushState) history.pushState(null, '', '#collage');
      else location.hash = 'collage';
      openWithDoorMorph();
    });

    /* The masthead glyph icons (chess / carabiner / book) are shortcuts into
       the view: open it if it's closed, then slide that domain group's label
       to the top and move focus onto its heading. Native smooth scroll on the
       view's own overflow:auto container — Lenis is parked while the view is
       open — and it drops to an instant jump under prefers-reduced-motion.
       Done synchronously, not in a rAF: applyOpen has already flipped
       .collage-open (visibility/opacity only, so geometry is live), and a
       deferred frame can be suspended in a background tab — same reason
       applyOpen focuses synchronously. */
    var jumpers = document.querySelectorAll('[data-collage-jump]');
    var bar = view.querySelector('.view__bar');
    var JUMP_GAP = 16;   // breathing room left between the sticky bar and the landed label
    function jumpToGroup(key) {
      var heading = document.getElementById('collage-' + key);
      if (!heading) return;
      var group = heading.closest('.view__group');
      /* Land the group's label under the sticky bar — it carries the glyph
         that was clicked, so it's what should arrive at the top. Scrolling to
         the group's own edge instead would park it below the 40–90px of
         inter-group padding that only reads right when you scroll in. */
      var anchor = (group && group.querySelector('.label')) || heading;
      var barH = bar ? bar.getBoundingClientRect().height : 0;
      var top = anchor.getBoundingClientRect().top
              - view.getBoundingClientRect().top
              + view.scrollTop - barH - JUMP_GAP;
      if (top < 0) top = 0;
      if (view.scrollTo) view.scrollTo({ top: top, behavior: reduce ? 'auto' : 'smooth' });
      else view.scrollTop = top;
      heading.focus({ preventScroll: true });   // preventScroll: don't fight the scroll
    }
    jumpers.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var key = btn.getAttribute('data-collage-jump');
        // Focus the button first so applyOpen captures it as returnFocus and
        // Back lands here — a plain mouse click doesn't focus a <button> in
        // every browser (Safari), which would otherwise send Back to the opener.
        btn.focus({ preventScroll: true });
        if (location.hash !== '#collage') {
          if (history.pushState) history.pushState(null, '', '#collage');
          else location.hash = 'collage';
          sync(false);        // masthead goes inert here; the icons are one-shot
        }
        jumpToGroup(key);
      });
    });

    if (backBtn) backBtn.addEventListener('click', leave);
    window.addEventListener('hashchange', function () { routeAfterHashChange(); });
    document.addEventListener('keydown', function (e) {
      // Stage 3: the lightbox is a layer on top of this view, with its own
      // Escape handler (initCollageLightbox) — this one no-ops while that
      // flag is set, so Escape closes one layer at a time rather than both.
      if ((e.key === 'Escape' || e.key === 'Esc') && applied && !lightboxOpen) {
        e.preventDefault(); leave();
      }
    });

    sync(true);   // deep-link path; the <head> script already set .collage-open
  }

  /* ---------- who: the rows answer the question (Spark Order S5 / move 19) ----
     Section 05 asks "which of these is you?" and, until now, gave no way to
     say. Each row gets an invisible overlay <button> (built here, so a no-JS
     reader still sees four plain rows and the CTA keeps its static href).
     Picking a row is single-choice and toggleable; it composes a first-person
     clause from the row's own data-prefill-* onto the section 06 Telegram CTA,
     so Igor receives the answer without the reader having to phrase it.
     Selection and language compose through one writer, updateCta(), which
     reads both every time — never the href built in two places. Wired before
     the reduced-motion return: this is interaction, not decoration. */
  function initWhoRows() {
    var cta = document.querySelector('.contact__cta');
    var rows = document.querySelectorAll('.rows > li');
    var ref = cta && cta.getAttribute('data-href-en');
    if (!cta || !rows.length || !ref || ref.indexOf('?text=') < 0) return;

    var BASE = ref.slice(0, ref.indexOf('?text=') + 6);   // "https://t.me/<handle>?text="
    var selected = null;                                   // picked row index, or null

    function lang() { return root.getAttribute('data-lang') === 'ru' ? 'ru' : 'en'; }
    function decodedBase(l) {
      var h = cta.getAttribute('data-href-' + l) || '';
      var i = h.indexOf('?text=');
      return i < 0 ? '' : decodeURIComponent(h.slice(i + 6));
    }
    // The one place the CTA href is written. No selection: hand it back to
    // theme.js's plain per-language default (applyLang sets the same value on
    // a switch — this keeps them in step between switches). A selection:
    // baseMessage + " — " + the row's clause, in the current language.
    function updateCta() {
      var l = lang();
      if (selected === null) { cta.setAttribute('href', cta.getAttribute('data-href-' + l)); return; }
      var clause = rows[selected].getAttribute('data-prefill-' + l) || '';
      cta.setAttribute('href', BASE + encodeURIComponent(decodedBase(l) + ' — ' + clause));
    }

    var picks = [];
    rows.forEach(function (li, i) {
      var h3 = li.querySelector('h3');
      if (!h3) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'row__pick';
      btn.setAttribute('aria-pressed', 'false');
      /* Named by a visually-hidden span carrying the heading's own
         data-en/data-ru — the exact shape .origin__hit uses, so theme.js's
         applyLang() keeps the label in the right language for free. Set the
         initial text here because applyLang has already run by the time
         main.js builds this. */
      var vh = document.createElement('span');
      vh.className = 'vh';
      if (h3.dataset.en) vh.setAttribute('data-en', h3.dataset.en);
      if (h3.dataset.ru) vh.setAttribute('data-ru', h3.dataset.ru);
      vh.textContent = h3.dataset[lang()] || h3.textContent || '';
      btn.appendChild(vh);
      btn.addEventListener('click', function () {
        selected = (selected === i) ? null : i;      // toggleable, single-choice
        picks.forEach(function (b, j) { b.setAttribute('aria-pressed', selected === j ? 'true' : 'false'); });
        rows.forEach(function (r, j) { r.classList.toggle('is-picked', selected === j); });
        updateCta();
      });
      li.appendChild(btn);
      picks.push(btn);
    });

    // A language switch re-sets the default href and fires this; re-run the
    // one writer so a live selection recomposes in the new language.
    document.addEventListener('vitnyr:langchange', updateCta);
  }

  /* ---------- the specimen reveal ----------
     Rest state is the "Correct:" line plus a prompt where the error used to
     be — "+ Show the common mistake", an amber-ruled control with an
     underline (and the pointer dot's own specimen ink over it, since HOT
     includes <button>). Hover, tap or keyboard focus opens it: the prompt's
     content swaps to the error sentence itself — the cloned .sig glyph and
     the <del> word in amber — and the marker flips to "−". A tap or Enter
     locks it open; a plain hover closes again on leave.

     No transform, nothing time-based, no scroll trigger, so this is wired
     before the reduced-motion return, same as the collage router and the
     origin panel: an affordance, not motion. With no JS the button is never
     built and the untouched static <del>/<ins> pair is the whole of it — the
     real .wrong line stays in the DOM (only `hidden` under JS) so that render
     and every box-measuring test keep their source of truth. */
  function initSpecimenReveal() {
    var specs = document.querySelectorAll('#specimen .spec');
    if (!specs.length) return;
    var isRu = function () { return document.documentElement.getAttribute('data-lang') === 'ru'; };

    specs.forEach(function (spec) {
      var lines = spec.querySelector('.spec__lines');
      // Some specimens carry one .line-spec.wrong (English-only grammar
      // examples); others carry two, one per data-l — pick whichever
      // matches the live language so the hover preview never freezes on
      // whichever language happened to be first in the DOM.
      var wrongs = spec.querySelectorAll('.line-spec.wrong');
      if (!lines || !wrongs.length) return;
      function currentWrong() {
        if (wrongs.length === 1) return wrongs[0];
        var want = isRu() ? 'ru' : 'en';
        for (var i = 0; i < wrongs.length; i++) {
          if (wrongs[i].getAttribute('data-l') === want) return wrongs[i];
        }
        return wrongs[0];
      }

      var wrap = document.createElement('div');
      wrap.className = 'spec__reveal';
      wrap.setAttribute('data-open', 'false');

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'spec__prompt';
      btn.setAttribute('aria-expanded', 'false');

      var mark = document.createElement('span');
      mark.className = 'spec__prompt-mark';
      mark.setAttribute('aria-hidden', 'true');
      mark.textContent = '+';

      var label = document.createElement('span');
      label.className = 'spec__prompt-label';
      label.setAttribute('data-en', 'Show the common mistake');
      label.setAttribute('data-ru', 'Показать типичную ошибку');
      label.textContent = isRu() ? 'Показать типичную ошибку' : 'Show the common mistake';

      var reveal = document.createElement('span');
      reveal.className = 'spec__prompt-mistake';
      reveal.hidden = true;

      function fillReveal() {
        reveal.textContent = '';
        var w = currentWrong();
        var sentence = w.children[w.children.length - 1];   // the visible sentence <span>
        var sig = w.querySelector('.sig');
        if (sig) reveal.appendChild(sig.cloneNode(true));
        if (sentence) reveal.appendChild(sentence.cloneNode(true));
      }
      fillReveal();

      btn.appendChild(mark);
      btn.appendChild(label);
      btn.appendChild(reveal);
      wrap.appendChild(btn);
      lines.insertBefore(wrap, wrongs[0]);
      wrongs.forEach(function (w) { w.hidden = true; });   // JS-only: the static pair stays the no-JS source of truth

      document.addEventListener('vitnyr:langchange', fillReveal);

      // hover previews it; a click/tap/Enter locks it open or shut. Keyboard
      // is the lock alone (Tab to the button, Enter) — no focus-preview, so a
      // mouse click that leaves the button focused can't wedge it open.
      var st = { hover: false, lock: false };
      function render() {
        var open = st.hover || st.lock;
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        wrap.setAttribute('data-open', open ? 'true' : 'false');
        label.hidden = open;
        reveal.hidden = !open;
        mark.textContent = open ? '−' : '+';   // − / +
      }

      btn.addEventListener('mouseenter', function () { st.hover = true; render(); });
      btn.addEventListener('mouseleave', function () { st.hover = false; render(); });
      btn.addEventListener('click', function () {
        st.lock = !st.lock;
        st.hover = false;   // a tap owns the state; ignore any synthetic hover it fires
        render();
      });

      render();
    });
  }

  /* ---------- mechanism fold (§02) ----------
     Independent disclosures, not an exclusive accordion — opening one
     doesn't close the others. All start collapsed (aria-expanded set here,
     not in the HTML, so a no-JS reader never sees a "closed" attribute with
     no script able to open it back up — style.css only clips .mech__panel
     under html.js, so the un-set default renders fully open there). The
     +/− swap mirrors initSpecimenReveal()'s mark; the panel's own open/close
     is CSS alone, reading this same aria-expanded via :has(). */
  function initMechanismFold() {
    var toggles = document.querySelectorAll('.mech__toggle');
    if (!toggles.length) return;
    toggles.forEach(function (btn) {
      btn.setAttribute('aria-expanded', 'false');
      var mark = btn.querySelector('.mech__toggle-mark');
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        if (mark) mark.textContent = open ? '+' : '−';
      });
    });
  }

  /* ---------- last resort ----------
     Anything on screen that is still hidden gets shown outright. A missed
     reveal must never cost someone the content. Read pass first, then write,
     so one stuck element doesn't cause a layout thrash down the whole page. */
  var sweepTimer = 0;
  function failsafe() {
    // The same line the observer uses, not the full viewport: an element
    // sitting in the bottom 20% is being held back on purpose, and forcing it
    // in would cost it the animation it was about to get.
    var line = (window.innerHeight || 0) * 0.8;
    var stuck = [];
    document.querySelectorAll('.reveal').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < line && r.bottom > 0 && parseFloat(getComputedStyle(el).opacity) < 0.05) stuck.push(el);
    });
    stuck.forEach(function (el) { el.classList.add('is-in'); });
    // The hero carries no .reveal class, so the sweep above cannot reach it —
    // armHeroGuard() covers it, on every play rather than only this one.
    if (!heroStarted) showHeroNow();
    // The masthead mark is not a .reveal target (it must not rise), so the
    // sweep can't reach it either. If initLockmark() never armed the draw its
    // clip rects are still collapsed under html.js — show it outright. Guarded,
    // so a mark that drew normally is left alone (no re-draw 2.5s in).
    var lm = document.querySelector('.lockup');
    if (lm && !lm.classList.contains('is-drawing')) lm.classList.add('is-drawing');
  }
  // Re-armed rather than one-shot: a language switch brings a different set of
  // elements on screen, all of them after this sweep would have come and gone.
  function armFailsafe() { clearTimeout(sweepTimer); sweepTimer = setTimeout(failsafe, 2500); }

  /* ---------- go ---------- */
  buildReveals();
  initOrigin();
  initLockmark();
  initCursor();
  initMagnetic();

  whenRendering(function () {
    /* Hold the hero until the display face is real, so the lines don't rise in
       a fallback and reflow at the top of the page — but never longer than
       1.5s, because a slow font CDN must not hold the headline hostage. */
    var ready = (document.fonts && document.fonts.ready) ? document.fonts.ready : Promise.resolve();
    var timeout = new Promise(function (r) { setTimeout(r, 1500); });
    Promise.race([ready, timeout]).then(playHero);
    armFailsafe();
  });

  // Switching language swaps in a different set of hero lines — replay them.
  // Ignored before the hero has run once: theme.js fires this at
  // DOMContentLoaded to stamp the initial language, which is not a change.
  document.addEventListener('vitnyr:langchange', function () {
    if (!heroStarted) return;
    whenRendering(function () { playHero(); armFailsafe(); });
  });
})();
