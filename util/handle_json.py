# coding=utf-8
import json
import os

curPath = os.path.abspath(os.path.dirname(__file__))


class HandleJson:
    # 读取json文件
    @staticmethod
    def load_json(file_name):
        if file_name is None:
            file_path = ""
        else:
            file_path = file_name
        try:
            with open(file_path, encoding='UTF-8') as f:
                data = json.load(f)
            return data
        except Exception:
            print("未找到json文件")
            return {}

    # 读取json文件里具体的字段值
    def getJson_value(self, key, file_name):
        if file_name is None:
            return ""
        json_data = self.load_json(file_name)
        if key is None:
            json_value = ""
        else:
            json_value = json_data.get(key)
        return json_value


handle_jsonData = HandleJson()
