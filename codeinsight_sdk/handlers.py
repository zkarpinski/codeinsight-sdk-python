import abc
from typing import List

from codeinsight_sdk.models import Project, ProjectInventory, ProjectInventoryItem, Report
from codeinsight_sdk.exceptions import CodeInsightError

class Handler(abc.ABC):
    def __init__(self, client):
        self.client = client
        self.cls = None

    @staticmethod
    def create(client, cls):
        k = cls.__name__
        handlers = {"Project": ProjectHandler,
                    "Report": ReportHandler
            }
        handler = handlers.get(k)
        if handler is None:
            raise ValueError(f"Handler not found for class '{k}'")
        return handler(client)

    @abc.abstractmethod
    def get(self):
        pass

class ProjectHandler(Handler):
    def __init__(self, client):
        super().__init__(client)
        self.cls = Project

    def create(self, name:str, description:str = None, folder:str = None,
               scanProfileName:str = None,
               owner:str = None,
               risk:str = None,
               folderId:int = None,
               customFields:List[dict] = None,
               ) -> int:
        """
        Creates a project.

        Args:
            name (str): The name of the project.
            description (str, optional): The description of the project. Defaults to None.
            folder (str, optional): The folder of the project. Defaults to None.

        Returns:
            Project: The created project id.
        """
        path = "projects"
        data = {"name": name,
                "description": description,
                "folderName": folder,
                "scanProfileName": scanProfileName,
                "owner": owner,
                "risk": risk,
                "folderId": folderId,
                "customFields": customFields}
        resp = self.client.request("POST", url_part=path, body=data)
        try:
            project_id = resp.json()['data']['id']
        except KeyError:
            raise CodeInsightError(resp)
        return project_id


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
    
    def upload_codebase(self, project_id:int,
                        codebase_path:str,
                        deleteExistingFileOnServer: bool = False,
                        expansionLevel: int = 1,
                        deleteArchiveAfterExpand: bool = False,
                        archiveDirSuffix: str = None,
                        ) -> int:
        path = "project/uploadProjectCodebase"
        params = {"projectId": project_id,
                    "deleteExistingFileOnServer": deleteExistingFileOnServer,
                    "expansionLevel": expansionLevel,
                    "deleteArchiveAfterExpand": deleteArchiveAfterExpand,
                    "archiveDirSuffix": archiveDirSuffix}
        code_file = {"file": open(codebase_path, 'rb')}
        content_type = "application/octet-stream"
        resp = self.client.request("POST", url_part=path, params=params, data=code_file,content_type=content_type)
        return resp.status_code

class ReportHandler(Handler):
    """
    A class that handles operations related to reports.

    Args:
        client (Client): The client object used for making API requests.

    Attributes:
        cls (Report): The class representing a report.

    Methods:
        get(id): Retrieves a report by its ID.
        all(): Retrieves all reports.

    """

    def __init__(self, client):
        super().__init__(client)
        self.cls = Report

    def get(self, id:int):
        """
        Retrieves a report by its ID.

        Args:
            id (int): The ID of the report to retrieve.

        Returns:
            Report: The report object.

        """
        path = f"reports/{id}"
        resp = self.client.request("GET", url_part=path)
        report_data = resp.json()['data']
        report = self.cls.from_dict(report_data)
        return report

    def all(self):
        """
        Retrieves all reports.

        Returns:
            list: A list of report objects.

        """
        path = "reports"
        resp = self.client.request("GET", url_part=path)
        reports = []
        for report_data in resp.json()['data']:
            reports.append(self.cls.from_dict(report_data))
        return reports
