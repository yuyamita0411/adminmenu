from flask import Flask, request, jsonify
from flask_cors import CORS

from module.function import Function
import json
from dotenv import load_dotenv
import os
import shutil
from pathlib import Path

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
        print("ファイルパスなし")
        return {}
    try:
        for url in data["filePath"]:
            jsondir = f'{os.getenv("VUE_APP_articleDirPath")}/{url}/language/jp/index.json'
            if Function.fileExists(jsondir)["status_code"] == 200:
                with open(jsondir, 'r', encoding='utf-8') as file:
                    jsondata = json.load(file)
                    if "pagetitle" in jsondata:
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

@app.route(os.getenv("VUE_APP_rebaseDirEndpoint"), methods=['POST'])
def make_dir_from_json():
    data = request.get_json()

    dirlits = os.listdir(f'{os.getenv("VUE_APP_articleDirPath")}')

    for dir in dirlits:
        if dir not in data["filePath"]:
            remove_directory_with_contents(f'{os.getenv("VUE_APP_articleDirPath")}/{dir}')

    for filePath in data["filePath"]:
        if filePath and filePath not in dirlits:
            makePath(f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}')
            makePath(f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}/language')
            makePath(f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}/language/jp')
            with open(f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}/language/jp/index.json', 'w') as file:
                json.dump({"pagetitle": "タイトルなし"}, file, ensure_ascii=False, indent=4)
    return {}


# 空のディレクトリを削除する関数
def remove_empty_directory(directory_path):
    try:
        os.rmdir(directory_path)
    except OSError as error:
        print(f"ディレクトリ {directory_path} の削除に失敗しました。ディレクトリが空でないか、存在しない可能性があります。")

# 内容を含むディレクトリを削除する関数
def remove_directory_with_contents(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"ディレクトリ {directory_path} とその内容が正常に削除されました。")
    except OSError as error:
        print(f"ディレクトリ {directory_path} の削除に失敗しました。")

def makePath(dirpath):
    dir_path = Path(dirpath)
    if not dir_path.exists():
        dir_path.mkdir()
        print(f"ディレクトリ'{dir_path}'が生成されました。")
    else:
        print(f"ディレクトリ'{dir_path}'は既に存在します。")

if __name__ == '__main__':
    app.run(debug=True)