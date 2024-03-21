import sys
sys.path.append("/Users/yuyamita/docker_environment/adminmenu/API/app/translation_tool")

from google.cloud import translate_v2 as translate
import os

class JSON:
    @staticmethod
    def trans(text, laguageVal):
        # 環境変数にAPIキーのパスを設定
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./translation_tool/translation-key.json"
        translate_client = translate.Client()
        # 翻訳の実行
        result = translate_client.translate(
            text,
            target_language=laguageVal
        )
        return result['translatedText']
        # 翻訳結果の表示

    @staticmethod
    def process_dict(di, lnkey):
        processed_dict = {}
        for key, value in di.items():
            if isinstance(value, str):
                # 文字列の場合は翻訳処理を実行
                processed_dict[key] = JSON.trans(value, lnkey)
            elif isinstance(value, dict):
                # 辞書の場合はさらに再帰処理
                processed_dict[key] = JSON.process_dict(value, lnkey)
            else:
                # その他のデータ型はそのまま保持
                processed_dict[key] = value
        return processed_dict

    @staticmethod
    def WriteJsonData(di, ln):
        return JSON.process_dict(di, ln)