import codecs
import json
import os
import pathlib
import re

class ExecuteClass:
    def __init__(self, name):
        self.name = name

    def MakeDir(self, path):
        os.mkdir(path)

    def MakeFile(self, path):
        p = pathlib.Path(path)
        p.touch()

    def GetData(self, path, Format):
        if Format == 'json':
            with open(path) as f:
                di = json.load(f)
                return di

    def FilterDom(self, doms, lnkey):
        ClickDom = {}
        for dom in doms:
            if dom.text == lnkey:
                ClickDom = dom
        return ClickDom

    def DomEvent(self, Dom, event):
        if event == 'click':
            Dom.click()

    def PreserveFile(self, data, path, Format):
        if Format == 'json':
            fw = codecs.open(path , 'w', 'utf-8')
            json.dump(data, fw, ensure_ascii=False, indent=4)
            fw.close()

    def AvoidTranslate(s):
        # タグ、単語の正規表現パターン
        patterns = [
            r'<([a-z]+)\s*([^>]*)>',   # 開始タグ
            r'(</[a-z0-9]+>)',            # タグの終了
            r' (?=[a-zA-Z]+<)',        # スペース（タグの前）
            r'([a-zA-Z0-9]+)',            # アルファベット
        ]

        combined_pattern = "|".join(patterns)
        matches = list(re.finditer(combined_pattern, s))

        data = s
        arraydata = {}
        counter = 1

        offset = 0
        for match in matches:
            start, end = match.span()
            value = match.group()

            if match.group(1):  # タグの開始
                tag_placeholder = f"<[@{counter}@]>"
                if match.group(1).startswith("<a "):
                    attr = match.group(1).split(" ", 1)[1].replace('href="', '').replace('"', '').replace(">", '')
                    arraydata[f"[@{counter}@]"] = attr
                else:
                    arraydata[f"[@{counter}@]"] = value[1:-1]
            elif match.group(2):  # タグの終了
                tag_placeholder = f"</[@{counter}@]>"
                arraydata[f"[@{counter}@]"] = match.group(2)[2:-1]
            else:  # アルファベットの単語
                tag_placeholder = f"[@{counter}@]"
                arraydata[f"[@{counter}@]"] = value

            data = data[:start + offset] + tag_placeholder + data[end + offset:]
            offset += len(tag_placeholder) - (end - start)
            counter += 1

        return {"data": data, "arraydata": arraydata}

    def appendArrVal(data, arraydata):
        for key, value in arraydata.items():
            data = data.replace(key, value)
        return data
    
    def exceptPattern(file_path):
        flag = False
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

        date_pattern = r'\d{4}-\d{2}-\d{2}'

        if any(file_path.endswith(ext) for ext in image_extensions):
            flag = True
        elif re.search(date_pattern, file_path):
            flag = True
#file_path が 2023-08-28もしくは数字のときもTrueにする処理を入れる
        
        return flag
    
    def removespace(data):
        # '@' の前後の半角スペースを除去
        data = re.sub(r' (?=@)', '', data)  # '@' の前の半角スペースを除去
        data = re.sub(r'(?<=@) ', '', data)  # '@' の後の半角スペースを除去
        data = re.sub(r' (?=\*)', '', data)
        # '<' の右側の半角スペースを除去
        data = re.sub(r'< ', '<', data)
        # '>' の左側の半角スペースを除去
        data = re.sub(r' >', '>', data)
        
        return data

class Handler:
    def __init__(self, name):
        self.name = name
        self.callback = None

    def define_callback(self, func):
        self.callback = func

    def execute_callback(self):
        if self.callback == None:
            return None
        #変数で定義したメソッドを実行
        return self.callback()