import abc
from typing import List

from codeinsight_sdk.models import Project, ProjectInventory, ProjectInventoryItem
from codeinsight_sdk.exceptions import CodeInsightError

class Handler(abc.ABC):
    def __init__(self, client, cls):
        self.client = client
        self.cls = cls
    
    @staticmethod
    def create(client, cls):
        k = cls.__name__
        handlers = {"Project": ProjectHandler,
                    "Report": ReportHandler
            }
        handler = handlers.get(k)
        if handler is None:
            raise Exception(f"Handler not found for class '{k}'")
        return handler(client, cls)
    
    @abc.abstractmethod
    def get(self):
        pass

class ProjectHandler(Handler):
    #Note API endpoints switch between projects and project...
    def all(self) -> List[Project]:
            """
            Retrieves all projects from the server.

            Returns:
                A list of Project objects representing all the projects.
            """
        
            path = "projects"
            resp = self.client.request("GET", url_part=path)
            projects = []
            for project_data in resp.json()['data']:
                projects.append(self.cls.from_dict(project_data))
            return projects
    
    def get(self, id:int) -> Project:
            """
            Retrieves a project by its ID.

            Args:
                id (int): The ID of the project requested.

            Returns:
                Project: The retrieved project.
            """
            path = f"projects/{id}"
            resp = self.client.request("GET", url_part=path)
            project_data = resp.json()['data']
            return self.cls.from_dict(project_data)
    
    def get_id(self, projectName:str) -> int:
            """
            Retrieves the ID of a project based on its name.

            Args:
                projectName (str): The name of the project.

            Returns:
                int: The ID of the project.
            """
            path = f"project/id"
            params = {"projectName": projectName}
            resp = self.client.request("GET", url_part=path, params=params)
            try:
                projectId = resp.json()['Content: '] # Yes, the key is called 'Content: ' ...
            except KeyError:
                raise CodeInsightError(resp)
                #raise Exception(f"Content key not found in response: {resp.json()}")
            return projectId
    
    def get_inventory_summary(self, project_id:int) -> List[ProjectInventoryItem]:
            """
            Retrieves the inventory summary for a specific project.

            Args:
                project_id (int): The ID of the project.

            Returns:
                List[ProjectInventoryItem]: A list of ProjectInventoryItem objects representing the inventory summary.
            """
            
            path = f"projects/{project_id}/inventorySummary"
            resp = self.client.request("GET", url_part=path)
            inventory = []
            for inv_item in resp.json()['data']:
                inventory.append(ProjectInventoryItem.from_dict(inv_item))
            return inventory
    
    def get_inventory(self,project_id:int,
                      skip_vulnerabilities: bool = False,
                      published:bool = True,
                      vendor:str = None,
                      product:str = None,
                      page_size: int = 100,
                      page: int = 1,
                      review_status: str = None,
                      alerts: str = None,
                      include_files: bool = True
                      ) -> ProjectInventory:
        path = f"project/inventory/{project_id}"
        #TODO: Add support for all parameters
        params = {"skipVulnerabilities": skip_vulnerabilities}
        resp = self.client.request("GET", url_part=path, params=params)
        project_inventory = resp.json()
        project_cls = ProjectInventory.from_dict(project_inventory)
        return project_cls


class ReportHandler(Handler):
    def get(self, id:int):
        path = f"reports/{id}"
        resp = self.client.request("GET", url_part=path)
        report_data = resp.json()['data']
        report = self.cls.from_dict(report_data)
        return report
    
    def all(self):
        path = "reports"
        resp = self.client.request("GET", url_part=path)
        reports = []
        for report_data in resp.json()['data']:
            reports.append(self.cls.from_dict(report_data))
        return reports
         
