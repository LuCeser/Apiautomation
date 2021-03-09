# coding:utf-8
import os

curPath = os.path.abspath(os.path.dirname(__file__))


class comparators():
    def assertEqual(self, result, check, expect):
        result_data = result.json()
        if check == 'status_code':
            assert str(result.status_code) == expect
        else:
            assert result_data[check] == expect

    def comparators_Assert(self, result, check, comparator, expect):
        if (comparator in ["eq", "equals", "equal"]):
            self.assertEqual(result, check, expect)


comparatorsTest = comparators()
