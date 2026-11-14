# www.blahfe.com

Blahfe & Grprの公開Webサイト。Confluence / RefinedからGitHub Pagesへ移行。

- `content/`: 公開済みコンテンツのMarkdown。内部資料・下書きは含めない。
- `assets/`: CMSに依存しない画像とスタイル。
- `scripts/build.py`: Markdownから静的HTMLを生成。
- `docs/`: GitHub Pages配信ディレクトリ（生成物もコミットする）。
- `legacy/`: 旧AWS/CDK構成。現行サイトでは使用しない。

## 更新

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
python3 -m http.server 8000 --directory docs
```

`content/`を編集し、再生成した`docs/`とともにコミットする。
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
