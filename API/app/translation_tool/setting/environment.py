from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join('/app/translation_tool', '.env'))

import sys
sys.path.append(os.getenv("Local_File_Directory"))

#基準のファイル
#python3 execute.py singleの時↓
#更新するファイルが複数ある時
#python3 execute.py multiの時↓
datafilrpatharr = [
#    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/common/ja/index.json',
#    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/category/ja/index.json',
#    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/detail/1/language/ja/index.json'
    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/home/language/ja/index.json'
]
#翻訳する言語と言語コード
# google APIで使う時
#lnarr = {
#    "英語語":"en"
#}

# ChatGPT APIで使う時
lnarr = {
    "アムハラ語": "am"
}
fullLinArr = {
    "am": "Amharic"
}
#python3 execute.py singleの時↓
#saveDir = './language'