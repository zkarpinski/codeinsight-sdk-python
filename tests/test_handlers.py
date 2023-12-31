import pytest

from codeinsight_sdk import CodeInsightClient
from codeinsight_sdk.handlers import *
from codeinsight_sdk.models import *

class TestHandlers(object):
    @pytest.fixture
    def client(self):
        return CodeInsightClient("","")
    
    def test_bad_handler(self, client):
        with pytest.raises(Exception):
            Handler.create(client, "BadClass")
    
    def test_project_handler(self, client):
        project_handler = Handler.create(client, Project)
        assert isinstance(project_handler, ProjectHandler)
        assert issubclass(ProjectHandler, Handler)