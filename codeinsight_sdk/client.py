import requests
import logging

from .handlers import ProjectHandler, ReportHandler
from .exceptions import CodeInsightError
from .experimental import ExperimentalHandler
from .handlers.inventory import InventoryHandler

logger = logging.getLogger(__name__)


class CodeInsightClient:
    """Client for the code insight API."""

    def __init__(
        self,
        base_url: str,
        api_token: str,
        timeout: int = 60,
        verify_ssl: bool = True,
        experimental: bool = False,
    ):
        self.base_url = base_url
        self.api_url = f"{base_url}/codeinsight/api"
        self.__api_token = api_token
        self.__api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__api_token}",
            "User-Agent": "codeinsight_sdk_python",
        }
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl
        self.experimental_enabled = experimental

    def request(
        self,
        method,
        url_part: str,
        params: dict = None,
        body: any = None,
        data: any = None,
        content_type: str = None,
    ):
        url = f"{self.api_url}/{url_part}"

        # Iterate over params and remove any that are None (Empty)
        if params:
            for k, v in list(params.items()):
                if v is None:
                    del params[k]

        # Update headers if content_type is specified
        headers = self.__api_headers
        if content_type:
            headers["Content-Type"] = content_type

        response = requests.request(
            method,
            url,
            headers=self.__api_headers,
            params=params,
            json=body,
            data=data,
            timeout=self.__timeout,
            verify=self.__verify_ssl,
        )

        if not response.ok:
            logger.error(
                f"Error: {response.status_code} - {response.reason}", exc_info=True
            )
            logger.error(response.text)
            raise CodeInsightError(response)

        return response

    @property
    def projects(self) -> ProjectHandler:
        return ProjectHandler(self)

    @property
    def reports(self) -> ReportHandler:
        return ReportHandler(self)

    @property
    def inventories(self):
        return InventoryHandler(self)

    @property
    def experimental(self) -> ExperimentalHandler:
        if self.experimental_enabled == False:
            raise CodeInsightError("Experimental API is not enabled for this instance")
        return ExperimentalHandler(self)

    @property
    def vulnerabilities(self):
        from .handlers import VulnerabilityHandler
        return VulnerabilityHandler(self)

    @property
    def users(self):
        from .handlers import UserHandler
        return UserHandler(self)

    @property
    def licenses(self):
        from .handlers import LicenseHandler
        return LicenseHandler(self)

    @property
    def tasks(self):
        from .handlers import TaskHandler
        return TaskHandler(self)

    @property
    def rules(self):
        from .handlers import RuleHandler
        return RuleHandler(self)

    @property
    def files(self):
        from .handlers import FileHandler
        return FileHandler(self)

    @property
    def folders(self):
        from .handlers import FolderHandler
        return FolderHandler(self)

    @property
    def jobs(self):
        from .handlers import JobHandler
        return JobHandler(self)

    @property
    def components(self):
        from .handlers import ComponentHandler
        return ComponentHandler(self)
