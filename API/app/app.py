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

from translation_tool.execute import single

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
        print(data["filePath"])
        print(data["fileData"])
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
        jsondir = f'{os.getenv("VUE_APP_articleDirPath")}/{url}/language/jp/index.json'
        if os.path.exists(jsondir):
            jsondata, _ = Json.read_json_data(jsondir)
            if "pagetitle" in jsondata:
                dirDict[url] = jsondata["pagetitle"]
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
        if filePath:
            dirPath = f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}'
            File.make_directory(dirPath)
            File.make_directory(f'{dirPath}/language')
            File.make_directory(f'{dirPath}/language/jp')
            Json.save_json_data(f'{dirPath}/language/jp/index.json', {"pagetitle": "タイトルなし"})
    return jsonify({}), 200

@app.route(os.getenv("VUE_APP_fileTranslateEndpoint"), methods=['POST'])
def translate_json():
    data = request.get_json()
    if Function.fileExists(data["filePath"])["status_code"] != 200:
        return {}
    single(data["filePath"])
    return {"status_code": 200}

if __name__ == '__main__':
    app.run(debug=True)