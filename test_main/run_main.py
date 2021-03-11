# coding:utf-8
import os

import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
BasePath = curPath[:curPath.find("Apiautomation/") + len("Apiautomation/")]

if __name__ == "__main__":
    pytest.main(['-s', '-v', 'test_case/testRequest/test_contractTest.py', '-q', '--alluredir', 'reports'])
