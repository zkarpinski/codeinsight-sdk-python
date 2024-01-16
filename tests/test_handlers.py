import pytest

from codeinsight_sdk import CodeInsightClient


class TestHandlers(object):
    @pytest.fixture
    def client(self):
        return CodeInsightClient("", "")
