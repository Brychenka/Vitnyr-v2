/* ============================================================
   Vitnyr — v2 motion
   One easing curve everywhere: cubic-bezier(.16, 1, .3, 1).
   One reveal rhythm: fade + 24px rise, 0.9s, 0.08s stagger, once.
   One signature move: custom cursor + magnetic targets.
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

  /* Four durations, and nothing between them. Every timing on the page comes
     from this table so the whole thing reads as one instrument.
       micro  — a thing appearing or disappearing outright
       state  — a hover, a magnet, a theme settling (this is --t in the sheet)
       follow — the pointer catching up: a lag, not a duration
       hero   — the single longest move on the page, used once
     The reveal's own 0.9s lives in the stylesheet, where the transition is. */
  var D = { micro: 0.3, state: 0.6, follow: 0.45, hero: 1.05 };
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
     reader reaches #origin, flips .past-origin so the rule's ink crossfades
     from specimen to target (the CSS owns the crossfade; this only picks the
     side). #origin's page offset is measured once and re-measured on resize
     and language switch, not read on every scroll frame. */
  var progressEl = document.querySelector('.progress');
  var originEl = document.getElementById('origin');
  var originY = 0;
  function scrollPos() { return lenis ? lenis.scroll : (window.scrollY || 0); }
  function measureOrigin() {
    if (originEl) originY = originEl.getBoundingClientRect().top + scrollPos();
  }
  function trackProgress(y) {
    if (!progressEl) return;
    var max = root.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
    progressEl.style.setProperty('--progress', p.toFixed(4));
    if (originEl) root.classList.toggle('past-origin', y + window.innerHeight * 0.5 >= originY);
  }
  function onScroll(y) { setStuck(y); trackProgress(y); }

  if (lenis) lenis.on('scroll', function (e) { onScroll(e.scroll); });
  else window.addEventListener('scroll', function () { onScroll(window.scrollY); }, { passive: true });
  measureOrigin();
  onScroll(scrollPos());
  window.addEventListener('resize', function () { measureOrigin(); onScroll(scrollPos()); }, { passive: true });
  document.addEventListener('vitnyr:langchange', function () {
    requestAnimationFrame(function () { measureOrigin(); onScroll(scrollPos()); });
  });

  // In-page links go through Lenis so the easing stays consistent.
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    if (a.hasAttribute('data-collage-open')) return;   // the collage router owns this one
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(target, { offset: 0, duration: 1.2 });
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
      onComplete: function () { root.classList.add('hero-done'); }
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
    items.forEach(function (el) { (el.closest('.hero') ? hero : rest).push(el); });

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

  /* The measured numbers do not animate. They are four readings off four
     different instruments (years, clients, an Elo scale, a climbing grade) and
     a shared count-up rhythm made them read as one — Spark Order move 17. They
     arrive on the ordinary .reveal rhythm with the rest of the row and sit at
     their value; nothing on the page runs a number up. */

  /* ---------- origin: interactive mark ----------
     Hover, focus, or tap one of the three real <button> hit-regions to light
     up its stroke and reveal its discipline in the panel. One setActive()
     drives every input mode so a hybrid device (touch + mouse) never gets
     two handlers fighting over the same element: focus covers keyboard tab
     and touch tap (tapping a button focuses it natively); pointerenter is
     layered on top only for fine-pointer devices, so coarse pointers never
     get a stuck-hover state.
     aria-hidden on the panel items is set here, at runtime, rather than
     baked into the HTML — that's what keeps the no-JS fallback (CLAUDE.md:
     everything animation-related is additive) genuinely additive: a no-JS
     reader never gets these attributes at all, so all three stay visible to
     assistive tech exactly as they do visually.
     The idle hint below borrows these same is-active/is-dim classes rather
     than defining its own visual language — a real engagement and the hint
     produce identical-looking states, just triggered differently. */
  function initOrigin() {
    var mark = document.querySelector('.origin__mark');
    if (!mark) return;
    var hits = mark.querySelectorAll('.origin__hit');
    var parts = mark.querySelectorAll('.glyph__part');
    var panelItems = document.querySelectorAll('.origin__panel-item');
    if (!hits.length) return;

    panelItems.forEach(function (el) { el.setAttribute('aria-hidden', 'true'); });

    var idleTl = null;
    // True the instant a real engagement happens, permanently. Checked by
    // every idle-timeline step, rather than trusting .kill() alone to be
    // synchronous: a step already queued on GSAP's ticker for the current
    // frame can still fire after .kill() is called mid-frame, which without
    // this guard could paint a stale idle discipline right over a real one
    // landing in the same frame (e.g. a hover arriving as the hint starts).
    var engaged = false;

    // The visual half of activation — glyph active/dim plus which panel
    // item is opaque — shared by real engagement and the idle hint below, so
    // the two can never drift into two different-looking "active" states.
    // aria-hidden/aria-pressed are deliberately not touched here: the idle
    // hint is a decorative preview, not a real selection, so it stays silent
    // to assistive tech rather than announcing three unrequested changes.
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
    // C6 (2026-09-06): rest state is English lit, not neutral — English is
    // the offer, chess and climbing are proof it transfers, not equal-weight
    // alternatives. This used to strip every class instead, so the mark sat
    // fully neutral (all three strokes equal weight, panel blank) until the
    // idle hint below happened to run, or forever under reduced motion,
    // where the hint never runs at all. Now it just re-asserts the default.
    function clearPaint() {
      paint('english');
    }

    function setActive(name) {
      engaged = true;
      if (idleTl) { idleTl.kill(); idleTl = null; }
      paint(name);
      panelItems.forEach(function (el) {
        el.setAttribute('aria-hidden', el.dataset.discipline === name ? 'false' : 'true');
      });
      hits.forEach(function (el) {
        el.setAttribute('aria-pressed', el.dataset.discipline === name ? 'true' : 'false');
      });
    }

    // Establishes the resting default from the first frame — covers reduced
    // motion (the idle hint below never runs there) and the gap before the
    // hint's own IntersectionObserver fires. paint()/clearPaint() carry no
    // aria side effects (see the comment above paint()), so this is silent
    // to assistive tech exactly like the hint is.
    clearPaint();

    hits.forEach(function (btn) {
      var name = btn.dataset.discipline;
      btn.addEventListener('focus', function () { setActive(name); });
      if (finePointer) btn.addEventListener('pointerenter', function () { setActive(name); });
    });

    // One-shot hint, not a loop: previews all three discipline/stat pairs a
    // couple of times when the section first scrolls into view, then settles
    // back to the neutral resting state on its own. It has to preview the
    // panel too, not just the glyph — a shimmer with no text next to it
    // teaches nothing about what hovering actually does. Skipped outright
    // under reduced motion; the real interaction above still works either
    // way, and paint()/clearPaint() carry no aria side effects, so this
    // stays silent to assistive tech.
    if (reduce || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        if (engaged) return;
        var order = ['english', 'chess', 'climbing'];
        var tl = gsap.timeline({
          repeat: 1,
          onComplete: function () { if (!engaged) clearPaint(); idleTl = null; }
        });
        order.forEach(function (name) {
          tl.call(function () { if (!engaged) paint(name); }).to({}, { duration: 1 });
        });
        idleTl = tl;
      });
    }, { threshold: 0.4 });
    io.observe(mark);
  }

  /* ---------- signature move: cursor + magnetic ---------- */
  function initCursor() {
    if (!finePointer) return;
    var el = document.querySelector('.cursor');
    if (!el) return;

    var setX = gsap.quickSetter(el, 'x', 'px');
    var setY = gsap.quickSetter(el, 'y', 'px');
    var sc = gsap.quickTo(el, 'scale', { duration: D.follow, ease: EASE });
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
        // has-cursor only hides the native pointer over hot targets now
        // (C13 — see the CSS), so this no longer has to race a replacement
        // onto the screen; it just arms the class the hot-target rules and
        // cursor-active's opacity toggle are both keyed off.
        shown = true;
        cx = mx; cy = my;
        gsap.set(el, { x: mx, y: my });
        root.classList.add('has-cursor');
      }
      kick();
    }, { passive: true });

    // The dot's own visibility is CSS now (html.has-cursor.cursor-active
    // .cursor { opacity: 1 }) rather than a tween kicked off here — it
    // only ever needs to be on while the pointer is over one of these, so
    // there is no separate "hide it when the mouse leaves the window" case
    // to handle either: leaving a hot target through the viewport edge
    // fires this same mouseout first.
    var HOT = 'a, button, [data-magnetic]';
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest && e.target.closest(HOT)) { root.classList.add('cursor-active'); sc(3); }
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest && e.target.closest(HOT)) { root.classList.remove('cursor-active'); sc(1); }
    });
  }

  function initMagnetic() {
    if (!finePointer) return;
    var RADIUS = 60, PULL = 12;
    document.querySelectorAll('[data-magnetic]').forEach(function (el) {
      var qx = gsap.quickTo(el, 'x', { duration: D.state, ease: EASE });
      var qy = gsap.quickTo(el, 'y', { duration: D.state, ease: EASE });
      var box = null;

      /* Measured once on enter, with the element's own translate subtracted,
         so the reading can't feed the displacement back into itself — and no
         layout is forced on every mousemove. */
      function capture() {
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
        /* Normalised per axis against the element's own half-size, so a full
           width link answers the pointer the same way a 40px button does
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

    function applyOpen(cold) {
      if (applied) return;
      applied = true;
      returnFocus = (document.activeElement && document.activeElement !== document.body)
        ? document.activeElement : opener;
      // A deep link makes the browser scroll the document toward the #collage
      // element (last in the DOM); a cold open therefore returns to the top,
      // a warm one returns exactly where the reader was.
      savedScroll = cold ? 0 : bgScroll();
      root.classList.add('collage-open');        // CSS flips the view visible synchronously
      setBehindInert(true);
      if (lenis) lenis.stop();
      view.scrollTop = 0;
      promoteCollageImages(view);   // first open: let the 18 figures actually fetch
      armCollageReveals(view);   // first open: hand the tiles to their own observer
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

    function leave() {
      // Real history keeps forward working; only synthesise a state if we'd
      // otherwise walk off the site (deep link opened in a fresh tab).
      if (window.history.length > 1) window.history.back();
      else { history.replaceState(null, '', location.pathname + location.search); sync(false); }
    }

    if (opener) opener.addEventListener('click', function (e) {
      e.preventDefault();
      if (history.pushState) history.pushState(null, '', '#collage');
      else location.hash = 'collage';
      sync(false);
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
    window.addEventListener('hashchange', function () { sync(false); });
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.key === 'Esc') && applied) { e.preventDefault(); leave(); }
    });

    sync(true);   // deep-link path; the <head> script already set .collage-open
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
  }
  // Re-armed rather than one-shot: a language switch brings a different set of
  // elements on screen, all of them after this sweep would have come and gone.
  function armFailsafe() { clearTimeout(sweepTimer); sweepTimer = setTimeout(failsafe, 2500); }

  /* ---------- go ---------- */
  buildReveals();
  initOrigin();
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
