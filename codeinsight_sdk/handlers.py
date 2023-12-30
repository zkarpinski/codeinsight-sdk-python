import abc
from typing import List

from codeinsight_sdk.models import Project, ProjectInventory, ProjectInventoryItem

class Handler(abc.ABC):
    def __init__(self, client, cls):
        self.client = client
        self.cls = cls
    
    @staticmethod
    def create(client, cls):
        k = cls.__name__
        handlers = {"Project": ProjectHandler, 
            }
        handler = handlers.get(k)
        return handler(client, cls)
    
    @abc.abstractmethod
    def get(self):
        pass

class ProjectHandler(Handler):
    #Note API endpoints switch between projects and project...
    def all(self) -> List[Project]:
        path = "projects"
        resp = self.client.request("GET", url_part=path)
        projects = []
        for project_data in resp.json()['data']:
            projects.append(self.cls.from_dict(project_data))
        return projects
    
    def get(self, id:str) -> Project:
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
                str: The ID of the project.
            """
            path = f"project/id"
            params = {"projectName": projectName}
            resp = self.client.request("GET", url_part=path, params=params)
            projectId = resp.json()['Content']
            return projectId
    
    def get_inventory_summary(self, project_id:int) -> List[ProjectInventoryItem]:
        path = f"projects/{project_id}/inventorySummary"
        resp = self.client.request("GET", url_part=path)
        inventory = []
        for inv_item in resp.json()['data']:
            inventory.append(ProjectInventoryItem.from_dict(inv_item))
        return inventory
    
    def get_inventory(self,project_id:int,
                      skip_vulnerabilities: bool = False,
                      published:bool = True,
                      ) -> ProjectInventory:
        path = f"project/inventory/{project_id}"
        params = {"skipVulnerabilities": skip_vulnerabilities}
        resp = self.client.request("GET", url_part=path, params=params)
        project_inventory = resp.json()
        project_cls = ProjectInventory.from_dict(project_inventory)
        return project_cls

