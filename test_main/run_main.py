# coding:utf-8
import os
import sys

import pytest

sys.path.append('../')
sys.path.append('/Users/zhanglu/workspace/Apiautomation')
curPath = os.path.abspath(os.path.dirname(__file__))
BasePath = curPath[:curPath.find("Apiautomation/") + len("Apiautomation/")]

if __name__ == "__main__":
    pytest.main(['-s', '-v', 'test_case/testRequest/', '-q', '--alluredir', 'reports'])
