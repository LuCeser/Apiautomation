import os

import pytest

from util.handle_init import handle_ini

cur_path = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def get_node_ip():
    return handle_ini.get_value('node', 'environment')
