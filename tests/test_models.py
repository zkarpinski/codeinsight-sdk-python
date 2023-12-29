import pytest

from codeinsight_sdk.models import Project

class TestProject(object):
    @pytest.fixture
    def project(self):
        return Project(id=1, name="Test")
    
    def test_project(self, project):
        assert project.id == 1
        assert project.name == "Test"
