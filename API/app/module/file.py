import os
import shutil

class File:
    def __init__(self, name):
        self.name = name

    def file_exists_adtion(filePath):
        if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
        return os.path.exists(filePath)

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