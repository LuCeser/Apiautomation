# coding:utf-8
import ast

import allure
from pactverify.matchers import Like, PactVerify

from commons import common
from util.handle_apirequest import apiRequest
from util.handle_comparators import comparatorsTest
from util.handle_log import run_log as logger

rule = r'<(.*?)>'  # 正则规则

code_prefix = '@@'
func_prefix = '>>'


def execute(code):
    """
    执行文件中嵌入的代码
    :param code: 代码文本
    :return: 执行结果
    """
    block = ast.parse(code, mode='exec')
    last = ast.Expression(block.body.pop().value)
    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode='exec'), _globals, _locals)
    return eval(compile(last, '<string>', mode='eval'), _globals, _locals)


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

    def test_caseSuits(self, base_url, case_suit):
        """
        执行测试用例集合
        一次执行的是一个测试用例文件中的内容
        :param base_url:
        :param case_suit: 一个测试用例json文件中的内容
        :return:
        """

        test_cases = case_suit['testCase']
        case_config = case_suit['config']
        dependencies = case_suit['dependencies']

        self.update_dict(case_suit, dependencies)

        for case_data in test_cases:
            self.request_one(base_url, case_config, case_data)

    def update_dict(self, data, dependencies):

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) or isinstance(value, list):
                    self.update_dict(value, dependencies)
                else:
                    if isinstance(value, str) and value.startswith(code_prefix):
                        value = execute(value.strip(code_prefix).strip())
                        data[key] = value
                    elif isinstance(value, str) and value.startswith(func_prefix):
                        func_name = value.strip(func_prefix).strip()
                        for dependency in dependencies:
                            if dependency['name'] == func_name:
                                dependency_func = getattr(common, func_name)
                                data[key] = dependency_func(**dependency['params'])

        elif isinstance(data, list):
            for value in data:
                if isinstance(value, dict) or isinstance(value, list):
                    self.update_dict(value, dependencies)
                else:
                    if isinstance(value, str) and value.startswith(code_prefix):
                        value = execute(value.strip(code_prefix).strip())
