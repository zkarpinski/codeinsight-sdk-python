import pytest

from codeinsight_sdk import CodeInsightClient

class TestNotImplemented(object):

    @pytest.fixture
    def client(self):
        return CodeInsightClient("","")

    ## Coming soon features ##
    def test_inventories(self, client):
        with pytest.raises(NotImplementedError):
            client.inventories() != None
    
    def test_vulnerabilities(self, client):
        with pytest.raises(NotImplementedError):
            client.vulnerabilites() != None
    
    def test_users(self, client):
        with pytest.raises(NotImplementedError):
            client.users() != None
    
    def test_licenses(self, client):
        with pytest.raises(NotImplementedError):
            client.licenses() != None

    def test_tasks(self, client):
        with pytest.raises(NotImplementedError):
            client.tasks() != None

    def test_rules(self, client):
        with pytest.raises(NotImplementedError):
            client.rules() != None

    def test_reports(self, client):
        with pytest.raises(NotImplementedError):
            client.reports() != None

    def test_files(self, client):
        with pytest.raises(NotImplementedError):
            client.files() != None

    def test_folders(self, client):
        with pytest.raises(NotImplementedError):
            client.folders() != None