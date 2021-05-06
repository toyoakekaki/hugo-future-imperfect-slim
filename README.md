# README

## セットアップ

サイト作成

```shell
hugo new site hugo-imperfect-slim-contentful
```

レポジトリ初期化

```shell
cd hugo-future-imperfect-slim-contentful
git init
echo '*~' >> .gitignore
echo '*.bak' >> .gitignore
echo '*.orig' >> .gitignore
echo '.env' >> .gitignore
echo 'public' >> .gitignore
echo 'resources' >> .gitignore
```

テーマ設定(submoduleはhttpsプロトコルで追加)

```shell
git submodule add https://github.com/pacollins/hugo-future-imperfect-slim.git themes/future-imperfect-slim
```

(参考)submoduleの削除

```shell
git submodule deinit -f themes/future-imperfect-slim
git rm themes/future-imperfect-slim
rm -fr .git/modules/future-imperfect-slim
```

サイト設定

```shell
cp themes/future-imperfect-slim/exampleSite/config.toml .
```

config.toml

```toml
baseURL = "https://example.com/"
languageCode = "en-us"
defaultContentLanguage = "ja"
title = "My New Hugo Site"
theme = "future-imperfect-slim"
```

> github pagesやnetlifyで使う場合はbaseURLのプロトコルはhttpsにすること

起動確認(http://localhost:1313)

```shell
cp /path/to/someplace/Makefile .
make run
```

### GraphCMSとの連携

#### トークンの取得


* `GRAPHCMS_ENDPOINT`: ダッシュボード>`Settings`>Endpoints
* `GRAPHCMS_TOKEN`
  * `Permanent Auth Tokens`にて以下を設定して`Create`
    * `Name`: 適当な名前
    * `Content from stage Published`: チェック

#### コンテンツの取得

コンテンツの取得は[Python Script](./app/main.py)で実施

### Github

#### レポジトリ

Github管理画面のダッシュボードでレポジトリ作成後

```shell
git remote add origin git@github.com:toyoakekaki/hugo-future-imperfect-slim.git
git add .
git commit -m 'first commit'
git branch -M main
git push -u origin main
```

#### Webhook

Gihub Actionsの設定

* [workflows](./.github/workflows/gh-pages.yaml)の設定
* 以下の`Secrets`を登録
  * `GRAPHCMS_ENDPOINT`
  * `GRAPHCMS_TOKEN`

Webhookの設定

* ダッシュボード>右上のユーザアイコン>`Settings`>`Developper Settings`>`Personal accesss tokens`>`Generate new token`
  * `Note`: 適当な名前
  * `Select scopes`: 一番上の`repo`にチェック

[Rest Client for VS Code](./test.http)で確認できる

GraphCMS側の設定(**Github Actionsに対応していないので中継サーバに投げる**)
<sup id="a1">[1](#f1)</sup>

* ダッシュボード>`Webhooks`>`Create`
* 以下を設定
  * Name: toyoakekaki/hugo-future-imperfect-slim-contentful
  * Description: toyoakekaki/hugo-future-imperfect-slim-contentful
  * Include payload: Off
  * Url: <中継サーバのエンドポイント>
  * Triggers
    * Content Model: postとpageを選択
    * Stage: Published
  * Headers: None

<b id="f1">1</b>Github ActionsのWebhookではpayloadにevent_typeが必須だがGraphcmsでは設定できない(2021/5/6) [↩](#a1)

## デザイン

### 基本のテンプレート

* layouts/_default/baseof.html
  * 全ページで使われるBase Template
  * ここでページのカラムレイアウトなどを設計し各パーツを読み込む
* layouts/index.html
  * トップページ
  * 存在しない場合は以下のlist.htmlを呼び出す
* layouts/_default/list.html
  * セクションやTaxonomy(カテゴリーやタグ等のグルーピング)ごとの記事一覧ページ
* layouts/_default/single.html
  * 記事個別ページ
  * ブログ本文

### future-imperfect-slimのテンプレート構成

* 基本構成
  * layouts/_default/baseof.html: 大本の基本レイアウト
    * layouts/partials/head.html: htmlのheadタグ
      * layouts/partials/meta.html: htmlのheadタグ内のmeta情報
    * layouts/partials/site-header.html: サイト共通のヘッダーセクション
      * layouts/partials/theme-notification.html: テーマ配給元のお知らせ
        * layouts/partials/theme-message.md: 上記から呼び出されるメッセージ
      * layouts/partials/language-menu.html: 言語メニュー表示用ドロップダウン
    * layouts/partials/site-intro.html: サイドバー上部のサイト情報
      * layouts/partials/rss-icon.html
      * layouts/partials/socnet-icon.html
    * layouts/partials/site-sidebar.html: サイト共通のサイドバー
    * layouts/partials/site-footer.html: サイト共通のフッタセクション
      * layouts/partials/rss-icon.html
      * layouts/partials/socnet-icon.html
    * layouts/partials/scripts.html: javascriptの読み込み
* セクション
  * layouts/_default/about.html: aboutレイアウト
  * layouts/_default/contact.html: contactレイアウト
  * layouts/_default/terms.html: termsレイアウト
* リスト
  * layouts/_default/list.html
    * layouts/_default/content-list.html(.Render)
* 個別ページ
  * layouts/_default/single.html: 個別ページ
    * layouts/_default/header.html: 個別ページのヘッダ(.Render)
      * layouts/_default/date.html: ヘッダの日付(.Rneder)
      * layouts/_default/date.nl.html; ヘッダの日付(オランダ語)(.Rneder)
    * layouts/partials/share-buttons.html: シェアボタン
    * layouts/_default/featured.html: 特集コンテンツ(.Render)
    * layouts/_default/stats.html(.Render)
    * layouts/_default/comments.html(.Render)
* その他
  * layouts/_default/index.json.json: 全文検索用ファイル(**要確認**)

## Link

* [Hugo Future Imperfect Slim \| Hugo Themes](https://themes.gohugo.io/hugo-future-imperfect-slim/)
* [ModiiMedia/contentful\-hugo: Tool that pulls data from Contentful and turns it into markdown files for Hugo\. Can be used with other Static Site Generators, but has some Hugo specific features\.](https://github.com/ModiiMedia/contentful-hugo)
* [Running static site builds with GitHub Actions and Contentful \| Contentful](https://www.contentful.com/blog/2020/06/01/running-static-site-builds-with-github-actions-and-contentful/)
* [Creating an image gallery with Hugo and Lightbox2 \- Christian Specht](https://christianspecht.de/2020/08/10/creating-an-image-gallery-with-hugo-and-lightbox2/)
* [Hugo のレイアウトの仕組み \- Marbles Day](https://marbles.hatenablog.com/entry/2020/11/22/204751)
* [タクソノミー関連のテンプレートを定義する \| まくまくHugo/Goノート](https://maku77.github.io/hugo/taxonomy/template.html)
* [各種ページにおいて \.Kind や \.IsPage、\.IsSection、\.IsNode の値がどうなるかの一覧 \| まくまくHugo/Goノート](https://maku77.github.io/hugo/template/page-types.html)
