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

def get_json_data():
    data = request.get_json()
    if data is None:
        return None, jsonify({'error': 'No JSON data received'}), 400
    return data, None, None

def file_exists(filePath):
    if not os.path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
    return os.path.exists(filePath)

def save_json_data(filePath, fileData):
    try:
        with open(filePath, 'w', encoding='utf-8') as json_file:
            json.dump(fileData, json_file, ensure_ascii=False, indent=4)
        return jsonify({'message': 'JSON data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def read_json_data(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            return json.load(file), 200
    except FileNotFoundError:
        return {'error': f"The file '{filePath}' does not exist."}, 404
    except Exception as e:
        return {'error': str(e)}, 500

def list_directory(filePath):
    try:
        return os.listdir(filePath), 200
    except FileNotFoundError:
        return {'error': f"The directory '{filePath}' does not exist."}, 404
    except PermissionError:
        return {'error': f"Permission denied to access '{filePath}'."}, 403

def make_directory(path):
    os.makedirs(path, exist_ok=True)

def remove_empty_directory(directory_path):
    try:
        os.rmdir(directory_path)
    except OSError as error:
        print(f"ディレクトリ {directory_path} の削除に失敗しました。ディレクトリが空でないか、存在しない可能性があります。")

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

@app.route(os.getenv("VUE_APP_fileEndpoint"), methods=['POST'])
def save_json():
    data, error, status_code = get_json_data()
    if error:
        return error, status_code
    if not file_exists(data["filePath"]):
        print(data["filePath"])
        print(data["fileData"])
        return save_json_data(data["filePath"], data["fileData"])
    if "fileData" not in data or data["fileData"] is None:
        return jsonify({'error': 'No JSON data provided'}), 400
    return save_json_data(data["filePath"], data["fileData"])

@app.route(os.getenv("VUE_APP_fileReadEndpoint"), methods=['POST'])
def list_directory_contents_Data():
    data, error, status_code = get_json_data()
    if error:
        return error, status_code

    response, status_code = read_json_data(data["filePath"])
    return jsonify(response), status_code

@app.route(os.getenv("VUE_APP_fileDirectory"), methods=['POST'])
def list_directory_contents():
    data, error, status_code = get_json_data()
    if error:
        return error, status_code
    response, status_code = list_directory(data["filePath"])
    return jsonify(response), status_code

@app.route(os.getenv("VUE_APP_filetitle"), methods=['POST'])
def make_file_title_json_data():
    data, error, status_code = get_json_data()
    if error:
        return error, status_code
    dirDict = {}
    for url in data["filePath"]:
        jsondir = f'{os.getenv("VUE_APP_articleDirPath")}/{url}/language/jp/index.json'
        if os.path.exists(jsondir):
            jsondata, _ = read_json_data(jsondir)
            if "pagetitle" in jsondata:
                dirDict[url] = jsondata["pagetitle"]
    return jsonify(dirDict), 200

@app.route(os.getenv("VUE_APP_rebaseDirEndpoint"), methods=['POST'])
def make_dir_from_json():
    data, error, status_code = get_json_data()
    if error:
        return error, status_code
    dirlits = os.listdir(f'{os.getenv("VUE_APP_articleDirPath")}')
    for dir in dirlits:
        if dir not in data["filePath"]:
            remove_directory_with_contents(f'{os.getenv("VUE_APP_articleDirPath")}/{dir}')
    for filePath in data["filePath"]:
        if filePath:
            dirPath = f'{os.getenv("VUE_APP_articleDirPath")}/{filePath}'
            make_directory(dirPath)
            make_directory(f'{dirPath}/language')
            make_directory(f'{dirPath}/language/jp')
            save_json_data(f'{dirPath}/language/jp/index.json', {"pagetitle": "タイトルなし"})
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug=True)