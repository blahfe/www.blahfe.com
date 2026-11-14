# www.blahfe.com

Blahfe & Grprの公開Webサイト。Confluence / RefinedからGitHub Pagesへ移行。

- `content/`: 公開済みコンテンツのMarkdown。内部資料・下書きは含めない。
- `assets/`: CMSに依存しない画像・フォント・既存テーマCSS。
- `templates/`: 現行HPの固定ページと共通ヘッダー・フッターのレイアウト。
- `scripts/build.py`: Markdownから静的HTMLを生成。
- `docs/`: GitHub Pages配信ディレクトリ（生成物もコミットする）。

## 更新

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
python3 -m http.server 8000 --directory docs
```

ナレッジ本文は`content/`、固定ページの配置・文言は`templates/`で編集し、再生成した`docs/`とともにコミットする。固定ページのMarkdownも併せて更新する。

元HPの青いヒーロー・3列サービス紹介・画像カード・フォント・配色を引き継ぐ。画像とスタイルはローカル配信し、CMSへの実行時依存を持たない。ナレッジ検索・ツリー展開・追加読み込みは`assets/site.js`で動作する。
公開URLは https://www.blahfe.com/ 。引数なしの`build.py`が canonical と `docs/CNAME`（`www.blahfe.com`）を書き出す。
GitHub Pagesの配信元はこのリポジトリ（`blahfe/www.blahfe.com`）の`master`ブランチ・`/docs`ディレクトリ。`master`へマージするとそのまま公開される。
内部資料は非公開の https://github.com/blahfe/docs に置く。

## 移管元

https://www.blahfe.com/ の匿名公開Markdown出力から取得。
公開ナレッジは移管時の公開インデックスで確認できた19ページ・3ブログ。
nabinno.github.io の公開記事38本は `content/space/knowledge/blog/n*.md`、画像は `assets/blog/` に置いた。外部インタビュー3件はナレッジのBlog欄から元URLへつなぐ。
Confluence固有の画像参照は添付ファイルに置換する。
旧URLのID付きパスは404ページで移管先へ案内する。

## 独自ドメイン

正本のホストゾーンは Infrastructure（158393879384）の `Z052732628FNUHCOJ247C`。委任されている NS は `ns-218.awsdns-27.com`、`ns-1645.awsdns-13.co.uk`、`ns-1347.awsdns-40.org`、`ns-635.awsdns-15.net`。CorporateSite の `Z05416883ATWMHT2BYQGW` は同名だが委任されていないので変更しない。

`www` は `CNAME blahfe.github.io.`。apex は GitHub Pages の A（185.199.108.153、185.199.109.153、185.199.110.153、185.199.111.153）と AAAA（2606:50c0:8000::153、2606:50c0:8001::153、2606:50c0:8002::153、2606:50c0:8003::153）。カスタムドメインは `www.blahfe.com` なので、apex は www へ誘導される。MX、TXT、DKIM、`mail`、`autodiscover` は変更しない。

ロールバックは `www` の CNAME を `blahfe.refined.site.` に戻し、apex の A と AAAA を削除する。

ヘッダーメニューは画面幅にかかわらず常時表示する。文字サイズを維持し、現行サイトの透明な背景・余白・文字の太さ・下線に合わせる。背景画像はページ上部500pxとヘッダーで同じ範囲を表示し、濃い帯を加えない。Night Eyeがページ全体にかける明るさ・コントラストは画像側で逆補正し、元画像の色を維持する。

サービス紹介の背景色は元と同じ`#0086ea`を維持する。ブラウザ拡張によるCSS背景色の書換えにも表示を保つため、同色の装飾SVGを背景へ配置する。
