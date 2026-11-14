# 現行サイトのデザイン

www.blahfe.comの公開ページを2026-11-14にレンダリングして移管した静的テンプレート。
`home / vision / member / contact / knowledge`が各固定ページ、`header / footer`は共通部分。
CMSの実行コード・API・ログイン状態は含めない。ナレッジ本文は`content/`のMarkdownから生成する。
画像・フォント・既存テーマCSSは`assets/design/`に配置。元の配色・余白・画像・3列構成を維持する。
固定ページの文言や配置を変更する場合はHTMLテンプレートと対応するMarkdownを更新する。

装飾背景は通常の`img.static-background`として埋め込み、表示位置・cover・画像フィルターを保持する。CMS固有のCSS変数や疑似要素に背景画像の読み込みを任せない。共通バナーも同じ方法で描画する。
