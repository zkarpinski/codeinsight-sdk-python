from typing import List
from ..handler import Handler
from ..models import Job

class JobHandler(Handler):
    def all(self) -> List[Job]:
        """
        Retrieves all jobs.
        """
        path = "jobs"
        resp = self.client.request("GET", url_part=path)
        return [Job.from_dict(job) for job in resp.json()["data"]]

    def get(self, id: int) -> Job:
        """
        Retrieves a job by its ID.
        """
        path = f"jobs/{id}"
        resp = self.client.request("GET", url_part=path)
        return Job.from_dict(resp.json()["data"])
