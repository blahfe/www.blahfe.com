#!/usr/bin/env python3
"""Build the public Markdown snapshot; no CMS or JavaScript runtime required."""
import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse
import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base', default='/', help='URL prefix (default: /)')
parser.add_argument('--domain', default='www.blahfe.com', help='Verified custom domain; requires --base /')
args = parser.parse_args()
if args.base != '/' and args.domain == 'www.blahfe.com':
    args.domain = None
if args.domain and args.base != '/':
    parser.error('--domain requires --base /')
base = '/' + args.base.strip('/') + '/' if args.base.strip('/') else '/'
site_url = ('https://' + args.domain if args.domain else 'https://blahfe.github.io') + base
out = ROOT / 'docs'
if out.exists():
    shutil.rmtree(out)
out.mkdir()
shutil.copytree(ROOT / 'assets', out / 'assets')
(out / '.nojekyll').touch()
if args.domain:
    (out / 'CNAME').write_text(args.domain + '\n')
nav = [('ビジョン', 'page/vision/'), ('メンバー', 'page/member/'), ('ナレッジ', 'space/knowledge/'), ('コンタクト', 'page/contact/')]
manifest = []
search_index = []
asset_versions = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:12] for name in ["assets/design/refined.css", "assets/design/theme.css", "assets/design/components.css", "assets/site.css", "assets/site.js"]}

def local_urls(markup):
    def attribute(match):
        attr, quote, url = match.groups()
        url = html.unescape(url)
        if url.startswith('https://www.blahfe.com/'):
            url = url[len('https://www.blahfe.com'):]
        if url.startswith('/') and not url.startswith('//') and not (base != '/' and url.startswith(base)):
            url = base + url.lstrip('/')
        return attr + '=' + quote + html.escape(url, quote=True) + quote
    markup = re.sub(r'(href|src)=(["\'])(.*?)\2', attribute, markup)
    return markup.replace('url(&quot;/assets/', 'url(&quot;' + base + 'assets/').replace('url("/assets/', 'url("' + base + 'assets/').replace("url('/assets/", "url('" + base + 'assets/')


def page(title, body, route, toc_html='', date_html=''):
    title = html.escape(title)
    templates = ROOT / 'templates'
    name = {'': 'home', 'page/vision/': 'vision', 'page/member/': 'member', 'page/contact/': 'contact', 'space/knowledge/': 'knowledge'}.get(route)
    if name:
        main = (templates / (name + '.html')).read_text()
    else:
        outline = f'<details class="article-toc" open><summary>目次</summary><nav aria-label="この記事の目次">{toc_html}</nav></details>' if toc_html else ''
        breadcrumb = '<a class="breadcrumb" href="/space/knowledge/">ナレッジ</a>' if route.startswith('space/knowledge/') else ''
        main = f'<main id="rw_main_id" class="knowledge-article"><article>{breadcrumb}{date_html}<h1>{title}</h1>{outline}{body}</article></main>'
    header = (templates / 'header.html').read_text()
    header = re.sub(r' aria-current="page"', '', header)
    header = header.replace(' rw_active', '').replace('router-link-active', '').replace('router-link-exact-active', '')
    header = header.replace('href="/' + route + '"', 'aria-current="page" href="/' + route + '"')
    footer = (templates / 'footer.html').read_text()
    shell = f'''<div id="rw_wrapper" data-v-c819b962="" class="rw_background_partial rw_effects_popup_shadow rw_round_corners rw_header_spacious rw_theme_27164 rw_portal_styling"><div class="rw_structure" data-v-c819b962=""><div class="rw_banner" data-v-c819b962=""><img class="static-background static-banner-background" src="/assets/design/b6c3eab67b26eab3.png" alt="" aria-hidden="true" decoding="async"></div><div class="rw_full" data-v-c819b962=""></div>{header}<div id="rw_main" data-v-c819b962=""><div class="rw_bg_shadow" data-v-c819b962=""><div class="rw_shadow_container" data-v-c819b962="" style="width:85%"><div class="rw_shadow_left" data-v-c819b962=""></div><div class="rw_shadow_top" data-v-c819b962=""></div><div class="rw_shadow_right" data-v-c819b962=""></div></div></div><div id="rw_content" data-v-c819b962="" style="width:85%">{main}</div></div>{footer}</div></div>'''
    shell = local_urls(shell)
    return f'''<!doctype html>
<html lang="ja" nighteye="disabled"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}{"" if title == "Blahfe &amp; Grpr" else " | Blahfe &amp; Grpr"}</title><meta name="description" content="Blahfe &amp; Grpr — IT・セキュリティコンサルティングとナレッジ">
<link rel="icon" href="{base}assets/design/favicon.png"><link rel="canonical" href="{site_url}{route}"><link rel="stylesheet" href="{base}assets/design/refined.css?v={asset_versions['assets/design/refined.css']}"><link rel="stylesheet" href="{base}assets/design/theme.css?v={asset_versions['assets/design/theme.css']}"><link rel="stylesheet" href="{base}assets/design/components.css?v={asset_versions['assets/design/components.css']}"><link rel="stylesheet" href="{base}assets/site.css?v={asset_versions['assets/site.css']}">
<script src="{base}assets/site.js?v={asset_versions['assets/site.js']}" defer></script></head><body><a class="skip" href="#rw_main_id">本文へ</a>{shell}</body></html>'''

def route_for(rel):
    # index.md and README.md are the page for their directory. content/index.md stays the home page.
    if rel.name in {'index.md', 'README.md'}:
        parent = rel.parent.as_posix()
        return '' if parent == '.' else parent + '/'
    return rel.with_suffix('').as_posix() + '/'

for source in sorted((ROOT / 'content').rglob('*.md')):
    rel = source.relative_to(ROOT / 'content')
    route = route_for(rel)
    text = source.read_text()
    title = source.stem
    toc_depth = '1-3'
    date_html = ''
    if text.startswith('---\n'):
        meta, text = text[4:].split('\n---\n', 1)
        match = re.search(r'^title: (.+)$', meta, re.M)
        if match:
            title = json.loads(match.group(1))
        depth_match = re.search(r'^toc_depth: "([1-6]-[1-6])"$', meta, re.M)
        if depth_match:
            toc_depth = depth_match.group(1)
        date_match = re.search(r'^date: "(\d{4}-\d{2}-\d{2})"$', meta, re.M)
        if date_match:
            year, month, day = date_match.group(1).split('-')
            label = f'{int(day)} {int(month)}月, {year}'
            date_html = f'<time class="article-date" datetime="{date_match.group(1)}">{label}</time>'
    title = html.unescape(title)
    # Local public links keep working both at the project URL and custom domain.
    text = re.sub(r'(?m)^\[TOC\]\s*$', '', text)
    renderer = markdown.Markdown(
        extensions=['tables', 'fenced_code', 'sane_lists', 'footnotes', 'toc'],
        extension_configs={'toc': {'slugify': slugify_unicode, 'toc_depth': toc_depth}},
    )
    body = renderer.convert(text)
    toc_html = renderer.toc if len(re.findall(r'<a href="#', renderer.toc)) > 1 else ''
    body = re.sub(r'<(/?)h([1-5])(\s[^>]*)?>', lambda m: '<' + m[1] + 'h' + str(int(m[2])+1) + (m[3] or '') + '>', body)
    dest = out / route / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text('\n'.join(line.rstrip() for line in page(title, body, route, toc_html, date_html).splitlines()) + '\n')
    raw = out / rel
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(source.read_text())
    manifest.append({'title': title, 'path': route, 'source': str(rel)})
    search_index.append({'title': title, 'path': route, 'text': html.unescape(re.sub(r'<[^>]+>', ' ', body))})

(out / 'search-index.json').write_text(json.dumps(search_index, ensure_ascii=False) + '\n')

# Preserve previous Refined paths whose human-readable suffix varied by title.
redirect = '''<p>ページのURLを更新しました。<a href="BASEspace/knowledge/">ナレッジ一覧</a>からも探せます。</p>
<script>const p=location.pathname;const m=p.match(/\\/space\\/knowledge\\/(blog\\/)?(\\d+)(?:\\/.*)?$/);const ids=IDS;if(m&&ids.includes(m[2]))location.replace('BASEspace/knowledge/'+(m[1]||'')+m[2]+'/'+location.hash);</script>'''
ids = [Path(p['source']).stem for p in manifest if re.search(r'/\d+\.md$', p['source'])]
redirect = redirect.replace('BASE', base).replace('IDS', json.dumps(ids))
(out / '404.html').write_text(page('ページを探す', redirect, '404.html'))
(out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + site_url + html.escape(p['path']) + '</loc></url>' for p in manifest) + '</urlset>')
(out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + site_url + 'sitemap.xml\n')
(out / 'llms.txt').write_text('# Blahfe & Grpr\n\n' + '\n'.join(f"- [{p['title']}]({base}{p['source']})" for p in manifest) + '\n')
print(f'Built {len(manifest)} pages in {out} (base={base})')
