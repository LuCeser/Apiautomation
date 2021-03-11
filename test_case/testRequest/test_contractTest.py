# coding:utf-8

import allure
from pactverify.matchers import Like, PactVerify

from util.handle_apirequest import apiRequest
from util.handle_comparators import comparatorsTest
from util.handle_log import run_log as logger


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

        for case_data in test_cases:
            self.request_one(base_url, case_config, case_data)
