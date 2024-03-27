from dotenv import load_dotenv
from openai import OpenAI
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join('/app/translation_tool', '.env'))

import sys
sys.path.append(os.getenv("Local_File_Directory"))

class ChatGPTApi:
    @staticmethod
    def translate(LangFrom, LangTo, text):
        client = OpenAI(api_key=os.getenv("ChatGPT_API_KEY"))

        completion = client.chat.completions.create(
            model    = "gpt-3.5-turbo",

            messages  = [
                {"role": "system", "content": f'You are a helpful assistant that translates {LangFrom} to {LangTo}.'},
                {"role": "user", "content": f'Translate the following {LangFrom} text to {LangTo} :「{text}」. And Output only translated text'}
            ] , 

            max_tokens  = os.getenv("ChatGPT_MAX_TOKENS"),
            n           = os.getenv("ChatGPT_Response_amount"),
            stop        = os.getenv("ChatGPT_Stop"),
            temperature = os.getenv("ChatGPT_Temperature"),
        )

        response = completion.choices[0].message.content
        return response