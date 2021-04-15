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

### Contentfulとの連携

package.json

```json
{
  "name": "my-hugo-project",
  "scripts": {
    "dev": "contentful-hugo --preview && hugo server",
    "build": "contentful-hugo && hugo --minify"
  }
}
```

```shell
npm i -S contentful-hugo
contentful-hugo --init
```

上記で作成された`contentful-hugo.config.js`をカスタマイズする

### Github

#### レポジトリ

ウェブのダッシュボードでレポジトリ作成後

```shell
git remote add origin git@github.com:toyoakekaki/hugo-future-imperfect-slim-contentful.git
git add .
git commit -m 'first commit'
git branch -M main
git push -u origin main
```

#### Webhook

Gihub Actionsの設定

* [workflows](./.github/workflows/gh-pages.yaml)の設定
* 以下の`Secrets`を登録
  * `CONTENTFUL_SPACE`
  * `CONTENTFUL_TOKEN`

Webhookの設定

* ダッシュボード>右上のユーザアイコン>`Settings`>`Developper Settings`>`Personal accesss tokens`>`Generate new token`
  * `Note`: 適当な名前
  * `Select scopes`: 一番上の`repo`にチェック

[Rest Client for VS Code](./test.http)で確認できる


Contentful側の設定

* ダッシュボード>`Settings`>`Webhooks`>`Add Webhook`
* 以下を設定

  * Details
    * Name: toyoakekaki/hugo-future-imperfect-slim-contentful
    * URL: POST https://api.github.com/repos/toyoakekaki/hugo-future-imperfect-slim-contentful/dispatches
  * Triggers
    * Select specific triggering envents
      * Entry (Publish/Unpublish/Delete)
      * Assets (Publish/Unpublish/Delete)
  * Headers
    * Custome Header
      * Accept: application/vnd.github.everest-preview+json
      * User-Agent: Contentful Webhook
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
