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

#            messages  = [
#                {"role": "system", "content": f'You are a helpful assistant that translates {LangFrom} to {LangTo} but translate only inside html string.'},
#                {"role": "user", "content": f'Translate the following {LangFrom} text string to {LangTo} : {text} And Output only translated text'}
#            ] , 
#            messages=[
#                {"role": "system", "content": f'You are a translation assistant. Translate from {LangFrom} to {LangTo}. Only translate text that is inside HTML strings and output only the translated text.'},
#                {"role": "user", "content": f'Translate this text from {LangFrom} to {LangTo}: "{text}"'}
#            ],
            messages=[
                {"role": "system", "content": f'You are a translation assistant. Your task is to translate text from {LangFrom} to {LangTo} without adding any extra information.'},
                {"role": "user", "content": f'Please translate this: {text}'}
            ], 
#            messages=[
#                {"role": "system", "content": f'You are a dedicated translation assistant. Your sole task is to provide direct translations from {LangFrom} to {LangTo}. Do not add any additional information or commentary, only the translated text.'},
#                {"role": "user", "content": f'Please directly translate the following text from {LangFrom} to {LangTo}: {text}'}
#            ], 
            max_tokens  = int(os.getenv("ChatGPT_MAX_TOKENS")),
            n           = int(os.getenv("ChatGPT_Response_amount")),
            stop        = ChatGPTApi.convert_string_to_none(os.getenv("ChatGPT_Stop")),
            temperature = int(os.getenv("ChatGPT_Temperature")),
        )

        response = completion.choices[0].message.content
        return response

    @staticmethod
    def convert_string_to_none(s):
        if s == "None":
            return None
        else:
            return s