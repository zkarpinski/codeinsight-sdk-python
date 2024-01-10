import requests
import logging

from .handlers import ProjectHandler, ReportHandler
from .exceptions import CodeInsightError

logger = logging.getLogger(__name__)

class CodeInsightClient:
    def __init__(self,
                 base_url: str,
                 api_token: str,
                 timeout: int = 60,
                 verify_ssl: bool = True
                 ):
        self.base_url = base_url
        self.api_url = f"{base_url}/codeinsight/api"
        self.__api_token = api_token
        self.__api_headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer %s" % self.__api_token,
            "User-Agent": "codeinsight_sdk_python",
        }
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl

    def request(self, method, url_part: str, params: dict = None, body: any = None, data: any = None, content_type: str = None):
        url = f"{self.api_url}/{url_part}"

        # Iterate over params and remove any that are None (Empty)
        if(params):
            for k, v in list(params.items()):
                if v is None:
                    del params[k]

        # Update headers if content_type is specified
        headers = self.__api_headers
        if content_type:
            headers['Content-Type'] = content_type

        response = requests.request(method, url,
                                     headers=self.__api_headers, params=params, json=body, data=data,
                                     timeout=self.__timeout, verify=self.__verify_ssl)

        if not response.ok:
            logger.error(f"Error: {response.status_code} - {response.reason}", exc_info=True)
            logger.error(response.text)
            raise CodeInsightError(response)   

        return response

    @property
    def projects(self) -> ProjectHandler:
        return ProjectHandler(self)
    
    @property
    def reports(self) -> ReportHandler:
        return ReportHandler(self)
    
    
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
    
    def files(self):
        raise NotImplementedError
    
    def folders(self):
        raise NotImplementedError
    
    def jobs(self):
        raise NotImplementedError
    
    def components(self):
        raise NotImplementedError

