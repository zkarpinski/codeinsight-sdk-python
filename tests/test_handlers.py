import pytest

from codeinsight_sdk import CodeInsightClient
from codeinsight_sdk.handlers import ProjectHandler, ReportHandler
from codeinsight_sdk.models import Project, Report


class TestHandlers(object):
    @pytest.fixture
    def client(self):
        return CodeInsightClient("","")
