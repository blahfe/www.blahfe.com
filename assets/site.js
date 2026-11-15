// Keep links from the previous project Pages URL after moving to the organization root.
if (location.hostname === 'blahfe.github.io' && location.pathname.startsWith('/www.blahfe.com/')) {
  location.replace(location.pathname.slice('/www.blahfe.com'.length) + location.search + location.hash);
}
// Preserve the original banner pixels when a browser extension filters the entire page.
(() => {
  let last = '';
  let queued = false;
  const factor = (filter, name) => {
    const match = filter.match(new RegExp(name + '\\(([-\\d.]+)(%)?\\)'));
    return match ? Number(match[1]) / (match[2] ? 100 : 1) : 1;
  };
  const update = () => {
    queued = false;
    const root = document.documentElement;
    const filter = getComputedStyle(root).filter;
    const key = root.getAttribute('nighteye') + ':' + filter;
    if (key === last) return;
    last = key;
    const active = root.getAttribute('nighteye') === 'active';
    const brightness = active ? factor(filter, 'brightness') : 1;
    const contrast = active ? factor(filter, 'contrast') : 1;
    root.style.setProperty('--artwork-brightness', String(brightness > 0 ? 1 / brightness : 1));
    root.style.setProperty('--artwork-contrast', String(contrast > 0 ? 1 / contrast : 1));
  };
  const schedule = () => {
    if (!queued) { queued = true; requestAnimationFrame(update); }
  };
  new MutationObserver(schedule).observe(document.documentElement, { attributes: true, attributeFilter: ['nighteye', 'style', 'class'] });
  new MutationObserver(schedule).observe(document.head, { childList: true, subtree: true });
  update();
})();
const siteScriptURL = document.currentScript?.src;
for (const button of document.querySelectorAll('[data-tree-toggle]')) {
  button.addEventListener('click', () => {
    const list = document.getElementById(button.getAttribute('aria-controls'));
    list.hidden = !list.hidden;
    button.setAttribute('aria-expanded', String(!list.hidden));
  });
}
document.querySelector('[data-load-pages]')?.addEventListener('click', event => {
  for (const card of document.querySelectorAll('[data-extra-page]')) card.hidden = false;
  event.currentTarget.hidden = true;
});
const BLOG_PAGE_SIZE = 30;
const blogList = document.querySelector('[data-blog-cards]');
const blogNav = document.querySelector('[data-blog-pagination]');
if (blogList && blogNav) {
  const cards = [...blogList.querySelectorAll(':scope > a.card_container')];
  const total = Math.max(1, Math.ceil(cards.length / BLOG_PAGE_SIZE));
  const requested = Number(new URLSearchParams(location.search).get('page') || '1');
  const current = Number.isInteger(requested) && requested >= 1 ? Math.min(requested, total) : 1;
  cards.forEach((card, index) => {
    card.hidden = Math.floor(index / BLOG_PAGE_SIZE) + 1 !== current;
  });
  const pageItems = () => {
    if (total <= 6) return Array.from({ length: total }, (_, index) => index + 1);
    const pages = [...new Set([1, 2, total - 1, total, current - 1, current, current + 1])]
      .filter(page => page >= 1 && page <= total)
      .sort((a, b) => a - b);
    const items = [];
    let previous = 0;
    for (const page of pages) {
      if (page - previous > 1) items.push('...');
      items.push(page);
      previous = page;
    }
    return items;
  };
  const pageHref = page => {
    const url = new URL(location.href);
    if (page === 1) url.searchParams.delete('page');
    else url.searchParams.set('page', String(page));
    url.hash = 'blog';
    return url.pathname + url.search + url.hash;
  };
  const addDisabled = label => {
    const item = document.createElement('span');
    item.className = 'blog-page is-disabled';
    item.textContent = label;
    item.setAttribute('aria-disabled', 'true');
    blogNav.append(item);
  };
  const addLink = (label, page, isCurrent) => {
    const item = document.createElement('a');
    item.className = 'blog-page' + (isCurrent ? ' is-current' : '');
    item.textContent = label;
    item.href = pageHref(page);
    if (isCurrent) item.setAttribute('aria-current', 'page');
    blogNav.append(item);
  };
  blogNav.replaceChildren();
  if (total > 1) {
    if (current === 1) addDisabled('Prev');
    else addLink('Prev', current - 1, false);
    for (const item of pageItems()) {
      if (item === '...') {
        const ellipsis = document.createElement('span');
        ellipsis.className = 'blog-page-ellipsis';
        ellipsis.textContent = '...';
        blogNav.append(ellipsis);
      } else {
        addLink(String(item), item, item === current);
      }
    }
    if (current === total) addDisabled('Next');
    else addLink('Next', current + 1, false);
  }
}
const search = document.querySelector('[data-static-search]');
search?.addEventListener('input', async () => {
  const query = search.value.trim().toLocaleLowerCase();
  let results = document.querySelector('#static-search-results');
  if (!results) {
    results = document.createElement('ul');
    results.id = 'static-search-results';
    results.className = 'static-search-results';
    results.setAttribute('aria-live', 'polite');
    search.closest('.search_container')?.after(results);
    if (!results.isConnected) search.parentElement.after(results);
  }
  results.replaceChildren();
  results.hidden = !query;
  if (!query) return;
  try {
    const url = new URL('../search-index.json', siteScriptURL || document.querySelector('script[src*="assets/site.js"]').src);
    const response = await fetch(url);
    if (!response.ok) throw new Error('Search unavailable');
    const index = await response.json();
    if (search.value.trim().toLocaleLowerCase() !== query) return;
    const matches = index.filter(page => (page.title + ' ' + page.text).toLocaleLowerCase().includes(query));
    for (const page of matches) {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = new URL(page.path, url).href;
      link.textContent = page.title;
      item.append(link);
      results.append(item);
    }
    if (!matches.length) results.textContent = '該当するページがありません。';
  } catch {
    results.textContent = '検索を利用できません。下の一覧からお探しください。';
  }
});
