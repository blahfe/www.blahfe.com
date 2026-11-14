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
