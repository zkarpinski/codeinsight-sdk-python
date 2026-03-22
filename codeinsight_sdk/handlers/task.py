from typing import List
from ..handler import Handler
from ..models import Task

class TaskHandler(Handler):
    def all(self) -> List[Task]:
        """
        Retrieves all tasks.
        """
        path = "tasks"
        resp = self.client.request("GET", url_part=path)
        return [Task.from_dict(task) for task in resp.json()["data"]]

    def get(self, id: int) -> Task:
        """
        Retrieves a task by its ID.
        """
        path = f"tasks/{id}"
        resp = self.client.request("GET", url_part=path)
        return Task.from_dict(resp.json()["data"])
