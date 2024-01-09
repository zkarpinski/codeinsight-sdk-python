from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, dataclass_json
from typing import Any, Optional, List, Dict

@dataclass
class Project(DataClassJsonMixin):
    id: int
    name: str
    status: Optional[str] = None
    owner: Optional[str] = None
    description: Optional[str] = None
    dateCreated: Optional[str] = None
    projectPath: Optional[str] = None
    # TODO: Should this be a dictionary or another class? This structure is reused in a few APIs
    vulnerabilities: Optional[Dict[str, Dict]] = None


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
    componentName: str
    componentVersionName: str
    name: str
    type: str
    priority: str
    createdBy: str
    createdOn: str
    updatedOn: str
    url: Optional[str] = None
    componentUrl: Optional[str] = None
    componentDescription: Optional[str] = None
    vulnerabilities: Optional[List[Vulnerability]] = None
    vulnerabilitySummary: Optional[Dict[str, Dict]] = None
    filePaths: Optional[List[str]] = None

@dataclass_json #Trying this style instead of DataClassJsonMixin
@dataclass
class ProjectInventory():
    projectId: int
    inventoryItems: List[ProjectInventoryItem]

@dataclass
class Report(DataClassJsonMixin):
    id: int
    name: str
    path: str
    default: bool
    enabled: bool
    enableProjectPicker: bool
    order: int
    createdDateTime: str
    updatedDateTime: str