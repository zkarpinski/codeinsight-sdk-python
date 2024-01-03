import pytest

from codeinsight_sdk import CodeInsightClient

class TestNotImplemented(object):

    @pytest.fixture
    def client(self):
        return CodeInsightClient("","")

    ## Coming soon features ##
    def test_inventories(self, client):
        with pytest.raises(NotImplementedError):
            client.inventories()
    
    def test_vulnerabilities(self, client):
        with pytest.raises(NotImplementedError):
            client.vulnerabilites()
    
    def test_users(self, client):
        with pytest.raises(NotImplementedError):
            client.users()
    
    def test_licenses(self, client):
        with pytest.raises(NotImplementedError):
            client.licenses()

    def test_tasks(self, client):
        with pytest.raises(NotImplementedError):
            client.tasks()

    def test_rules(self, client):
        with pytest.raises(NotImplementedError):
            client.rules()

    def test_files(self, client):
        with pytest.raises(NotImplementedError):
            client.files()

    def test_folders(self, client):
        with pytest.raises(NotImplementedError):
            client.folders()