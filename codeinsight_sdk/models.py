from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, dataclass_json
from typing import Any, Optional, List
from .handlers import Handler

@dataclass
class Project(DataClassJsonMixin):
    id: int
    name: str
    status: Optional[str] = None
    owner: Optional[str] = None
    description: Optional[str] = None
    dateCreated: Optional[str] = None

    @property
    def inventory(self) -> Handler:
        return Handler.create(self, ProjectInventory)

@dataclass
class Vulnerability(DataClassJsonMixin):
    vulnerabilityId: int
    vulnerabilityName: str
    vulnerabilityDescription: str
    vulnerabilityCvssV3Score: int
    vulnerabilityCvssV3Severity: str

@dataclass
class ProjectInventoryItem(DataClassJsonMixin):
    itemNumber: int
    id: int
    name: str
    type: str
    priority: str
    createdBy: str
    createdOn: str
    updatedOn: str
    componentName: str
    componentVersionName: str
    vulnerabilites: Optional[List[Vulnerability]] = None
    filePaths: Optional[List[str]] = None

@dataclass_json #Trying this style instead of DataClassJsonMixin
@dataclass
class ProjectInventory(DataClassJsonMixin):
    projectId: int
    inventoryItems: List[ProjectInventoryItem]