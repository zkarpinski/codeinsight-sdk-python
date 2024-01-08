import pytest

from codeinsight_sdk import CodeInsightClient
from codeinsight_sdk.handlers import Handler, ProjectHandler, ReportHandler
from codeinsight_sdk.models import Project, Report


class TestHandlers(object):
    @pytest.fixture
    def client(self):
        return CodeInsightClient("","")
    
    def test_bad_handler(self, client):
        with pytest.raises(Exception):
            Handler.create(client)
    
    def test_project_handler(self, client):
        project_handler = Handler.create(client, Project)
        assert isinstance(project_handler, ProjectHandler)
        assert issubclass(ProjectHandler, Handler)
    
    def test_report_handler(self, client):
        _handler = Handler.create(client, Report)
        assert isinstance(_handler, ReportHandler)
        assert issubclass(ReportHandler, Handler)