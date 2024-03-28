#基準のファイル
#python3 execute.py singleの時↓
#更新するファイルが複数ある時
#python3 execute.py multiの時↓
datafilrpatharr = [
    './translation_tool/pagecategory/category/jp/index.json',
    './translation_tool/pagecategory/common/jp/index.json',
    './translation_tool/pagecategory/detail/1/language/jp/index.json',
    './translation_tool/pagecategory/home/language/jp/index.json'
]
#翻訳する言語と言語コード
# google APIで使う時
#lnarr = {
#    "英語語":"en"
#}

# ChatGPT APIで使う時
lnarr = {
    "英語":"en"
}
fullLinArr = {
    "en": "english"
}
#python3 execute.py singleの時↓
#saveDir = './language'