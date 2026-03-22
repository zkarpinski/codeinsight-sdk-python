import pytest
import logging

from codeinsight_sdk import CodeInsightClient
from codeinsight_sdk.testing import codeinsight_mock

logger = logging.getLogger(__name__)

TEST_URL = "https://api.revenera.com"
TEST_API_TOKEN = "your_api_token"

@pytest.fixture
def client(codeinsight_mock):
    # The fixture starts the mock adapter automatically
    return CodeInsightClient(TEST_URL, TEST_API_TOKEN)

class TestVulnerabilityEndpoints:
    def test_get_vulnerability(self, client):
        vuln = client.vulnerabilities.get(1)
        assert vuln.vulnerabilityId == 1
        assert vuln.vulnerabilityName == "CVE-123"

class TestUserEndpoints:
    def test_get_all_users(self, client):
        users = client.users.all()
        assert len(users) == 1
        assert users[0].name == "Mock User 1"

    def test_get_user(self, client):
        user = client.users.get(1)
        assert user.id == 1
        assert user.name == "Mock User 1"

class TestLicenseEndpoints:
    def test_get_all_licenses(self, client):
        licenses = client.licenses.all()
        assert len(licenses) == 1
        assert licenses[0].name == "Mock License 1"

    def test_get_license(self, client):
        license = client.licenses.get(1)
        assert license.id == 1
        assert license.name == "Mock License 1"

class TestTaskEndpoints:
    def test_get_all_tasks(self, client):
        tasks = client.tasks.all()
        assert len(tasks) == 1
        assert tasks[0].name == "Mock Task 1"

    def test_get_task(self, client):
        task = client.tasks.get(1)
        assert task.id == 1
        assert task.name == "Mock Task 1"

class TestRuleEndpoints:
    def test_get_all_rules(self, client):
        rules = client.rules.all()
        assert len(rules) == 1
        assert rules[0].name == "Mock Rule 1"

    def test_get_rule(self, client):
        rule = client.rules.get(1)
        assert rule.id == 1
        assert rule.name == "Mock Rule 1"

class TestFileEndpoints:
    def test_get_file(self, client):
        file = client.files.get(1)
        assert file.id == 1
        assert file.name == "Mock File 1"

class TestFolderEndpoints:
    def test_get_folder(self, client):
        folder = client.folders.get(1)
        assert folder.id == 1
        assert folder.name == "Mock Folder 1"

class TestJobEndpoints:
    def test_get_all_jobs(self, client):
        jobs = client.jobs.all()
        assert len(jobs) == 1
        assert jobs[0].name == "Mock Job 1"

    def test_get_job(self, client):
        job = client.jobs.get(1)
        assert job.id == 1
        assert job.name == "Mock Job 1"

class TestComponentEndpoints:
    def test_get_all_components(self, client):
        components = client.components.all()
        assert len(components) == 1
        assert components[0].name == "Mock Component 1"

    def test_get_component(self, client):
        component = client.components.get(1)
        assert component.id == 1
        assert component.name == "Mock Component 1"
