/* Runs from <head>, render-blocking on purpose: the theme and language are
   stamped on <html> before first paint, so there is no flash of the wrong pair.
   Everything here degrades safely if localStorage throws (private mode). */
(function () {
  var LANG_KEY = 'vitnyr-lang', THEME_KEY = 'vitnyr-theme';

  /* Marks the document as script-driven. The reveal animations hide their
     elements only under this class, so if the scripts never arrive the page
     still renders complete. main.js removes it if GSAP failed to load. */
  document.documentElement.classList.add('js');

  function stored(key, a, b) {
    var v = null;
    try { v = localStorage.getItem(key); } catch (e) {}
    return (v === a || v === b) ? v : null;
  }
  function save(key, v) { try { localStorage.setItem(key, v); } catch (e) {} }

  var prefersLight = window.matchMedia && matchMedia('(prefers-color-scheme: light)');

  function effectiveTheme() {
    return stored(THEME_KEY, 'light', 'dark')
        || (prefersLight && prefersLight.matches ? 'light' : 'dark');
  }
  function applyTheme() {
    var chosen = stored(THEME_KEY, 'light', 'dark');
    if (chosen) document.documentElement.setAttribute('data-theme', chosen);
    else document.documentElement.removeAttribute('data-theme');
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', effectiveTheme() === 'light' ? '#EFEBE3' : '#14181A');
    labelTheme();
  }
  function labelTheme() {
    /* More than one .themeswitch: the masthead's, plus the one in the collage
       view's bar (which sits above the masthead when that view is open). */
    var btns = document.querySelectorAll('.themeswitch');
    if (!btns.length) return;
    var next = effectiveTheme() === 'dark' ? 'light' : 'dark';
    var lang = document.documentElement.getAttribute('data-lang') || 'en';
    var words = { en: { light: 'Cream', dark: 'Charcoal' },
                  ru: { light: 'Крем',  dark: 'Уголь' } };
    for (var i = 0; i < btns.length; i++) {
      btns[i].textContent = words[lang][next];
      btns[i].setAttribute('aria-label',
        lang === 'ru' ? 'Переключить оформление' : 'Switch to the ' + next + ' theme');
    }
  }

  var lang = new URLSearchParams(location.search).get('lang');
  if (lang !== 'ru' && lang !== 'en') {
    lang = stored(LANG_KEY, 'ru', 'en')
        || ((navigator.language || '').toLowerCase().indexOf('ru') === 0 ? 'ru' : 'en');
  }
  function applyLang(l) {
    var d = document.documentElement;
    d.setAttribute('data-lang', l);
    d.setAttribute('lang', l);
    var nodes = document.querySelectorAll('[data-en][data-ru]');
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = nodes[i].dataset[l];
    /* P8 (Stage 6, 2026-09-06): same generic-attribute-copy idea as the loop
       above, for a link whose destination text differs per language (the
       Telegram deep link pre-fills a message, so it reads as the right
       language before the reader even sends it) rather than its label. */
    var hrefNodes = document.querySelectorAll('[data-href-en][data-href-ru]');
    for (var h = 0; h < hrefNodes.length; h++) {
      hrefNodes[h].setAttribute('href', hrefNodes[h].dataset['href' + (l === 'ru' ? 'Ru' : 'En')]);
    }
    /* More than one .langswitch: the masthead's, plus the one in the collage
       view's bar (which sits above the masthead when that view is open) —
       same reason labelTheme() below loops over every .themeswitch. */
    var sws = document.querySelectorAll('.langswitch');
    for (var j = 0; j < sws.length; j++) {
      sws[j].textContent = (l === 'ru') ? 'EN' : 'RU';
      sws[j].setAttribute('aria-label', (l === 'ru') ? 'Switch to English' : 'Переключить на русский');
    }
    labelTheme();
    // the hero lines differ per language, so their masks need re-measuring
    document.dispatchEvent(new CustomEvent('vitnyr:langchange', { detail: l }));
  }

  /* P2 (Stage 6, 2026-09-06): language lived only in localStorage — the URL
     a Russian reader copies and sends opens in English for everyone else,
     since ?lang= was read on load but never written back. Called only from
     the switch handler below, not from the initial applyLang() call, so a
     plain visit never rewrites the address bar on its own; a link someone
     actually shares after switching does. Wrapped like every other
     history/URL call here: the live artifact runs this page inside a
     cross-origin iframe, where replaceState can throw. Also what gives
     hreflang (index.html) something real to point at. */
  function syncLangUrl(l) {
    try {
      var url = new URL(location.href);
      url.searchParams.set('lang', l);
      history.replaceState(null, '', url.pathname + url.search + url.hash);
    } catch (e) {}
  }

  document.documentElement.setAttribute('data-lang', lang);
  applyTheme();

  /* The wordmark is live SVG text positioned at Lora's own advances, so it must
     never paint in a fallback face. Reveal it only once Lora has actually
     loaded; until then the mark shows alone, which is a sanctioned lockup. */
  if (document.fonts && document.fonts.load) {
    document.fonts.load('600 100px Lora', 'VITNYR')
      .then(function () { document.documentElement.classList.add('lora-ready'); })
      .catch(function () {});
  } else {
    document.documentElement.classList.add('lora-ready');
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyLang(lang);
    applyTheme();

    var langBtns = document.querySelectorAll('.langswitch');
    for (var k = 0; k < langBtns.length; k++) langBtns[k].addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-lang') === 'ru' ? 'en' : 'ru';
      lang = next;
      save(LANG_KEY, next);
      /* The swap itself. main.js may wrap this in a crossfade of #app by
         installing window.__vitnyrLangFade (Spark Order S4 / move 05) — a
         hook, not an interception. If nothing installed it (main.js absent,
         GSAP missing, reduced motion) the swap runs straight through, exactly
         as before; the required degradation is that theme.js still switches
         instantly on its own. */
      var swap = function () { applyLang(next); syncLangUrl(next); };
      if (typeof window.__vitnyrLangFade === 'function') window.__vitnyrLangFade(swap);
      else swap();
    });
    var ths = document.querySelectorAll('.themeswitch');
    for (var i = 0; i < ths.length; i++) ths[i].addEventListener('click', function () {
      save(THEME_KEY, effectiveTheme() === 'dark' ? 'light' : 'dark');
      applyTheme();
    });
    if (prefersLight && prefersLight.addEventListener) {
      prefersLight.addEventListener('change', function () {
        if (!stored(THEME_KEY, 'light', 'dark')) applyTheme();
      });
    }
  });
})();
