# coding=utf-8
import json
import os

import allure

from base.base_request import baseRequest
from util.handle_getexceldata import GetData
from util.handle_init import handle_ini


root_path = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(root_path, "../.."))
excel_case_dir = os.path.join(root_path, 'test_data', 'exceldata')

file_name = os.path.join(excel_case_dir, 'case1.xls')
sheet_id = 0


@allure.feature('测试Excel模块')
class TestMainExcel():
    @allure.title('测试标题')
    @allure.testcase('测试地址：https://www.imooc.com')
    def test_mainExcel(self):
        excel_data = GetData(file_name, sheet_id)
        rows_count = excel_data.get_case_lines()
        for i in range(1, rows_count):
            is_run = excel_data.get_is_run(i)
            if is_run:
                url = excel_data.get_request_url(i)
                method = excel_data.get_request_method(i)
                request_data = json.loads(excel_data.get_request_data(i))
                header = json.loads(handle_ini.get_value('headerDefault', 'header'))
                expect = excel_data.get_expcet_data(i)
                with allure.step('接口请求信息：'):
                    allure.attach(
                        '接口名：{},接口请求地址：{}，接口请求方式：{}，接口请求参数：{}'.format(excel_data.get_name(i), url, method,
                                                                      request_data))
                res = baseRequest.run_main(method, url, request_data, header)
                res_data = res.json()
                excel_data.write_result(i, json.dumps(res_data, ensure_ascii=False))
                try:
                    assert json.loads(expect) == res_data
                    excel_data.write_pass(i, 'PASS')
                except Exception as e:
                    excel_data.write_pass(i, 'NO')


TestMainExcel()
