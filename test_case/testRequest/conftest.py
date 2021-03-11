#!/usr/bin/env python
# encoding: utf-8
"""
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- WellCloud                           
#-------------------------------------------------------------------
#                                                                   
#                   @Project Name : Apiautomation                 
#                                                                   
#                   @File Name    : conftest.py                      
#                                                                   
#                   @Programmer   : zhanglu                          
#                                                                     
#                   @Start Date   : 2021/3/11 09:53                 
#                                                                   
#                   @Last Update  : 2021/3/11 09:53                 
#                   
#                   @Description  : 
#                                                                   
#-------------------------------------------------------------------
# Classes:                                                          
#                                                                   
#-------------------------------------------------------------------
"""
import os
import sys

import pytest

from commons import common
from util.handle_init import handle_ini
from util.handle_json import handle_jsonData

curPath = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.abspath(os.path.dirname(curPath) + os.path.sep + "../")
sys.path.append(root_path)
os.chdir(root_path)

# 使用os.path.join()拼接路径，避免不同操作系统路径符不同的问题
case_data_dir = os.path.join(root_path, 'test_data', 'jsondata', 'testRequest')
# 保存测试用例文件路径

testCaseData = []  # 一个元素就是一个文件


def load_test_cases():
    """
    扫描并加载数据文件夹下所有数据
    :return:
    """
    test_cases_dirs = []
    for top_dir, dirs, files in os.walk(case_data_dir):
        # logger.info("{} 下共有 {} 个测试文件", top_dir, len(files))
        for file in files:
            if file.endswith(".json"):
                test_data_file = os.path.join(top_dir, file)
                test_cases_dirs.append(test_data_file)
                testCaseData.append(handle_jsonData.load_json(test_data_file))
    return test_cases_dirs


load_test_cases()


def parser_base_url(node_ip, module_name):
    module_port = handle_ini.get_value(module_name, 'module')
    return 'http://%s:%s' % (node_ip, module_port)


@pytest.fixture
def base_url(get_node_ip, case_suit):
    print(">>> 生成URL")
    return parser_base_url(get_node_ip, case_suit['config']['module'])


@pytest.fixture(autouse=True)
def load_func(case_suit):
    try:
        for dependency in case_suit['dependencies']:
            print('需要处理的依赖:', dependency)
            # TODO 需要处理异常情况
            dependency_func = getattr(common, dependency['name'])
            dependency_func(**dependency['params'])
    except Exception:
        print("执行依赖函数失败")


@pytest.fixture(params=testCaseData)
def case_suit(request):
    """
    参数化fixture，将数据拉取放到前置
    :param request: 上下文信息
    :return: 用例
    """
    return request.param
