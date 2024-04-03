ページを読み込むとjsonデータを配列に切り替える

エディタ上のプラスボタンを押すとタグの種類を選択できる。

↑のタグを押すと+ボタンを押した箇所に編集用のテキストエリアが追加される。
他の箇所をターゲットにするとクリックした箇所が編集対象のテキストエリアに切り替わる。

エディタの文字をクリックすると今カーソルを当てたタグが何タグなのかを特定する

# jsonデータのフォーマット
⚫︎home
{
    "ogImg": "",
    "pageName": "",
    "pagetitle": "",
    "description": "",
    "contenttitle1": "",
    "content2": "",
    ...
    "created_at": "",
    "updated_at": "",
    "created_at_for_sitemap": "",
    "updated_at_for_sitemap": ""
}

⚫︎detail
{
    "pagetitle": "",
    "categoryID": "",
    "contenttitle1": "",
    "articleMiddleImg1": "",
    "content1": "",
    "contentsecondtitle1": "",
    ...
    "description": "",
    "created_at": "",
    "updated_at": "",
    "created_at_for_sitemap": "",
    "updated_at_for_sitemap": "",
    "thumbnail": "",
    "ogImg": ""
}

⚫︎common
{
    "categoryArticle": "",
    "categoryArticleEN": "",
    "notificationurl": "",
    "sitemapinfo": {
        "title": "",
        "ogImg": ""
    },
    "toctitle":""
}

⚫︎category
{
    "1": {
        "category": "",
        "description": "",
        "ogImg": "",
        "catlist": [
            "1"
        ],
        "created_at": "",
        "updated_at": "",
        "created_at_for_sitemap": "",
        "updated_at_for_sitemap": ""
    }
}