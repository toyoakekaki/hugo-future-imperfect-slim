// contentful-hugo.config.js

module.exports = {
    // fetches from default locale if left blank
    //locales: ['ja-JP', 'en-US'],
    locales: [
        {
            code: 'ja-JP',
            mapTo: ''
        },
        {
            code: 'en-US',
            mapTo: 'en'
        }
    ],

    singleTypes: [
        /*
        シングルページの設定

        * Content model `Page`がターゲット
        * fields.slugで特定ページを指定

        */
        {
            id: 'page',
            directory: 'content',
            fileName: '_index',
            fileExtension: 'md',
            ignoreLocales: false,
            mainContent: 'body',
            layout: 'about',
            //isHeadless: true,
            filters: {
                'fields.slug': 'home'
            }
        },
        {
            id: 'page',
            directory: 'content/about',
            fileName: 'index',
            fileExtension: 'md',
            ignoreLocales: false,
            mainContent: 'body',
            layout: 'about',
            filters: {
                'fields.slug': 'about'
            }
        },
        //{
        //    id: 'siteSettings',
        //    directory: 'data',
        //    fileName: 'settings',
        //    fileExtension: 'yaml',
        //},
    ],

    repeatableTypes: [
        /*
        複数ページの設定

        * Content model `Post`がターゲット
        * body: mainContent(本文)
        * categories: 表示をCategory.titleに変換
        * tags: 表示をTag.titleに変換

        */
        {
            id: 'post',
            //directory: 'content/posts',
            directory: 'content/blog',
            fileExtension: 'md',
            mainContent: 'body',
            resolveEntries: [
                {
                    field: 'categories',
                    resolveTo: 'fields.title',
                },
                {
                    field: 'tags',
                    resolveTo: 'fields.title',
                },
            ],
            overrides: [
                {
                    // the image field is a multi-reference field
                    field: 'images',
                    options: {
                        valueTransformer: (imageRefs) => {
                            const images = [];
                            for (const ref of imageRefs) {
                              if (ref.fields.title) {
                                // get the name, photo, and bio of the image
                                // and add it to the array
                                images.push({
                                  alt: ref.fields.title,
                                  src: ref.fields.file.url,
                                  stretch: "stretchH"
                                });
                               }}
                            return images;
                        },
                    },
                },
            ],
            //overrides: [
            //    {
            //        field: 'image',
            //        options: {
            //          valueTransformer: (ref) => {
            //            class Image {
            //              constructor(src, alt) {
            //                this.src = src;
            //                this.alt = alt;
            //              }
            //            }
            //            return  new Image(ref.fields.width, ref.fields.url);
            //            },
            //        },
            //    },
            //],
        },
        //{
        //    id: 'seoFields',
        //    isHeadless: true,
        //    directory: 'content/seo-fields',
        //},
        //{
        //    id: 'reviews',
        //    directory: 'content/reviews',
        //    mainContent: 'reviewBody',
        //},
    ],
};
