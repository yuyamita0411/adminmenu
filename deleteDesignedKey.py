import os
import json

def remove_key_from_json_files(directory, key):
    # ディレクトリ内のすべてのファイルとフォルダを走査
    for root, dirs, files in os.walk(directory):
        for file in files:
            # JSONファイルのみを対象とする
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(file_path)
                try:
                    with open(file_path, 'r+', encoding='utf-8') as f:
                        data = json.load(f)
                        # 特定のキーが存在するかチェックし、存在すれば削除
                        if key in data:
                            del data[key]
                            # ファイルを更新する
                            f.seek(0)  # ファイルの先頭に移動
                            json.dump(data, f, ensure_ascii=False, indent=4)
                            f.truncate()  # 変更後の内容でファイルを上書き
                except json.JSONDecodeError as e:
                    print(f"JSONファイルの読み込みに失敗しました: {file_path}")
                    print(str(e))
                except FileNotFoundError:
                    print(f"ファイルが見つかりません: {file_path}")
                except Exception as e:
                    print(f"予期せぬエラーが発生しました: {file_path}")
                    print(str(e))

# ここでディレクトリのパスと削除したいキーを設定
path_to_directory = "./API/app/translation_tool/genre/webblog/pagecategory/home"
key_to_remove = "content12"  # ここに削除したいキーを指定

# 関数を呼び出し
remove_key_from_json_files(path_to_directory, key_to_remove)