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
            raise ValueError(f"Handler not found for class '{k}'")
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
    
    def get_id(self, project_name:str) -> int:
            """
            Retrieves the ID of a project based on its name.

            Args:
                projectName (str): The name of the project.

            Returns:
                int: The ID of the project.
            """
            path = "project/id"
            params = {"projectName": project_name}
            resp = self.client.request("GET", url_part=path, params=params)
            try:
                project_id = resp.json()['Content: '] # Yes, the key is called 'Content: ' ...
            except KeyError:
                raise CodeInsightError(resp)
            return project_id
    
    def get_inventory_summary(self, project_id:int,
                                  vulnerabilitySummary : bool = False,
                                  cvssVersion: str = 'ANY',
                                  published: str = 'ALL',
                                  offset:int = 1,
                                  limit:int = 25) -> List[ProjectInventoryItem]:
            """
            Retrieves the inventory summary for a specific project.

            Args:
                project_id (int): The ID of the project.
                vulnerabilitySummary (bool, optional): Flag to include vulnerability summary. Defaults to False.
                cvssVersion (str, optional): The CVSS version to filter vulnerabilities. Defaults to 'ANY'.
                published (str, optional): The publication status. Defaults to 'ALL'.
                offset (int, optional): The offset for pagination. Defaults to 1.
                limit (int, optional): The maximum number of items to return. Defaults to 25.

            Returns:
                List[ProjectInventoryItem]: A list of ProjectInventoryItem objects representing the inventory summary.
            """
            path = f"projects/{project_id}/inventorySummary"
            params = {"vulnerabilitySummary": vulnerabilitySummary,
                    "cvssVersion": cvssVersion,
                    "published": published,
                    "offset": offset,
                    "limit": limit         
            }
            resp = self.client.request("GET", url_part=path, params=params)
            current_page = int(resp.headers['current-page'])
            number_of_pages = int(resp.headers['number-of-pages'])
            total_records = int(resp.headers['total-records'])
            inventory = []
            for inv_item in resp.json()['data']:
                inventory.append(ProjectInventoryItem.from_dict(inv_item))
            
            # Iterate through all the pages
            if number_of_pages > offset:
                params.update({"offset": offset+1})
                chunk = self.get_inventory_summary(project_id, **params)
                # Only append the inventory records
                inventory.extend(chunk)
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
        params = {"skipVulnerabilities": skip_vulnerabilities,
                    "published": published,
                    "vendor": vendor,
                    "product": product,
                    "page": page,
                    "pageSize": page_size,
                    "reviewStatus": review_status,
                    "alerts": alerts,
                    "includeFiles": include_files}

        resp = self.client.request("GET", url_part=path, params=params)
        project_inventory = resp.json()
        project = ProjectInventory.from_dict(project_inventory)

        # Iterate through all the pages
        if int(resp.headers['number-of-pages']) > page:
            chunk = self.get_inventory(project_id, page=page+1)
            # Only append the inventory records
            project.inventoryItems.extend(chunk.inventoryItems)

        return project


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
         
