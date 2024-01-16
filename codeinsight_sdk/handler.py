import abc
from typing import List

from .models import Project, ProjectInventory, ProjectInventoryItem, Report
from .exceptions import CodeInsightError


class Handler(abc.ABC):
    def __init__(self, client):
        self.client = client
        self.cls = None

    @abc.abstractmethod
    def get(self):
        pass
