import requests
import logging

from .handlers import Handler
from .models import Project, ProjectInventory

logger = logging.getLogger(__name__)

class CodeInsightClient:
    def __init__(self,
                 base_url: str,
                 api_token: str,
                 page_size: int = 100
                 ):
        self.base_url = base_url
        self.api_url = f"{base_url}/codeinsight/api"
        self.api_token = api_token
        self.page_size = page_size
        self.api_headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer %s" % self.api_token,
            "User-Agent": "codeinsight_sdk_python",
        }

    def request(self, method, url_part: str, params: dict = None):
        url = f"{self.api_url}/{url_part}"
        response = requests.request(method, url, headers=self.api_headers, params=params)

        if not response.ok:
            logger.error(f"Error: {response.status_code} - {response.reason}")
            logger.error(response.text)
            raise response.raise_for_status()      

        return response

    @property
    def projects(self) -> Handler:
        return Handler.create(self, Project)
    
    
    # Coming soon...?
    def inventories(self):
        raise NotImplementedError("Inventories are not yet implemented")
    
    def vulnerabilites(self):
        raise NotImplementedError
    
    def users(self):
        raise NotImplementedError
    
    def licenses(self):
        raise NotImplementedError
    
    def tasks(self):
        raise NotImplementedError
    
    def rules(self):
        raise NotImplementedError
    
    def reports(self):
        raise NotImplementedError
    
    def files(self):
        raise NotImplementedError
    
    def folders(self):
        raise NotImplementedError
    
    def jobs(self):
        raise NotImplementedError
    
    def components(self):
        raise NotImplementedError

