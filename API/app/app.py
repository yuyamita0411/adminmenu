from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

from module.function import Function
from module.file import File
from module.json import Json
import json
from dotenv import load_dotenv
import os
import re
import shutil
from pathlib import Path

from translation_tool.execute import single, multi

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(f'{basedir}translation_tool', '.env'))

@app.route(os.getenv("VUE_APP_fileReadEndpoint"), methods=['POST'])
def list_directory_contents_Data():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}

    with open(data["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
        return data

@app.route(os.getenv("VUE_APP_fileEndpoint"), methods=['POST'])
def save_json():
    data, error, status_code = Json.get_json_data()
    if error:
        return error, status_code
    if not File.file_exists_adtion(data["filePath"]):
        return Json.save_json_data(data["filePath"], data["fileData"])
    if "fileData" not in data or data["fileData"] is None:
        return jsonify({'error': 'No JSON data provided'}), 400
    return Json.save_json_data(data["filePath"], data["fileData"])

@app.route(os.getenv("VUE_APP_fileDirectory"), methods=['POST'])
def list_directory_contents():
    data, error, status_code = Json.get_json_data()
    if error:
        return error, status_code
    response, status_code = File.list_directory(data["filePath"])
    return jsonify(response), status_code

@app.route(os.getenv("VUE_APP_filetitle"), methods=['POST'])
def make_file_title_json_data():
    data, error, status_code = Json.get_json_data()
    if error:
        return error, status_code
    dirDict = {}
    for url in data["filePath"]:
        jsondir = f'{os.getenv("VUE_APP_articleDirPath")}/{url}/language/{os.getenv("VUE_APP_FromCode")}/index.json'
        categorydir = f'{os.getenv("VUE_APP_listupPath")}/category/{os.getenv("VUE_APP_FromCode")}/index.json'
        if not os.path.exists(jsondir) or not os.path.exists(categorydir):
            continue
        jsondata, _ = Json.read_json_data(jsondir)
        categorydata, _ = Json.read_json_data(categorydir)
        if url not in dirDict:
            dirDict[url] = {}

        dirDict[url]["title"] = ''
        dirDict[url]["category"] = 'カテゴリなし'
        dirDict[url]["categoryID"] = 0

        if "pagetitle" not in jsondata:
            continue
        dirDict[url]["title"] = jsondata["pagetitle"]

        if "categoryID" not in jsondata:
            continue
        dirDict[url]["categoryID"] = jsondata["categoryID"]

        try:
            dirDict[url]["category"] = categorydata[jsondata["categoryID"]].get("category", 'カテゴリなし')
        except:
            continue

    return jsonify(dirDict), 200

@app.route(os.getenv("VUE_APP_rebaseDirEndpoint"), methods=['POST'])
def make_dir_from_json():
    data, error, status_code = Json.get_json_data()
    if error:
        return error, status_code
    dirlits = os.listdir(f'{os.getenv("VUE_APP_articleDirPath")}')
    for dir in dirlits:
        if dir not in data["filePath"]:
            File.remove_directory_with_contents(f'{os.getenv("VUE_APP_articleDirPath")}/{dir}')
    for filePath in data["filePath"]:
        if filePath is None:
            continue
        
        dirPath = f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}'
        if os.path.exists(dirPath):
            continue

        File.make_directory(dirPath)
        File.make_directory(f'{dirPath}/language')
        File.make_directory(f'{dirPath}/language/{os.getenv("VUE_APP_FromCode")}')
        Json.save_json_data(f'{dirPath}/language/{os.getenv("VUE_APP_FromCode")}/index.json', {"pagetitle": "タイトルなし"})

    return jsonify({}), 200

@app.route(os.getenv("VUE_APP_UpdateDirContentEndpoint"), methods=['POST'])
def update_dir():
    for filename in os.listdir(os.getenv("VUE_APP_targetDirPath")):
        file_path = os.path.join(os.getenv("VUE_APP_targetDirPath"), filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return {"msg": f"ファイルの削除中にエラーが発生しました: {e}", "status_code": 500}

    for filename in os.listdir(os.getenv("VUE_APP_listupPath")):
        src_file = os.path.join(os.getenv("VUE_APP_listupPath"), filename)
        dst_file = os.path.join(os.getenv("VUE_APP_targetDirPath"), filename)
        try:
            if os.path.isfile(src_file):
                shutil.copy(src_file, dst_file)
            elif os.path.isdir(src_file):
                shutil.copytree(src_file, dst_file)
        except Exception as e:
            return {"msg": f"ファイルの削除中にエラーが発生しました: {e}", "status_code": 500}

    return {"msg": "ファイルのコピーが完了しました", "status_code": 200}

@app.route(os.getenv("VUE_APP_fileTranslateEndpoint"), methods=['POST'])
def translate_json():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}
#    multi(data["translateLanguageArr"])
    single(data["filePath"], data["translateLanguageArr"], data["whichlng"])
    return {"status_code": 200}

@app.route(os.getenv("VUE_APP_categoryDirectory"), methods=['POST'])
def getCategory():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}

    with open(data["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
        return data

@app.route(os.getenv("VUE_APP_categoryDetailDirectory"), methods=['POST'])
def getCategoryDetail():
    info = request.get_json()
    if Function.fileExists(info["filePath"])["status_code"] != 200:
        return {}

    with open(info["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
        return {"data": data}

@app.route(os.getenv("VUE_APP_categoryDetailRebaseDirectory"), methods=['POST'])
def getCategoryDetailRebase():
    info = request.get_json()
    if Function.fileExists(info["filePath"])["status_code"] != 200:
        return {}

    with open(info["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
    
        if not isinstance(data, dict):
            data = json.loads(data)

        try:
            cat_id_str = info["cat_id"]
            if cat_id_str in data:
                data[cat_id_str] = info["rebaseData"]
            else:
                data = info["rebaseData"]
        except:
            data = info["rebaseData"]

        Json.save_json_data(info["filePath"], data)
        return {"data": data, "rebaseData": info["rebaseData"]}

@app.route(os.getenv("VUE_APP_categoryAddDirectory"), methods=['POST'])
def getCategoryDetailAdd():
    info = request.get_json()
    if Function.fileExists(info["filePath"])["status_code"] != 200:
        return {}

    with open(info["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
    
        if not isinstance(data, dict):
            data = json.loads(data)

        if not isinstance(info["newData"], dict):
            info["newData"] = json.loads(info["newData"])
        
        data = info["newData"]

        Json.save_json_data(info["filePath"], data)
        return {"data": data, "newData": info["newData"]}

@app.route(os.getenv("VUE_APP_categoryDeleteDirectory"), methods=['POST'])
def getCategoryDetailDelete():
    info = request.get_json()
    if Function.fileExists(info["filePath"])["status_code"] != 200:
        return {}

    with open(info["filePath"], 'r', encoding='utf-8') as file:
        data = file.read()
    
        if not isinstance(data, dict):
            data = json.loads(data)

        if info["deleteNum"] in data:
            del data[info["deleteNum"]]
        
        Json.save_json_data(info["filePath"], data)
        return {"data": data, "deleteNum": info["deleteNum"]}

def contains_japanese(text):
    # 日本語の文字範囲を確認する正規表現
    return bool(re.search(r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]', text))

def extract_language_codes(path):
    pattern = r'/([^/]+)/index\.json$'
    ln = ''
    match = re.search(pattern, path)
    if match:
        ln = match.group(1)
    return ln

@app.route(os.getenv("VUE_APP_checkFailTranslate"), methods=['POST'])
# 第一引数には API/app/translation_tool/genre/webblog/pagecategory/detail などの翻訳できてるかチェックするディレクトリが入る
def checkFailTranslateDetail():
    info = request.get_json()
    # ディレクトリを再帰的に探索
    errorArr = []
    okArr = []
    for root, dirs, files in os.walk(info["directory"]):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if any(contains_japanese(str(value)) for value in data.values()):
                            errorArr.append(extract_language_codes(file_path))
                        else:
                            okArr.append(extract_language_codes(file_path))
                except json.JSONDecodeError as e:
                    # JSON配列が空の時とか
                    continue
                except UnicodeDecodeError as e:
                    continue
    return {"data": okArr}

# ファイルアップロード関連
@app.route(os.getenv("VUE_APP_uploadfile"), methods=['POST'])
def upload_file():
    info = request.get_json()
    return {"fileData": ""}


if __name__ == '__main__':
    app.run(debug=True)