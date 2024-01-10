import pytest
import logging

import requests_mock


from codeinsight_sdk import CodeInsightClient
from codeinsight_sdk.exceptions import CodeInsightError

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

class TestProjectEndpoints:
    @pytest.fixture
    def client(self):
        return CodeInsightClient(TEST_URL, TEST_API_TOKEN)
    
    def test_create_project(self, client):
        project_name = "Test"
        with requests_mock.Mocker() as m:
            m.post(f"{TEST_URL}/codeinsight/api/projects", text='{"data": {"id":1}}')
            project_id = client.projects.create(project_name)
        assert project_id == 1
   
    def test_get_all_projects(self, client):
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/projects", text='{"data": [{"id":1, "name":"Test"}, {"id":2, "name":"Test 2"}]}')
            projects = client.projects.all()
        assert len(projects) > 0

    def test_get_project_id(self, client):
        project_name = "Test"
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/project/id", text='{ "Content: ": 1 }') # Yes, the key is called 'Content: ' ...
            project_id = client.projects.get_id(project_name)
        assert project_id == 1

    def test_get_project_id_invalid(self,client):
        project_name = "Invalid_Project"
        fake_response_json = """{ "Arguments: " : ["",""],
            "Key: ": " InvalidProjectNameParm",
            "Error: ": "The project name entered was not found" }
        """
        with requests_mock.Mocker() as m:
            # Note, the key names end with a colon and space '...: ' 
            m.get(f"{TEST_URL}/codeinsight/api/project/id", text=fake_response_json, status_code=400)
            with pytest.raises(CodeInsightError):
                client.projects.get_id(project_name)
    
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

    def test_get_project_inventory_multipage(self,client):
        project_id = 1
        total_pages = 4
        total_records = total_pages * 2
        response_header = {"content-type": "application/json"}
        response_header["current-page"] = "1"
        response_header["number-of-pages"] = str(total_pages)
        response_header["total-records"] = str(total_records)

        fake_response_json = """
        { "projectId": 1, "inventoryItems": [
            {"itemNumber":1, "id":1234, "name":"Example component","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0","vulnerabilities":[{"vulnerabilityId":1,"vulnerabilityName":"CVE-2020-1234","vulnerabilityDescription":"Example vulnerability","vulnerabilityCvssV3Score":9.8,"vulnerabilityCvssV3Severity":"Critical"}]},
            {"itemNumber":2, "id":1235, "name":"Example component 2","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0"}
            ]}
        """
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/project/inventory/{project_id}",
                text=fake_response_json, headers=response_header)
            project_inventory = client.projects.get_inventory(project_id)
        assert project_inventory.projectId == project_id
        assert len(project_inventory.inventoryItems) == total_records
        assert project_inventory.inventoryItems[0].vulnerabilities[0].vulnerabilityName == "CVE-2020-1234"
    
    def test_upload_codebase(self,client):
        project_id = 1
        codebase_path = "tests/resources/test_codebase.zip"
        with requests_mock.Mocker() as m:
            m.post(f"{TEST_URL}/codeinsight/api/project/uploadProjectCodebase", text='{"data": {"id":1}}')
            resp = client.projects.upload_codebase(project_id, codebase_path)
        assert resp == 200

    #### FIX THIS! ####
    def test_get_project_inventory_summary(self,client):
        project_id = 1
        total_pages = 4
        total_records = total_pages * 2
        response_header = {"content-type": "application/json"}
        response_header["current-page"] = "1"
        response_header["number-of-pages"] = str(total_pages)
        response_header["total-records"] = str(total_records)
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
                text=fake_response_json, headers=response_header)
            project_inventory_summary = client.projects.get_inventory_summary(project_id)

        assert len(project_inventory_summary) == 8
        assert project_inventory_summary[1].id == 12346


class TestReportsEndpoints:
    @pytest.fixture
    def client(self):
        return CodeInsightClient(TEST_URL, TEST_API_TOKEN)
    
    def test_get_reports_all(self,client):
        fake_response_json = """ { "data": [
            {
                "id": 1,
                "name": "Report 1",
                "path": "path/to/report",
                "default": true,
                "enabled": true,
                "enableProjectPicker": true,
                "order": 1,
                "createdDateTime": "Today",
                "updatedDateTime": "Tomorrow"
            },
            {
                "id": 2,
                "name": "Report 2",
                "path": "path/to/report",
                "default": false,
                "enabled": false,
                "enableProjectPicker": false,
                "order": 2,
                "createdDateTime": "Today",
                "updatedDateTime": "Tomorrow"
            }
            ]
    
        }
        """
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/reports",
                text=fake_response_json)
            reports = client.reports.all()
        assert len(reports) == 2
        assert reports[1].id == 2
        assert reports[1].enabled == False

    def test_get_report(self,client):
        report_id = 1
        fake_response_json = """ { "data":
            {
                "id": 1,
                "name": "Report 1",
                "path": "path/to/report",
                "default": true,
                "enabled": true,
                "enableProjectPicker": true,
                "order": 1,
                "createdDateTime": "Today",
                "updatedDateTime": "Tomorrow"
            }
        }
        """
        with requests_mock.Mocker() as m:
            m.get(f"{TEST_URL}/codeinsight/api/reports/{report_id}",
                text=fake_response_json)
            report = client.reports.get(1)
        assert report.id == 1
        assert report.enabled == True