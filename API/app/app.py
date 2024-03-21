from flask import Flask, request, jsonify
from flask_cors import CORS

from module.function import Function
import json
from dotenv import load_dotenv
import os

from translation_tool.execute import single

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(f'{basedir}translation_tool', '.env'))

@app.route(os.getenv("VUE_APP_fileEndpoint"), methods=['POST'])
def save_json():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        os.makedirs(os.path.dirname(data["filePath"]), exist_ok=True)
        with open(data["filePath"], 'w', encoding='utf-8') as json_file:
            json.dump(data["fileData"], json_file, ensure_ascii=False, indent=4)
        return jsonify({'message': 'JSON data saved successfully'}), 200

    if data["fileData"] is None:
        return jsonify({'error': 'No JSON data received'}), 400
    # JSONファイルに保存、ensure_ascii=Falseを指定して日本語がエスケープされないようにする
    try:
        with open(data["filePath"], 'w', encoding='utf-8') as json_file:
            json.dump(data["fileData"], json_file, ensure_ascii=False, indent=4)
        return jsonify({'message': 'JSON data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route(os.getenv("VUE_APP_fileReadEndpoint"), methods=['POST'])
def list_directory_contents_Data():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}

    with open(data["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
        return data

@app.route(os.getenv("VUE_APP_fileDirectory"), methods=['POST'])
def list_directory_contents():
    data = request.get_json()
    dirList = []
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}
    try:
        # ディレクトリ内の項目をリストアップ
        contents = os.listdir(data["filePath"])
        for item in contents:
            dirList.append(item)
        return dirList
    except FileNotFoundError:
        return f"The directory '{data['filePath']}' does not exist."
    except PermissionError:
        return f"Permission denied to access '{data['filePath']}'."

@app.route(os.getenv("VUE_APP_filetitle"), methods=['POST'])
def make_file_title_json_data():
    data = request.get_json()
    dirDict = {}
    if data["filePath"] is None:
        return {}
    try:
        for url in data["filePath"]:
            jsondir = f'{os.getenv("VUE_APP_articleDirPath")}/{url}/index.json'
            if Function.fileExists(jsondir)["status_code"] != 200:
                return {}
            print(url)
            with open(jsondir, 'r', encoding='utf-8') as file:
                jsondata = json.load(file)  # ファイルの内容をJSONとして読み込む
                if "pagetitle" in jsondata:  # ページタイトルが存在するか確認
                    dirDict[url] = jsondata["pagetitle"]
    except FileNotFoundError:
        return f"The directory '{data['filePath']}' does not exist."
    except PermissionError:
        return f"Permission denied to access '{data['filePath']}'."

    return dirDict

@app.route(os.getenv("VUE_APP_fileTranslateEndpoint"), methods=['POST'])
def translate_json():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}

    single(data["filePath"])

    return {"status_code": 200}

if __name__ == '__main__':
    app.run(debug=True)