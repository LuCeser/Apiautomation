# coding:utf-8
import os
import sys

import allure
import pytest
from pactverify.matchers import Like, PactVerify

from util.handle_apirequest import apiRequest
from util.handle_comparators import comparatorsTest
from util.handle_init import handle_ini
from util.handle_json import handle_jsonData
from util.handle_log import run_log as logger

curPath = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.abspath(os.path.dirname(curPath) + os.path.sep + "../")
sys.path.append(root_path)
os.chdir(root_path)

node_ip = handle_ini.get_value('node', 'environment')

# 使用os.path.join()拼接路径，避免不同操作系统路径符不同的问题
case_data_dir = os.path.join(root_path, 'test_data', 'jsondata', 'testRequest')
testCaseData = []

logger.info('扫描{}下测试文件', case_data_dir)
for top_dir, dirs, files in os.walk(case_data_dir):
    logger.info("{} 下共有 {} 个测试文件", top_dir, len(files))
    for file in files:
        if file.endswith(".json"):
            test_data_file = os.path.join(top_dir, file)
            testCaseData.append(handle_jsonData.load_json(test_data_file))


@allure.feature('契约测试')
class TestRequestOne:

    @staticmethod
    def request_one(base_url, case_config, test_case):
        try:
            api_response = apiRequest.api_request(base_url, case_config, test_case)
            # pactverity——全量契约校验
            config_contract_format = Like({
                "error": 0,
                "msg": 'success',
                "lan": 'en'
            })
            mPactVerify = PactVerify(config_contract_format)
            try:
                mPactVerify.verify(api_response.json())
                logger.info(
                    'verify_result：{}，verify_info:{}'.format(mPactVerify.verify_result, mPactVerify.verify_info))
                assert mPactVerify.verify_result is True
            except Exception as e:
                logger.exception(
                    '测试用例契约校验失败，verify_result：{}，verify_info:{}，exception:{}'.format(mPactVerify.verify_result,
                                                                                     mPactVerify.verify_info, e))
            try:
                for case_validate in test_case['validate']:
                    logger.info('断言期望相关参数：check：{},comparator：{},expect：{}'.format(case_validate['check'],
                                                                                   case_validate['comparator'],
                                                                                   case_validate['expect']))
                    comparatorsTest.comparators_Assert(api_response, case_validate['check'],
                                                       case_validate['comparator'], case_validate['expect'])
                    logger.info('测试用例断言成功')
            except Exception as e:
                logger.exception('测试用例断言失败')
        except Exception as e:
            logger.exception('测试用例请求失败，{}'.format(e))

    @pytest.mark.parametrize('case_suit', testCaseData)
    def test_caseSuit(self, case_suit):

        # allure.title(case['config']['name'])

        test_cases = case_suit['testCase']
        case_config = case_suit['config']

        base_url = self.parser_base_url(case_config['module'])
        for case_data in test_cases:
            self.request_one(base_url, case_config, case_data)

    @staticmethod
    def parser_base_url(module_name):
        module_port = handle_ini.get_value(module_name, 'module')
        return 'http://%s:%s' % (node_ip, module_port)
