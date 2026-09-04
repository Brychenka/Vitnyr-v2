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
    var btn = document.querySelector('.themeswitch');
    if (!btn) return;
    var next = effectiveTheme() === 'dark' ? 'light' : 'dark';
    var lang = document.documentElement.getAttribute('data-lang') || 'en';
    var words = { en: { light: 'Cream', dark: 'Charcoal' },
                  ru: { light: 'Крем',  dark: 'Уголь' } };
    btn.textContent = words[lang][next];
    btn.setAttribute('aria-label',
      lang === 'ru' ? 'Переключить оформление' : 'Switch to the ' + next + ' theme');
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
    var sw = document.querySelector('.langswitch');
    if (sw) {
      sw.textContent = (l === 'ru') ? 'EN' : 'RU';
      sw.setAttribute('aria-label', (l === 'ru') ? 'Switch to English' : 'Переключить на русский');
    }
    labelTheme();
    // the hero lines differ per language, so their masks need re-measuring
    document.dispatchEvent(new CustomEvent('vitnyr:langchange', { detail: l }));
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

    var sw = document.querySelector('.langswitch');
    if (sw) sw.addEventListener('click', function () {
      lang = document.documentElement.getAttribute('data-lang') === 'ru' ? 'en' : 'ru';
      save(LANG_KEY, lang);
      applyLang(lang);
    });
    var th = document.querySelector('.themeswitch');
    if (th) th.addEventListener('click', function () {
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
