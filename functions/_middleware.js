// Cloudflare Pages Function. Crawlers and link-preview bots (Yandex, Telegram,
// LinkedIn) don't run theme.js, so /?lang=ru would look like the English page.
// For that URL only, rewrite the <head> to Russian at the edge. Every other
// request passes straight through to the static file.
const SITE = 'https://vitnyrcoach.com';

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const res = await handle(context, url);
  // the *.pages.dev address is a duplicate of the real domain: keep it out of search
  if (url.hostname.endsWith('.pages.dev')) {
    const out = new Response(res.body, res);
    out.headers.set('X-Robots-Tag', 'noindex');
    return out;
  }
  return res;
}

async function handle(context, url) {
  const res = await context.next();
  const type = res.headers.get('content-type') || '';
  if (url.searchParams.get('lang') !== 'ru' || !type.includes('text/html')) return res;

  const origin = SITE;
  const ruUrl = origin + '/?lang=ru';
  let title = '', desc = '';

  // pass 1: read the Russian twins that index.html already carries
  await new HTMLRewriter()
    .on('title[data-head-ru]', { element(e) { title = e.getAttribute('data-head-ru') || ''; } })
    .on('meta[name="description"][data-head-ru]', { element(e) { desc = e.getAttribute('data-head-ru') || ''; } })
    .transform(res.clone())
    .arrayBuffer();

  const set = (name, value) => ({ element(e) { if (value) e.setAttribute(name, value); } });
  return new HTMLRewriter()
    .on('html', { element(e) { e.setAttribute('lang', 'ru'); e.setAttribute('data-lang', 'ru'); } })
    .on('title', { element(e) { if (title) e.setInnerContent(title); } })
    .on('meta[name="description"]', set('content', desc))
    .on('meta[property="og:description"]', set('content', desc))
    .on('meta[name="twitter:description"]', set('content', desc))
    .on('meta[property="og:locale"]', set('content', 'ru_RU'))
    .on('meta[property="og:locale:alternate"]', set('content', 'en_US'))
    .on('meta[property="og:url"]', set('content', ruUrl))
    .on('meta[property="og:image"]', set('content', origin + '/assets/share/og-share-ru.png'))
    .on('meta[name="twitter:image"]', set('content', origin + '/assets/share/og-share-ru.png'))
    .on('head', { element(e) { e.append('<link rel="canonical" href="' + ruUrl + '">', { html: true }); } })
    .transform(res);
}
