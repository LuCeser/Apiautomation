# coding=utf-8
import os

import yaml

curPath = os.path.abspath(os.path.dirname(__file__))


class HandleYaml:
    # 读取yaml文件
    @staticmethod
    def load_yaml(file_name):
        if file_name is None:
            file_path = ""
        else:
            file_path = file_name
        try:
            with open(file_path, encoding='UTF-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            return data
        except Exception:
            print("未找到yaml文件")
            return {}

    # 读取yaml文件里具体的字段值
    def getYaml_Data(self, file_name):
        if file_name is None:
            return ""
        yaml_data = self.load_yaml(file_name)
        return yaml_data


handle_YamlData = HandleYaml()
