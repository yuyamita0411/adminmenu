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
    "ar": "Arabic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "en": "English",
    "af": "Afrikaans",
    "am": "Amharic",
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
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "ku": "Central Kurdish",
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
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "ty": "Tahitian",
    "ug": "Uighur",
    "ur": "Urdu",
    "uz": "Uzbek"
}
#python3 execute.py singleの時↓
#saveDir = './language'