import pytest

from codeinsight_sdk.models import Project, Report

class TestProject(object):
    @pytest.fixture
    def project(self):
        return Project(id=1, name="Test")
    
    def test_project(self, project):
        assert project.id == 1
        assert project.name == "Test"
    

@pytest.mark.skip(reason="Not implemented")
class TestReport(object):
    @pytest.fixture
    def report(self):
        return Report(id=1)
    
    def test_report(self, report):
        assert report.id == 1
