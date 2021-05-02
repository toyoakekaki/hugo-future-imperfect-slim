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

ウェブのダッシュボードでレポジトリ作成後

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

GraphCMS側の設定

* ダッシュボード>`Webhooks`>`Create`
* 以下を設定
  * Name: toyoakekaki/hugo-future-imperfect-slim-contentful
  * Description: toyoakekaki/hugo-future-imperfect-slim-contentful
  * Include payload: オン
  * Url: https://api.github.com/repos/toyoakekaki/hugo-future-imperfect-slim-contentful/dispatches
  * Triggers
    * Content Model: postとpageを選択
    * Stage: Published
  * Headers
    * Custome Header
      * Accept: application/vnd.github.everest-preview+json
      * User-Agent: GraphCMS Webhook
    * Secret Header
      * Authorization: token [上記の`Personal accesss token`]
    * Content type: application/json
  * Payload
    * Customize the webhook payload (valueはなんでもよい:Github Actionsに表示される)
      ```json
    {
      "event_type": "update_contentful"
    }
    ```

## 使い方

### 投稿

新規投稿

```shell
hugo new posts/2020/05/helloworld.md
content/posts/2020/05/helloworld.md created
```

```shell
SLUG=helloworld DATE=20200505 make post
```

文書作成

```shell
vi content/posts/2020/05/helloworld.md
```

下書きモード解除

```shell
vi content/posts/2020/05/helloworld.md
draft: false
```

## 注意

メディアファイル(css/js)を/から参照するのでnetlifyやgithub pagesのproject向き(github pagesのuserはだめ)

## Link

* [Hugo Future Imperfect Slim \| Hugo Themes](https://themes.gohugo.io/hugo-future-imperfect-slim/)
* [ModiiMedia/contentful\-hugo: Tool that pulls data from Contentful and turns it into markdown files for Hugo\. Can be used with other Static Site Generators, but has some Hugo specific features\.](https://github.com/ModiiMedia/contentful-hugo)
* [Running static site builds with GitHub Actions and Contentful \| Contentful](https://www.contentful.com/blog/2020/06/01/running-static-site-builds-with-github-actions-and-contentful/)
* [Creating an image gallery with Hugo and Lightbox2 \- Christian Specht](https://christianspecht.de/2020/08/10/creating-an-image-gallery-with-hugo-and-lightbox2/)
