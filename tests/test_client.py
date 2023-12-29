import pytest
import logging

import requests_mock


from codeinsight_sdk import CodeInsightClient

logger = logging.getLogger(__name__)

## CHANGE ME ##
TEST_URL = "https://api.revenera.com"
TEST_API_TOKEN = "your_api_token"

class TestCodeInsightClient:
    @pytest.fixture
    def client(self):
        return CodeInsightClient(TEST_URL, TEST_API_TOKEN)
    
    def test_client(self, client):
        assert client.base_url == TEST_URL

    def test_endpoint_not_found(self, client):
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/projects", status_code=404)
            with pytest.raises(Exception):
                client.projects.all()
    
    
    def test_get_all_projects(self, client):
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/projects", text='{"data": [{"id":1, "name":"Test"}, {"id":2, "name":"Test 2"}]}')
            projects = client.projects.all()
        assert len(projects) > 0

    def test_get_project(self,client):
        projectName = "Test"
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/project/id", text='{ "Content": 1 }')
            project_id = client.projects.get_id(projectName)
        assert project_id == 1

    def test_get_project_inventory(self,client):
        project_id = 1
        fake_json = """
{ "projectId": 1, "inventoryItems": [
    {"itemNumber":1, "id":1234, "name":"Example component","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0"},
    {"itemNumber":2, "id":1235, "name":"Example component 2","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0"}
    ]}
"""
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/project/inventory/{project_id}",
                text=fake_json)
            projectInventory = client.project_inventory.get(project_id)
        print(projectInventory)
        assert projectInventory.projectId == project_id
        assert len(projectInventory.inventoryItems) >= 2
    

    ## Coming soon features ##
    def test_inventories(self, client):
        with pytest.raises(NotImplementedError):
            client.inventories() != None
    
    def test_vulnerabilities(self, client):
        with pytest.raises(NotImplementedError):
            client.vulnerabilites() != None
