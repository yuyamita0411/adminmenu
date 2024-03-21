import sys
sys.path.append("/Users/yuyamita/docker_environment/scraping_tool")

from Class.function import ExecuteClass

testdata = '<a href="~~~~~">サンプル is test テスト</a>'
testdata2 = '<a href="~~~~~">サンプル is test テスト 1234 is black</a><h2>title タイトル</h2>'
testdataH2 = '<h2>サンプル is test テスト 1234 is black</h2>'
testdata3 = '/img/test.png'

testdata4 = '\
                <div class="global-navi-inner" id="global-navi-inner">\
                    <div class="" id="global-navi-linkarea">\
                        <ul class="global-navi-menue-inner mb-0" id="menu">\
                            <li class="mb-md-0" id="menu-item-8">\
                                <a class="menu-font font-weight-bold position-relative d-inline-block mr-1" href="">サンプル is test テスト 1234 is black</a>\
                            </li>\
                        </ul>\
                        <h2>title タイトル</h2>\
                        <img src="img/translateLogo.png"\
                        class="translateLogo cursor"\
                        alt="translateLogo"\
                        style="width:1.3rem; height:1.3rem;margin: .5rem 0 .5rem 0; float: right;">\
                    </div>\
                </div>'

result = ExecuteClass.AvoidTranslate(testdata2)
result2 = ExecuteClass.appendArrVal(result["data"], result["arraydata"])

def testfunc(testdata):
    result = ExecuteClass.AvoidTranslate(testdataH2)
    result2 = ExecuteClass.appendArrVal(result["data"], result["arraydata"])
    return testdata == result2

t = '<h3>    <i></i>    1. サイト概要</h3>「Web Marketing Masterclass」は、アフィリエイトマーケティングの成功を目指す個人・企業を対象に、webマーケティングの最新手法やアクセス解析技術などの情報を提供するブログサイトです。<br><br><h3>    <i></i>    2. 主要コンテンツ</h3>アクセス解析の基本: Google Analyticsやその他のツールの使い方、訪問者の動向の読み取り方、効果的なデータの活用法などを紹介。SEOの重要性: アフィリエイトサイトのトラフィックを増やすための基本的なSEO技術や、最新のトレンドに対応する方法について解説。コンテンツマーケティング: 高品質なコンテンツの作成方法、ターゲットオーディエンスの特定、エンゲージメントを高めるテクニックなどを特集。ソーシャルメディア戦略: SNSを活用したアフィリエイトプロモーションの効果的な方法や、インフルエンサーとのコラボレーションの取り組み方を紹介。PPC広告の利用: アフィリエイトをブーストするための有料広告の戦略や、ROIを最大化するためのコツについてのガイド。メールマーケティング: 訪問者をリピーターに変え、アフィリエイトのコンバージョンを向上させるためのメールマーケティングのベストプラクティス。<br><br><h3>    <i></i>    3. 独自の価値提案</h3>「Web Marketing Masterclass」は、一般的なマーケティング情報だけでなく、アフィリエイトに特化したアドバイスや実例、事例研究を提供します。また、実際のアフィリエイトマーケターからのインタビューやゲスト記事も定期的に掲載して、読者に実践的な情報を提供します。'

#print(ExecuteClass.AvoidTranslate(testdata))
# < @ 1@ > Sample @ 2@ @ 3@ Pagsulay @ 4@

#print(ExecuteClass.AvoidTranslate(testdataH2)["data"])
#print(ExecuteClass.removespace('< @ 1@ > Sample @ 2@ @ 3@ Pagsulay @ 4@'))
#print(ExecuteClass.removespace('@ 1 @ 2 @ @ 3 @: យុទ្ធសាស្រ្តសម្រាប់ជោគជ័យសម្ព័ន្ធ'))
#print(testfunc(testdata))
#print(testfunc(testdata2))
#print(testfunc(testdataH2))
#print(testfunc(testdata3))
print(result2)