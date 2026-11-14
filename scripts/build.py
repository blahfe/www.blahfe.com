#!/usr/bin/env python3
"""Build the public Markdown snapshot; no CMS or JavaScript runtime required."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse
import markdown

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base', default='/www.blahfe.com/', help='URL prefix, / after custom-domain cutover')
args = parser.parse_args()
base = '/' + args.base.strip('/') + '/' if args.base.strip('/') else '/'
out = ROOT / 'docs'
if out.exists():
    shutil.rmtree(out)
out.mkdir()
shutil.copytree(ROOT / 'assets', out / 'assets')
(out / '.nojekyll').touch()
nav = [('ビジョン', 'page/vision/'), ('メンバー', 'page/member/'), ('ナレッジ', 'space/knowledge/'), ('コンタクト', 'page/contact/')]
manifest = []

def page(title, body, route):
    title = html.escape(title)
    links = ''.join(f'<a href="{base}{path}">{label}</a>' for label, path in nav)
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Blahfe &amp; Grpr</title><meta name="description" content="Blahfe &amp; Grpr — IT・セキュリティコンサルティングとナレッジ">
<link rel="canonical" href="https://www.blahfe.com/{route}"><link rel="stylesheet" href="{base}assets/site.css">
</head><body><a class="skip" href="#main">本文へ</a><header><a class="brand" href="{base}">Blahfe &amp; Grpr</a><nav aria-label="メイン">{links}</nav></header>
<main id="main"><article><h1>{title}</h1>{body}</article></main>
<footer>© Blahfe &amp; Grpr. <a href="{base}page/contact/">コンタクト</a> · <a href="https://github.com/blahfe/www.blahfe.com">GitHub</a></footer></body></html>'''

for source in sorted((ROOT / 'content').rglob('*.md')):
    rel = source.relative_to(ROOT / 'content')
    route = '' if str(rel) == 'index.md' else str(rel.with_suffix('')) + '/'
    text = source.read_text()
    title = source.stem
    if text.startswith('---\n'):
        meta, text = text[4:].split('\n---\n', 1)
        match = re.search(r'^title: (.+)$', meta, re.M)
        if match:
            title = json.loads(match.group(1))
    title = html.unescape(title)
    # Local public links keep working both at the project URL and custom domain.
    body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists', 'toc'])
    body = re.sub(r'<(/?)h([1-5])(\s[^>]*)?>', lambda m: '<' + m[1] + 'h' + str(int(m[2])+1) + (m[3] or '') + '>', body)
    def local(match):
        attr, quote, url = match.groups()
        if url.startswith('https://www.blahfe.com/'):
            url = url[len('https://www.blahfe.com'):]
        if url.startswith('/') and not url.startswith('//'):
            url = base + url.lstrip('/')
        return attr + '=' + quote + html.escape(url, quote=True) + quote
    body = re.sub(r'(href|src)=([\"\'])(.*?)\2', local, body)
    dest = out / route / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text('\n'.join(line.rstrip() for line in page(title, body, route).splitlines()) + '\n')
    raw = out / rel
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(source.read_text())
    manifest.append({'title': title, 'path': route, 'source': str(rel)})

# Preserve previous Refined paths whose human-readable suffix varied by title.
redirect = '''<p>ページのURLを更新しました。<a href="BASEspace/knowledge/">ナレッジ一覧</a>からも探せます。</p>
<script>const p=location.pathname;const m=p.match(/\\/space\\/knowledge\\/(blog\\/)?(\\d+)(?:\\/.*)?$/);const ids=IDS;if(m&&ids.includes(m[2]))location.replace('BASEspace/knowledge/'+(m[1]||'')+m[2]+'/'+location.hash);</script>'''
ids = [Path(p['source']).stem for p in manifest if re.search(r'/\d+\.md$', p['source'])]
redirect = redirect.replace('BASE', base).replace('IDS', json.dumps(ids))
(out / '404.html').write_text(page('ページを探す', redirect, '404.html'))
(out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>https://www.blahfe.com/' + html.escape(p['path']) + '</loc></url>' for p in manifest) + '</urlset>')
(out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://www.blahfe.com/sitemap.xml\n')
(out / 'llms.txt').write_text('# Blahfe & Grpr\n\n' + '\n'.join(f"- [{p['title']}]({base}{p['source']})" for p in manifest) + '\n')
print(f'Built {len(manifest)} pages in {out} (base={base})')
