from flask import Flask, request, jsonify
from flask_cors import CORS

from module.function import Function
from module.file import File
from module.json import Json
import json
from dotenv import load_dotenv
import os
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

        if "pagetitle" not in jsondata:
            continue
        dirDict[url]["title"] = jsondata["pagetitle"]

        try:
            dirDict[url]["category"] = categorydata[jsondata["categoryID"]].get("description", 'カテゴリなし')
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
    multi()
#    single(data["filePath"])
    return {"status_code": 200}

if __name__ == '__main__':
    app.run(debug=True)