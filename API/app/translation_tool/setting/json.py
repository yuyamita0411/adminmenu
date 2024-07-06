from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join('/app/translation_tool', '.env'))

import sys
sys.path.append(os.getenv("Local_File_Directory"))

from translation_tool.module.googleApi import GoogleAPI
from translation_tool.module.ChatGPTApi import ChatGPTApi
from translation_tool.setting.environment import fullLinArr

class JSON:
    @staticmethod
    def process_dict(di, lnkey, which):
        processed_dict = {}
        for key, value in di.items():
            if isinstance(value, str):
                # 文字列の場合は翻訳処理を実行
                # 
                # ここはjsonデータを変えないといけない。
                # LangFrom   = "Japanese"
                # LangTo   = "English"
                if which == "GoogleAPI":
                    processed_dict[key] = GoogleAPI.translate(value, lnkey)
                if which == "ChatGpt":
                    processed_dict[key] = ChatGPTApi.translate(os.getenv("VUE_APP_translateFrom"), fullLinArr[lnkey], value)

                if "img" in key:
                    processed_dict[key] = value
                if "Img" in key:
                    processed_dict[key] = value
                if "thumbnail" in key:
                    processed_dict[key] = value
                if "categoryID" in key:
                    processed_dict[key] = value
                if "created_at_for_sitemap" in key:
                    processed_dict[key] = value
                if "updated_at_for_sitemap" in key:
                    processed_dict[key] = value
                
                print(f'{lnkey} - {value}: {processed_dict[key]}')

            elif isinstance(value, dict):
                # 辞書の場合はさらに再帰処理
                processed_dict[key] = JSON.process_dict(value, lnkey, which)
            else:
                # その他のデータ型はそのまま保持
                processed_dict[key] = value
        return processed_dict

    @staticmethod
    def WriteJsonData(di, ln, which):
        return JSON.process_dict(di, ln, which)