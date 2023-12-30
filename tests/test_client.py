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

    def test_get_project_id(self,client):
        projectName = "Test"
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/project/id", text='{ "Content": 1 }')
            project_id = client.projects.get_id(projectName)
        assert project_id == 1
    
    def test_get_project(self,client):
        project_id = 1
        fake_response_json = """ { "data": {
            "id": 1,
            "name": "Test",
            "description": "Test project",
            "createdBy": "Zach",
            "createdOn": "Today",
            "updatedOn": "Tomorrow",
            "projectType": "maven",
            "projectUrl": "",
            "vulnerabilities": {
                "CvssV2": {
                    "High": 2,
                    "Medium": 2,
                    "Low": 3,
                    "Unknown": 4
                },
                "CvssV3": {
                    "Critical": 1,
                    "High": 1,
                    "Medium": 2,
                    "Low": 6,
                    "Unknown": 1
                }
            }
        }}
        """
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/projects/{project_id}", text=fake_response_json)
            project = client.projects.get(project_id)
        assert project.id == 1
        assert project.name == "Test"
        assert project.vulnerabilities["CvssV3"]["Critical"] == 1
        assert project.vulnerabilities["CvssV3"]["High"] == 1
        assert project.vulnerabilities["CvssV2"]["High"] == 2
        assert project.vulnerabilities["CvssV2"]["Unknown"] == 4

    def test_get_project_inventory(self,client):
        project_id = 1
        fake_response_json = """
{ "projectId": 1, "inventoryItems": [
    {"itemNumber":1, "id":1234, "name":"Example component","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0"},
    {"itemNumber":2, "id":1235, "name":"Example component 2","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0"}
    ]}
"""
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/project/inventory/{project_id}",
                text=fake_response_json)
            projectInventory = client.projects.get_inventory(project_id)
        assert projectInventory.projectId == project_id
        assert len(projectInventory.inventoryItems) >= 2

    #### FIX THIS! ####
    def test_get_project_inventory_summary(self,client):
        project_id = 1
        fake_response_json = """ { "data": [
            {
                "itemNumber": 1,
                "id": 12345,
                "name": "Inventory Item 1",
                "type":"component",
                "priority":"low",
                "createdBy":"Zach",
                "createdOn":"Today",
                "updatedOn":"Tomorrow",
                "componentName":"snakeyaml",
                "componentVersionName":"2.0"
            },
            {
                "itemNumber": 2,
                "id": 12346,
                "name": "Inventory Item 2",
                "type":"component",
                "priority":"low",
                "createdBy":"Zach",
                "createdOn":"Today",
                "updatedOn":"Tomorrow",
                "componentName":"snakeyaml",
                "componentVersionName":"2.0"
            }
            ]
    
        }
        """
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/projects/{project_id}/inventorySummary",
                text=fake_response_json)
            project_inventory_summary = client.projects.get_inventory_summary(project_id)

        assert len(project_inventory_summary) == 2
        assert project_inventory_summary[1].id == 12346

