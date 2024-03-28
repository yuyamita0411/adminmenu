from dotenv import load_dotenv
import os

from translation_tool.Class.function import Handler, ExecuteClass
from translation_tool.setting.environment import datafilrpatharr, lnarr
from translation_tool.setting.json import JSON

# 現在のファイルのディレクトリパスを取得
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def multi():
    for lnkey, ln in lnarr.items():
        for val in datafilrpatharr:
            savepath = val.replace(os.getenv("VUE_APP_FromCode"), ln)
            folderpath = savepath.replace('/index.json', '')
            common(val, folderpath, savepath, ln)

def single(filePath):
    for lnkey, ln in lnarr.items():
        saveDir = GetTwoUpperDirectory(filePath)
        common(filePath, f'{saveDir}/{ln}', f'{saveDir}/{ln}/{os.getenv("SaveFilename")}', ln)

def GetTwoUpperDirectory(fileDir):
    # 相対パスを絶対パスに変換
    absolute_path = os.path.abspath(fileDir)
    # 2つ上のディレクトリへのパスを取得
    return os.path.dirname(os.path.dirname(absolute_path))

def common(data, folderpath, savepath, ln):
    #メソッドを制御するクラス
    handler = Handler("Handler")
    #メソッドを実行するクラス
    executeClass = ExecuteClass("ExecuteClass")

    #何かしらの生データ ここではjson
    di = executeClass.GetData(data, 'json')

    #変数で定義したメソッドを実行する
    #フォルダーがない場合作る
    if(os.path.exists(folderpath) == False):
        handler.define_callback(executeClass.MakeDir(folderpath))
    #ファイルがない場合作る
    if(os.path.exists(savepath) == False):
        handler.define_callback(executeClass.MakeFile(savepath))

    appendData = JSON.WriteJsonData(di, ln)
    #指定したパスへjsonファイルを保存する
    executeClass.PreserveFile(appendData, savepath, "json")