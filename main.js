/* ============================================================
   Vitnyr motion
   One easing curve (cubic-bezier(.16, 1, .3, 1)) and one reveal rhythm
   (fade and a 24px rise, 0.9s, 0.08s stagger, once). Everything degrades:
   no JS, no GSAP, reduced motion, touch or a background tab all end with
   the same readable page.
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

  /* Every animation timing comes from this table, so the page reads as one
     instrument. Scrolling is separate: Lenis's duration and the scrollTo
     calls are scroll physics.
       micro: a thing appearing or disappearing outright
       state: a hover, a magnet, a theme settling (--t in the sheet)
       hero:  the single longest move on the page, used once
     The reveal's own 0.9s lives in the stylesheet, where the transition is. */
  var D = { micro: 0.3, state: 0.6, hero: 1.05 };
  var STAGGER = 0.08;

  /* ---------- first-frame gate ----------
     A tab that loads hidden has rAF suspended, so tweens would sit at their
     from-state. Nothing time-based starts until a frame has rendered; rAF
     itself is the test, because it is what the tweens need. */
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

  /* The progress hairline rides the same scroll source. trackProgress scales
     .progress off document depth and flips .past-origin once the reader
     crosses the ink switch, so the rule crossfades from specimen to target
     (the CSS owns the crossfade; this only picks the side). */
  var progressEl = document.querySelector('.progress');
  // The switch sits at #who on a discipline page and at the mark (#origin) on
  // home: where the page stops explaining and starts sending people on.
  var INK_SWITCH_EL = document.getElementById('who') || document.getElementById('origin');
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
  /* Phone masthead, out of the way while reading: scroll down past 120px and
     the bar slides up (.mast-hidden, its own transform); any scroll up brings
     it back. Never hidden near the top, while focus is inside it, while the
     collage view is open, or during a jump from an in-page link (navLock, set
     by jumpTo()), since hiding mid-jump would leave headerHeight()'s offset
     as an empty band over the destination. */
  var mastEl = document.querySelector('.masthead');
  var phoneMast = window.matchMedia('(max-width: 602px)');
  var navLock = false, lastY = 0, downRun = 0, upRun = 0;
  function showMast() { root.classList.remove('mast-hidden'); downRun = 0; upRun = 0; }
  function releaseNav() { navLock = false; showMast(); }
  function trackMast(y) {
    var max = Math.max(0, root.scrollHeight - window.innerHeight);
    y = Math.min(max, Math.max(0, y));          // iOS bounce must not flip it
    var dy = y - lastY;
    lastY = y;
    if (!mastEl || !phoneMast.matches || navLock || y <= 120 ||
        root.classList.contains('collage-open') ||
        mastEl.contains(document.activeElement)) { showMast(); return; }
    // Runs, not single deltas: Lenis reports a smoothed scroll a few px per
    // frame, so one frame's delta almost never clears a threshold on its own.
    if (dy < 0) {
      downRun = 0; upRun -= dy;
      if (upRun >= 4) showMast();
    } else if (dy > 0) {
      upRun = 0; downRun += dy;
      if (downRun >= 8) root.classList.add('mast-hidden');
    }
  }
  if (mastEl) mastEl.addEventListener('focusin', showMast);
  function onScroll(y) { setStuck(y); trackProgress(y); trackMast(y); }

  if (lenis) lenis.on('scroll', function (e) { onScroll(e.scroll); });
  else window.addEventListener('scroll', function () { onScroll(window.scrollY); }, { passive: true });
  measureInkSwitch();
  onScroll(scrollPos());
  window.addEventListener('resize', function () { measureInkSwitch(); onScroll(scrollPos()); }, { passive: true });
  document.addEventListener('vitnyr:langchange', function () {
    requestAnimationFrame(function () { measureInkSwitch(); onScroll(scrollPos()); });
  });

  /* Every in-page destination lands clear of the fixed masthead. CSS
     scroll-margin-top covers the browser's own fragment jumps; Lenis ignores
     it, so Lenis jumps pass the same clearance as a negative offset, measured
     off the masthead's rendered height. */
  function headerHeight() {
    var el = document.querySelector('.masthead');
    return el ? el.getBoundingClientRect().height : 0;
  }

  // In-page links go through Lenis so the easing stays consistent. Links that
  // JS builds later (the pick status) use jumpTo() too.
  function jumpTo(target) {
    navLock = true;
    showMast();
    if (lenis) lenis.scrollTo(target, { offset: -headerHeight(), duration: 1.2, onComplete: releaseNav });
    else { target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); setTimeout(releaseNav, 900); }
    /* Scrolling is not navigating. preventDefault also cancels the focus move
       the browser would have made, which for the skip link is the entire
       point of the link — a keyboard user would land back in the masthead. */
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  }
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    if (a.hasAttribute('data-collage-open')) return;   // the collage router owns this one
    if (a.hasAttribute('data-collage-link')) return;   // and these
    if (a.hasAttribute('data-permalink')) return;      // initSpecimenPermalinks owns these
    if (a.classList.contains('footmark-home')) return; // initCollageView owns this one too
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      jumpTo(target);
    });
  });

  /* The collage view is routing, not motion — it has to work under reduced
     motion and with GSAP present but Lenis off, so it is wired before the
     reduced-motion path returns. */
  initCollageView();
  initWhoRows();
  initDock();
  initFoot();             // a clock and a focus fix, not motion
  initSpecimenPermalinks();
  initMechanismFold();    // same: a disclosure, not motion — CSS handles the open/close transition itself
  initEarTest();          // an affordance, not motion

  /* ---------- reduced motion: show the finished state and stop ---------- */
  if (reduce) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
    gsap.set('.line__inner', { y: '0%' });
    root.classList.add('hero-done');
    // Reduced motion drops the animation, not the content: the mark's hover
    // and focus still work (initOrigin gates its own idle hint).
    initOrigin();
    return;
  }

  /* ---------- language crossfade ----------
     theme.js swaps the language inside its own click handler, so it calls
     window.__vitnyrLangFade with the swap as a callback when one exists, and
     runs the swap bare otherwise (no main.js, no GSAP, reduced motion: an
     instant switch). Installed past the reduced-motion return, so it exists
     only when motion is allowed. The swap runs at once, then #app is cut to
     transparent and fades back over D.state. */
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
        // The mark sequences its own draw-in after this, listening for the event
        // rather than reaching into this tween.
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
     One pattern for the whole page: 24px rise and fade, 0.9s, the brand
     curve, staggered 0.08s, fired once when the element itself is 20% into
     view. Observed per element, not per section, so items far below the fold
     haven't finished before they are seen. */
  var REVEAL_CAP = 4;   // past four beats a stagger reads as lag, so the count restarts

  // The one place a batch of .reveal targets becomes a staggered entrance,
  // shared with the collage view's observer (armCollageReveals).
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
    // Collage tiles are .reveal too, but in a hidden fixed view the page's
    // observer would fire them all at load. They ship .is-in and get their own
    // observer on first open (armCollageReveals).
    var items = [];
    document.querySelectorAll('.reveal').forEach(function (el) {
      if (!el.closest('#collage')) items.push(el);
    });
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    // The hero is on screen at load, so it gets its own observer against the
    // true viewport; the -20% margin is for everything below it (on the hero it
    // cut a dead band where .scrollcue lives).
    var hero = [], rest = [];
    items.forEach(function (el) {
      // The mark stays in `items` (so a no-IO browser force-shows it), but its
      // .is-in is sequenced after the hero by initOrigin(), not fired here.
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

  /* The collage tiles run the page's reveal rhythm off the view's own
     overflow: auto root, wired on first open (until then the view is fixed and
     hidden, and a viewport observer would burn the whole entrance). Tiles
     ship .is-in; this strips it so the observer can stagger them in. Once. */
  /* The figures ship data-src/data-srcset, inert to the browser's loader, so
     a hidden view doesn't download every photo on page load (native lazy
     loading treats a fixed panel over the viewport as near enough to fetch).
     Promoted to real attributes here, on first open; a <noscript> copy keeps
     the no-JS page whole. */
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

  /* ---------- collage lightbox ----------
     Click a tile to enlarge it. The per-tile <button> and the dialog are
     built here at runtime, so the no-JS document keeps plain <figure>s.
     Routing stays outside location.hash: Escape closes the lightbox, closing
     returns focus to the tile that opened it, and browser Back still closes
     the whole #collage view. */
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

    // Icon-only controls: plain English aria-label, like the masthead icons.
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

    // Re-run on open and on every prev/next step; theme.js's applyLang() does
    // the language.
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

    // Open/close motion is additive: with GSAP absent or reduced motion, open()
    // just flips `hidden`. canAnimate is re-checked on every call, and
    // killBoxTween stops a double-click stacking two tweens.
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
      // Touch has no hover, so the colour reveal fires here on open and clears on
      // close.
      if (!finePointer) box.classList.add('is-colour');
      if (canInert) {
        if (bar) bar.inert = true;
        if (body) body.inert = true;
      }
      box.focus({ preventScroll: true });

      if (canAnimate()) {
        killBoxTween();
        // The photo grows from where its tile sat, so it reads as the photo
        // answering the click. transform-origin is relative to media's own box, so
        // the opener's rect is measured against media's rect after box.hidden
        // flips.
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
    // Close stays synchronous: Escape and the buttons read `hidden` and the
    // focus back at once, and a keyboard user tabbing right after Escape must
    // land on reachable content. Only the entrance animates.
    function close() {
      if (!lightboxOpen) return;
      lightboxOpen = false;
      killBoxTween();
      box.hidden = true;
      box.classList.remove('is-colour');
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

    // Wraps each figure's .collage__slot in a real button, so click, Enter and
    // Space work natively. Prev/next follow the flat figure order.
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
     Home page only. The mark's three strokes and the three doors below it
     are links to the discipline pages. Hovering or focusing either one
     lights that stroke, shows its sigil and lights its door; leaving puts
     the mark back to rest (all three strokes at full ink). */
  function initOrigin() {
    var mark = document.querySelector('.origin__mark');
    if (!mark) return;
    var hits = document.querySelectorAll('.origin__hit');
    if (!hits.length) return;
    var parts = mark.querySelectorAll('.glyph__part');
    var sigils = mark.querySelectorAll('.origin__sigil');
    var doors = document.querySelectorAll('.door');
    var idleTl = null;
    // Set by any real hover or focus. The idle hint checks it on every step
    // as well as being killed, because a step already queued for this frame
    // can still fire after .kill().
    var engaged = false;

    // The strokes and sigils only; the idle hint uses this on its own.
    function paintGlyph(name) {
      parts.forEach(function (el) {
        var on = el.dataset.discipline === name;
        el.classList.toggle('is-active', on);
        el.classList.toggle('is-dim', !!name && !on);
      });
      sigils.forEach(function (el) {
        el.classList.toggle('is-preview', el.dataset.discipline === name);
      });
    }
    function endIdle() {
      if (idleTl) { idleTl.kill(); idleTl = null; }
    }
    function preview(name) {
      engaged = true;
      // a reader who tabs in before the draw-in has started must not land
      // on an invisible control
      mark.classList.add('is-in');
      endIdle();
      paintGlyph(name);
      doors.forEach(function (el) {
        el.classList.toggle('is-active', el.dataset.discipline === name);
      });
    }
    function wire(el) {
      var name = el.dataset.discipline;
      el.addEventListener('focus', function () { preview(name); });
      el.addEventListener('blur', function () { preview(null); });
      if (finePointer) {
        el.addEventListener('pointerenter', function () { preview(name); });
        el.addEventListener('pointerleave', function () { preview(null); });
      }
    }
    hits.forEach(wire);
    doors.forEach(wire);

    // One-shot hint when the section first scrolls into view: the strokes
    // light in turn (each with its sigil), then the mark comes back to rest.
    // It never touches the doors. Skipped under reduced motion.
    if (reduce || !('IntersectionObserver' in window)) return;
    // The draw-in (~0.9s of CSS, keyed off .is-in) finishes before the hint
    // starts, so the two never drive the same strokes in one frame.
    var DRAW_HOLD = 1.0;
    // The mark waits for the hero to land (the vitnyr:heroin event), with a
    // fixed fallback in case that one-time event fired before the mark was
    // seen. Never reach into playHero() itself: see the NaN-transform note
    // in BUILD-NOTES.
    var HERO_WAIT_MS = 1800;
    function drawThenHint() {
      if (engaged || mark.classList.contains('is-in')) return;
      mark.classList.add('is-in');
      var tl = gsap.timeline({
        delay: DRAW_HOLD,
        onComplete: function () {
          idleTl = null;
          if (!engaged) paintGlyph(null);
        }
      });
      ['english', 'chess', 'climbing'].forEach(function (name) {
        tl.call(function () { if (!engaged) paintGlyph(name); }).to({}, { duration: 1 });
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
     On a fine pointer one dot is the cursor (cursor: none is page-wide under
     .has-cursor). It never changes size; its one signal is colour, easing to
     an accent over a control (the colours live in the stylesheet). The
     magnetic pull lives in initMagnetic(), on non-text controls only. */
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
        // First real move: .has-cursor hides the native pointer page-wide and fades
        // the dot in (the opacity is the sheet's).
        shown = true;
        cx = mx; cy = my;
        gsap.set(el, { x: mx, y: my });
        root.classList.add('has-cursor');
      }
      root.classList.remove('cursor-out');   // back inside the window
      kick();
    }, { passive: true });

    /* The dot is the pointer, so it answers the pointer leaving the window
       instead of stranding at the last edge; mouseenter and the next mousemove
       clear it. */
    root.addEventListener('mouseleave', function () { root.classList.add('cursor-out'); });
    root.addEventListener('mouseenter', function () { root.classList.remove('cursor-out'); });

    /* The one signal is colour: .cursor-active plus the two ink variants. Over
       a control inside #specimen the dot takes amber, elsewhere the target ink.
       The sheet owns every visual; this only names the state. */
    var HOT = 'a, button, [data-magnetic]';
    // The footer grounds in the other pair, so the dot flips its ink there
    // (.on-foot).
    document.addEventListener('mouseover', function (e) {
      el.classList.toggle('on-foot', !!(e.target.closest && e.target.closest('.foot')));
    });
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
     Non-text controls only (.tool, .view__back, the home mark), never running
     copy or text links. A 60px halo, up to 12px of displacement, peaking
     halfway out and back to zero at the rim. Past the reduced-motion return.
     The home mark is also a .reveal, so on first hover it drops `transform`
     from its transition list and quickTo owns the channel from then on. */
  /* ---------- in their words: the testimonials marquee ----------
     Past the reduced-motion return, so reduced motion keeps the static grid.
     The list is cloned once (aria-hidden and inert, so screen readers and the
     tab order meet each quote once) and the track drifts one list-width, then
     wraps. The page's scroll steers it: down pushes it left and faster, up
     swings it right, then it eases back to a slow drift. Velocity comes from
     scrollPos() deltas, so native touch scrolling steers it too. Hover holds
     it, Pause stops it, and it idles while off screen. */
  function initVoices() {
    var band = document.querySelector('.voices__band');
    var track = band && band.querySelector('.voices__track');
    var list = track && track.querySelector('.voices__list');
    if (!list) return;
    var toggle = document.querySelector('.voices__toggle');
    var hint = document.querySelector('.voices__hint');

    var clone = list.cloneNode(true);
    clone.classList.add('is-clone');
    clone.setAttribute('aria-hidden', 'true');
    clone.inert = true;
    track.appendChild(clone);
    band.classList.add('is-marquee');
    if (toggle) toggle.hidden = false;
    if (hint) hint.hidden = false;

    var BASE = 38;          // px per second at rest
    var loopW = 0, x = 0, dir = -1, speed = 1;
    var held = false, paused = false, visible = false;
    var lastY = scrollPos();

    function measure() {
      loopW = clone.offsetLeft - list.offsetLeft;
      if (loopW > 0) x = x % loopW;
    }

    gsap.ticker.add(function (time, dtMs) {
      var y = scrollPos();
      var dy = y - lastY;
      lastY = y;
      if (!visible || !loopW) return;
      var dt = Math.min(dtMs || 16, 64) / 1000;
      var v = dy / (dt * 60);                         // px per 60fps frame
      if (Math.abs(v) > 0.6) dir = v > 0 ? -1 : 1;
      var want = (held || paused) ? 0 : 1 + Math.min(Math.abs(v) * 0.45, 9);
      speed += (want - speed) * Math.min(1, dt * (want > speed ? 6 : 2.5));
      x += dir * BASE * speed * dt;
      x = x % loopW;
      if (x > 0) x -= loopW;
      // Only while the scroll is pushing it: the row leans into its own
      // direction of travel, then straightens as it settles to the drift.
      var skew = -dir * Math.min(Math.max(speed - 1, 0) * 0.8, 6);
      track.style.transform = 'translate3d(' + x.toFixed(2) + 'px,0,0) skewX(' + skew.toFixed(2) + 'deg)';
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[entries.length - 1].isIntersecting;
      }, { rootMargin: '120px 0px' }).observe(band);
    } else visible = true;

    if (finePointer) {
      band.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') held = true; });
      band.addEventListener('pointerleave', function () { held = false; });
    }

    if (toggle) {
      var pauseLbl = toggle.querySelector('.voices__toggle-pause');
      var playLbl = toggle.querySelector('.voices__toggle-play');
      toggle.addEventListener('click', function () {
        paused = !paused;
        toggle.setAttribute('aria-pressed', paused ? 'true' : 'false');
        pauseLbl.hidden = paused;
        playLbl.hidden = !paused;
      });
    }

    measure();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    window.addEventListener('resize', measure, { passive: true });
    document.addEventListener('vitnyr:langchange', function () { requestAnimationFrame(measure); });
  }

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

  /* ---------- masthead mark: draw-in ----------
     The V/Y assembles from its three strokes once, a beat after load, then
     holds; no hover replay. Past the reduced-motion return (the stylesheet
     pins it open there). .is-drawing is all the CSS needs and is never
     removed. */
  var LOCKMARK_INTRO = 150;
  function initLockmark() {
    var lockup = document.querySelector('.lockup');
    if (!lockup) return;
    // A short beat, not frame 0, so it reads as deliberate. failsafe() is the
    // backstop if this never fires.
    setTimeout(function () { lockup.classList.add('is-drawing'); }, LOCKMARK_INTRO);
  }

  /* ---------- specimen permalinks ----------
     Each specimen has a stable id and its label links to it, so a reader can
     share the one mistake that is theirs. A click also copies the URL and
     says so briefly. With this file absent the label is still a plain anchor.
     Navigation, not motion: reduced motion only makes the scroll instant. */
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
        /* pushState keeps Back working and doesn't fire hashchange, so the collage
           router stays out of it. */
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

    /* A cold load of a specimen permalink lands on the specimen and moves focus
       into it; scroll alone is not navigation. Measured from offsetTop, since
       the .reveal's box still carries part of its rise. The jump runs twice
       because the masthead is shorter at rest than once scrolled, and it waits
       for load, after the browser's own jump to the fragment. */
    var landed = document.getElementById((location.hash || '').slice(1));
    if (landed && landed.classList.contains('spec') && !document.querySelector('.origin__mark')) {
      if (!landed.hasAttribute('tabindex')) landed.setAttribute('tabindex', '-1');
      landed.focus({ preventScroll: true });
      var land = function () {
        if (!lenis) return;   // reduced motion / no Lenis: the native jump and scroll-margin-top already land it
        navLock = true;       // a downward jump: keep the phone masthead from sliding away
        showMast();
        for (var pass = 0; pass < 2; pass++) {
          var y = 0;
          for (var n = landed; n; n = n.offsetParent) y += n.offsetTop;
          lenis.scrollTo(y - headerHeight(), { immediate: true, force: true });
        }
        requestAnimationFrame(releaseNav);
      };
      if (document.readyState === 'complete') land();
      else window.addEventListener('load', function () { requestAnimationFrame(land); });
    }
  }

  /* ---------- collage: a hash-routed full-screen view ----------
     #collage behaves like its own page. location.hash is the single source of
     truth, so Back and Forward work: Back drops the hash, hashchange fires,
     the view closes. Opening makes #app and the masthead inert, moves focus to
     the heading and parks the Lenis scroll. With this file absent the view is
     the last section of the document. */
  function initCollageView() {
    var view = document.getElementById('collage');
    if (!view) return;
    var title = document.getElementById('collage-title');
    var backBtn = view.querySelector('.view__back');
    var homeLink = view.querySelector('.footmark-home');
    // The door (the "See me at work" band) is the one opener that morphs into
    // the view. The "Photos" links carry data-collage-link and open with the
    // plain crossfade, wired below.
    var opener = document.querySelector('[data-collage-open]');
    // The view's own "Photographs" label, the first .label in the view, is the
    // door's morph target.
    var doorLabel = view.querySelector('.label');
    var canInert = 'inert' in HTMLElement.prototype;
    // everything that is not the view, made inert while it is open
    var behind = [
      document.getElementById('app'),
      document.querySelector('.masthead'),
      document.querySelector('.skip')
    ].filter(Boolean);
    function setBehindInert(on) { if (canInert) behind.forEach(function (el) { el.inert = on; }); }
    var returnFocus = null;
    var savedScroll = 0;   // where the site was when the view opened
    var applied = false;   // have the open side-effects run? The <head> script can set .collage-open on
                           // a deep link, so the class alone isn't the test.

    function bgScroll() { return lenis ? lenis.scroll : (window.scrollY || 0); }
    function bgScrollTo(y) {
      if (lenis) lenis.scrollTo(y, { immediate: true });
      else window.scrollTo(0, y);
    }

    // A warm open's click also puts #collage in the URL, and the browser's
    // scroll-to-fragment for it still runs on a later task. The open runs inside
    // a View Transition, so the scroll and focus snapshot is taken here,
    // synchronously, before withTransition() defers the rest.
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
      promoteCollageImages(view);   // first open: let the figures fetch
      armCollageReveals(view);   // first open: hand the tiles to their own observer
      initCollageLightbox(view);   // first open: wrap the tiles in real controls
      // Synchronous: rAF can be suspended in a background tab, and a deferred
      // focus move might never happen.
      if (title) title.focus({ preventScroll: true });
      /* On a deep link the browser's own scroll-to-fragment runs after this and
         focuses #collage (an overflow: auto container is focusable), undoing the
         line above. Re-assert the heading once the document settles, and reset
         the saved scroll so the way back returns to the top. */
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
      // Reopening lands on a settled view: every tile back to .is-in. Any the
      // observer hasn't fired stay observed.
      view.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
    }

    function sync(cold) { (location.hash === '#collage') ? applyOpen(cold) : applyClose(); }

    /* Both directions animate with a View Transition. applyOpen()'s class flip
       and focus move stay adjacent and synchronous inside whichever call runs
       them; withTransition()'s failsafe covers the callback never running. */
    function canTransition() {
      return typeof document.startViewTransition === 'function' && !reduce
        && document.visibilityState === 'visible';
    }
    // Shared by every route that transitions. `mutate` is one of sync()'s two
    // idempotent halves, so racing a direct call after a short failsafe costs
    // nothing if the update callback is merely slow.
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
      // Only a real open/closed flip takes the transition; otherwise every
      // unrelated in-page hash would fire an invisible crossfade.
      var opening = !applied && location.hash === '#collage';
      var closing = applied && location.hash !== '#collage';
      if (opening) captureOpenState(false);   // before the transition's own delay, see applyOpen
      if (opening || closing) withTransition(function () { sync(false); });
      else sync(false);
    }

    /* The door: "See me at work" morphs into the view's "Photographs" label, so
       the way in reads as one element moving. Both ends carry the same
       view-transition-name for one transition only (the source before the call,
       the destination inside the callback), cleared once it settles. */
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
    document.querySelectorAll('[data-collage-link]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        if (location.hash === '#collage') return;
        if (history.pushState) history.pushState(null, '', '#collage');
        else location.hash = 'collage';
        routeAfterHashChange();
      });
    });

    /* Jumps into a domain group of the view: open it if it's closed, slide that
       group's label to the top and focus its heading. Native smooth scroll on
       the view's own container (Lenis is parked), instant under reduced motion.
       Synchronous, not in a rAF, for the same reason as applyOpen's focus. */
    var jumpers = document.querySelectorAll('[data-collage-jump]');
    var bar = view.querySelector('.view__bar');
    var JUMP_GAP = 16;   // breathing room left between the sticky bar and the landed label
    function jumpToGroup(key) {
      var heading = document.getElementById('collage-' + key);
      if (!heading) return;
      var group = heading.closest('.view__group');
      /* Land the group's label under the sticky bar: it carries the glyph that
         was clicked. */
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
        // Focus the button first so applyOpen records it for Back; Safari doesn't
        // focus a <button> on a mouse click.
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
    // The mark always goes to the top of the main page, like the masthead's
    // .lockup. A plain #top link would fall into the generic #-anchor handler
    // and never close the view, so: pushState #top (no hashchange), force the
    // close to land at the very top, and run the usual transition path.
    if (homeLink) homeLink.addEventListener('click', function (e) {
      e.preventDefault();
      if (history.pushState) history.pushState(null, '', '#top');
      else location.hash = 'top';
      savedScroll = 0;
      returnFocus = null;
      withTransition(applyClose);
    });
    window.addEventListener('hashchange', function () { routeAfterHashChange(); });
    document.addEventListener('keydown', function (e) {
      // The lightbox sits on top with its own Escape handler; this one waits, so
      // Escape closes one layer at a time.
      if ((e.key === 'Escape' || e.key === 'Esc') && applied && !lightboxOpen) {
        e.preventDefault(); leave();
      }
    });

    sync(true);   // deep-link path; the <head> script already set .collage-open
  }

  /* ---------- who: the rows answer the question ----------
     Each row gets an invisible overlay <button> (built here, so a no-JS
     reader sees plain rows and a static CTA). Picking is single-choice and
     toggleable; it adds a first-person clause from the row's data-prefill-*
     to the Telegram message. Interaction, not decoration: wired before the
     reduced-motion return. */
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
    // The one place the offer's Telegram links are written: the CTA, the phone
    // contact bar (.dock), the footer's "Your move" line and the draft preview.
    // No pick: theme.js's per-language default. A pick: the base message, " — ",
    // and the row's clause in the current language.
    var targets = document.querySelectorAll('.contact__cta, .dock, .foot__move, .page-cta');
    var draft = document.querySelector('.contact__draft');
    function updateCta() {
      var l = lang();
      var href = cta.getAttribute('data-href-' + l);
      var message = null;
      if (selected !== null) {
        var clause = rows[selected].getAttribute('data-prefill-' + l) || '';
        message = decodedBase(l) + ' — ' + clause;
        href = BASE + encodeURIComponent(message);
      }
      targets.forEach(function (a) { a.setAttribute('href', href); });
      if (!draft) return;
      if (message === null) {
        draft.classList.remove('is-in');
        draft.hidden = true;
        draft.textContent = '';
        return;
      }
      draft.textContent = l === 'ru' ? '«' + message + '»' : '“' + message + '”';
      if (draft.hidden) {
        draft.hidden = false;
        requestAnimationFrame(function () { draft.classList.add('is-in'); });
      }
    }

    // The pick status under the rows: silent at rest; confirms a pick and points
    // at the contact section. aria-live, so the confirmation is announced.
    var list = document.querySelector('.rows');
    var status = document.createElement('p');
    status.className = 'rows__status';
    status.setAttribute('aria-live', 'polite');
    list.parentNode.insertBefore(status, list.nextSibling);
    function setStatus(picked) {
      status.textContent = '';
      var l = lang();
      if (picked) {
        var a = document.createElement('a');
        a.href = '#contact';
        var t = document.createElement('span');
        t.setAttribute('data-en', 'Added to your message');
        t.setAttribute('data-ru', 'Добавлено в ваше сообщение');
        t.textContent = t.dataset[l];
        a.appendChild(t);
        a.insertAdjacentHTML('beforeend', '<svg viewBox="0 0 12 24" aria-hidden="true"><path d="M6 0 V22 M1 17 L6 22 L11 17" fill="none" stroke="currentColor" stroke-width="1.25"/></svg>');
        a.addEventListener('click', function (e) {
          var dest = document.getElementById('contact');
          if (!dest) return;
          e.preventDefault();
          jumpTo(dest);
        });
        status.appendChild(a);
        requestAnimationFrame(function () { a.classList.add('is-in'); });
      } else {
        var v = document.createElement('span');
        v.className = 'vh';
        v.setAttribute('data-en', 'Removed from your message');
        v.setAttribute('data-ru', 'Убрано из сообщения');
        v.textContent = v.dataset[l];
        status.appendChild(v);
      }
    }

    var picks = [];
    rows.forEach(function (li, i) {
      var h3 = li.querySelector('h3');
      if (!h3) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'row__pick';
      btn.setAttribute('aria-pressed', 'false');
      /* Named by a visually hidden span carrying the heading's own data-en/data-ru,
         so applyLang() keeps it in the right language. applyLang has already run,
         so the first text is set here. */
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
        setStatus(selected !== null);
      });
      li.appendChild(btn);
      picks.push(btn);
    });

    // A language switch resets the default href and fires this; the one writer
    // recomposes a live pick in the new language.
    document.addEventListener('vitnyr:langchange', updateCta);
  }

  /* ---------- phone contact bar ----------
     Shows .dock once the hero has scrolled away and hides it while #contact
     or the footer is on screen, so it never doubles the real CTA. Visibility,
     not motion: wired before the reduced-motion return. */
  function initDock() {
    var dock = document.querySelector('.dock');
    var hero = document.getElementById('hero');
    var contact = document.getElementById('contact');
    // The footer is pinned under <main> (the curtain), so it's geometrically
    // on screen the whole time; its flow edge is what says it's uncovered.
    var foot = document.querySelector('.foot-edge');
    if (!dock || !hero || !contact || !('IntersectionObserver' in window)) return;
    var state = { heroAbove: false, contact: false, foot: false };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.target === hero) state.heroAbove = !en.isIntersecting && en.boundingClientRect.top < 0;
        else if (en.target === contact) state.contact = en.isIntersecting;
        else state.foot = en.isIntersecting || en.boundingClientRect.top < 0;
      });
      var on = state.heroAbove && !state.contact && !state.foot;
      dock.classList.toggle('is-on', on);
    }, { rootMargin: '0px 0px -56px 0px' });
    io.observe(hero); io.observe(contact); if (foot) io.observe(foot);
  }

  /* ---------- footer: Yerevan clock and keyboard reach ----------
     "Yerevan · 14:32 local time", so a reader abroad can tell whether a
     message lands at a sensible hour; re-arms on each minute boundary. The
     footer is pinned under <main>, so a Tab into it from above would focus a
     link the reader can't see: on focus, go to the bottom first. */
  function initFoot() {
    var foot = document.querySelector('.foot');
    if (!foot) return;
    var clock = foot.querySelector('.foot__clock');
    var time = foot.querySelector('.foot__time');
    if (clock && time && window.Intl) {
      try {
        var fmt = new Intl.DateTimeFormat('en-GB', {
          timeZone: 'Asia/Yerevan', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
        });
        var tick = function () {
          var hm = fmt.format(new Date());
          time.textContent = hm;
          time.setAttribute('datetime', hm);
          clock.hidden = false;
          setTimeout(tick, 60000 - (Date.now() % 60000) + 50);
        };
        tick();
      } catch (err) { /* no Asia/Yerevan zone data: the line just reads "Yerevan" */ }
    }
    initFootClock(foot);
    foot.addEventListener('focusin', function () {
      if (getComputedStyle(foot).position !== 'sticky') return;
      var end = document.documentElement.scrollHeight - window.innerHeight;
      if (window.scrollY >= end - 2) return;
      if (lenis) lenis.scrollTo(end, { immediate: true });
      else window.scrollTo(0, end);
    });
  }

  /* The engraved chess clock: the reader's dial (the raised button) keeps
     Yerevan time; Igor's dial is stopped, its hands baked into the SVG. The
     hands are SVG transform attributes, not CSS transforms, so nothing here
     touches a reveal. Under reduced motion the second hand is hidden and the
     dial moves once a minute. */
  function initFootClock(foot) {
    var hands = foot.querySelectorAll('.vig__hand[data-side="you"]');
    if (!hands.length || !window.Intl) return;
    var fmt;
    try {
      fmt = new Intl.DateTimeFormat('en-GB', {
        timeZone: 'Asia/Yerevan', hour: 'numeric', minute: 'numeric', second: 'numeric', hourCycle: 'h23'
      });
    } catch (err) { return; }
    var tick = function () {
      var t = {};
      fmt.formatToParts(new Date()).forEach(function (p) { t[p.type] = +p.value; });
      var deg = {
        h: (t.hour % 12 + t.minute / 60) * 30,
        m: (t.minute + t.second / 60) * 6,
        s: t.second * 6
      };
      Array.prototype.forEach.call(hands, function (g) {
        g.setAttribute('transform', 'rotate(' + deg[g.getAttribute('data-hand')].toFixed(1) + ' ' + g.getAttribute('data-c') + ')');
      });
      var step = reduce ? 60000 : 1000;
      setTimeout(tick, step - (Date.now() % step) + 20);
    };
    tick();
  }

  /* ---------- "Test your ear" (English page) ----------
     The reader toggles the sentences that sound right, then checks. Each row
     shows its verdict and, for the wrong ones, the natural form; the score and
     the habits behind the misses read out in a polite live region, and "Send
     me your score" carries the score into a prefilled Telegram message.
     Nothing is stored. Re-renders on a language switch. Wired before the
     reduced-motion return. */
  function initEarTest() {
    var root = document.querySelector('.ear');
    if (!root) return;
    var items = [].slice.call(root.querySelectorAll('.ear__item'));
    var check = root.querySelector('.ear__check');
    var again = root.querySelector('.ear__again');
    var result = root.querySelector('.ear__result');
    var scoreEl = root.querySelector('.ear__score');
    var habitEl = root.querySelector('.ear__habit');
    var send = root.querySelector('.ear__send');
    if (!items.length || !check || !again || !result || !scoreEl || !habitEl || !send) return;
    var baseHref = send.getAttribute('href');
    var checked = false;
    var T = {
      en: {
        score: function (n, t) { return 'You judged ' + n + ' of ' + t + ' correctly.'; },
        missed: 'missed: this one isn’t natural',
        natural: 'missed: this one is natural',
        habits: function (l) { return 'What tripped you: ' + l + '.'; },
        strict: 'No wrong sentence got past you; you were stricter than English is.',
        clean: 'A clean ear. Saying it under pressure is the next skill, and that’s where a lesson starts.',
        msg: function (n, t) { return 'Hi! I took the ear test on your site: ' + n + '/' + t + '. I’d like a free trial English lesson.'; }
      },
      ru: {
        score: function (n, t) { return 'Вы верно оценили ' + n + ' из ' + t + '.'; },
        missed: 'мимо: так не говорят',
        natural: 'мимо: так говорят',
        habits: function (l) { return 'Где вы споткнулись: ' + l + '.'; },
        strict: 'Ни одна ошибка не прошла мимо; вы оказались строже самого английского.',
        clean: 'Чистый слух. Следующий навык — сказать так же под давлением, с этого и начинается занятие.',
        msg: function (n, t) { return 'Здравствуйте! Мой результат в тесте на слух на вашем сайте: ' + n + '/' + t + '. Хочу записаться на бесплатное пробное занятие по английскому.'; }
      }
    };
    function lang() { return document.documentElement.getAttribute('data-lang') === 'ru' ? 'ru' : 'en'; }
    function pick(li) { return li.querySelector('.ear__pick'); }

    items.forEach(function (li) {
      var b = pick(li);
      b.addEventListener('click', function () {
        if (checked) return;
        b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      });
    });

    function render() {
      if (!checked) return;
      var l = lang(), t = T[l], hits = 0, habits = [], strict = false;
      items.forEach(function (li) {
        var right = li.getAttribute('data-right') === 'true';
        var ok = (pick(li).getAttribute('aria-pressed') === 'true') === right;
        var v = li.querySelector('.ear__verdict');
        var fix = li.querySelector('.ear__fix');
        if (fix) fix.hidden = false;
        li.classList.toggle('is-miss', !ok);
        if (ok) { hits++; v.hidden = true; v.textContent = ''; return; }
        v.hidden = false;
        v.textContent = right ? t.natural : t.missed;
        if (right) strict = true;
        else habits.push(li.getAttribute('data-habit-' + l));
      });
      scoreEl.textContent = t.score(hits, items.length);
      habitEl.textContent = habits.length ? t.habits(habits.join(', ')) : (strict ? t.strict : t.clean);
      send.setAttribute('href', 'https://t.me/yngvil?text=' + encodeURIComponent(t.msg(hits, items.length)));
    }

    check.addEventListener('click', function () {
      checked = true;
      root.classList.add('is-checked');
      items.forEach(function (li) { pick(li).disabled = true; });
      check.hidden = true;
      again.hidden = false;
      result.hidden = false;
      render();
      scoreEl.setAttribute('tabindex', '-1');
      scoreEl.focus({ preventScroll: true });   // the button that had focus just left the page
    });
    again.addEventListener('click', function () {
      checked = false;
      root.classList.remove('is-checked');
      items.forEach(function (li) {
        var b = pick(li);
        b.disabled = false;
        b.setAttribute('aria-pressed', 'false');
        li.classList.remove('is-miss');
        li.querySelector('.ear__verdict').hidden = true;
        var fix = li.querySelector('.ear__fix');
        if (fix) fix.hidden = true;
      });
      result.hidden = true;
      again.hidden = true;
      check.hidden = false;
      send.setAttribute('href', baseHref);
      pick(items[0]).focus();
    });
    document.addEventListener('vitnyr:langchange', render);
  }

  /* ---------- method fold ----------
     Independent disclosures, not an exclusive accordion. aria-expanded is set
     here, not in the HTML, so a no-JS reader never sees a closed panel with
     no way to open it. The panel's open/close is CSS, reading the same
     aria-expanded via :has(). */
  function initMechanismFold() {
    var toggles = document.querySelectorAll('.mech__toggle');
    if (!toggles.length) return;
    // The first principle ships open, so a reader who never clicks still gets
    // one and sees what the fold does.
    toggles.forEach(function (btn, i) {
      var startOpen = i === 0;
      btn.setAttribute('aria-expanded', startOpen ? 'true' : 'false');
      var mark = btn.querySelector('.mech__toggle-mark');
      if (mark && startOpen) mark.textContent = '−';
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
    // The hero has no .reveal class, so the sweep can't reach it; armHeroGuard()
    // covers it.
    if (!heroStarted) showHeroNow();
    // The masthead mark isn't a .reveal either. If initLockmark() never armed
    // the draw, its clip rects are still collapsed under html.js: show it
    // outright. A mark that drew normally is left alone.
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
  initVoices();

  whenRendering(function () {
    /* Hold the hero until the display face is real, so the lines don't rise in
       a fallback and reflow, but never longer than 1.5s. */
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
