import pytest
import requests_mock

from codeinsight_sdk import CodeInsightClient


class CodeInsightMockAdapter:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_url = f"{base_url}/codeinsight/api"
        self.mocker = requests_mock.Mocker()

    def start(self):
        self.mocker.start()
        self._setup_mocks()

    def stop(self):
        self.mocker.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _setup_mocks(self):
        # Projects
        self.mocker.get(
            f"{self.api_url}/projects",
            json={"data": [{"id": 1, "name": "Mock Project 1"}]},
        )
        self.mocker.post(f"{self.api_url}/projects", json={"data": {"id": 1}})
        self.mocker.get(
            f"{self.api_url}/projects/1",
            json={"data": {"id": 1, "name": "Mock Project 1"}},
        )
        self.mocker.get(f"{self.api_url}/project/id", json={"Content: ": 1})
        self.mocker.get(
            f"{self.api_url}/project/inventory/1",
            json={
                "projectId": 1,
                "inventoryItems": [{"itemNumber": 1, "id": 1, "name": "Mock Item 1"}],
            },
            headers={"number-of-pages": "1"},
        )

        # Reports
        self.mocker.get(
            f"{self.api_url}/reports",
            json={
                "data": [
                    {
                        "id": 1,
                        "name": "Mock Report 1",
                        "path": "path",
                        "default": True,
                        "enabled": True,
                        "enableProjectPicker": True,
                        "order": 1,
                        "createdDateTime": "today",
                        "updatedDateTime": "today",
                    }
                ]
            },
        )
        self.mocker.get(
            f"{self.api_url}/reports/1",
            json={
                "data": {
                    "id": 1,
                    "name": "Mock Report 1",
                    "path": "path",
                    "default": True,
                    "enabled": True,
                    "enableProjectPicker": True,
                    "order": 1,
                    "createdDateTime": "today",
                    "updatedDateTime": "today",
                }
            },
        )

        # Vulnerabilities
        self.mocker.get(
            f"{self.api_url}/vulnerabilities/1",
            json={
                "data": {
                    "vulnerabilityId": 1,
                    "vulnerabilityName": "CVE-123",
                    "vulnerabilityDescription": "Desc",
                    "vulnerabilityCvssV3Score": "9.8",
                    "vulnerabilityCvssV3Severity": "Critical",
                }
            },
        )

        # Users
        self.mocker.get(
            f"{self.api_url}/users", json={"data": [{"id": 1, "name": "Mock User 1"}]}
        )
        self.mocker.get(
            f"{self.api_url}/users/1", json={"data": {"id": 1, "name": "Mock User 1"}}
        )

        # Licenses
        self.mocker.get(
            f"{self.api_url}/licenses",
            json={"data": [{"id": 1, "name": "Mock License 1"}]},
        )
        self.mocker.get(
            f"{self.api_url}/licenses/1",
            json={"data": {"id": 1, "name": "Mock License 1"}},
        )

        # Tasks
        self.mocker.get(
            f"{self.api_url}/tasks", json={"data": [{"id": 1, "name": "Mock Task 1"}]}
        )
        self.mocker.get(
            f"{self.api_url}/tasks/1", json={"data": {"id": 1, "name": "Mock Task 1"}}
        )

        # Rules
        self.mocker.get(
            f"{self.api_url}/rules", json={"data": [{"id": 1, "name": "Mock Rule 1"}]}
        )
        self.mocker.get(
            f"{self.api_url}/rules/1", json={"data": {"id": 1, "name": "Mock Rule 1"}}
        )

        # Files
        self.mocker.get(
            f"{self.api_url}/files/1", json={"data": {"id": 1, "name": "Mock File 1"}}
        )

        # Folders
        self.mocker.get(
            f"{self.api_url}/folders/1",
            json={"data": {"id": 1, "name": "Mock Folder 1"}},
        )

        # Jobs
        self.mocker.get(
            f"{self.api_url}/jobs", json={"data": [{"id": 1, "name": "Mock Job 1"}]}
        )
        self.mocker.get(
            f"{self.api_url}/jobs/1", json={"data": {"id": 1, "name": "Mock Job 1"}}
        )

        # Components
        self.mocker.get(
            f"{self.api_url}/components",
            json={"data": [{"id": 1, "name": "Mock Component 1"}]},
        )
        self.mocker.get(
            f"{self.api_url}/components/1",
            json={"data": {"id": 1, "name": "Mock Component 1"}},
        )


@pytest.fixture
def codeinsight_mock(request):
    # This fixture allows users to use `codeinsight_mock` in their tests
    base_url = getattr(request.module, "TEST_URL", "https://api.revenera.com")
    with CodeInsightMockAdapter(base_url) as adapter:
        yield adapter


def mock_client(base_url="https://api.revenera.com"):
    # Convenience context manager for inline use
    return CodeInsightMockAdapter(base_url)
