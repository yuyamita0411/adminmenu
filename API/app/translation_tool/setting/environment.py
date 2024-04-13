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
    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/common/ja/index.json',
    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/category/ja/index.json',
#    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/detail/1/language/ja/index.json',
    f'./translation_tool/genre/{os.getenv("VUE_APP_whichblog")}/pagecategory/home/language/ja/index.json'
]
#翻訳する言語と言語コード
# google APIで使う時
#lnarr = {
#    "英語語":"en"
#}

# ChatGPT APIで使う時
lnarr = {
    "アラビア語": "ar",
    "アゼルバイジャン語": "az",
    "ベラルーシ語": "be",
    "ブルガリア語": "bg",
    "ベンガル語": "bn",
    "英語": "en",
    "アフリカーンス語": "af",
    "ボスニア語": "bs",
    "カタロニア語": "ca",
    "チェコ語": "cs",
    "ウェールズ語": "cy",
    "ドイツ語": "de",
    "ギリシャ語": "el",
    "エスペラント語": "eo",
    "スペイン語": "es",
    "エストニア語": "et",
    "バスク語": "eu",
    "ペルシャ語": "fa",
    "フィンランド語": "fi",
    "フランス語": "fr",
    "ガリシア語": "gl",
    "ヘブライ語": "he",
    "ヒンディー語": "hi",
    "クロアチア語": "hr",
    "ハンガリー語": "hu",
    "インドネシア語": "id",
    "アイスランド語": "is",
    "イタリア語": "it",
    "ジャワ語": "jv",
    "カザフ語": "kk",
    "韓国語": "ko",
    "クルド語": "ku",
    "リトアニア語": "lt",
    "ラトビア語": "lv",
    "マケドニア語": "mk",
    "モンゴル語": "mn",
    "モンゴル語": "mn",
    "マラーティー語": "mr",
    "マレー語": "ms",
    "ネパール語": "ne",
    "オランダ語": "nl",
    "ポーランド語": "pl",
    "ポルトガル語": "pt",
    "ルーマニア語": "ro",
    "ロシア語": "ru",
   "シンド語": "sd",
    "スロバキア語": "sk",
    "スロベニア語": "sl",
    "アルバニア語": "sq",
    "スウェーデン語": "sv",
    "スワヒリ語": "sw",
    "タイ語": "th",
    "タガログ語": "tl",
    "トルコ語": "tr",
    "ウルドゥ語": "ur",
    "ウズベク語": "uz"
}
fullLinArr = {
    "am": "Amharic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "km": "Khmer",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "en": "English",
    "af": "Afrikaans",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "de": "German",
    "el": "Greek",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "jv": "Javanese",
    "kk": "Kazakh",
    "kn": "Kannada",
    "ko": "Korean",
    "ku": "Kurdish",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "my": "Burmese",
    "ne": "Nepali",
    "nl": "Dutch",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sq": "Albanian",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "ug": "Uighur",
    "ur": "Urdu",
    "uz": "Uzbek",
    "sw": "Swahili"
}
#python3 execute.py singleの時↓
#saveDir = './language'