# www.blahfe.com

Blahfe & Grprの公開Webサイト（https://www.blahfe.com/）。

## 構成

- `content/`: 公開コンテンツのMarkdown（固定ページ `page/*.md`、ナレッジ一覧 `space/knowledge/README.md`、個別ページ `space/knowledge/*.md`、ブログ `space/knowledge/blog/*.md`）。
- `assets/`: 画像（`design/`、`attachments/`、`blog/`）・フォント・CSS・`site.js`。
- `templates/`: 固定ページ（`home` / `vision` / `member` / `contact` / `knowledge`）と共通ヘッダー・フッターのHTMLテンプレート。
- `scripts/build.py`: Markdownとテンプレートから静的HTML・検索インデックス・サイトマップを生成。
- `docs/`: GitHub Pages配信ディレクトリ（生成物もコミットする）。

## 更新・ビルド

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
python3 -m http.server 8000 --directory docs
```

- ナレッジ・ブログ本文は `content/`、固定ページの配置・文言は `templates/` と対応する `content/` のMarkdownを編集し、`scripts/build.py` で再生成した `docs/` とともにコミットする。
- 引数なしの `build.py` が `https://www.blahfe.com/` 向けの canonical URL、`docs/CNAME`、`docs/search-index.json`、`docs/sitemap.xml`、`docs/404.html` を出力する。
- ナレッジ検索・ツリー展開・Blogのページ送りは `assets/site.js` で動作する。Blogは30件ずつ表示し、超える分は `Prev`、ページ番号、`Next` のリンク（`?page=`）で移動する。
- GitHub Pagesの配信元はこのリポジトリ（`blahfe/www.blahfe.com`）の `master` ブランチ・`/docs` ディレクトリ。`master` へマージするとそのまま公開される。

## 独自ドメイン（DNS）

正本のホストゾーンは Infrastructure（158393879384）の `Z052732628FNUHCOJ247C`。委任されている NS は `ns-218.awsdns-27.com`、`ns-1645.awsdns-13.co.uk`、`ns-1347.awsdns-40.org`、`ns-635.awsdns-15.net`。CorporateSite の `Z05416883ATWMHT2BYQGW` は同名だが委任されていないため使用しない。

- `www`: `CNAME blahfe.github.io.`
- apex（`blahfe.com`）: GitHub Pages の A（`185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`）および AAAA（`2606:50c0:8000::153`、`2606:50c0:8001::153`、`2606:50c0:8002::153`、`2606:50c0:8003::153`）。カスタムドメインは `www.blahfe.com` のため、apex は `www` へリダイレクトされる。
- MX、TXT、DKIM、`mail`、`autodiscover` レコードはメール用途のため変更しない。

## 表示仕様

- ヘッダーメニューは画面幅にかかわらず常時表示し、透明な背景とページ上部500pxの共通バナー画像を使用する。
- ダークモード拡張（Night Eye等）による色調変化やCSS背景色の書き換えを防ぐため、`html[nighteye="disabled"]` の指定、背景画像の逆補正、およびサービス紹介セクション（`#0086ea`）への同色装飾SVG背景の配置を行っている。
