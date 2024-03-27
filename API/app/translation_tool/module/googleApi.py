from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join('/app/translation_tool', '.env'))

import sys
sys.path.append(os.getenv("Local_File_Directory"))

from google.cloud import translate_v2 as translate

class GoogleAPI:
    @staticmethod
    def translate(text, laguageVal):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./translation_tool/translation-key.json"
        translate_client = translate.Client()

        result = translate_client.translate(
            text,
            target_language=laguageVal
        )
        return result['translatedText']