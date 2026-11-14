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
