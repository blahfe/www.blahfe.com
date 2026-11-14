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
.venv/bin/python scripts/build.py --base /
python3 -m http.server 8000 --directory docs
```

ナレッジ本文は`content/`、固定ページの配置・文言は`templates/`で編集し、再生成した`docs/`とともにコミットする。固定ページのMarkdownも併せて更新する。

元HPの青いヒーロー・3列サービス紹介・画像カード・フォント・配色を引き継ぐ。画像とスタイルはローカル配信し、CMSへの実行時依存を持たない。ナレッジ検索・ツリー展開・追加読み込みは`assets/site.js`で動作する。
ローカル確認後、コミット前に引数なしの`build.py`でプロジェクトURL向けに再生成する。
GitHub Pagesの配信元は`master`ブランチの`/docs`。
カスタムドメイン切替前は`https://blahfe.github.io/www.blahfe.com/`で確認する。
内部資料は非公開の https://github.com/blahfe/docs に置く。

## 移管元

https://www.blahfe.com/ の匿名公開Markdown出力から取得。
公開ナレッジは移管時の公開インデックスで確認できた19ページ・3ブログ。
Confluence固有の画像参照は添付ファイルに置換する。
旧URLのID付きパスは404ページで移管先へ案内する。

## 独自ドメインへの切替

AWSにログインできたら、Route 53の`blahfe.com`ゾーンの`www`レコードを確認する。
切替前の値は`CNAME blahfe.refined.site.`。他のレコードは変更しない。

1. GitHub Pages設定に`www.blahfe.com`を登録する。
2. `.venv/bin/python scripts/build.py --base / --domain www.blahfe.com`で再生成・コミットする。
3. Route 53の`www` CNAMEを`blahfe.github.io.`に変更する。
4. DNS伝播、HTTPS証明書、全ページと画像を確認してHTTPS強制を有効にする。
5. 検証後にRefined契約を解約する。Confluenceは内部資料と添付の完全性を別途確認してから解約する。

ロールバックはDNSのCNAMEを旧値へ戻す。旧CMSは検証完了まで契約を維持する。

ヘッダーメニューは画面幅にかかわらず常時表示する。文字サイズを維持し、現行サイトの透明な背景・余白・文字の太さ・下線に合わせる。背景画像はページ上部500pxとヘッダーで同じ範囲を表示し、濃い帯を加えない。Night Eyeがページ全体にかける明るさ・コントラストは画像側で逆補正し、元画像の色を維持する。
