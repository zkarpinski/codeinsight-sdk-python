import pytest
import logging

import requests_mock


from codeinsight_sdk import CodeInsightClient

logger = logging.getLogger(__name__)

## CHANGE ME ##
TEST_URL = "https://api.revenera.com"
TEST_API_TOKEN = "your_api_token"


class TestExperimental:
    @pytest.fixture
    def client(self):
        return CodeInsightClient(TEST_URL, TEST_API_TOKEN, experimental=True)

    def test_experimental_enabled(self, client):
        assert client.experimental_enabled == True

    def test_get_project_vulnerabilities(self, client):
        project_id = 1
        total_pages = 1
        total_records = total_pages * 3
        response_header = {"content-type": "application/json"}
        response_header["current-page"] = "1"
        response_header["number-of-pages"] = str(total_pages)
        response_header["total-records"] = str(total_records)
        fake_response_json = """
        { "projectId": 1, "inventoryItems": [
            {"itemNumber":1, "id":1234, "name":"Example component","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0","vulnerabilities": [ { 
            "vulnerabilityId":123456,
            "vulnerabilityName":"CVE-123-45678",
            "vulnerabilityDescription":"Insecure library! Watch out.",
            "vulnerabilityCvssV3Score": 3.3,
            "vulnerabilityCvssV3Severity":"LOW"},
            { 
            "vulnerabilityId":123457,
            "vulnerabilityName":"CVE-987-65432",
            "vulnerabilityDescription":"Insecure library 2! Watch out.",
            "vulnerabilityCvssV3Score": 9,
            "vulnerabilityCvssV3Severity":"CRITICAL"} ] },
            {"itemNumber":2, "id":1235, "name":"Example component 2","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0"},
            {"itemNumber":3, "id":1235, "name":"Example component 3","type":"component","priority":"low","createdBy":"Zach","createdOn":"Today","updatedOn":"Tomorrow","componentName":"snakeyaml","componentVersionName":"2.0","vulnerabilities":[]}
            ]}
        """

        with requests_mock.Mocker() as m:
            m.get(
                f"{TEST_URL}/codeinsight/api/project/inventory/{project_id}",
                text=fake_response_json,
                headers=response_header,
            )
            vulnerable_items = client.experimental.get_project_vulnerabilities(
                project_id
            )
        assert len(vulnerable_items) == 1
        assert vulnerable_items[0].vulnerabilities is not None
        assert (
            vulnerable_items[0].vulnerabilities[1].vulnerabilityName == "CVE-987-65432"
        )
